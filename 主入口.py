import pandas as pd

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    当前索引 = 0
    计数 = 100
    while True:
        列表 = [
            {
                "数据": "数据1",
                "前往": 1
            },
            {
                "数据": "数据2",
                "前往": 2
            },
            {
                "数据": "数据3",
                "前往": 3
            },
            {
                "数据": "数据4",
                "前往": 1
            }
        ]

        print(列表[当前索引]["数据"])
        当前索引 = 列表[当前索引]["前往"]
        if 当前索引 == -1:
            break
        计数 -= 1
        if 计数 == 0:
            break
