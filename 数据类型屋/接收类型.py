from pydantic import BaseModel


class 执行数据类(BaseModel):
    模拟器的ip和端口: str
    项目名: str
    任务列表: list


class 测试任务数据类(BaseModel):
    模拟器的ip和端口: str
    项目名: str
    任务名: str


# 用于测试单个步骤的数据类型
class 测试步骤数据类(BaseModel):
    模拟器的ip和端口: str
    项目名: str
    # 文件名称
    名称: str
    # 数据的序号
    编号: int


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


class 匹配再匹配数据类(BaseModel):
    序号: int | None = None
    图片名: str
    编码: str
    X偏移: int
    Y偏移: int
    算法: int
    最低相似度: float
    额外补充: int


class 无图匹配数据类(BaseModel):
    序号: int | None = None
    图片名: str
    X轴: int
    Y轴: int


class 步骤数据类(BaseModel):
    序号: int | None = None
    名称: str
    界面编码: str
    方法编码: str
    行为编码: str
    动后编码: str
    循环次数: int
    循环间隔: float


class 任务数据类(BaseModel):
    序号: int | None = None
    名称: str
    编号: int
    是: int
    否: int
