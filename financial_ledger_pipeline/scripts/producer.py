import json
import time
import uuid
import random
from kafka import KafkaProducer

def run_producer():
    print("Starting Kafka Transaction Producer...")
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    sequence_num = 1
    try:
        while True:
            txn = {
                "transaction_id": str(uuid.uuid4()),
                "sequence_num": sequence_num,
                "account_from": f"ACC_{random.randint(100, 199)}",
                "account_to": f"ACC_{random.randint(200, 299)}",
                "amount": round(random.uniform(10.0, 5000.0), 2),
                "timestamp": int(time.time() * 1000)
            }
            producer.send('ledger_transactions', value=txn)
            print(f"[Record Sent] Sequence #{sequence_num} | ID: {txn['transaction_id'][:8]}... | Amount: ${txn['amount']}")
            sequence_num += 1
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProducer stopped.")

if __name__ == "__main__":
    run_producer()