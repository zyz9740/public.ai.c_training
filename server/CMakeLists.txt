cmake_minimum_required(VERSION 3.10)
project(MLFlowClient)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_BUILD_TYPE Release)

# 查找 CURL 库
# set(CMAKE_PREFIX_PATH "path/to/vcpkg/installed/x64-windows")
set(CMAKE_PREFIX_PATH "C:/Users/intel/Desktop/vcpkg/installed/x64-windows")

find_package(CURL REQUIRED)

# 创建可执行文件
add_executable(call call.cpp)

# 链接 CURL 库
target_link_libraries(call ${CURL_LIBRARIES})
target_include_directories(call PRIVATE ${CURL_INCLUDE_DIRS})
