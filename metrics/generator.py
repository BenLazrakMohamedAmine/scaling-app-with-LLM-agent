import random
from prometheus_client import Gauge

# Définition des métriques Prometheus
CPU_GAUGE = Gauge("demo_cpu_usage_percent", "CPU usage in percent")
RAM_GAUGE = Gauge("demo_ram_usage_percent", "RAM usage in percent")
RPS_GAUGE = Gauge("demo_requests_per_sec", "Requests per second")
LAT_GAUGE = Gauge("demo_latency_ms", "Latency in milliseconds")


def generate_metrics():
    """Génère des métriques aléatoires ET met à jour les gauges Prometheus."""
    metrics = {
        "cpu": random.randint(10, 95),
        "ram": random.randint(20, 90),
        "requests_per_sec": random.randint(10, 800),
        "latency_ms": random.randint(50, 400),
    }

    # 🔹 Mise à jour des métriques Prometheus
    CPU_GAUGE.set(metrics["cpu"])
    RAM_GAUGE.set(metrics["ram"])
    RPS_GAUGE.set(metrics["requests_per_sec"])
    LAT_GAUGE.set(metrics["latency_ms"])

    return metrics
