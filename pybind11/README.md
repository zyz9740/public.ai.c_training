# Setup Env

```
conda create -n pb python=3.11
pip install -r requirements.txt
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
