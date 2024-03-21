# -*- coding: utf-8 -*-
import io
import inspect
import time
import os
import json

from PIL import Image
from fastapi import FastAPI, UploadFile
from typing import Union
import uvicorn
from fastapi.openapi.models import Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from fastapi.responses import ORJSONResponse

from 公共函数屋.图片处理 import 保存图片
from 数据类型屋.接收类型 import 任务数据类, 图片匹配数据类
from 核心对象屋.安卓对象 import 安卓指令类
from 核心对象屋.方法对象 import 匹配方法类

from 核心对象屋.执行对象 import 任务类
from 通用对象屋.委托对象 import 委托对象类
from 通用对象屋.表格对象 import 表格处理类

# 使用网络地址访问执行端的入口
快捷应用程序接口 = FastAPI()
# 解决跨站问题的配置
跨域资源共享来源列表 = [
    # 如何地址都可以访问。
    "*",
]

# 添加中间键，解决跨站的问题
快捷应用程序接口.add_middleware(
    CORSMiddleware,
    allow_origins=跨域资源共享来源列表,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 应用程序接口测试
@快捷应用程序接口.get("/测试")
def 测试():
    return {"Hello": "World"}


# 对模拟器屏幕进行截图
@快捷应用程序接口.get("/模拟器屏幕")
# def read_root(模拟器的ip和端口: Union[str, None] = None):
def 模拟器屏幕(模拟器的ip和端口: str):
    我的模拟器 = 安卓指令类(模拟器的ip和端口)
    我的图片 = 我的模拟器.截屏()
    return StreamingResponse(我的图片, media_type="image/png")


# 保存图片匹配的图片到相应文件夹中
@快捷应用程序接口.post("/图片匹配/上传截图")
async def 上传图片匹配截图(图片: UploadFile, 项目名: str):
    目录路径 = os.path.join('图片存取屋', 项目名)
    # 不存在目录就创建目录，存在的话就不要报错了
    os.makedirs(目录路径, exist_ok=True)

    存储路径 = os.path.join(目录路径, 图片.filename)
    with open(存储路径, 'wb') as 文件:
        文件内容 = await 图片.read()
        文件.write(文件内容)
    函数名 = inspect.stack()[0][3]
    return 函数名 + " 保存成功"


# 保存数据到相应的csv表格中
@快捷应用程序接口.post("/图片匹配/添加数据")
async def 添加图片匹配数据(数据: 图片匹配数据类, 项目名: str):
    print(数据.model_dump())
    表格目录 = os.path.join('表格文件屋', 项目名, '方法间')
    # # 不存在目录就创建目录，存在的话就不要报错了
    os.makedirs(表格目录, exist_ok=True)
    #
    # # 完整路径
    文件完整路径 = os.path.join(表格目录, '图片匹配.csv')
    # print(文件完整路径)
    数据字典 = 数据.model_dump()
    新字典 = {}
    for 索引 in 数据字典.keys():
        新字典[索引] = [数据字典[索引]]

    表格 = 表格处理类(文件完整路径, 新字典)
    表格.添加数据()
    函数名 = inspect.stack()[0][3]
    return 函数名 + " 保存成功"


@快捷应用程序接口.get("/测试/裁剪图片")
# def read_root(模拟器的ip和端口: Union[str, None] = None):
def 截取图片(模拟器的ip和端口: str, 范围: str):
    # 除掉首尾空格后用空格分割，使用map遍历将每个值执行一遍int()函数后，转成元组。
    范围 = tuple(map(int, 范围.strip().split(' ')))

    我的模拟器 = 安卓指令类(模拟器的ip和端口)
    我的图片路径, 我的图片 = 我的模拟器.裁剪图片(范围)
    return FileResponse(我的图片路径, media_type="image/jpg")


@快捷应用程序接口.get("/测试/图片匹配")
# def read_root(模拟器的ip和端口: Union[str, None] = None):
def 图片匹配(模拟器的ip和端口: str, 范围: str):
    # 以下代码仅供测试时使用，很多数据都是固定的。
    # 除掉首尾空格后用空格分割，使用map遍历将每个值执行一遍int()函数后，转成元组。
    范围 = tuple(map(int, 范围.strip().split(' ')))
    我的模拟器 = 安卓指令类(模拟器的ip和端口)

    我的图片路径, 我的图片 = 我的模拟器.裁剪图片(范围)
    参数字典 = {
        "新图": 我的图片,
        "旧图路径": os.path.join('图片存取屋', '测试项目', '应用中心.jpg'),
        '算法': 5,
        '最低相似度': 0.8,
        '额外补充': 0
    }
    返回值 = 匹配方法类.图片匹配(**参数字典)
    return ORJSONResponse(返回值.__dict__())


@快捷应用程序接口.post("/测试/执行任务")
def 执行任务(任务数据: 任务数据类):
    # 使用类接收数据需要使用post方法
    print(任务数据.模拟器的ip和端口)
    我的模拟器 = 安卓指令类(任务数据.模拟器的ip和端口)
    委托对象类.注册('我的模拟器', 我的模拟器)
    for 任务名 in 任务数据.任务列表:
        任务 = 任务类(任务数据.项目名, 任务名)
    return '执行完毕'


# uvicorn 接入口:快捷应用程序接口 --reload --port 8888
# pip install python-multipart 可能出现报错需要安卓
if __name__ == "__main__":
    服务配置 = uvicorn.Config("接入口:快捷应用程序接口", port=8888, log_level="info", reload=True)
    服务 = uvicorn.Server(服务配置)
    服务.run()
