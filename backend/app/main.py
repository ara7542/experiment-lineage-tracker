from fastapi import FastAPI

app = FastAPI(title="Experiment Lineage Tracker")


@app.get("/")
def read_root():
    return {"message": "Experiment Lineage Tracker API"}