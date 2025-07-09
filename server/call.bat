@echo off
echo "=== 测试训练和停止功能 ==="

echo "1. 启动训练任务..."
curl -X POST http://localhost:8000/train ^
  -H "Content-Type: application/json" ^
  -d "{\"learning_rate\": 0.01, \"epochs\": 10}" > response.json

echo.
echo "2. 训练任务响应:"
type response.json

echo.
echo "3. 等待5秒让训练开始..."
timeout /t 5 /nobreak > nul

echo.
echo "4. 查看正在运行的任务..."
curl -X GET http://localhost:8000/running_tasks

echo.
echo "5. 如果要停止训练，请复制上面响应中的task_id，然后运行:"
echo "curl -X POST http://localhost:8000/stop_train -H "Content-Type: application/json" -d "{\"task_id\": \"YOUR_TASK_ID\"}""

echo.
pause
