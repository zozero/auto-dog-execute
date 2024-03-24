# -*- coding: utf-8 -*-
import io
import inspect
import time
import os
import json

from PIL import Image
from fastapi import FastAPI, UploadFile, HTTPException, status
from typing import Union
import uvicorn
from fastapi.openapi.models import Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles

from 公共函数屋.图片处理 import 保存图片
from 公共函数屋.字符转换 import 字符串转换
from 数据类型屋.接收类型 import 执行数据类, 图片匹配数据类, 图片二值化匹配数据类, 步骤数据类, 测试步骤数据类, 任务数据类
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
@快捷应用程序接口.post("/方法/上传截图")
async def 上传图片截图(图片: UploadFile, 项目名: str):
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
@快捷应用程序接口.post("/方法/添加")
async def 添加方法数据(数据: Union[图片匹配数据类, 图片二值化匹配数据类], 项目名: str, 方法名: str):
    表格目录 = os.path.join('表格文件屋', 项目名, '方法间')
    # # 不存在目录就创建目录，存在的话就不要报错了
    os.makedirs(表格目录, exist_ok=True)

    # 完整路径
    文件完整路径 = os.path.join(表格目录, 方法名 + '.csv')
    数据字典 = 数据.model_dump()
    新字典 = {}
    for 索引 in 数据字典.keys():
        新字典[索引] = [数据字典[索引]]

    表格 = 表格处理类(文件完整路径, 新字典)
    表格.添加数据()
    函数名 = inspect.stack()[0][3]
    return 函数名 + " 保存成功"


# 获取csv文件
@快捷应用程序接口.put("/方法/覆盖")
async def 覆盖方法表格(csv文件: UploadFile, 项目名: str, 方法名: str):
    表格目录 = os.path.join('表格文件屋', 项目名, '方法间')
    # # 不存在目录就创建目录，存在的话就不要报错了
    os.makedirs(表格目录, exist_ok=True)

    # 完整路径
    文件完整路径 = os.path.join(表格目录, 方法名 + '.csv')
    with open(文件完整路径, 'wb') as 文件:
        文件内容 = await csv文件.read()
        # 之所以如此麻烦的转换是因为，国内大部分使用excel打开csv文件，但excel不具备自动切换编码的功能
        # 这就导致使用utf-8编码的文件直接出现乱码
        文件内容 = 文件内容.decode(encoding='utf-8')
        文件内容 = 文件内容.encode('gbk')
        文件.write(文件内容)
    return "保存成功"


# 获取csv文件
@快捷应用程序接口.get("/方法/表格")
async def 获取表格(项目名: str, 文件名: str):
    文件名 = 文件名 + '.csv'
    文件路径 = os.path.join('表格文件屋', 项目名, '方法间', 文件名)
    if os.path.exists(文件路径):
        return FileResponse(文件路径, media_type="csv/text", filename=文件名)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="表格文件没有找到！",
        )


# 获取csv文件
@快捷应用程序接口.get("/方法/序号尾巴")
async def 获得序号尾巴(项目名: str, 文件名: str):
    文件路径 = os.path.join('表格文件屋', 项目名, '方法间', 文件名 + '.csv')
    print(文件路径)
    if os.path.exists(文件路径):
        表格 = 表格处理类(文件路径)
        # fastapi无法直接返回numpy.*的数据，所以添加了item来转换成 python 类型
        return 表格.序号尾巴.item()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="表格文件没有找到！",
        )


@快捷应用程序接口.put("/步骤/创建")
async def 创建步骤表格(csv文件: UploadFile, 项目名: str, 文件名: str):
    表格目录 = os.path.join('表格文件屋', 项目名, '步骤间')
    # 不存在目录就创建目录，存在的话就不要报错了
    os.makedirs(表格目录, exist_ok=True)

    # 完整路径
    文件完整路径 = os.path.join(表格目录, 文件名 + '.csv')
    with open(文件完整路径, 'wb') as 文件:
        文件内容 = await csv文件.read()
        # 之所以如此麻烦的转换是因为，国内大部分使用excel打开csv文件，但excel不具备自动切换编码的功能
        # 这就导致使用utf-8编码的文件直接出现乱码
        文件内容 = 文件内容.decode(encoding='utf-8')
        文件内容 = 文件内容.encode('gbk')
        文件.write(文件内容)
    return "创建步骤表格成功"


