#include <iostream>
#include <pybind11/embed.h> // Required for embedding Python

namespace py = pybind11;

int main() {
    // Initialize the Python interpreter
    py::scoped_interpreter guard{}; 

    try {
        // Import a Python script named 'training.py'
        auto training_script = py::module::import("training");
        py::tuple results = training_script.attr("start_training")(
                                                py::arg("num_epochs")=3
                                            ).cast<py::tuple>();;
        float loss = results[0].cast<float>();
        float train_acc = results[1].cast<float>();
        float test_acc = results[2].cast<float>();
        
        std::cout << "\n--------------------- " << std::endl;
        std::cout << "Getting results from python script: " << std::endl;
        std::cout << "  Loss: " << loss << std::endl;
        std::cout << "  Train Accuracy: " << train_acc << std::endl;
        std::cout << "  Test Accuracy: " << test_acc << std::endl;


    } catch (const py::error_already_set& e) {
        // Handle Python exceptions
        std::cerr << "Python error: " << e.what() << std::endl;
    }

    return 0;
}