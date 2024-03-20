import os.path

from 数据类型屋.接收类型 import 任务数据类
from 通用对象屋.表格对象 import 逗号分隔符类

目录名称对象 = {
    '表格目录': '表格文件屋',
    '任务目录': '任务间',
}


class 执行类:
    # 最为核心的类，最要是收集数据、识别方法执行、模拟器行为执行
    def __init__(self):
        print("执行类")
        self.搜集参数()
        self.识别位置()
        self.执行行为()
        self.动后执行()

    def 搜集参数(self):
        print("搜集参数")

    def 识别位置(self):
        print("识别位置")

    def 执行行为(self):
        print("执行行为")

    def 动后执行(self):
        print("动后执行")


class 任务类:
    # 发配任务给执行类
    def __init__(self, 任务数据: 任务数据类):
        self.任务数据 = 任务数据
        self.执行任务()
        print("任务类")

    def 获取数据(self, 任务名: str):
        print("获取数据")
        文件路径 = os.path.join(目录名称对象['表格目录'], self.任务数据.项目名, 目录名称对象['任务目录'], 任务名 + '.csv')
        表格文件 = 逗号分隔符类(文件路径)
        return 表格文件.文件数据列表

    def 执行任务(self):
        print("执行任务")
        任务列表=self.获取数据(self.任务数据.任务列表[0])
        print(任务列表[0])
        print(任务列表[1])

    def 步骤组(self):
        print("步骤组")

    def 步骤(self):
        print("步骤")
