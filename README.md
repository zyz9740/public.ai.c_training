目前，基于C++ 使用 pytorch 进行训练，大致有如下两种方式
1. 使用 Python 作为 Server 提供训练服务，C++ 作为 client 进行调用
2. 使用 Pybind 的方式将 python 嵌入 C++ 代码中直接调用
