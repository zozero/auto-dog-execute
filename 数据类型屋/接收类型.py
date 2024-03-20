from pydantic import BaseModel


class 任务数据类(BaseModel):
    模拟器的ip和端口: str
    项目名: str
    任务名列表: list
