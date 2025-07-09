import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import mlflow
import mlflow.pytorch
import torchvision

LR = 0.001
DOWNLOAD = True
DATA = "datasets/cifar10/"

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(10, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.fc(x)

def train(learning_rate, epochs):
    mlflow.start_run()
    mlflow.log_param("learning_rate", learning_rate)
    mlflow.log_param("epochs", epochs)

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

    model = torchvision.models.resnet34()
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=LR, momentum=0.9)
    model.train()
    model = model.to("xpu")
    criterion = criterion.to("xpu")

    print(f"Initiating training")
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
            print(f"Iteration [{batch_idx+1}/{train_len}], Loss: {iteration_loss:.4f}")
            # Log loss to MLflow
            mlflow.log_metric("loss", iteration_loss, step=batch_idx)
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
        },
        "checkpoint.pth",
    )

    # Log model to MLflow
    mlflow.pytorch.log_model(model, "model")

    # End MLflow run
    mlflow.end_run()

    print("Execution finished")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--learning_rate", type=float, default=0.001)
    parser.add_argument("--epochs", type=int, default=5)
    args = parser.parse_args()
    train(args.learning_rate, args.epochs)