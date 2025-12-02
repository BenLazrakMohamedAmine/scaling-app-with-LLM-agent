from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from openai import RateLimitError
import random

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

def rule_based_decision(metrics):
    cpu = metrics["cpu"]
    rps = metrics["requests_per_sec"]
    latency = metrics["latency_ms"]

    if cpu > 80 or latency > 300:
        return "up"
    elif cpu < 50 and rps < 300:
        return "down"
    else:
        return "none"

def decide_action(metrics):
    # 🔹 1) Par défaut : décision par règles
    decision = rule_based_decision(metrics)

    # 🔹 2) De temps en temps : on demande l'avis du LLM
    # Par exemple 1 fois sur 5
    if random.randint(1, 5) != 1:
        return decision  # on ne fait PAS appel à l'API à chaque fois

    prompt = f"""
Tu es un agent d'auto-scaling.
Voici les métriques :
- CPU: {metrics['cpu']}%
- RAM: {metrics['ram']}%
- Requêtes/s: {metrics['requests_per_sec']}
- Latence: {metrics['latency_ms']} ms

Retourne UNIQUEMENT: "up", "down" ou "none".
"""

    try:
        resp = llm.invoke([HumanMessage(content=prompt)])
        text = resp.content.strip().lower()
        if "up" in text:
            return "up"
        if "down" in text:
            return "down"
        return "none"
    except RateLimitError as e:
        # Si le quota est dépassé → on retombe sur la version règles
        print("[LLM ERROR] Rate limit, fallback règles:", e)
        return decision
