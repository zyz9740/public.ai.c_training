#include <iostream>
#include <string>
#include <curl/curl.h>

// 回调函数用于接收响应数据
size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* response) {
    size_t totalSize = size * nmemb;
    response->append((char*)contents, totalSize);
    return totalSize;
}

int main() {
    std::cout << "Starting HTTP client..." << std::endl;

    CURL* curl;
    CURLcode res;
    std::string response;

    // 初始化 curl
    std::cout << "Initializing curl..." << std::endl;
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    
    if(curl) {
        std::cout << "Curl initialized successfully" << std::endl;
        // 设置 URL
        curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:8000/train");
        
        // 设置 POST 请求
        curl_easy_setopt(curl, CURLOPT_POST, 1L);
        
        // 设置请求头
        struct curl_slist* headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        
        // 设置 JSON 数据
        std::string jsonData = "{\"learning_rate\": 0.01, \"epochs\": 3, \"experiment_name\": \"zyz\"}";
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonData.c_str());
        
        std::cout << "Sending request to: http://localhost:8000/train" << std::endl;
        std::cout << "JSON data: " << jsonData << std::endl;
        
        // 设置回调函数来接收响应
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
        
        // 执行请求
        std::cout << "Executing request..." << std::endl;
        res = curl_easy_perform(curl);
        
        // 检查错误
        if(res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        } else {
            std::cout << "Request successful!" << std::endl;
            std::cout << "Response: " << response << std::endl;
        }
        
        // 清理
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    } else {
        std::cerr << "Failed to initialize curl!" << std::endl;
    }
    
    std::cout << "Cleaning up..." << std::endl;
    curl_global_cleanup();
    std::cout << "Program finished." << std::endl;
    return 0;
}
