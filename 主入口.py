import pandas as pd
# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':

    import re

    # 假设我们要匹配一个点（.）
    text = "This is a sentence This is another sentence"

    # 正则表达式中点（.）需要转义
    escaped_dot = "\."

    # 使用re模块的search方法进行匹配
    matches = re.search(escaped_dot, text)

    # 如果匹配成功，打印匹配结果
    if matches:
        print("匹配成功:", matches.group())
    else:
        print("没有匹配到点（.）")
