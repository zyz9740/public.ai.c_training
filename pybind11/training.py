import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torchvision.models import resnet18, ResNet18_Weights
from torch.utils.data import DataLoader
# import matplotlib.pyplot as plt


def train(model, device, train_loader, optimizer, epoch, num_epochs):
    model.train()  
    total_loss = 0.0
    correct = 0
    total = 0
    criterion = nn.CrossEntropyLoss()  

    for batch_idx, (data, targets) in enumerate(train_loader):
        data, targets = data.to(device), targets.to(device)
        optimizer.zero_grad()
        
        outputs = model(data)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()
        
        # 打印训练进度
        if (batch_idx+1) % 100 == 0:
            print(f"Epoch: {epoch}/{num_epochs}, Batch: {batch_idx+1}/{len(train_loader)}, "
                  f"Loss: {loss.item():.4f}, Accuracy: {100.*correct/total:.2f}%")
    
    average_loss = total_loss / len(train_loader)
    train_accuracy = 100. * correct / total
    return average_loss, train_accuracy

def evaluate(model, device, test_loader):
    model.eval()  # 设置为评估模式
    correct = 0
    total = 0
    with torch.no_grad():  # 关闭梯度计算
        for data, targets in test_loader:
            data, targets = data.to(device), targets.to(device)
            outputs = model(data)
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()
    
    test_accuracy = 100. * correct / total
    return test_accuracy

def start_training(num_epochs: int = 10,
                    batch_size: int = 128,
                    learning_rate: float = 0.001,
                    momentum: float = 0.9
                    ) -> tuple:
    print("Starting Training...")
    device = torch.device("xpu" if torch.xpu.is_available() else "cpu")
    print(f"Training Device: {device}")
    # 数据预处理（标准化和数据增强）
    transform = transforms.Compose([
        transforms.RandomCrop(32, padding=4),  # 随机裁剪增强
        transforms.RandomHorizontalFlip(),     # 随机水平翻转
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],  # ImageNet 均值（适用于 CIFAR-10）
            std=[0.229, 0.224, 0.225]   # ImageNet 标准差
        )
    ])

    # 加载数据集
    train_dataset = datasets.CIFAR10(
        root="./data",
        train=True,
        download=True,
        transform=transform
    )

    test_dataset = datasets.CIFAR10(
        root="./data",
        train=False,
        download=True,
        transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    )

    # 数据加载器
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    # 加载预训练的 ResNet18（适用于 ImageNet，需调整最后一层全连接层）
    model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1).to(device)

    # 修改最后一层全连接层以匹配 CIFAR-10 类别数
    num_classes = 10  # CIFAR-10 
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes).to(device)

    optimizer = optim.SGD(
        model.parameters(),
        lr=learning_rate,
        momentum=momentum,
        weight_decay=5e-4  # 权重衰减防止过拟合
    )

    # 学习率衰减策略（每 30 个 epoch 衰减 10 倍）
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)

    train_losses = []
    train_accuracies = []
    test_accuracies = []

    for epoch in range(1, num_epochs+1):
        # 训练 epoch
        loss, train_acc = train(model, device, train_loader, optimizer, epoch, num_epochs)
        train_losses.append(loss)
        train_accuracies.append(train_acc)
        
        # 评估 epoch
        test_acc = evaluate(model, device, test_loader)
        test_accuracies.append(test_acc)
        
        # 学习率衰减
        scheduler.step()
        
        print(f"Epoch {epoch} complete | training loss: {loss:.4f} | training acc: {train_acc:.2f}% | test acc: {test_acc:.2f}%")

    print("training done！")

    torch.save(model.state_dict(), "resnet18_cifar10.pth")
    print("model saved to resnet18_cifar10.pth")
    return loss, train_acc, test_acc

if __name__ == "__main__":
    start_training(num_epochs=3)
