import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/nkh/ROS2/CHAPT5/install/demo_python_tf'
