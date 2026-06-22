###################################
# SHARED
###################################

data "google_project" "current" {}

resource "google_artifact_registry_repository" "market_analytics_platform_repo" {
  repository_id = "market-analytics-platform-repository"
  format        = "DOCKER"
  location      = "asia-south1"
  project       = "instant-medium-491107-t6"
  lifecycle {
    prevent_destroy = true
  }
}

resource "google_iam_workload_identity_pool" "github_pool" {
  workload_identity_pool_id = "github-actions-pool"
  display_name              = "GitHub Actions Pool"
  description               = "Identity pool for market analytics CI pipeline"
}

resource "google_iam_workload_identity_pool_provider" "github_provider" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github_pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"
  display_name                       = "GitHub Actions Provider"

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
    "attribute.owner"      = "assertion.repository_owner"
  }

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
    attribute_condition = "assertion.repository_owner == 'MayurCodes2508'"
}

resource "google_service_account_iam_member" "wif_binding" {
  service_account_id = "projects/instant-medium-491107-t6/serviceAccounts/github-workflows@instant-medium-491107-t6.iam.gserviceaccount.com"
  role               = "roles/iam.workloadIdentityUser"
  member = "principalSet://iam.googleapis.com/projects/144449440045/locations/global/workloadIdentityPools/github-actions-pool/attribute.repository/MayurCodes2508/market-analytics-platform"
  
  depends_on = [ 
    google_iam_workload_identity_pool.github_pool,
    google_iam_workload_identity_pool_provider.github_provider
   ]
}




###################################
# DEV
###################################

resource "google_storage_bucket" "dev_market_analytics_platform_bucket" {
  name                     = "dev-market-analytics-platform-bucket"
  location                 = "asia-south1"
  storage_class            = "STANDARD"
  public_access_prevention = "enforced"
  force_destroy            = true

  soft_delete_policy {
    retention_duration_seconds = 0
  }
}

resource "google_secret_manager_secret" "dev_market_analytics_platform_secrets" {
  secret_id = "dev_market_analytics_platform_secrets"

  replication {
    auto {}
  }
}

resource "google_cloud_run_v2_job" "dev_el_system_run" {
  name     = "dev-el-system-run"
  location = "asia-south1"
  deletion_protection = false
  template {
    template {
      containers {
        
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/el-job:testing"

        command = ["bash", "-c"]

        args = [
          "python -u -m system_runner.runner --file_path configs/coingecko_sources/dev/market_price.json --schema_path schemas/root_schema.json"
        ]

        env {
          name = "COINGECKO_API_KEY"
          value_source {
            secret_key_ref {
              secret  = "dev_market_analytics_platform_secrets"
              version = "4"
            }
          }
        }

        env {
          name = "DB_URL"
          value_source {
            secret_key_ref {
              secret  = "dev_market_analytics_platform_secrets"
              version = "5"
            }
          }
        }
      }
      service_account = "development-cloud-resources-jo@instant-medium-491107-t6.iam.gserviceaccount.com"
    }
  }
}

resource "google_cloud_run_v2_job" "dev_dbt_transformations_run" {
  name = "dev-dbt-transformations-run"
  location = "asia-south1"

  deletion_protection = false

  lifecycle {
    prevent_destroy = false
  }
  template {
    template {
      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/dbt-job:dev_v1"
        
        command = ["bash", "-c"]

        args = [
          "dbt deps && dbt source freshness --target $DBT_TARGET --profiles-dir . && dbt build --target $DBT_TARGET -s tag:dev --fail-fast --store-failures --profiles-dir ."
        ]

        env {
          name = "DBT_TARGET"
          value = "dev"
        }
      }
      service_account = "development-cloud-resource-396@instant-medium-491107-t6.iam.gserviceaccount.com"
    }
  }
}

