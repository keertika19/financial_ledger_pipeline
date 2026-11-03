import json
from pyflink.common import Configuration, SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.datastream.checkpointing_mode import CheckpointingMode

def run_pipeline():
    print("Initializing Flink Streaming Execution Environment...")
    config = Configuration()
    
    # Attach Kafka connector JAR
    config.set_string("pipeline.jars", "file:///tmp/flink-sql-connector-kafka.jar")
    
    # Configure State Storage for Checkpoints
    config.set_string("state.backend", "hashmap")
    config.set_string("state.checkpoints.dir", "file:///tmp/flink-checkpoints")
    config.set_string("execution.checkpointing.mode", "EXACTLY_ONCE")
    config.set_string("execution.checkpointing.interval", "5000")

    env = StreamExecutionEnvironment.get_execution_environment(configuration=config)
    
    # Configure Kafka Consumer Source
    kafka_props = {
        'bootstrap.servers': 'kafka:29092',
        'group.id': 'ledger_group'
    }
    
    kafka_consumer = FlinkKafkaConsumer(
        topics='ledger_transactions',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )
    
    ds = env.add_source(kafka_consumer)
    ds.print()
    
    print("Submitting job graph asynchronously to Flink...")
    env.execute_async("Financial Ledger Pipeline")

if __name__ == "__main__":
    run_pipeline()