#include <iostream>
#include <functional> //函数包装器

// 自由函数

void save_with_free_fun(const std::string &file_name)
{
    std::cout << "自由函数:" << file_name << std::endl;
}

class FileSave
{
private:
public:
    FileSave() = default;
    ~FileSave() = default;

    void save_with_member_fun(const std::string &file_name)
    {
        std::cout << "成员方法" << file_name << std::endl;
    }
};

int main()
{
    FileSave file_save;

    // lambda函数
    auto save_with_lambda_fun = [](const std::string &file_name) -> void
    {
        std::cout << "lambda函数" << file_name << std::endl;
    };

    // save_with_free_fun("File.txt");
    // file_save.save_with_member_fun("File.txt");
    // save_with_lambda_fun("File.txt");

    std::function<void(const std::string &)> savel1 = save_with_free_fun;
    std::function<void(const std::string &)> savel2 = save_with_lambda_fun;
    // 成员函数放入包装器
    std::function<void(const std::string &)> savel3 = std::bind(&FileSave::save_with_member_fun, 
        &file_save, std::placeholders::_1);

    //统一的调用的函数方法
    savel1("file.txt");
    savel2("file.txt");
    savel3("file.txt");

    return 0;
}