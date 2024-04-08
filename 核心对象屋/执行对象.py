import os.path
import time

from 公共函数屋.字符转换 import 字符串转换, 编码转换
from 数据类型屋.结果类型 import 结果类
from 核心对象屋.安卓对象 import 安卓预处理类
from 核心对象屋.方法对象 import 匹配方法类, 方法预处理类
from 通用对象屋.委托对象 import 委托对象类
from 通用对象屋.表格对象 import 逗号分隔符类
from 通用对象屋.默认对象 import 目录名称对象


class 执行类:
    # 最为核心的类，最要是收集数据、识别方法执行、模拟器行为执行
    # 它只执行一个步骤

    def __init__(self, 项目名: str, 任务数据):
        print("执行类")
        self.项目名 = 项目名
        self.任务数据 = 任务数据
        self.步骤数据 = None
        self.行为参数 = {}
        self.判断结果 = 结果类()
        # 预先给一个状态用于判断
        self.判断结果.状态 = False

        # 循环状态参数
        self.循环次数 = 1
        self.中断布尔值 = False
        # 判断是否找了界面
        self.界面布尔值 = False
        # 最终执行结果，它关系到任务流程
        self.最终状态 = False
        # 判断是否要执行行为后进行再次执行
        self.动后布尔值 = False
        # 为了动后判定也特别保存的。
        self.位置编码列表 = ''

        # 具体开始执行
        self.搜集参数()
        self.统筹过程()

    def 搜集参数(self):
        print("搜集参数")
        文件路径 = os.path.join(str(目录名称对象['表格目录']), self.项目名, 目录名称对象['步骤目录'], self.任务数据['名称'] + '.csv')
        表格文件 = 逗号分隔符类(文件路径)
        步骤列表 = 表格文件.数据列表
        self.步骤数据 = 步骤列表[self.任务数据['编号']]

    def 统筹过程(self):
        print("统筹过程")
        while True:
            # 开始之前判断是否停止执行，如果要求停止就立即中断
            if 委托对象类.字典[self.项目名 + '停止']:
                break

            self.判定界面(self.步骤数据['界面编码'])
            self.判定位置(self.步骤数据['方法编码'])
            self.执行行为(self.步骤数据['行为编码'])

            self.动后判定(self.步骤数据['动后编码'])

            self.判定循环()
            if self.中断布尔值:
                break
            else:
                continue

    def 判定循环(self):
        if self.判断结果.状态:
            self.中断布尔值 = True
            self.最终状态 = True
            return
        # 如果没有找到结果，那么根据要求再次去运行一遍统筹过程。
        if self.步骤数据['循环次数'] == 0 or self.循环次数 < self.步骤数据['循环次数']:
            time.sleep(self.步骤数据['循环间隔'])
            self.循环次数 += 1
            # 继续循环
            self.中断布尔值 = False
        else:
            self.中断布尔值 = True
            self.最终状态 = False

    def 判定界面(self, 编码):
        print('判定界面')
        # 很多时候它不是必须的，但它是个可以做补充的策略。
        编码列表 = 字符串转换(编码)
        if 编码列表 and len(编码列表) == 2:
            判断结果: 结果类 = self.识别位置(编码列表)
            self.界面布尔值 = 判断结果.状态
        else:
            self.界面布尔值 = True

    def 判定位置(self, 编码):
        print("判定位置")
        # 这几乎是必须要的，有了它就可以找到对应图片的位置，然后就是执行行为
        编码列表 = 字符串转换(编码)
        self.位置编码列表 = 编码列表
        if 编码列表 and len(编码列表) == 2 and self.界面布尔值:
            self.判断结果: 结果类 = self.识别位置(编码列表)
            print("self.判断结果-----", self.判断结果.__dict__())

    def 识别位置(self, 编码列表):
        """
        识别位置需要两个编码，其中字母编码是用分辨匹配方法的
        :param 编码列表:
        :return:
        """
        print("识别位置")
        # 获取匹配方法
        函数字典 = 匹配方法类.分配函数(编码列表[0])
        项目路径 = os.path.join(目录名称对象['表格目录'], self.项目名)
        文件路径 = os.path.join(项目路径, 目录名称对象['方法目录'], 函数字典['文件名'] + '.csv')

        表格文件 = 逗号分隔符类(文件路径)
        # 编码列表[1]是指第几行数据，拿出来后直接生成一个字典类型。
        参数字典 = 表格文件.数据列表[编码列表[1]].to_dict()
        参数字典['项目名'] = self.项目名
        参数字典['项目路径'] = 项目路径
        # 预处理各种参数，之后用于给匹配方法传参
        预处理 = 方法预处理类(编码列表[0], 参数字典)
        return 函数字典['函数实例'](**预处理.参数字典)

    def 执行行为(self, 编码):
        # 状态不对就直接不执行了
        if self.判断结果.状态 is False:
            return
        编码列表 = 编码转换(编码)
        行为 = 安卓预处理类(self.项目名, 编码列表, self.判断结果)
        行为.参数字典['行为函数'](**行为.参数字典)

    def 动后判定(self, 编码):
        # 该行为可能为了防止执行行为没有成功，有一定极小概率点击失败，并且可能一些会发生网络波动的情况，它可以解决问题。
        # A1J0 A1表示匹配策略A的第1个，J0表示【Z：为真时循环执行，J：为假时循环执行，0：无限次循环，大于零时表示相应循环次数】
        # 它会重复执行一次“执行行为”函数
        # 除非你家网络经常波动，否则这就是个鸡肋行为。
        print("动后判定")
        # 状态不对就直接不执行了
        if self.判断结果.状态 is False or self.界面布尔值 is False:
            return

        编码列表 = 编码转换(编码)
        if len(编码列表) != 4:
            return

        计数 = 1
        while True:
            # 开始之前判断是否停止执行，如果要求停止就立即中断
            if 委托对象类.字典[self.项目名 + '停止']:
                break

            self.动后行为(编码列表)
            time.sleep(self.步骤数据['循环间隔'])

            计数 += 1
            if self.动后布尔值 is False:
                break
            if 计数 > 编码列表[3] != 0:
                break

    def 动后行为(self, 编码列表):
        print("动后行为")
        临时列表 = [编码列表[0], 编码列表[1]]
        判断结果: 结果类 = self.识别位置(临时列表)
        # 判断到啦，我想要再次执行
        if 判断结果.状态 and 编码列表[2] == 'Z':
            判断结果: 结果类 = self.识别位置(self.位置编码列表)
            if 判断结果.状态:
                self.执行行为(self.步骤数据['行为编码'])
            self.动后布尔值 = True
        # 没有判断到，我想要再次执行
        elif 判断结果.状态 is False and 编码列表[2] == 'J':
            判断结果: 结果类 = self.识别位置(self.位置编码列表)
            if 判断结果.状态:
                self.执行行为(self.步骤数据['行为编码'])
            # 这意味继续执行
            self.动后布尔值 = True
        else:
            self.动后布尔值 = False