@快捷应用程序接口.get("/步骤/文件列表")
def 获得步骤文件列表(项目名: str):
    表格目录 = os.path.join('表格文件屋', 项目名, '步骤间')
    if os.path.exists(表格目录):
        文件列表 = os.listdir(表格目录)
        return ORJSONResponse(文件列表)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件没有找到！",
        )


@快捷应用程序接口.delete("/步骤/删除文件")
def 删除步骤文件(项目名: str, 文件名: str):
    文件目录 = os.path.join('表格文件屋', 项目名, '步骤间', 文件名 + '.csv')
    if os.path.exists(文件目录):
        os.remove(文件目录)
        return "删除成功"
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件没有找到！",
        )


@快捷应用程序接口.get("/步骤/表格")
async def 获得步骤文件(项目名: str, 文件名: str):
    文件名 = 文件名 + '.csv'
    文件路径 = os.path.join('表格文件屋', 项目名, '步骤间', 文件名)
    print(文件路径)
    if os.path.exists(文件路径):
        return FileResponse(文件路径, media_type="csv/text", filename=文件名)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="表格文件没有找到！",
        )


@快捷应用程序接口.put("/步骤/覆盖")
async def 覆盖步骤表格(csv文件: UploadFile, 项目名: str, 文件名: str):
    表格目录 = os.path.join('表格文件屋', 项目名, '步骤间')
    # # 不存在目录就创建目录，存在的话就不要报错了
    os.makedirs(表格目录, exist_ok=True)

    # 完整路径
    文件完整路径 = os.path.join(表格目录, 文件名 + '.csv')
    with open(文件完整路径, 'wb') as 文件:
        文件内容 = await csv文件.read()
        # 之所以如此麻烦的转换是因为，国内大部分使用excel打开csv文件，但excel不具备自动切换编码的功能
        # 这就导致使用utf-8编码的文件直接出现乱码
        文件内容 = 文件内容.decode(encoding='utf-8')
        文件内容 = 文件内容.encode('gbk')
        文件.write(文件内容)
    return "保存成功"


# 保存数据到相应的csv表格中
@快捷应用程序接口.post("/步骤/添加")
async def 添加步骤数据(数据: 步骤数据类, 项目名: str, 文件名: str):
    表格目录 = os.path.join('表格文件屋', 项目名, '步骤间')
    # # 不存在目录就创建目录，存在的话就不要报错了
    os.makedirs(表格目录, exist_ok=True)

    # 完整路径
    文件完整路径 = os.path.join(表格目录, 文件名 + '.csv')
    数据字典 = 数据.model_dump()
    新字典 = {}
    for 索引 in 数据字典.keys():
        # 新字典[索引] = [字符串转换(数据字典[索引])
        新字典[索引] = [数据字典[索引]]

    表格 = 表格处理类(文件完整路径, 新字典)
    表格.添加数据()
    函数名 = inspect.stack()[0][3]
    return 函数名 + " 保存成功"


@快捷应用程序接口.put("/任务/创建")
async def 创建任务表格(csv文件: UploadFile, 项目名: str, 文件名: str):
    表格目录 = os.path.join('表格文件屋', 项目名, '任务间')
    # 不存在目录就创建目录，存在的话就不要报错了
    os.makedirs(表格目录, exist_ok=True)

    # 完整路径
    文件完整路径 = os.path.join(表格目录, 文件名 + '.csv')
    with open(文件完整路径, 'wb') as 文件:
        文件内容 = await csv文件.read()
        # 之所以如此麻烦的转换是因为，国内大部分使用excel打开csv文件，但excel不具备自动切换编码的功能
        # 这就导致使用utf-8编码的文件直接出现乱码
        文件内容 = 文件内容.decode(encoding='utf-8')
        文件内容 = 文件内容.encode('gbk')
        文件.write(文件内容)
    return "创建步任务格成功"


@快捷应用程序接口.get("/任务/文件列表")
def 获得任务文件列表(项目名: str):
    表格目录 = os.path.join('表格文件屋', 项目名, '任务间')
    if os.path.exists(表格目录):
        文件列表 = os.listdir(表格目录)
        return ORJSONResponse(文件列表)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件没有找到！",
        )


