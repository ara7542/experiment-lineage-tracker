from typing import Optional
from fastapi import FastAPI, HTTPException
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

def find_experiment_by_version(version: str):
    for experiment in experiments:
        if experiment.version == version:
            return experiment
    return None


def find_experiment_by_version(version: str):
    for experiment in experiments:
        if experiment.version == version:
            return experiment
    return None


@app.get("/experiments/{version}/children")
def get_children(version: str):
    parent = find_experiment_by_version(version)

    if parent is None:
        raise HTTPException(status_code=404, detail="Experiment not found")

    children = [
        experiment
        for experiment in experiments
        if experiment.parent_version == version
    ]

    return children


@app.get("/experiments/{version}/lineage")
def get_lineage(version: str):
    lineage = []
    seen_versions = set()
    current = find_experiment_by_version(version)

    if current is None:
        raise HTTPException(status_code=404, detail="Experiment not found")

    while current is not None:
        if current.version in seen_versions:
            raise HTTPException(status_code=400, detail="Cycle detected in lineage")

        seen_versions.add(current.version)
        lineage.append(current)

        if current.parent_version is None:
            break

        current = find_experiment_by_version(current.parent_version)

    return {
        "version": version,
        "lineage": list(reversed(lineage)),
    }


@app.get("/experiments/{version}", response_model=Experiment)
def get_experiment(version: str):
    experiment = find_experiment_by_version(version)

    if experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")

    return experiment