###################################
# SHARED
###################################

data "google_project" "current" {}

resource "google_artifact_registry_repository" "market_analytics_platform_repo" {
  repository_id = "market-analytics-platform-repository"
  format        = "DOCKER"
  location      = "asia-south1"
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

resource "google_cloud_run_v2_job" "dev_market_analytics_platform_run" {
  name     = "dev-market-analytics-platform-run"
  location = "asia-south1"
  deletion_protection = false
  template {
    template {
      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/market-job:latest"

        args = [
          "python -u -m orchestrator.runner --file_path configs/coingecko_sources/dev_market_price.json --schema_path schemas/api_exec_schema.json"
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

resource "google_cloud_run_v2_job" "prod_market_analytics_platform_run" {
  name     = "prod-market-analytics-platform-run"
  location = "asia-south1"

  deletion_protection = true

  template {
    template {
      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/market-job:prod_v1"

        args = [
          "--file_path",
          "configs/coingecko_sources/prod_market_price.json",
          "--schema_path",
          "schemas/api_exec_schema.json"
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
    }
  }
}

resource "google_cloud_scheduler_job" "prod_market_analytics_platform_scheduler" {
  name      = "prod-market-analytics-platform-scheduler"
  region    = "asia-south1"
  schedule  = "0 * * * *"
  time_zone = "Asia/Kolkata"

  retry_config {
    retry_count          = 3
    max_retry_duration   = "0s"
    min_backoff_duration = "5s"
    max_backoff_duration = "3600s"
    max_doublings        = 5
  }

  http_target {
    uri         = "https://asia-south1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/instant-medium-491107-t6/jobs/prod-market-analytics-platform-run:run"
    http_method = "POST"

    oauth_token {
      service_account_email = "production-cloud-resources-job@instant-medium-491107-t6.iam.gserviceaccount.com"
      scope                 = "https://www.googleapis.com/auth/cloud-platform"
    }
  }
}