@快捷应用程序接口.get("/任务/表格")
async def 获得任务文件(项目名: str, 文件名: str):
    文件名 = 文件名 + '.csv'
    文件路径 = os.path.join('表格文件屋', 项目名, '任务间', 文件名)
    print(文件路径)
    if os.path.exists(文件路径):
        return FileResponse(文件路径, media_type="csv/text", filename=文件名)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="表格文件没有找到！",
        )


@快捷应用程序接口.put("/任务/覆盖")
async def 覆盖任务表格(csv文件: UploadFile, 项目名: str, 文件名: str):
    表格目录 = os.path.join('表格文件屋', 项目名, '任务间')
    # # 不存在目录就创建目录，存在的话就不要报错了
    os.makedirs(表格目录, exist_ok=True)

    # 完整路径
    文件完整路径 = os.path.join(表格目录, 文件名 + '.csv')
    with open(文件完整路径, 'wb') as 文件:
        文件内容 = await csv文件.read()
        # 之所以如此麻烦的转换是因为，国内大部分使用excel打开csv文件，但excel不具备自动切换编码的功能
        # 这就导致使用utf-8编码的文件直接出现乱码
        文件内容 = 文件内容.decode(encoding='utf-8')
        文件内容 = 文件内容.encode('gbk')
        文件.write(文件内容)
    return "保存成功"


# 保存数据到相应的csv表格中
@快捷应用程序接口.post("/任务/添加")
async def 添加任务数据(数据: 任务数据类, 项目名: str, 文件名: str):
    表格目录 = os.path.join('表格文件屋', 项目名, '任务间')
    # # 不存在目录就创建目录，存在的话就不要报错了
    os.makedirs(表格目录, exist_ok=True)

    # 完整路径
    文件完整路径 = os.path.join(表格目录, 文件名 + '.csv')
    print(文件完整路径)
    数据字典 = 数据.model_dump()
    新字典 = {}
    for 索引 in 数据字典.keys():
        # 新字典[索引] = [字符串转换(数据字典[索引])
        新字典[索引] = [数据字典[索引]]

    表格 = 表格处理类(文件完整路径, 新字典)
    表格.添加数据()
    函数名 = inspect.stack()[0][3]
    return 函数名 + " 保存成功"


@快捷应用程序接口.delete("/任务/删除文件")
def 删除任务文件(项目名: str, 文件名: str):
    文件目录 = os.path.join('表格文件屋', 项目名, '任务间', 文件名 + '.csv')
    if os.path.exists(文件目录):
        os.remove(文件目录)
        return "删除成功"
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件没有找到！",
        )


@快捷应用程序接口.post("/执行/测试步骤")
async def 测试步骤(步骤数据: 测试步骤数据类):
    # 使用类接收数据需要使用post方法
    我的模拟器 = 安卓指令类(步骤数据.模拟器的ip和端口)
    委托对象类.注册('我的模拟器', 我的模拟器)
    # 任务名为空，因为不是必须的
    任务 = 任务类(步骤数据.项目名, '')
    步骤信息 = {
        '名称': 步骤数据.名称,
        '编号': 步骤数据.编号,
    }
    任务.步骤(步骤信息)

    return '执行完毕。'


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
def 执行任务(任务数据: 执行数据类):
    # 使用类接收数据需要使用post方法
    print(任务数据.模拟器的ip和端口)
    我的模拟器 = 安卓指令类(任务数据.模拟器的ip和端口)
    委托对象类.注册('我的模拟器', 我的模拟器)
    for 任务名 in 任务数据.任务列表:
        任务 = 任务类(任务数据.项目名, 任务名)

        任务.获取数据()
        任务.执行任务()
    return '执行完毕'


# uvicorn 接入口:快捷应用程序接口 --reload --port 8888
# pip install python-multipart 可能出现报错需要安卓
if __name__ == "__main__":
    服务配置 = uvicorn.Config("接入口:快捷应用程序接口", port=8888, log_level="info", reload=True)
    服务 = uvicorn.Server(服务配置)
    服务.run()
