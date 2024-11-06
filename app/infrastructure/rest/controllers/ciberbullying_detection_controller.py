from fastapi import APIRouter, HTTPException
from app.application.service.ciberbullying_detection_service import CiberbullyingDetectionService
from app.infrastructure.config import modelo

router = APIRouter()
service = CiberbullyingDetectionService(modelo)

@router.post("/detection")
async def analizar_mensaje(message: str):
    try:
        result = service.analize_message(message)
        return JSONResponse(content={"result": result}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"timestamp": date.today().isoformat(), "messages": [str(e)]}, status_code=500)