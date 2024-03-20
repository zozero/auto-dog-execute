import re


def 字符串转换(字符串) -> float | int | str | list:
    字符串 = 字符串.strip()

    if re.search(r"^[A-Z]+\d+", 字符串):
        数据列表 = [
            re.findall(r"[A-Z]", 字符串)[0],
            int(re.findall(r"\d+", 字符串)[0])
        ]
        return 数据列表

    if re.search(r"^\d+.\d+|^-\d+.\d+|^\.\d+", 字符串):
        return float(字符串)

    if re.search(r"^\d+|^-\d+", 字符串):
        return int(字符串)

    return 字符串


def 编码转换(字符串) -> list:
    正则结果 = re.findall(r"[A-Z]|\d+", 字符串)
    新列表 = []
    for 字符 in 正则结果:
        新列表.append(字符串转换(字符))
    return 新列表


def 字典值转数字(字典):
    新字典 = {}
    for 键, 值 in 字典.items():
        新字典[键] = 字符串转换(值)
    return 新字典
