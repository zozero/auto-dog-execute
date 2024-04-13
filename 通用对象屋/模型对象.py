import os
import shutil

from 通用对象屋.消息对象 import 消息提示类


class 模型操作类:
    # 主要用于对模型的删除，增加，复制等操作
    def __init__(self, 项目名: str, 分类名: str, 模型类型: str = '你只看一次'):
        print("模型操作类")
        self.项目名 = 项目名
        self.模型类型 = 模型类型
        self.分类名 = 分类名

        self.原模型存放路径 = os.path.join('资源存放屋', 模型类型, '基础模型.pt')
        self.模型箱目录 = os.path.join('项目文件屋', 项目名, '智能间', 模型类型, 分类名, '模型箱')
        self.模型目录 = os.path.join(self.模型箱目录, 'train', 'weights')
        self.项目模型存放路径 = os.path.join(self.模型目录, 'best.pt')

        self.检查()

    def 检查(self):
        if os.path.exists(self.模型目录) is False:
            os.makedirs(self.模型目录, exist_ok=True)
        # 复制模型
        if os.path.exists(self.项目模型存放路径) is False:
            shutil.copy(self.原模型存放路径, self.项目模型存放路径)

    def 最佳模型路径(self):
        文件夹列表 = os.listdir(self.模型箱目录)
        计数 = len(文件夹列表)

        for i in range(1, 计数 + 1):
            文件路径 = os.path.join(self.模型箱目录, 文件夹列表[-i], 'weights', 'best.pt')
            if os.path.exists(文件路径):
                return 文件路径
        return 消息提示类.致命错误('模型操作类->最佳模型路径','不存在模型文件。')
