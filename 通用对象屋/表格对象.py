import os

import pandas as pd

统一编码 = 'gbk'


class 逗号分隔符类:
    def __init__(self, 完整文件路径: str):
        print("逗号分隔符类")
        self.完整文件路径 = 完整文件路径
        self.文件数据表 = None
        self.数据列表 = None
        self.数据数量 = 0
        self.索引列表 = []
        self.读取数据()

    def 读取数据(self):
        self.文件数据表 = pd.read_csv(self.完整文件路径, index_col="序号", encoding=统一编码, na_filter=False)
        self.数据列表 = self.文件数据表.loc
        self.数据数量 = len(self.文件数据表)
        self.索引列表 = self.文件数据表.index.tolist()


class 表格处理类:
    """
    主要是数据的增加或者减少
    创建对应的表格
    确保每个表格都会有序号
    """

    def __init__(self, 完整路径, 一条数据: dict):
        self.完整路径 = 完整路径
        self.一条数据 = 一条数据
        self.数据数量 = 0
        self.序号尾巴 = 0
        self.数据表 = None
        self.读取数据表()

    def 读取数据表(self):
        # 判断是否存在csv文件
        if os.path.exists(self.完整路径):
            self.数据表 = pd.read_csv(self.完整路径, index_col="序号", encoding=统一编码, na_filter=False)
        else:
            self.创建csv表格()

        self.数据数量 = len(self.数据表)
        if self.数据数量 > 0:
            self.序号尾巴 = self.数据表[-1:].index[0]

    def 添加数据(self):
        if self.一条数据["序号"][0] is None or self.一条数据["序号"][0] == "":
            self.一条数据["序号"][0] = self.序号尾巴 + 1
        数据帧 = pd.DataFrame(self.一条数据)
        数据帧.to_csv(self.完整路径, mode='a', header=False, index=False, encoding=统一编码)

    def 创建csv表格(self):
        键列表 = self.一条数据.keys()
        字典 = {}
        for 键 in 键列表:
            字典[键] = []
        数据帧 = pd.DataFrame(字典)
        # 因为是第一次添加所以要添加列名
        数据帧.to_csv(self.完整路径, mode='a', index=False, header=True, encoding=统一编码)
        self.数据表 = pd.read_csv(self.完整路径, index_col="序号", encoding=统一编码, na_filter=False)
