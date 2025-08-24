#include <memory>
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "rclcpp/rclcpp.hpp" //提供消息接口
#include "tf2/LinearMath/Quaternion.h" //提供tf2::Quaternion类
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp" //消息接口转换函数
#include "tf2_ros/transform_listener.h" //坐标监听类
#include "tf2_ros/buffer.h" //提供buffer
#include "tf2/utils.h" //提供了四元数转欧拉角
#include "chrono"

using namespace std::chrono_literals;

class TFListener:public rclcpp::Node{
    private:
        std::shared_ptr<tf2_ros::TransformListener>boardcaster;
        rclcpp::TimerBase::SharedPtr timer;
        std::shared_ptr<tf2_ros::Buffer> buffer;

    public:
        TFListener():Node("tf_listener")
        {
            buffer=std::make_shared<tf2_ros::Buffer>(this->get_clock());
            this->boardcaster=std::make_shared<tf2_ros::TransformListener>(*buffer,this);
            // this->publish_tf();
            timer=this->create_wall_timer(1s,std::bind(&TFListener::get_transform,this));
        }

        void get_transform()
        {
            //buffer 查询坐标关系
            try
            {
                //查询坐标关系
                const auto transform=buffer->lookupTransform(
                    "base_link","target_point",this->get_clock()->now(),rclcpp::Duration::from_seconds(1.0f)
                );
                auto translation=transform.transform.translation;
                auto rotation=transform.transform.rotation;
                double y,p,r;
                tf2::getEulerYPR(rotation,y,p,r);
                RCLCPP_INFO(get_logger(),"平移%f,%f,%f",translation.x,translation.y,translation.z);
                RCLCPP_INFO(get_logger(),"旋转%f,%f,%f",y,p,r);
            }
            catch(const std::exception& e)
            {
                RCLCPP_WARN(get_logger(),"%s",e.what());
            }
        }

};


int main(int argc,char* argv[])
{
    rclcpp::init(argc,argv);
    auto node =std::make_shared<TFListener>();
    rclcpp::spin(node);
    rclcpp::shutdown();
}