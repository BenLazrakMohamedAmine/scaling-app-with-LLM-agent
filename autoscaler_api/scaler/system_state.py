import json
from pathlib import Path

STATE_FILE = Path(__file__).resolve().parent / "state.json"

def load_state():
    if not STATE_FILE.exists():
        return {"instances": 2}  # par défaut 2 instances
    return json.loads(STATE_FILE.read_text())

def save_state(state):
    STATE_FILE.write_text(json.dumps(state))

def change_instances(delta: int):
    state = load_state()
    state["instances"] = max(1, state["instances"] + delta)
    save_state(state)
    return state
