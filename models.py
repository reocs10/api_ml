from pydantic import BaseModel
from typing import List

class Task(BaseModel):
    id: int
    task: str
    completed: bool

class Prediction_Input(BaseModel):
    id: int
    features: List[float]  # Ajustar según tus necesidades

class Prediction_Output(BaseModel):
    id: int
    features: List[float]  # Ajustar según tus necesidades
    pred: float
