from pydantic import BaseModel, Field, ConfigDict
from typing import List


# Entra no modelo (imagem com pixels)
class PredictionRequest(BaseModel):
    model_config = ConfigDict(
        strict = True,
        extra = "forbid",
        str_strip_whitespace = True
    )
    image_path: str = Field(...,
                                 min_length=1, 
                                 max_length=1000,
                                 description="Caminho da Imagem")

# Saida do modelo (número)
class PredictionResponse(BaseModel):
    model_config = ConfigDict(
        strict = True,
        extra = "forbid"
    )
    digit: int = Field(...,
                       ge=0,
                       le=9,
                       description="Dígito previsto pelo modelo")

class HealthResponse(BaseModel):
    model_config = ConfigDict(
        strict=True,
        extra = "forbid"
    )
    status: str = Field(...,
                        description="Estado do serviço")
    model_loaded: bool = Field(...,
                               description="Estado do modelo na memoria (carregado/não)")