resource "google_cloudfunctions2_function" "dev_metadata_pipeline" {
  name = "dev-metadata-pipeline"
  location = "asia-south1"
  build_config {
    runtime = "python311"
    entry_point = "handler"
    source {
      storage_source {
        bucket = "function-bucket-metadata-pipeline"
        object = "dev_metadata_pipeline.zip"
      }
    }
  }
  service_config {
    max_instance_count = 1
    available_memory = "512M"
    timeout_seconds = 30
    environment_variables = {
      ENV = "dev"
    }
    secret_environment_variables {
      key = "DB_URL"
      project_id = "instant-medium-491107-t6"
      secret = "dev_market_analytics_platform_secrets"
      version = "5"
    }
    service_account_email = "development-cloud-resources-se@instant-medium-491107-t6.iam.gserviceaccount.com"
  }
}


resource "google_cloud_scheduler_job" "dev_metadata_pipeline_scheduler" {
  name      = "dev-metadata-pipeline-scheduler"
  region    = "asia-south1"
  schedule  = "0 * * * *"
  time_zone = "Asia/Kolkata"
  lifecycle {
    prevent_destroy = true
  }
  depends_on = [ 
    google_cloudfunctions2_function.dev_metadata_pipeline
   ]

  retry_config {
    retry_count          = 3
    max_retry_duration   = "3600s"
    min_backoff_duration = "5s"
    max_backoff_duration = "3600s"
    max_doublings        = 5
  }

  http_target {
    uri         = google_cloudfunctions2_function.dev_metadata_pipeline.service_config[0].uri
    http_method = "POST"

    headers = {
      "Content-Type" = "application/json"
    }

    oidc_token {
      service_account_email = "development-cloud-resources-sc@instant-medium-491107-t6.iam.gserviceaccount.com"
      audience              = google_cloudfunctions2_function.dev_metadata_pipeline.service_config[0].uri
    }
  }
}



###################################
# PROD
###################################

resource "google_storage_bucket" "prod_market_analytics_platform_bucket" {
  name                     = "prod-market-analytics-platform-bucket"
  location                 = "asia-south1"
  storage_class            = "STANDARD"
  public_access_prevention = "enforced"

  lifecycle {
    prevent_destroy = true
  }

  soft_delete_policy {
    retention_duration_seconds = 604800
  }

  lifecycle_rule {
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
    condition {
      age = 90
    }
  }
}

resource "google_secret_manager_secret" "prod_market_analytics_platform_secrets" {
  secret_id = "prod-market-analytics-platform-secret"

  replication {
    auto {}
  }

  deletion_protection = true
}

resource "google_cloud_run_v2_job" "prod_el_system_run" {
  name     = "prod-el-system-run"
  location = "asia-south1"

  deletion_protection = true

  lifecycle {
    prevent_destroy = true
  }

  template {
    template {
      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/el-job:prod_v1"

        command = ["bash", "-c"]

        args = [
          "python -u -m orchestrator.runner --file_path configs/coingecko_sources/prod/market_price.json --schema_path schemas/root_schema.json"
        ]

        env {
          name = "COINGECKO_API_KEY"
          value_source {
            secret_key_ref {
              secret  = "prod-market-analytics-platform-secret"
              version = "1"
            }
          }
        }

        env {
          name = "DB_URL"
          value_source {
            secret_key_ref {
              secret  = "prod-market-analytics-platform-secret"
              version = "2"
            }
          }
        }
      }
      service_account = "production-cloud-resources-job@instant-medium-491107-t6.iam.gserviceaccount.com"
    }
  }
}

resource "google_cloud_run_v2_job" "prod_dbt_transformations_run" {
  name = "prod-dbt-transformations-run"
  location = "asia-south1"

  deletion_protection = true

  lifecycle {
    prevent_destroy = true
  }
  template {
    template {
      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/dbt-job:prod_v1"
        
        command = ["bash", "-c"]

        args = [
          "dbt deps && dbt source freshness --target $DBT_TARGET --profiles-dir . && dbt build --target $DBT_TARGET -s tag:prod --fail-fast --store-failures --profiles-dir ."
        ]

        env {
          name = "DBT_TARGET"
          value = "prod"
        }
      }
      service_account = "production-cloud-resources-960@instant-medium-491107-t6.iam.gserviceaccount.com"
    }
  }
}

