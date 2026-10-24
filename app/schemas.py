from pydantic import BaseModel, Field
from typing import List


# Entra no modelo (imagem com pixels)
class PredictionRequest(BaseModel):
    pixels: List[float] = Field(...,
                                 min_length=784, 
                                 max_length=784,
                                 description="Vetor com os 784 pixels da imagem")

# Saida do modelo (número)
class PredictionResponse(BaseModel):
    digit: int = Field(...,
                       description="Dígito previsto pelo modelo")
    confidence: float = Field(...,
                              description="Probabilidade da previsão")
