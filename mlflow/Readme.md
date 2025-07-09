# Console 1: Start MLflow Server
conda env create -f conda.yaml
conda activate train-env
mlflow server

# Console 2: Start Training Server
set MLFLOW_TRACKING_URI=http://localhost:5000
conda activate train-env
uvicorn app:app --reload

# Console 3: Mock Client Call
call.bat
