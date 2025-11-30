import random
import time
from prometheus_client import Gauge, start_http_server

# Définition des métriques Prometheus
CPU_GAUGE = Gauge("demo_cpu_usage_percent", "CPU usage in percent")
RAM_GAUGE = Gauge("demo_ram_usage_percent", "RAM usage in percent")
RPS_GAUGE = Gauge("demo_requests_per_sec", "Requests per second")
LAT_GAUGE = Gauge("demo_latency_ms", "Latency in milliseconds")

def generate_metrics():
    metrics = {
        "cpu": random.randint(10, 95),
        "ram": random.randint(20, 90),
        "requests_per_sec": random.randint(10, 800),
        "latency_ms": random.randint(50, 400),
    }
    return metrics

def loop():
    # Expose /metrics sur le port 8001
    start_http_server(8001)
    print("Exporter Prometheus lancé sur http://localhost:8001/metrics")

    while True:
        m = generate_metrics()
        # Met à jour les métriques Prometheus
        CPU_GAUGE.set(m["cpu"])
        RAM_GAUGE.set(m["ram"])
        RPS_GAUGE.set(m["requests_per_sec"])
        LAT_GAUGE.set(m["latency_ms"])

        print("[METRICS]", m)
        time.sleep(5)

if __name__ == "__main__":
    loop()
