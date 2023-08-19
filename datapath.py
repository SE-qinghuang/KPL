import os

'''
对于整个项目级别的一些常量进行定义，方便其他地方引用。
注意：在代码中千万不要使用绝对路径，要使用基于ROOT_DIR的相对路径
'''

# Path_name
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root

general_DIR = ROOT_DIR + "/data/"