class 任务类:
    """
    发配任务给执行类
    我们必须假设没有意外情况......
    假设某些判断标准会在任意一处出现，且该判断标准在游戏读取界面内唯一不重复，则把它纳入每次循环之内
    每次点击必须通过判断确定位置
    它只执行一个任务
    """
    任务表: 逗号分隔符类

    def __init__(self, 项目名, 任务名):
        print("任务类")
        self.项目名 = 项目名
        self.任务名 = 任务名
        # 为了实现流程控制，设置初始序号必定为1
        self.序号 = 1
        self.最终执行状态 = True

        # 拆分至外部调用，这样可以一步一步测试。
        # self.获取数据()
        # self.执行任务()

    def 获取数据(self):
        # 获取任务间的指定表格
        print("获取数据")
        文件路径 = os.path.join(str(目录名称对象['表格目录']), self.项目名, 目录名称对象['任务目录'],
                                self.任务名 + '.csv')
        self.任务表 = 逗号分隔符类(文件路径)

    def 执行任务(self):
        print("执行任务")
        数据列表 = self.任务表.文件数据表.loc
        while True:
            # 开始之前判断是否停止执行，如果要求停止就立即中断
            if 委托对象类.字典[self.项目名 + '停止']:
                break

            任务数据 = 数据列表[self.序号]
            if 任务数据['编号'] == 0:
                self.步骤组(任务数据)
            else:
                self.步骤(任务数据)
            # 用于控制执行下一步要做什么，无论如何你必须在最后一步的时候赋值序号为-1
            if self.最终执行状态:
                self.序号 = 数据列表[self.序号]['是']
            else:
                self.序号 = 数据列表[self.序号]['否']
            # 终止了无休止的循环
            if self.序号 == -1:
                break

    def 步骤组(self, 任务信息):
        # 先去拿一遍步骤组里面的数据获取序号，然后一个一个发送给执行类去执行。
        文件路径 = os.path.join(str(目录名称对象['表格目录']), self.项目名, 目录名称对象['步骤目录'],
                                任务信息['名称'] + '.csv')
        表格文件 = 逗号分隔符类(文件路径)
        索引列表 = 表格文件.索引列表
        for i in 索引列表:
            print("步骤组", i)
            参数字典 = {
                '名称': 任务信息['名称'],
                '编号': i,
            }
            执行 = 执行类(self.项目名, 参数字典)
            # 只要步骤名子中有*号，就可以继续执行，这里步骤的名字不会对运行过程产生其他的影响，用于意外突发情况的判定，这样尽可能避免发生最终状态导致的终止
            if '*' in 表格文件.数据列表[i]['名称']:
                continue
            # 我们必须假定没有意外，除非特殊情况，如果有意外就直接停止执行步骤组，进行下一个步骤，当循环出现有限次数，它将变得有意义
            self.最终执行状态 = 执行.最终状态
            if 执行.最终状态 is False:
                break

    def 步骤(self, 任务信息):
        print("步骤")
        参数字典 = {
            '名称': 任务信息['名称'],
            '编号': 任务信息['编号'],
        }
        执行 = 执行类(self.项目名, 参数字典)
        self.最终执行状态 = 执行.最终状态
