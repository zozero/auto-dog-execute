from pydantic import BaseModel


class 任务数据类(BaseModel):
    模拟器的ip和端口: str
    项目名: str
    任务列表: list


class 图片匹配数据类(BaseModel):
    序号: int | None = None
    图片名: str
    范围: str
    算法: int
    最低相似度: float
    额外补充: int


class 图片二值化匹配数据类(BaseModel):
    序号: int | None = None
    图片名: str
    范围: str
    阈值: int
    阈值类型: int
    算法: int
    最低相似度: float
