import re


def 字符串转数字(字符串) -> float | int | str:
    if '.' in 字符串:
        return float(字符串)

    if re.search(r"\d+", 字符串):
        return int(字符串)
    return 字符串
