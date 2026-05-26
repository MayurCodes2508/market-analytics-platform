# 🏛️ Market Analytics Platform Architecture

## 🧠 Overview

The Market Analytics Platform is a modular, config-driven data engineering system designed to extract, process, and analyze cryptocurrency market data.

The platform follows a declarative architecture where pipeline behavior is defined through structured JSON configurations, validated against strict schemas, and executed through a custom-built orchestration engine.

The system is designed with clear separation of concerns between execution, data extraction, and data loading, enabling extensibility, maintainability, and scalability.

👉 [Read detailed overview](overview/PROJECT_OVERVIEW.md)

---

## 🎯 Data Products

The platform generates the following analytical outputs:

- Top Performing Coins  
- Consistently Performing Coins  
- Worst Performing Coins  
- Category-Based Performance  

These data products represent the final analytical insights derived from processed cryptocurrency data.

---

## 🗺️ Architectural Topology

The system follows a modular execution pipeline:

Job Config (JSON)

▼

Schema Validation Layer

▼

Execution Engine (Runner)

▼

Data Lake (GCS)

▼

Data Warehouse (BigQuery)

▼

dbt Transformations

▼

Analytics Layer

👉 [View full topology breakdown](architecture/TOPOLOGY.md)

---

## ⚙️ Core System Components

### 1. Execution Engine

The execution engine is responsible for orchestrating pipeline runs. It loads job configurations, validates them against schemas, triggers execution commands, and manages run lifecycle tracking.

👉 [Deep dive](core/EXECUTION_ENGINE.md)

---

### 2. Configuration System

The system uses declarative JSON-based job configurations to define pipeline behavior, enabling flexible and reusable pipeline definitions.

👉 [Deep dive](core/CONFIG_SYSTEM.md)

---

### 3. Schema Validation Layer

All job configurations are validated against a predefined JSON schema to enforce structural consistency and prevent runtime errors.

👉 [Deep dive](core/SCHEMA_VALIDATION.md)

---

### 4. Destination Engine

The destination engine processes extracted data and writes it to storage systems such as GCS in optimized formats like Parquet or JSON.

👉 [Deep dive](core/DESTINATION_ENGINE.md)

---

### 5. Run Tracking & Observability

Pipeline executions are tracked in a metadata database, capturing execution status, timestamps, and error information for monitoring and debugging.

👉 [Deep dive](core/RUN_TRACKING.md)

---

## 🛠️ Data Pipeline Layers

### 1. Data Lake Layer

Raw data is stored in a partitioned and optimized format for efficient storage and retrieval.

👉 [Deep dive](layers/DATA_LAKE.md)

---

### 2. Data Warehouse Layer

Processed data is modeled using a multi-layer architecture (Bronze, Silver, Gold) within BigQuery.

👉 [Deep dive](layers/WAREHOUSE.md)

---

## 🔄 Environment Strategy

The system supports environment-based configuration for development and production isolation.

👉 [Full environment setup](environments/ENVIRONMENTS.md)

---

## 💰 FinOps & Cost Strategy

The platform is designed to optimize cost through serverless infrastructure and efficient data storage techniques.

👉 [Cost model](finops/COST_MODEL.md)  
👉 [Optimization strategies](finops/OPTIMIZATION.md)

---

## 📈 Reliability & Observability

The system ensures reliability through structured logging, validation, and execution tracking.

👉 [SLO definitions](reliability/SLOS.md)

---

## 🧠 Design Decisions & Tradeoffs

Key architectural decisions balance flexibility, performance, and cost.

👉 [Detailed tradeoffs](design/TRADEOFFS.md)

---

## 🚀 Future Improvements

The platform is designed to evolve with additional features such as streaming ingestion and advanced analytics.

👉 [See roadmap](future/IMPROVEMENTS.md)
