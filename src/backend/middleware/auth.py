from fastapi import Request
from fastapi.responses import JSONResponse
from ..config import get_settings

settings = get_settings()

async def api_key_auth_middleware(request: Request, call_next):
    """
    REQ-SEC-01: API Key Verification Middleware.
    """
    # Whitelist paths
    if request.url.path in ["/api/v1/health", "/docs", "/openapi.json", "/ws/api/v1/status"]:
        return await call_next(request)
        
    api_key = request.headers.get("X-API-Key")
    
    if not api_key or api_key != settings.api_key:
        return JSONResponse(
            status_code=401,
            content={
                "status": "error", 
                "error_id": "ERR-401-001", 
                "message": "Unauthorized: Invalid or Missing API Key"
            }
        )
        
    return await call_next(request)
