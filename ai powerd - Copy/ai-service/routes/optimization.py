from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.task_optimizer import TaskOptimizer

router = APIRouter()
optimizer = TaskOptimizer()

class OptimizationRequest(BaseModel):
    deadline_days: int
    num_dependencies: int
    current_workload: int

@router.post("/")
async def get_priority_score(request: OptimizationRequest):
    try:
        features = [request.deadline_days, request.num_dependencies, request.current_workload]
        score = optimizer.predict_priority(features)
        return {"priority_score": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
