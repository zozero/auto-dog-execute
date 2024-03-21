import re

import pandas as pd

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    字符串="1000"
    结果=re.search(r"^\d+\.\d+|^-\d+\.\d+|^\.\d+", 字符串)
    print(结果)