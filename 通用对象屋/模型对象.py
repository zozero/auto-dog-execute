import os
import shutil


class 模型操作类:
    # 主要用于对模型的删除，增加，复制等操作
    def __init__(self, 项目名: str, 模型类型: str = '你只看一次'):
        print("模型操作类")
        self.项目名 = 项目名
        self.模型类型 = 模型类型

        self.原模型存放路径 = os.path.join('资源存放屋', 模型类型, '基础模型.pt')
        self.项目智能目录路径 = os.path.join('项目文件屋', 项目名, '智能间', 模型类型, '模型箱')
        self.项目模型存放路径 = os.path.join(self.项目智能目录路径, '模型.pt')

        self.检查()

    def 检查(self):
        if os.path.exists(self.项目智能目录路径) is False:
            os.makedirs(self.项目智能目录路径, exist_ok=True)
        # 复制模型
        if os.path.exists(self.项目模型存放路径) is False:
            shutil.copy(self.原模型存放路径, self.项目模型存放路径)

    def 保存旧模型(self):
        模型数量 = len(os.listdir(self.项目智能目录路径))
        # 这边已经给模型一个新的名字了。
        旧模型存放路径 = os.path.join(self.项目智能目录路径, self.项目名 + '-' + self.模型类型 + str(模型数量) + '.pt')
        # 复制模型
        if os.path.exists(self.项目模型存放路径):
            shutil.copy(self.项目模型存放路径, 旧模型存放路径)
