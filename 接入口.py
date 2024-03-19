# -*- coding: utf-8 -*-
import io
import time
import os

from PIL import Image
from fastapi import FastAPI, UploadFile
from typing import Union
import uvicorn
from fastapi.openapi.models import Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse

from 核心对象屋.安卓对象 import 安卓指令类

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


@快捷应用程序接口.get("/测试/裁剪图片")
# def read_root(模拟器的ip和端口: Union[str, None] = None):
def 截取图片(模拟器的ip和端口: str, 范围: str):
    # 除掉首尾空格后用空格分割，使用map遍历将每个值执行一遍int()函数后，转成元组。
    范围 = tuple(map(int, 范围.strip().split(' ')))

    我的模拟器 = 安卓指令类(模拟器的ip和端口)
    我的图片路径,我的图片 = 我的模拟器.裁剪图片(范围)
    return FileResponse(我的图片路径, media_type="image/jpg")


# uvicorn 接入口:快捷应用程序接口 --reload --port 8888
if __name__ == "__main__":
    服务配置 = uvicorn.Config("接入口:快捷应用程序接口", port=8888, log_level="info", reload=True)
    服务 = uvicorn.Server(服务配置)
    服务.run()
