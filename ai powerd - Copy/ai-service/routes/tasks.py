from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Example task data model
class Task(BaseModel):
    description: str
    deadlineDays: int
    dependencies: list
    assignedUserTaskCount: int

# Sample task data (you can replace this with your real data source)
sample_task = Task(
    description="Task is taking longer than expected due to multiple delays in frontend implementation.",
    deadlineDays=5,
    dependencies=["Dependency 1", "Dependency 2"],
    assignedUserTaskCount=3
)

@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    return sample_task  # Here you return the task for the given task_id
    