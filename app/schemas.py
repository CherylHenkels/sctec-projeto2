from pydantic import BaseModel, Field
from typing import List


# Entra no modelo (imagem com pixels)
class PredictionRequest(BaseModel):
    image_path: str = Field(...,
                                 min_length=1, 
                                 max_length=1000,
                                 description="Caminho da Imagem")

# Saida do modelo (número)
class PredictionResponse(BaseModel):
    digit: int = Field(...,
                       strict=True,
                       ge=0,
                       le=9,
                       description="Dígito previsto pelo modelo")

