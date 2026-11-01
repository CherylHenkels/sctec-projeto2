from fastapi import APIRouter, HTTPException
import logging

from .schemas import PredictionRequest, PredictionResponse, HealthResponse
from .services import predict_digit, is_model_loaded

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/health", response_model=HealthResponse, status_code=200)
def health():
    loaded = is_model_loaded()
    status = "ok" if loaded else "não carregado"

    return HealthResponse(status=status, model_loaded=loaded)


@router.post("/predict", response_model=PredictionResponse, status_code = 200)
def predict(request: PredictionRequest):
    # Processamento de entrada
    try:
        # Para simular um erro interno descomente a próxima linha
        #raise RuntimeError("Falha simulada para teste")
        
        digit = predict_digit(request.image_path)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error

    except Exception as error:
        logger.exception("Erro interno durante a predição")
        raise HTTPException(
            status_code = 500,
            detail = "Não foi possível realizar a predição"
        ) from error

    # Validação de saída
    try:
        return PredictionResponse(digit = digit)
    except Exception as error:
        logger.exception("Erro na resposta da predição")

        raise HTTPException(
            status_code = 500,
            detail = "Erro ao retornar a resposta"
        ) from error

