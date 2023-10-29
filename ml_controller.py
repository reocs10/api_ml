from fastapi import APIRouter, HTTPException, status
from models import Prediction_Input, Prediction_Output
import pickle
import numpy as np

# Carga del modelo y del normalizador
MODEL_PATH = 'optimal_rf_model.pkl'
SCALER_PATH = 'scaler.pkl'
with open(MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)
with open(SCALER_PATH, 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

router = APIRouter()
preds = []

@router.get('/ml')
def get_preds():
    return preds

@router.post('/ml', status_code=status.HTTP_201_CREATED, response_model=Prediction_Output)
def predict(pred_input: Prediction_Input):
    # Preprocesamiento de los datos
    data = np.array(pred_input.features).reshape(1, -1)
    scaled_data = scaler.transform(data)
    prediction = model.predict(scaled_data)
    
    prediction_dict = {"id": pred_input.id, "features": pred_input.features, "pred": prediction[0]}
    preds.append(prediction_dict)
    return prediction_dict

@router.post('/ml/add', status_code=status.HTTP_201_CREATED, response_model=Prediction_Output)
def add_prediction(pred_output: Prediction_Output):
    preds.append(pred_output.dict())
    return pred_output

@router.put('/ml/{pred_id}', status_code=status.HTTP_202_ACCEPTED, response_model=Prediction_Output)
def update_prediction(pred_id: int, pred_output: Prediction_Output):
    for index, pred in enumerate(preds):
        if pred["id"] == pred_id:
            preds[index] = pred_output.dict()
            return pred_output
    raise HTTPException(status_code=404, detail="Prediction not found")

@router.delete('/ml/{pred_id}')
def delete_prediction(pred_id: int):
    global preds
    preds = [pred for pred in preds if pred["id"] != pred_id]
    return {"message": "Prediction deleted"}
