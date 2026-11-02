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
