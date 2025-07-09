# PyTorch Training Service with FastAPI

这是一个使用FastAPI提供训练服务的PyTorch项目

## 快速开始

### 使用conda环境
```bash
# 创建并激活环境
conda env create -f conda.yaml
conda activate train-env

# 启动服务
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```s
# 客户端调用示例

## 快速训练调用脚本
```bash
call.bat
```

## Console (C++版本): 完整的训练控制客户端

### 依赖
- CMake (3.10 or higher)
- libcurl development library
- C++ compiler (g++, clang++, or MSVC)

### 在Windows上安装libcurl

download vcpkg from https://learn.microsoft.com/en-us/vcpkg/get_started/get-started?pivots=shell-powershell

```cmd
vcpkg install curl
```
After install curl
- Set git clone vcpkg path in CMakeLists.txt:7
- Set environment path in `path\to\vcpkg\installed\x64-windows\debug\bin` or `path\to\vcpkg\installed\x64-windows\bin` to find dll

## Build
```cmd
mkdir build
cd build
cmake ..
cmake --build .
```

## Run
```cmd
.\Debug\call.exe
```



## API使用

### 启动训练任务
```bash
curl -X POST "http://localhost:8000/train" \
  -H "Content-Type: application/json" \
  -d '{"learning_rate": 0.001, "epochs": 5}'
```

响应示例：
```json
{
  "message": "Training started.",
  "task_id": "train_0.001_5_1720603200000",
  "parameters": {
    "learning_rate": 0.001,
    "epochs": 5
  }
}
```

### 查看正在运行的任务
```bash
curl -X GET "http://localhost:8000/running_tasks"
```

响应示例：
```json
{
  "running_tasks": ["train_0.001_5_1720603200000"],
  "count": 1
}
```

### 停止训练任务
```bash
curl -X POST "http://localhost:8000/stop_train" \
  -H "Content-Type: application/json" \
  -d '{"task_id": "train_0.001_5_1720603200000"}'
```

响应示例：
```json
{
  "message": "训练任务 train_0.001_5_1720603200000 已被终止",
  "task_id": "train_0.001_5_1720603200000"
}
```

### 检查服务状态
```bash
curl -X GET "http://localhost:8000/"
```

## 训练输出

训练完成后，结果将保存在 `training_outputs` 目录中：
- `training_params.txt`: 训练参数
- `training_losses.txt`: 训练损失记录
- `checkpoint.pth`: 模型检查点
- `trained_model.pth`: 完整训练模型
