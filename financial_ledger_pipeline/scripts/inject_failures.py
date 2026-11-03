import os
import time

def inject_network_delay():
    print("[Chaos 1/3] Pausing Kafka container to simulate severe network stall/unavailability...")
    # Native Docker Compose pause stops container network execution directly
    os.system("docker compose pause kafka")
    print("[Chaos 1/3] Kafka paused. Letting pipeline process under network stall for 10 seconds...")
    time.sleep(10)
    
    print("[Chaos 1/3] Unpausing Kafka container...")
    # Resumes container execution
    os.system("docker compose unpause kafka")
    print("[Chaos 1/3] Network simulation complete.\n")

def kill_and_restart_taskmanager():
    print("[Chaos 2/3] Killing Flink TaskManager process mid-stream...")
    os.system("docker compose kill taskmanager")
    print("[Chaos 2/3] TaskManager killed. Waiting 10 seconds to observe state recovery delay...")
    time.sleep(10)
    
    print("[Chaos 2/3] Restarting Flink TaskManager...")
    os.system("docker compose start taskmanager")
    print("[Chaos 2/3] TaskManager container restarted and reconnected.\n")

def restart_kafka_broker():
    print("[Chaos 3/3] Restarting Kafka Broker...")
    os.system("docker compose restart kafka")
    print("[Chaos 3/3] Kafka Broker restarted.\n")

if __name__ == "__main__":
    print("==================================================")
    print("Starting Failure Injection & Chaos Engineering Suite")
    print("==================================================\n")
    
    inject_network_delay()
    time.sleep(5)
    
    kill_and_restart_taskmanager()
    time.sleep(5)
    
    restart_kafka_broker()
    
    print("==================================================")
    print("Chaos execution finished. Run verification scripts.")
    print("==================================================")