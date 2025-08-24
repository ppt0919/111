from demo_python_pkg.person_node import PersonNode

class WritterNode(PersonNode):
    def __init__(self,name:str,age:int,book:str)->None:
        print("WritterNode __init__ 方法被调用了")
        super().__init__(name,age)
        self.book = book


def main():

    node = WritterNode("张三",18,"书")
    node.eat("ROS")