from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time

# Initialize Limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Remote PC Controller API", version="1.2.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Dummy API Key for initial testing (In production, this would come from DB)
VALID_API_KEY = "DEV-SECRET-KEY-123"

@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    # Skip auth for root or health checks if needed
    if request.url.path == "/":
        return await call_next(request)
        
    api_key = request.headers.get("X-API-Key")
    if api_key != VALID_API_KEY:
        return JSONResponse(
            status_code=401,
            content={
                "status": "error",
                "error_id": "ERR-401-001",
                "message": "Invalid or missing API Key"
            }
        )
    
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    return {"message": "Remote PC Controller API is live", "version": "1.2.0"}

@app.post("/api/v1/webhook")
@limiter.limit("10/second")
async def webhook(request: Request):
    data = await request.json()
    intent = data.get("intent")
    
    # Placeholder for intent parsing and execution
    # This will be connected to the OS handler in the next step
    
    return {
        "status": "success",
        "message": f"Intent '{intent}' received",
        "data": {
            "action": "log_only",
            "execution_time_ms": 10
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
