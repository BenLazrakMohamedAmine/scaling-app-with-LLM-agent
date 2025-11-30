import time
import requests
from pathlib import Path
from .analyzer import decide_action

LOG_AGENT_FILE = Path(__file__).resolve().parent.parent / "logs" / "agent.log"
PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

BASE_URL = "http://127.0.0.1:8000"

def log_agent(msg: str):
    LOG_AGENT_FILE.parent.mkdir(exist_ok=True)
    with open(LOG_AGENT_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def get_metrics_from_prometheus():
    def query(metric):
        r = requests.get(PROMETHEUS_URL, params={"query": metric})
        data = r.json()["data"]["result"]
        if not data:
            return 0
        return float(data[0]["value"][1])

    return {
        "cpu": query("demo_cpu_usage_percent"),
        "ram": query("demo_ram_usage_percent"),
        "requests_per_sec": query("demo_requests_per_sec"),
        "latency_ms": query("demo_latency_ms"),
    }

def loop():
    while True:
        metrics = get_metrics_from_prometheus()
        print("[PROM METRICS]", metrics)
        log_agent(f"PROM METRICS: {metrics}")

        decision = decide_action(metrics)
        print("[DECISION]", decision)
        log_agent(f"DECISION: {decision}")

        # ici même logique que dans ton controller actuel (appel /scale/up ou /down)
        time.sleep(5)

if __name__ == "__main__":
    loop()
