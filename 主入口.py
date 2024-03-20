import re

import pandas as pd

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    结果 = re.findall(r"[a-zA-Z]|\d+", 'A1J0')
    print(结果)
