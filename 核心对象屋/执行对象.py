from 数据类型屋.接收类型 import 任务数据类


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
    def __init__(self,任务数据: 任务数据类):
        self.任务数据=任务数据
        print("任务类")
    def 分析数据(self):
        print("分析数据")
        # self.任务数据.项目名

    def 步骤组(self):
        print("步骤组")

    def 步骤(self):
        print("步骤")

