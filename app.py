from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

app = FastAPI(title="API Dual de Prevención de Fraude", description="ML Predictivo + IA Generativa")

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

class Transaccion(BaseModel):
    Time: float
    Amount: float
    V_features: list[float]

@app.post("/predecir/")
def predecir(data: Transaccion):
    if len(data.V_features) != 28:
         return {"error": "Se requieren exactamente 28 variables PCA."}
         
    features = np.array([[data.Time] + data.V_features + [data.Amount]])
    
    pred = model.predict(features)[0]
    proba = model.predict_proba(features)[0]
    
    resultado = "Fraude" if pred == 1 else "Legitima"
    explicacion = "Transacción regular autorizada."
    
    if pred == 1:
        explicacion = f"Alerta de IA: Cargo atípico detectado por ${data.Amount}. Las variables de comportamiento difieren del patrón histórico del usuario."
    
    return {
        "prediccion": int(pred),
        "resultado": resultado,
        "confianza_fraude": float(proba[1]),
        "reporte_analista": explicacion
    }