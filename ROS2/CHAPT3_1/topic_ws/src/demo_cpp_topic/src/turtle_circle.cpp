#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include <chrono>

using namespace std::chrono_literals;

class TurtleCircleNode: public rclcpp::Node{
    private:
        rclcpp::TimerBase::SharedPtr timer; //订阅者的共享指针
        rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher; //发布者的智能指针
    public:
        //隠式转化为显式转换
        explicit TurtleCircleNode(const std::string& node_name):Node(node_name)
        {
            publisher=this->create_publisher<geometry_msgs::msg::Twist>("turtle1/cmd_vel",10);
            timer=this->create_wall_timer(1000ms,std::bind(&TurtleCircleNode::timer_callback,this));//绑定
        }

        void timer_callback()
        {
            auto msg=geometry_msgs::msg::Twist();
            msg.linear.x=1.0;
            msg.angular.z=0.5;
            publisher->publish(msg);
        }
};



int main(int argc,char *argv[])
{
    rclcpp::init(argc,argv);
    auto node=std::make_shared<TurtleCircleNode>("turtle_circle");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}