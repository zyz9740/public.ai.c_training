from fastapi import FastAPI
from pydantic import BaseModel
import mlflow.projects

app = FastAPI()

class TrainRequest(BaseModel):
    learning_rate: float = 0.001
    epochs: int = 5
    experiment_name: str = "default"

@app.post("/train")
def trigger_training(req: TrainRequest):
    # 使用 mlflow.projects.run 运行项目
    mlflow.projects.run(
        uri=".",
        parameters={
            "learning_rate": req.learning_rate,
            "epochs": req.epochs
        },
        experiment_name=req.experiment_name,
        synchronous=False  # 非阻塞执行
    )
    return {"message": "Training started."}