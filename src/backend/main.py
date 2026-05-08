from fastapi import FastAPI, Request, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import logging
import json
import time

from .config import get_settings
from .core.intent_parser import IntentParser
from .core.skill_registry import SkillRegistry
from .core.skill_generator import SkillGenerator
from .core.os_handler import OSHandler

app = FastAPI(title="Agentic Remote PC Controller", version="2.0.0")
settings = get_settings()

# Initialize Core Services
registry = SkillRegistry()
parser = IntentParser()
# We'll initialize generator inside the endpoint or as a singleton

# Setup Logging
logging.basicConfig(
    level=settings.log_level,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)

# REQ-RT-01: WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

manager = ConnectionManager()

# --- MIDDLEWARE ---
from .middleware.auth import api_key_auth_middleware
app.middleware("http")(api_key_auth_middleware)

# --- ENDPOINTS ---

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "ok", 
        "pc_name": settings.pc_name, 
        "version": "2.0.0",
        "timestamp": time.time()
    }

@app.post("/api/v1/webhook")
async def process_webhook(request: Request):
    data = await request.json()
    raw_intent = data.get("intent", "")
    source = data.get("source", "type")
    
    if not raw_intent:
        raise HTTPException(status_code=400, detail="Intent is required")

    # 1. Parse Intents (REQ-CMD-01: Chaining)
    parsed_commands = parser.parse(raw_intent)
    results = []
    
    generator = SkillGenerator(websocket_manager=manager)

    for cmd in parsed_commands:
        intent_name = cmd.get("intent") or cmd.get("target")
        
        # 2. Check Registry (REQ-AI-01)
        skill = registry.get_skill(intent_name)
        
        if not skill:
            # 3. Auto-Build Skill (Agentic Loop)
            success, msg = await generator.build_skill(intent_name)
            if not success:
                results.append({"intent": intent_name, "status": "failed", "message": msg})
                continue
            # After building, re-fetch skill (Simulated for now)
            skill = registry.get_skill(intent_name)

        # 4. Execute Skill
        if skill:
            # Logic to call OSHandler based on skill["target"]
            # e.g., OSHandler.open_app(skill["target"])
            results.append({"intent": intent_name, "status": "success", "action": skill["action_type"]})
        else:
            results.append({"intent": intent_name, "status": "pending", "message": "Skill built but needs registration"})

    return {
        "status": "success",
        "processed_commands": len(results),
        "results": results
    }

@app.websocket("/ws/api/v1/status")
async def status_websocket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
