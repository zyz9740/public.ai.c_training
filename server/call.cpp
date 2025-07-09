#include <iostream>
#include <string>
#include <curl/curl.h>
#include <thread>
#include <chrono>
#include <sstream>

// 回调函数用于接收响应数据
size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* response) {
    size_t totalSize = size * nmemb;
    response->append((char*)contents, totalSize);
    return totalSize;
}

// HTTP GET请求函数
bool httpGet(const std::string& url, std::string& response, long& httpCode) {
    CURL* curl = curl_easy_init();
    if (!curl) return false;
    
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
    
    CURLcode res = curl_easy_perform(curl);
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &httpCode);
    curl_easy_cleanup(curl);
    
    return res == CURLE_OK;
}

// HTTP POST请求函数
bool httpPost(const std::string& url, const std::string& jsonData, std::string& response, long& httpCode) {
    CURL* curl = curl_easy_init();
    if (!curl) return false;
    
    // 设置请求头
    struct curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_POST, 1L);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonData.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
    
    CURLcode res = curl_easy_perform(curl);
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &httpCode);
    
    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);
    
    return res == CURLE_OK;
}

// 简单的JSON解析函数 - 提取task_id
std::string extractTaskId(const std::string& jsonResponse) {
    std::string searchStr = "\"task_id\":\"";
    size_t pos = jsonResponse.find(searchStr);
    if (pos != std::string::npos) {
        pos += searchStr.length();
        size_t endPos = jsonResponse.find("\"", pos);
        if (endPos != std::string::npos) {
            return jsonResponse.substr(pos, endPos - pos);
        }
    }
    return "";
}

// 检查服务状态
bool checkServiceStatus(const std::string& baseUrl) {
    std::cout << "🚀 测试训练任务的启动和停止功能..." << std::endl;
    std::cout << "\n1. 检查服务状态..." << std::endl;
    
    std::string response;
    long httpCode;
    
    if (!httpGet(baseUrl + "/", response, httpCode)) {
        std::cout << "✗ 无法连接到服务器" << std::endl;
        return false;
    }
    
    if (httpCode == 200) {
        std::cout << "✓ 服务状态: " << response << std::endl;
        return true;
    } else {
        std::cout << "✗ 服务未运行，HTTP状态码: " << httpCode << std::endl;
        return false;
    }
}

// 启动训练任务
std::string startTraining(const std::string& baseUrl) {
    std::cout << "\n2. 启动训练任务..." << std::endl;
    
    // 构建训练请求JSON
    std::string jsonData = "{\"learning_rate\": 0.001, \"epochs\": 10}";
    
    std::cout << "📚 启动训练任务: " << jsonData << std::endl;
    
    std::string response;
    long httpCode;
    
    if (!httpPost(baseUrl + "/train", jsonData, response, httpCode)) {
        std::cout << "✗ 网络请求失败" << std::endl;
        return "";
    }
    
    if (httpCode == 200) {
        std::string taskId = extractTaskId(response);
        
        std::cout << "✓ 训练任务已启动" << std::endl;
        std::cout << "  Task ID: " << taskId << std::endl;
        std::cout << "  响应: " << response << std::endl;
        
        return taskId;
    } else {
        std::cout << "✗ 启动训练失败，HTTP状态码: " << httpCode << std::endl;
        std::cout << "  错误响应: " << response << std::endl;
        return "";
    }
}

// 查看正在运行的任务
void checkRunningTasks(const std::string& baseUrl) {
    std::cout << "\n📋 查看正在运行的任务..." << std::endl;
    
    std::string response;
    long httpCode;
    
    if (httpGet(baseUrl + "/running_tasks", response, httpCode)) {
        if (httpCode == 200) {
            std::cout << "  正在运行的任务: " << response << std::endl;
        } else {
            std::cout << "✗ 获取任务列表失败，HTTP状态码: " << httpCode << std::endl;
        }
    } else {
        std::cout << "✗ 网络请求失败" << std::endl;
    }
}

