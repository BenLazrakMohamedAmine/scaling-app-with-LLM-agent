import time
import requests
from openai import RateLimitError
from pathlib import Path

from prometheus_client import start_http_server  # 👈 NEW

from metrics.generator import generate_metrics
from .analyzer import decide_action

LOG_AGENT_FILE = Path(__file__).resolve().parent.parent / "logs" / "agent.log"
BASE_URL = "http://127.0.0.1:8000"


def log_agent(msg: str):
    LOG_AGENT_FILE.parent.mkdir(exist_ok=True)
    with open(LOG_AGENT_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def call_api(action: str):
    if action == "up":
        r = requests.post(f"{BASE_URL}/scale/up/")
    elif action == "down":
        r = requests.post(f"{BASE_URL}/scale/down/")
    else:
        return

    try:
        data = r.json()
    except Exception:
        data = {"status_code": r.status_code, "text": r.text}

    log_agent(f"Called API for action={action}, response={data}")


def loop():
    while True:
        metrics = generate_metrics()
        print(f"[METRICS] {metrics}")
        log_agent(f"METRICS: {metrics}")

        try:
            decision = decide_action(metrics)
        except RateLimitError as e:
            msg = f"[LLM ERROR] Rate limit, fallback règles: {e}"
            print(msg)
            log_agent(msg)
            # on ne casse pas la boucle, on continue avec règles locales
            decision = "none"

        print(f"[DECISION] {decision}")
        log_agent(f"DECISION: {decision}")

        if decision in ("up", "down"):
            call_api(decision)
        else:
            log_agent("No action taken.")

        time.sleep(5)  # pause entre deux itérations


if __name__ == "__main__":
    # 🔹 Très important pour Prometheus : démarrer le serveur de métriques
    start_http_server(8001)
    print("[METRICS SERVER] Exposé sur http://localhost:8001/metrics")
    loop()
