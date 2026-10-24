from pathlib import Path

import joblib
import cv2
import numpy as np

#Caminho do modelo
# Path(__file__) -> caminho do arquivo atual

MODEL_PATH = (Path(__file__).resolve().parent.parent
              / "models"
              / "best_model_rf.joblib")


model = None

def load_model():
    # variável global para permitir mudança pela função
    global model

    if model is None:
        model = joblib.load(MODEL_PATH)


def redimencionaliza_figura(img):
    # blur leve
    img_blur = cv2.GaussianBlur(img, (3,3), 0)

    # threshold invertido (já inverte as cores das imagens - fundo branco se torna preto e traço preto se torna branco)
    _, img_bin = cv2.threshold(img_blur, 128, 255, cv2.THRESH_BINARY_INV)

    coords = cv2.findNonZero(img_bin)
    if coords is None:
        raise ValueError("Nenhum dígito foi encontrado na imagem.")
    
    x, y, w, h = cv2.boundingRect(coords)

    # padding
    pad = 4
    cropped = img_bin[max(y-pad,0):y+h+pad, max(x-pad,0):x+w+pad]

    # resize suave
    resized = cv2.resize(cropped, (20, 20), interpolation=cv2.INTER_AREA)

    # canvas preto
    canvas = np.zeros((28,28), dtype=np.uint8)
    x_offset = (28 - resized.shape[1]) // 2
    y_offset = (28 - resized.shape[0]) // 2
    canvas[y_offset:y_offset+resized.shape[0], x_offset:x_offset+resized.shape[1]] = resized

    return canvas


    
def predict_digit(image_path):
    if model is None:
        raise RuntimeError('O modelo ainda não foi carregado')
    
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Não foi possível ler a imagem.")

    img_processed = redimencionaliza_figura(img)
    img_norm = img_processed / 255.0
    img_flat = img_norm.reshape(1, 784)

    prediction = model.predict(img_flat)

    return int(prediction[0])