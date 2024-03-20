import pandas as pd
from pandas.core.indexing import _LocIndexer


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
        self.文件数据表 = pd.read_csv(self.完整文件路径, index_col="序号", encoding='gbk', na_filter=False)
        self.数据列表: _LocIndexer = self.文件数据表.loc
        self.数据数量 = self.文件数据表.count()
        self.索引列表 = self.文件数据表.index.tolist()
