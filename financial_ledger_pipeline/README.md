# Exactly-Once Financial Ledger Pipeline

An end-to-end, fault-tolerant real-time financial ledger processing pipeline built using **Apache Flink**, **Apache Kafka**, and **Apache Iceberg**. 

This system guarantees **Exactly-Once processing semantics** under failure conditions, ensuring zero duplicate transactions and zero sequence gaps during network partitions, node crashes, and pipeline failures.

---

## Architecture Overview