// 停止训练任务
bool stopTraining(const std::string& baseUrl, const std::string& taskId) {
    std::cout << "\n🛑 停止训练任务: " << taskId << std::endl;
    
    // 构建停止请求JSON
    std::string jsonData = "{\"task_id\": \"" + taskId + "\"}";
    
    std::string response;
    long httpCode;
    
    if (!httpPost(baseUrl + "/stop_train", jsonData, response, httpCode)) {
        std::cout << "✗ 网络请求失败" << std::endl;
        return false;
    }
    
    if (httpCode == 200) {
        std::cout << "✓ 训练任务已停止: " << response << std::endl;
        return true;
    } else {
        std::cout << "✗ 停止训练失败，HTTP状态码: " << httpCode << std::endl;
        std::cout << "  错误信息: " << response << std::endl;
        return false;
    }
}

// 测试停止不存在的任务
void testStopNonexistentTask(const std::string& baseUrl) {
    std::cout << "\n🧪 测试停止不存在的任务..." << std::endl;
    
    std::string fakeTaskId = "train_0.001_5_9999999999999";
    std::string jsonData = "{\"task_id\": \"" + fakeTaskId + "\"}";
    
    std::string response;
    long httpCode;
    
    if (httpPost(baseUrl + "/stop_train", jsonData, response, httpCode)) {
        if (httpCode == 404) {
            std::cout << "✓ 正确处理了不存在的任务: " << response << std::endl;
        } else {
            std::cout << "✗ 未正确处理不存在的任务，HTTP状态码: " << httpCode << std::endl;
        }
    } else {
        std::cout << "✗ 网络请求失败" << std::endl;
    }
}

// 获取用户输入
bool getUserInput(const std::string& prompt) {
    std::cout << prompt;
    std::string input;
    std::getline(std::cin, input);
    
    // 转换为小写
    for (auto& c : input) {
        c = std::tolower(c);
    }
    
    return input == "y" || input == "yes";
}

// 主测试函数
void testTrainAndStop() {
    const std::string baseUrl = "http://localhost:8000";
    
    // 1. 检查服务状态
    if (!checkServiceStatus(baseUrl)) {
        std::cout << "\n请先启动FastAPI服务器!" << std::endl;
        std::cout << "启动命令: uvicorn app:app --host 0.0.0.0 --port 8000 --reload" << std::endl;
        return;
    }
    
    // 2. 启动训练任务
    std::string taskId = startTraining(baseUrl);
    if (taskId.empty()) {
        return;
    }
    
    // 3. 等待训练开始
    std::cout << "\n⏳ 等待5秒让训练开始..." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(5));
    
    // 4. 查看正在运行的任务
    checkRunningTasks(baseUrl);
    
    // 5. 询问是否要停止训练
    bool shouldStop = getUserInput("\n❓ 是否要停止训练任务 " + taskId + "? (y/n): ");
    
    if (shouldStop) {
        // 6. 停止训练任务
        if (stopTraining(baseUrl, taskId)) {
            // 7. 等待一下再次查看任务状态
            std::this_thread::sleep_for(std::chrono::seconds(2));
            std::cout << "\n📋 停止后的运行任务状态..." << std::endl;
            checkRunningTasks(baseUrl);
        }
    } else {
        std::cout << "\n➡️ 训练任务 " << taskId << " 将继续运行" << std::endl;
        std::cout << "   您可以稍后使用以下命令停止:" << std::endl;
        std::cout << "   curl -X POST " << baseUrl << "/stop_train -H 'Content-Type: application/json' -d '{\"task_id\": \"" << taskId << "\"}'" << std::endl;
    }
}

int main() {
    std::cout << "=== 训练任务控制测试程序 (C++ 版本) ===" << std::endl;
    std::cout << "Starting HTTP client..." << std::endl;

    // 初始化 curl
    std::cout << "Initializing curl..." << std::endl;
    curl_global_init(CURL_GLOBAL_DEFAULT);
    
    // 执行主要测试流程
    testTrainAndStop();
    
    // 测试停止不存在的任务
    testStopNonexistentTask("http://localhost:8000");
    
    // 清理
    std::cout << "\nCleaning up..." << std::endl;
    curl_global_cleanup();
    std::cout << "Program finished." << std::endl;
    
    std::cout << "\n按任意键退出..." << std::endl;
    std::cin.get();
    
    return 0;
}
