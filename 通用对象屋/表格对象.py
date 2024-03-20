import csv

from 公共函数屋.字符转换 import 字符串转数字


class 逗号分隔符类:

    def __init__(self, 完整文件路径: str):
        print("逗号分隔符类")
        self.完整文件路径 = 完整文件路径
        self.文件数据列表 = []
        self.打开文件()

    def 打开文件(self):
        # 之所以使用gbk是为了方便用excel打开csv文件
        with open(self.完整文件路径, newline='', encoding='gbk') as 文件:
            文件阅读器 = csv.reader(文件)
            for 行 in 文件阅读器:
                # 转换数据格式
                新行 = list(map(字符串转数字, 行))
                self.文件数据列表.append(新行)
