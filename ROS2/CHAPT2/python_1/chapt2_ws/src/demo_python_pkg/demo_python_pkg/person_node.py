import rclpy
from rclpy.node import  Node

class PersonNode(Node):
    def __init__(self,node_name:str,name_value:str,age_value:int)->None:
        print("PersonNode __init__ 方法被调用了 添加了两个属性")
        super().__init__(node_name)
        self.name=name_value
        self.age=age_value

    def eat(self,food_name:str):
        """
        方法：吃东西
        :food_name 食物名字
        """
        # print(f"{self.name},{self.age}岁,爱吃{food_name}")
        self.get_logger().info(print(f"{self.name},{self.age}岁,爱吃{food_name}"))


def main():
    rclpy.init()
    node = PersonNode("zhangsan","张三",18)
    node.eat("鱼香肉丝")
    node1 = PersonNode("xiaowamg","小王",20)
    node1.eat("西红柿")
    rclpy.spin(node)
    rclpy.shutdown()
