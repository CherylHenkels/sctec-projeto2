from fastapi import APIRouter, HTTPException

from .schemas import PredictionRequest, PredictionResponse
from .services import predict_digit

router = APIRouter()

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

