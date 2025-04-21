from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.scheduler_predictor import SchedulerPredictor

router = APIRouter()
scheduler_model = SchedulerPredictor()

class ScheduleRequest(BaseModel):
    task_description: str

@router.post("/")
async def schedule_and_predict(request: ScheduleRequest):
    try:
        result = scheduler_model.predict(request.task_description)
        return {
            "label": result["predicted_label"],
            "confidence_scores": result["confidence_scores"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
