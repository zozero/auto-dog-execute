import os
import yaml
import shutil


class 仍是一种标记语言类:
    # 就是yaml文件，"Yet Another Markup Language"（仍是一种标记语言）

    def __init__(self, 项目名: str, 模型类型: str = '你只看一次'):
        print("仍是一种标记语言类")

        self.项目名 = 项目名

        self.原配置文件路径 = os.path.join('资源存放屋', 模型类型, '基础配置.yaml')
        self.项目智能目录路径 = os.path.join('项目文件屋', 项目名, '智能间', 模型类型)
        self.项目配置文件路径 = os.path.join(self.项目智能目录路径, '配置.yaml')

        self.数据存放路径 = os.path.join(self.项目智能目录路径, '数据箱')

        self.检查()
        # 它不是原配置文件路径的文件对象，而是项目下的配置文件对象
        self.项目配置文件对象 = None

    def 打开(self):
        # 打开文件修改
        with open(self.项目配置文件路径, 'r', encoding='utf-8') as 项目配置文件:
            项目配置文件对象 = yaml.safe_load(项目配置文件)
            self.项目配置文件对象 = 项目配置文件对象

    def 保存(self):
        with open(self.项目配置文件路径, 'w', encoding='utf-8') as 新文件:
            yaml.dump(self.项目配置文件对象, 新文件, default_flow_style=False, allow_unicode=True, encoding='utf-8')

    def 修改(self, 键, 值):
        self.项目配置文件对象[键] = 值

    def 增加分类(self, 分类: str):
        # 在分类最后面添加一个新的分类，然后保存
        self.项目配置文件对象['names'][len(self.项目配置文件对象['names'])] = 分类
        self.保存()

    def 获得分类列表(self):
        return self.项目配置文件对象['names']

    def 检查(self):
        """
        检查是否需要创建文件和文件夹
        :return:
        """
        if os.path.exists(self.项目智能目录路径) is False:
            os.makedirs(self.项目智能目录路径, exist_ok=True)

        # 复制配置文件
        if os.path.exists(self.项目配置文件路径) is False:
            shutil.copy(self.原配置文件路径, self.项目配置文件路径)

        # 数据存放路径
        if os.path.exists(self.数据存放路径) is False:
            os.makedirs(self.数据存放路径, exist_ok=True)
