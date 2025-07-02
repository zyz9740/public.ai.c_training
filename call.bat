curl -X POST http://localhost:8000/train ^
  -H "Content-Type: application/json" ^
  -d "{\"learning_rate\": 0.01, \"epochs\": 3, \"experiment_name\": \"zyz\"}"
