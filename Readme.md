# Console 1: Start MLflow Server
mlflow server

# Console 2: Start Training Server
set MLFLOW_TRACKING_URI=http://localhost:5000
uvicorn app:app --reload

# Console 3: Mock Client Call
call.bat
