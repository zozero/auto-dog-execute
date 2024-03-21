import re

import pandas as pd

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    df = pd.DataFrame({'name': ['Raphael', 'Donatello', 'Donatello2', 'Donatello3'],
                       'mask': ['red', 'purple', 'purple2', 'purple3'],
                       'weapon': ['sai', 'bo staff', 'bo staff2', 'bo staff3']},index=['name'])
    print(df)
    print(df[-1:].index)
