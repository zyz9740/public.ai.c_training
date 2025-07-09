# Console 1: Start MLflow Server
conda env create -f conda.yaml
conda activate train-env
mlflow server

# Console 2: Start Training Server
set MLFLOW_TRACKING_URI=http://localhost:5000
conda activate train-env
uvicorn app:app --reload

# Console 3: Mock Client Call
call.bat

# Console 3 (Optional): Mock Client Call in C++
## Dependencies
- CMake (3.10 or higher)
- libcurl development library
- C++ compiler (g++, clang++, or MSVC)

## Installing libcurl on Windows
```cmd
vcpkg install curl
```
set vcpkg path in CMakeLists.txt:7 
Set dll in path\to\vcpkg\installed\x64-windows\debug\bin or path\to\vcpkg\installed\x64-windows\bin

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


