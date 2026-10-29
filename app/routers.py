from fastapi import APIRouter, HTTPException

from .schemas import PredictionRequest, PredictionResponse, HealthResponse
from .services import predict_digit, is_model_loaded

router = APIRouter()

@router.get("/health", response_model=HealthResponse, status_code=200)
def health():
    loaded = is_model_loaded()
    status = "ok" if loaded else "não carregado"

    return HealthResponse(status=status, model_loaded=loaded)


@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        digit = predict_digit(request.image_path)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error

    return PredictionResponse(digit = digit)

