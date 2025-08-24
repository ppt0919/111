import rclpy
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector
import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory
import os
from cv_bridge import CvBridge
import time
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter,ParameterValue,ParameterType

class FaceDetectClientNode(Node):
    def __init__(self):
        super().__init__("face_detect_node")
        self.service=self.create_service(FaceDetector,"face_detect",self.detect_face_callback)
        self.bridge=CvBridge()
        self.default_image_path=os.path.join(get_package_share_directory("demo_python_service"),"resource/test.png")
        self.get_logger().info("人脸检测客户端已经启动")
        self.client=self.create_client(FaceDetector,"face_detect")
        self.image=cv2.imread(self.default_image_path)

    def call_set_parameters(self,parameters):
        """
        调用服务 修改参数值
        """
        #1. 创建一个客户端 等待服务上线
        updata_param_client = self.create_client(SetParameters,"face_detect_node/set_parameters")
        while updata_param_client.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info("等待参数更新服务端上线")

        #2.创建request
        request=SetParameters.Request()
        request.parameters=parameters
        # 3.调用服务器
        future=updata_param_client.call_async(request)
        rclpy.spin_until_future_complete(self,future)    # 等待服务端返回响应
        response=future.result()
        return response
    
    def updata_detect_model(self,model="hog"):
        """根据传入的moel 构造parameters 然后调用call_set_parameters 更新服务端的参数"""
        #1.创建参数对象
        param=Parameter()
        param.name="model"
        #2.赋值 param_value
        param_value=ParameterValue()
        param_value.string_value=model
        param_value.type=ParameterType.PARAMETER_STRING
        param.value=param_value
        #3.请求更新参数
        response=self.call_set_parameters([param])
        for result in response.results:
            self.get_logger().info(f"设置参数结果:{result.successful} {result.reason}")


    def send_request(self):
        # 1.判断服务是否在线
        while self.client.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info("等待服务端上线")
        # 2.构造request
        request=FaceDetector.Request()
        request.image=self.bridge.cv2_to_imgmsg(self.image)
        # 3.发送请求并等待处理完成
        future=self.client.call_async(request) # 现在的future并没有包含响应结果 需要等待服务
        # while future.done():
        #     time.sleep(1.0) # 休眠当前线程 等待服务处理完成 造成当前服务线程无法在接受来自服务端的返回 导致永远没有办法完成 future.done 无法返回true
        rclpy.spin_until_future_complete(self,future)    # 等待服务端返回响应
        response=future.result() # 获取响应
        self.get_logger().info(f"接受到响应,共有{response.number}张人脸,耗时{response.use_time}s")
        self.show_response(response)


    def show_response(self,response):
        for i in range(response.number):
            top=response.top[i]
            right=response.right[i]
            bottom=response.bottom[i]
            left=response.left[i]
            cv2.rectangle(self.image,{left,top},{right,bottom},{255,0,0},4)
        # cv2.imshow("face_detecte,rusult",self.image)
        # cv2.waitKey(0) # 也是阻塞的 会导致spin无法正常进行

def main():
    rclpy.init()
    node=FaceDetectClientNode()
    node.updata_detect_model("hog")
    node.send_request()
    node.updata_detect_model("cnn")
    node.send_request()
    rclpy.spin(node)
    rclpy.shutdown()