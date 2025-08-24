import rclpy
from rclpy.node import Node
import requests 
from example_interfaces.msg import String
from queue import Queue

# 定义节点类
class NovelPubNode(Node):
    def __init__(self,node_name):
        super().__init__(node_name)
        self.get_logger().info(f"{node_name},启动") # 打印日志
        self.novel_queue=Queue() # 创建队列  注:必须在初始化在前
        self.novel_publisher=self.create_publisher(String,'novel',10)  # 创建发布者
        self.create_timer(5,self.timer_callback)   # 创建定时器
        
    # 定义定时器
    def timer_callback(self):
        # self.novel_publisher.publish()
        if self.novel_queue.qsize()>0:
            line=self.novel_queue.get()
            msg=String()
            msg.data=line

            self.novel_publisher.publish(msg)
            self.get_logger().info(f"发布了:{msg}")
    
    # 下载链接
    def download(self,url):   
        response = requests.get(url)
        response.encoding = 'utf-8'
        text = response.text
        
        self.get_logger().info(f"下载{url},{len(text)}")
        for line in text.splitlines():
            self.novel_queue.put(line)
        # text.splitlines()

def main():
    rclpy.init()
    node=NovelPubNode('novel_pub')
    node.download('http://0.0.0.0:8000/novel1.txt')
    rclpy.spin(node)
    rclpy.shutdown()
