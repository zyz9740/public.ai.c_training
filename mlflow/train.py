import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import torchvision
import os
import sys
from datetime import datetime

LR = 0.001
DOWNLOAD = True
DATA = "datasets/cifar10/"

def train(learning_rate, epochs):
    print(f"Starting training with learning_rate={learning_rate}, epochs={epochs}")
    sys.stdout.flush()  # 强制刷新输出
    print(f"Training started at: {datetime.now()}")
    sys.stdout.flush()
    
    # 创建输出目录用于保存模型和日志
    output_dir = "training_outputs"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory created: {output_dir}")
    sys.stdout.flush()
    
    # 记录训练参数到文件
    with open(os.path.join(output_dir, "training_params.txt"), "w") as f:
        f.write(f"learning_rate: {learning_rate}\n")
        f.write(f"epochs: {epochs}\n")
        f.write(f"start_time: {datetime.now()}\n")

    transform = torchvision.transforms.Compose(
        [
            torchvision.transforms.Resize((224, 224)),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ]
    )
    train_dataset = torchvision.datasets.CIFAR10(
        root=DATA,
        train=True,
        transform=transform,
        download=DOWNLOAD,
    )
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=32)
    train_len = len(train_loader)
    print(f"Dataset loaded: {len(train_dataset)} samples, {train_len} batches")
    sys.stdout.flush()

    model = torchvision.models.resnet34()
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate, momentum=0.9)  # 使用传入的learning_rate
    model.train()
    print("Model initialized")
    sys.stdout.flush()
    model = model.to("xpu")
    criterion = criterion.to("xpu")
    print("Model moved to XPU device")
    sys.stdout.flush()

    print(f"Initiating training for {epochs} epochs")
    sys.stdout.flush()
    training_losses = []
    
    for epoch in range(epochs):
        print(f"\n=== Epoch {epoch+1}/{epochs} ===")
        sys.stdout.flush()
        
        for batch_idx, (data, target) in enumerate(train_loader):
            data = data.to("xpu")
            target = target.to("xpu")
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
            if (batch_idx + 1) % 10 == 0:
                iteration_loss = loss.item()
                training_losses.append(iteration_loss)
                print(f"Epoch [{epoch+1}/{epochs}], Batch [{batch_idx+1}/{train_len}], Loss: {iteration_loss:.4f}")
                sys.stdout.flush()
    
        # 保存训练损失到文件
        print("Saving training results...")
        sys.stdout.flush()
        with open(os.path.join(output_dir, "training_losses.txt"), "w") as f:
            for i, loss in enumerate(training_losses):
                f.write(f"step_{i*10}: {loss}\n")
        
        # 保存模型检查点
        checkpoint_path = os.path.join(output_dir, "checkpoint.pth")
        torch.save(
            {
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "training_losses": training_losses,
                "learning_rate": learning_rate,
                "epochs": epochs,
            },
            checkpoint_path,
        )
        print(f"Checkpoint saved to: {checkpoint_path}")

    
    # 保存完整模型
    model_path = os.path.join(output_dir, "trained_model.pth")
    torch.save(model, model_path)
    
    print(f"Model saved to: {model_path}")
    print("Execution finished")
    print(f"Training completed at: {datetime.now()}")
    sys.stdout.flush()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--learning_rate", type=float, default=0.001)
    parser.add_argument("--epochs", type=int, default=5)
    args = parser.parse_args()
    train(args.learning_rate, args.epochs)