resource "google_cloudfunctions2_function" "prod_metadata_pipeline" {
  name = "prod-metadata-pipeline"
  location = "asia-south1"
  lifecycle {
    prevent_destroy = true
  }
  build_config {
    runtime = "python311"
    entry_point = "handler"
    source {
      storage_source {
        bucket = "function-bucket-metadata-pipeline"
        object = "prod_metadata_pipeline.zip"
      }
    }
  }
  service_config {
    max_instance_count = 1
    available_memory = "512M"
    timeout_seconds = 30
    environment_variables = {
      ENV = "prod"
    }
    secret_environment_variables {
      key = "DB_URL"
      project_id = "instant-medium-491107-t6"
      secret = "prod-market-analytics-platform-secret"
      version = "2"
    }
    service_account_email = "production-cloud-resources-ser@instant-medium-491107-t6.iam.gserviceaccount.com"
  }
}

resource "google_cloud_scheduler_job" "prod_el_system_scheduler" {
  name      = "prod-el-system-scheduler"
  region    = "asia-south1"
  schedule  = "0 * * * *"
  time_zone = "Asia/Kolkata"
  lifecycle {
    prevent_destroy = true
  }
  depends_on = [ 
    google_cloud_run_v2_job.prod_el_system_run
   ]

  retry_config {
    retry_count          = 3
    max_retry_duration   = "3600s"
    min_backoff_duration = "5s"
    max_backoff_duration = "3600s"
    max_doublings        = 5
  }

  http_target {
    uri         = "https://asia-south1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/instant-medium-491107-t6/jobs/prod-el-system-run:run"
    http_method = "POST"

    oauth_token {
      service_account_email = "production-cloud-resources-sch@instant-medium-491107-t6.iam.gserviceaccount.com"
      scope                 = "https://www.googleapis.com/auth/cloud-platform"
    }
  }
}

resource "google_cloud_scheduler_job" "prod_dbt_transformations_scheduler" {
  name = "prod-dbt-transformations-scheduler"
  region = "asia-south1"
  schedule = "5 * * * *"
  time_zone = "Asia/Kolkata"
  depends_on = [
    google_cloud_run_v2_job.prod_dbt_transformations_run  
  ]
  retry_config {
    retry_count          = 3
    max_retry_duration   = "3600s"
    min_backoff_duration = "5s"
    max_backoff_duration = "3600s"
    max_doublings        = 5
  }

  http_target {
    uri = "https://asia-south1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/instant-medium-491107-t6/jobs/prod-dbt-transformations-run:run"
    http_method = "POST"
    oauth_token {
      service_account_email = "production-cloud-resources--38@instant-medium-491107-t6.iam.gserviceaccount.com"
      scope = "https://www.googleapis.com/auth/cloud-platform"
    }
  }
}


resource "google_cloud_scheduler_job" "prod_metadata_pipeline_scheduler" {
  name      = "prod-metadata-pipeline-scheduler"
  region    = "asia-south1"
  schedule  = "3 * * * *"
  time_zone = "Asia/Kolkata"
  lifecycle {
    prevent_destroy = true
  }
  depends_on = [ 
    google_cloudfunctions2_function.prod_metadata_pipeline
   ]

  retry_config {
    retry_count          = 3
    max_retry_duration   = "3600s"
    min_backoff_duration = "5s"
    max_backoff_duration = "3600s"
    max_doublings        = 5
  }

  http_target {
    uri         = google_cloudfunctions2_function.prod_metadata_pipeline.service_config[0].uri
    http_method = "POST"

    headers = {
      "Content-Type" = "application/json"
    }

    oidc_token {
      service_account_email = "production-cloud-resources-913@instant-medium-491107-t6.iam.gserviceaccount.com"
      audience              = google_cloudfunctions2_function.prod_metadata_pipeline.service_config[0].uri
    }
  }
}
