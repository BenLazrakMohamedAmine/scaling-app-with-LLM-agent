from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from pathlib import Path
import json

from .system_state import change_instances, load_state

LOG_FILE = Path(__file__).resolve().parent.parent.parent / "logs" / "audit.log"

def write_log(message: str):
    LOG_FILE.parent.mkdir(exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] {message}\n")

def state(request):
    state = load_state()
    return JsonResponse(state)

@csrf_exempt
def scale_up(request):
    state = change_instances(+1)
    write_log(f"SCALE UP -> {state['instances']} instances")
    return JsonResponse({"status": "ok", "action": "up", "instances": state["instances"]})

@csrf_exempt
def scale_down(request):
    state = change_instances(-1)
    write_log(f"SCALE DOWN -> {state['instances']} instances")
    return JsonResponse({"status": "ok", "action": "down", "instances": state["instances"]})
