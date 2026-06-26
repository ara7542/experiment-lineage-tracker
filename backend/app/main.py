from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="Experiment Lineage Tracker")


class ExperimentCreate(BaseModel):
    version: str
    title: str
    parent_version: Optional[str] = None
    series: str
    task: str
    model: str
    change_summary: str
    hypothesis: Optional[str] = None
    result_summary: Optional[str] = None
    decision: str = "pending"
    cv_score: Optional[float] = None
    lb_score: Optional[float] = None


class Experiment(ExperimentCreate):
    id: int


experiments: list[Experiment] = []
next_id = 1


@app.get("/")
def read_root():
    return {"message": "Experiment Lineage Tracker API"}


@app.get("/experiments")
def list_experiments():
    return experiments


@app.post("/experiments", response_model=Experiment)
def create_experiment(payload: ExperimentCreate):
    global next_id

    experiment = Experiment(id=next_id, **payload.model_dump())
    experiments.append(experiment)
    next_id += 1

    return experiment