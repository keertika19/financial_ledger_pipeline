# Exactly-Once Financial Ledger Pipeline

An end-to-end financial transaction processing pipeline designed to demonstrate reliable, fault-tolerant stream processing using Apache Kafka and Apache Flink.

The project focuses on exactly-once processing, duplicate detection, transaction integrity, and recovery from failures.

## Architecture Overview

The pipeline follows this data flow:

```text
Transaction Generator
        |
        v
   Apache Kafka
 (Transaction Topic)
        |
        v
   Apache Flink
 (Stream Processing)
        |
        v
 Financial Ledger
 (Target Data Store)
        |
        v
 Data Integrity Verification
 (Duplicate & Sequence Checks)
```

### Components

- **Apache Kafka:** Receives and buffers financial transactions.
- **Apache Flink:** Processes transaction streams.
- **Financial Ledger:** Represents the destination for processed transactions.
- **Failure Injector:** Simulates failures and repeated transaction delivery.
- **Verification Script:** Checks for duplicate transactions and missing sequence numbers.
- **Verification Notebook:** Helps inspect and summarize verification results.

## Project Structure

```text
financial_ledger_pipeline/
│
├── README.md
├── docker-compose.yml
├── .gitignore
│
├── docs/
│   ├── data_card.md
│   └── Exactly_Once_Financial_Ledger_Technical_Report.docx
│
├── notebooks/
│   └── results_verification.ipynb
│
└── scripts/
    ├── flink_ledger_pipeline.py
    ├── inject_failures.py
    └── verify_ledger.py
```

## Prerequisites

Install the following tools:

- Python 3.11
- Docker Desktop
- Git
- Java compatible with the installed Flink version
- Visual Studio Code (recommended)

Ensure Docker Desktop is running before starting the pipeline.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/keertika19/financial_ledger_pipeline.git
cd financial_ledger_pipeline
```

If the repository contains the project inside a nested directory, enter the directory containing `docker-compose.yml`.

### 2. Create a Virtual Environment

On Windows PowerShell, run:

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If activation is blocked, run Python directly through the virtual environment:

```powershell
.\.venv\Scripts\python.exe --version
```

### 3. Install Dependencies

If a `requirements.txt` file is available, install the dependencies:

```powershell
pip install -r requirements.txt
```

If no requirements file exists, install the packages specified by the project scripts and documentation.

### 4. Start Docker Services

Start the services defined in the Docker Compose configuration:

```powershell
docker compose up -d
```

Check the running containers:

```powershell
docker compose ps
```

The Flink dashboard is commonly available at:

http://localhost:8081

The Kafka host port is configured as `9092` in the Compose configuration.

### 5. Run the Transaction Pipeline

Execute the Flink pipeline script:

```powershell
.\.venv\Scripts\python.exe scripts\flink_ledger_pipeline.py
```

Check the terminal output for errors.

**Note:** Running the Python script does not, by itself, prove that a job was submitted to the Flink cluster. Verify the job in the Flink dashboard and confirm that data reaches the destination.

### 6. Inject Failures

Run the failure-injection script:

```powershell
.\.venv\Scripts\python.exe scripts\inject_failures.py
```

Review the terminal output to determine which failures or repeated deliveries were simulated.

### 7. Verify Data Integrity

Run the verification script:

```powershell
.\.venv\Scripts\python.exe scripts\verify_ledger.py
```

The intended checks include:

- Detecting duplicate transaction IDs.
- Checking transaction sequence continuity.
- Identifying missing transactions.

The results depend on the destination table, available data, and queries implemented in the script.

### 8. Inspect the Results Notebook

Open the notebook:

`notebooks/results_verification.ipynb`

Select the appropriate Python kernel and run the cells in order.

Use the notebook to review verification queries, outputs, and recorded results.

## Exactly-Once Processing

Exactly-once processing aims to ensure that each transaction affects the destination ledger only once, even when failures or retries occur.

Achieving this requires more than preventing duplicate messages in Kafka. The processing engine, checkpointing configuration, and destination sink must work together to provide the required guarantees.

This project investigates transaction integrity using:

- Transaction identifiers.
- Duplicate detection.
- Sequence continuity checks.
- Failure injection and recovery testing.
- Destination-side verification.

**Important:** Exactly-once processing should only be claimed after the implementation and relevant failure-recovery tests have been executed and their results verified.

## Data Integrity Verification

### 1. Duplicate Detection

A duplicate check groups records by transaction ID and identifies IDs that occur more than once.

Example SQL:

```sql
SELECT transaction_id, COUNT(*) AS transaction_count
FROM ledger_table
GROUP BY transaction_id
HAVING COUNT(*) > 1;
```

An empty result indicates that the query found no duplicate transaction IDs in the checked table.

### 2. Sequence Continuity

Sequence checks compare expected transaction sequence numbers against the records present in the destination.

Missing sequence numbers may indicate dropped records, incomplete processing, or gaps in the test data.

The verification logic must account for the expected sequence range before concluding that transactions are missing.

## Documentation

Additional project documentation is available in the `docs/` directory.

- **Technical Report:** Describes the project design, implementation, and evaluation.
- **Data Card:** Documents the data used by the pipeline and relevant assumptions.

## Limitations

- Verification is only as reliable as the queries and data being checked.
- Duplicate checks do not independently prove exactly-once processing.
- Sequence gaps must be evaluated against the expected input range.
- End-to-end guarantees depend on the actual Flink configuration and destination sink implementation.
- Results should be reported only after the corresponding tests have been executed.

## Future Improvements

- Add automated integration tests.
- Record throughput and processing latency.
- Run repeatable failure-recovery experiments.
- Export verification results to structured reports.
- Add monitoring and metrics for pipeline health.

## Author

**Keertika Acharya**

GitHub: https://github.com/keertika19

## License

A license can be added if the project is intended for public reuse.
