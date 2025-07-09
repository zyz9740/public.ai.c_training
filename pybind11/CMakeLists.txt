cmake_minimum_required(VERSION 3.4)
project(cmake_example)
find_package(pybind11 CONFIG REQUIRED)


add_executable(main main.cpp)
target_link_libraries(main PUBLIC pybind11::embed)
