import os
from langchain_openai import ChatOpenAI  # si tu utilises OpenAI
from langchain_core.messages import HumanMessage

# Mets ta clé API dans une variable d'environnement OPENAI_API_KEY
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

def build_prompt(metrics):
    return f"""
You are an autoscaling decision agent.

Given these metrics:
- CPU usage: {metrics['cpu']}%
- RAM usage: {metrics['ram']}%
- Requests per second: {metrics['requests_per_sec']}
- Latency: {metrics['latency_ms']} ms

Decision rules (simplified):
- If CPU > 80 or latency > 300 -> scale UP.
- If CPU < 30 and requests_per_sec < 100 -> scale DOWN.
- Otherwise -> do NOTHING.

Return ONLY one word: "up", "down" or "none".
"""

def decide_action(metrics):
    prompt = build_prompt(metrics)
    resp = llm.invoke([HumanMessage(content=prompt)])
    text = resp.content.strip().lower()
    if "up" in text:
        return "up"
    if "down" in text:
        return "down"
    return "none"

if __name__ == "__main__":
    test_metrics = {"cpu": 90, "ram": 60, "requests_per_sec": 500, "latency_ms": 350}
    print(decide_action(test_metrics))

