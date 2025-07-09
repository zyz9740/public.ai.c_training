from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import subprocess
import sys
import os
import threading
from typing import Dict, Optional

app = FastAPI()

# 全局变量来跟踪训练进程
running_processes: Dict[str, subprocess.Popen] = {}
process_lock = threading.Lock()

class TrainRequest(BaseModel):
    learning_rate: float = 0.001
    epochs: int = 5

class StopTrainRequest(BaseModel):
    task_id: str

def generate_task_id(learning_rate: float, epochs: int) -> str:
    """生成训练任务ID"""
    import time
    timestamp = int(time.time() * 1000)  # 毫秒时间戳
    return f"train_{learning_rate}_{epochs}_{timestamp}"

def run_training(learning_rate: float, epochs: int, task_id: str):
    """在后台运行训练任务"""
    process = None
    try:
        print(f"=== 开始训练任务 {task_id} ===")
        print(f"参数: learning_rate={learning_rate}, epochs={epochs}")
        
        # 使用Popen来实时获取输出
        process = subprocess.Popen([
            sys.executable, "train.py",
            "--learning_rate", str(learning_rate),
            "--epochs", str(epochs)
        ], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT,  # 将stderr重定向到stdout
        text=True,
        bufsize=1,  # 行缓冲
        universal_newlines=True,
        cwd=os.path.dirname(os.path.abspath(__file__)))
        
        # 将进程添加到全局跟踪字典
        with process_lock:
            running_processes[task_id] = process
        
        # 实时读取并输出训练日志
        for line in iter(process.stdout.readline, ''):
            if line:
                print(f"[TRAIN {task_id}] {line.rstrip()}")
        
        # 等待进程完成
        process.wait()
        
        print(f"=== 训练任务 {task_id} 完成，返回码: {process.returncode} ===")
        
        if process.returncode != 0:
            if process.returncode == -15 or process.returncode == -9:  # SIGTERM or SIGKILL
                print(f"训练任务 {task_id} 被用户主动终止")
            else:
                print(f"训练任务 {task_id} 出现错误，返回码: {process.returncode}")
            
    except Exception as e:
        print(f"训练任务 {task_id} 失败，异常信息: {str(e)}")
    finally:
        # 从全局跟踪字典中移除进程
        with process_lock:
            if task_id in running_processes:
                del running_processes[task_id]

@app.post("/train")
def trigger_training(req: TrainRequest, background_tasks: BackgroundTasks):
    """触发训练任务"""
    task_id = generate_task_id(req.learning_rate, req.epochs)
    background_tasks.add_task(run_training, req.learning_rate, req.epochs, task_id)
    return {
        "message": "Training started.",
        "task_id": task_id,
        "parameters": {
            "learning_rate": req.learning_rate,
            "epochs": req.epochs
        }
    }

@app.post("/stop_train")
def stop_training(req: StopTrainRequest):
    """停止指定的训练任务"""
    task_id = req.task_id
    
    with process_lock:
        if task_id not in running_processes:
            raise HTTPException(
                status_code=404, 
                detail=f"训练任务 {task_id} 不存在或已完成"
            )
        
        process = running_processes[task_id]
        
        try:
            # 尝试优雅地终止进程
            process.terminate()
            print(f"已发送终止信号给训练任务 {task_id}")
            
            # 等待一段时间看进程是否优雅退出
            try:
                process.wait(timeout=5)
                print(f"训练任务 {task_id} 已优雅退出")
            except subprocess.TimeoutExpired:
                # 如果进程没有在5秒内退出，强制杀死
                process.kill()
                print(f"强制终止训练任务 {task_id}")
                
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"终止训练任务 {task_id} 时出错: {str(e)}"
            )
    
    return {
        "message": f"训练任务 {task_id} 已被终止",
        "task_id": task_id
    }

@app.get("/running_tasks")
def get_running_tasks():
    """获取当前正在运行的训练任务列表"""
    with process_lock:
        running_task_ids = list(running_processes.keys())
        
        # 检查进程是否仍在运行，清理已完成的任务
        active_tasks = []
        for task_id in running_task_ids:
            process = running_processes[task_id]
            if process.poll() is None:  # 进程仍在运行
                active_tasks.append(task_id)
            else:
                # 进程已完成，从字典中移除
                del running_processes[task_id]
    
    return {
        "running_tasks": active_tasks,
        "count": len(active_tasks)
    }

@app.get("/")
def read_root():
    return {"message": "PyTorch Training Service", "status": "running"}