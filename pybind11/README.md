# Windows

## Setup Env

```
python -m venv pbvenv
pbvenv\Scripts\activate.bat
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/xpu
pip install pybind11[global]
set pybind11_DIR=C:\Users\your_venv_path\Lib\site-packages\pybind11\
```

> set the venv path in `set pybind11_DIR=C:\Users\your_venv_path\Lib\site-packages\pybind11\`

## Build

```
mkdir build
cd build
cmake ..
cmake --build . --config Release
```

## Run

```
cd ..
build\Release\main.exe

```

```
Starting Training...
Training Device: xpu
Epoch: 1/3, Batch: 100/391, Loss: 1.3030, Accuracy: 37.19%
Epoch: 1/3, Batch: 200/391, Loss: 0.9867, Accuracy: 46.07%
Epoch: 1/3, Batch: 300/391, Loss: 0.8834, Accuracy: 51.10%
Epoch 1 complete | training loss: 1.3110 | training acc: 53.94% | test acc: 66.83%
Epoch: 2/3, Batch: 100/391, Loss: 1.0084, Accuracy: 67.18%
Epoch: 2/3, Batch: 200/391, Loss: 0.9395, Accuracy: 67.70%
Epoch: 2/3, Batch: 300/391, Loss: 0.8713, Accuracy: 68.43%
Epoch 2 complete | training loss: 0.8946 | training acc: 68.76% | test acc: 72.47%
Epoch: 3/3, Batch: 100/391, Loss: 0.7668, Accuracy: 72.38%
Epoch: 3/3, Batch: 200/391, Loss: 0.8144, Accuracy: 72.50%
Epoch: 3/3, Batch: 300/391, Loss: 0.8550, Accuracy: 72.90%
Epoch 3 complete | training loss: 0.7692 | training acc: 73.14% | test acc: 75.48%
training done！
model saved to resnet18_cifar10.pth

---------------------
Getting results from python script:
  Loss: 0.76924
  Train Accuracy: 73.144
  Test Accuracy: 75.48

```


# Linux

## Setup Env

```
conda create -n pb python=3.11
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/xpu
pip install pybind11[global]
```


## Build

```
mkdir build
cd build
cmake ..
cmake --build . --config Release
```

## Run

```
cd ..
build/main
```

```
Training Device: cuda:0
Starting Training...

Epoch: 1/3, Batch: 100/391, Loss: 1.4052, Accuracy: 37.27%
Epoch: 1/3, Batch: 200/391, Loss: 1.2210, Accuracy: 45.99%
Epoch: 1/3, Batch: 300/391, Loss: 1.1098, Accuracy: 50.71%
Epoch 1 complete | training loss: 1.3143 | training acc: 53.60% | test acc: 66.11%
Epoch: 2/3, Batch: 100/391, Loss: 0.9303, Accuracy: 66.40%
Epoch: 2/3, Batch: 200/391, Loss: 0.7760, Accuracy: 67.57%
Epoch: 2/3, Batch: 300/391, Loss: 0.9335, Accuracy: 68.28%
Epoch 2 complete | training loss: 0.8962 | training acc: 68.75% | test acc: 72.59%
Epoch: 3/3, Batch: 100/391, Loss: 0.8401, Accuracy: 72.09%
Epoch: 3/3, Batch: 200/391, Loss: 0.7643, Accuracy: 72.36%
Epoch: 3/3, Batch: 300/391, Loss: 0.7163, Accuracy: 72.80%
Epoch 3 complete | training loss: 0.7746 | training acc: 73.06% | test acc: 75.41%
training done！
model saved to resnet18_cifar10.pth

---------------------
Getting results from python script:
  Loss: 0.774566
  Train Accuracy: 73.056
  Test Accuracy: 75.41

```
