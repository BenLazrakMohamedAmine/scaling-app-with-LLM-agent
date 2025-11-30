import time
import requests
from pathlib import Path

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
    log_agent(f"Called API for action={action}, response={r.json()}")

def loop():
    while True:
        metrics = generate_metrics()
        print(f"[METRICS] {metrics}")
        log_agent(f"METRICS: {metrics}")

        decision = decide_action(metrics)
        print(f"[DECISION] {decision}")
        log_agent(f"DECISION: {decision}")

        if decision in ("up", "down"):
            call_api(decision)
        else:
            log_agent("No action taken.")

        time.sleep(5)  # attendre avant le prochain cycle

if __name__ == "__main__":
    loop()
