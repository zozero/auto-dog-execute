# -*- coding: utf-8 -*-
import inspect
import shutil
import sys
import os
import time

import torch
from PIL import Image
from fastapi import FastAPI, UploadFile, HTTPException, status
from typing import Union
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles

from ultralytics import settings

from 公共函数屋.图片处理 import 上传图转二值图片
from 数据类型屋.接收类型 import 执行数据类, 图片匹配数据类, 图片二值化匹配数据类, 步骤数据类, 测试步骤数据类, \
    任务数据类, 测试任务数据类, 匹配再匹配数据类, 无图匹配数据类, 多图匹配数据类, 你只看一次数据类
from 核心对象屋.安卓对象 import 安卓指令类
from 核心对象屋.方法对象 import 匹配方法类

from 核心对象屋.执行对象 import 任务类
from 核心对象屋.智能对象 import 你只看一次类
from 通用对象屋.委托对象 import 委托对象类
from 通用对象屋.模型对象 import 模型操作类
from 通用对象屋.表格对象 import 表格处理类
from 通用对象屋.配置对象 import 你只看一次的仍是一种标记语言类

# 用于打包后防止报错
根路径 = os.getcwd()
sys.path.append(根路径)

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

# 直接访问静态资源，只需要根据目录路径进行访问就行，例如 http://127.0.0.1:8888/项目文件屋/项目1/图片间/临时.jpg
快捷应用程序接口.mount("/项目文件屋", StaticFiles(directory="项目文件屋"), name="项目文件屋")


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


@快捷应用程序接口.get("/配置/修改项目名")
def 修改项目名(项目名: str, 新名字: str):
    表格目录路径 = os.path.join('项目文件屋', 项目名, )
    新表格目录路径 = os.path.join('项目文件屋', 新名字, )
    if os.path.exists(表格目录路径) and os.path.exists(新表格目录路径) is False:
        shutil.move(表格目录路径, 新表格目录路径)
        return '修改目录完成。'
    else:
        return '修改目录失败，可能是不存在该目录或新目录名已存在。'


# 保存图片匹配的图片到相应文件夹中
@快捷应用程序接口.post("/方法/上传截图")
async def 上传图片截图(图片: UploadFile, 项目名: str):
    目录路径 = os.path.join('项目文件屋', 项目名, '图片间')
    # 不存在目录就创建目录，存在的话就不要报错了
    os.makedirs(目录路径, exist_ok=True)

    # 前端会直接指定图片名的
    存储路径 = os.path.join(目录路径, 图片.filename)
    with open(存储路径, 'wb') as 文件:
        文件内容 = await 图片.read()
        文件.write(文件内容)
    函数名 = inspect.stack()[0][3]
    return 函数名 + " 保存成功"


# 保存图片匹配的多张图片到相应文件夹中
@快捷应用程序接口.post("/方法/上传多张截图")
async def 上传多张截图(图片列表: list[UploadFile], 项目名: str):
    目录路径 = os.path.join('项目文件屋', 项目名, '图片间')
    # 不存在目录就创建目录，存在的话就不要报错了
    os.makedirs(目录路径, exist_ok=True)
    for 图片 in 图片列表:
        # 前端会直接指定图片名的
        存储路径 = os.path.join(目录路径, 图片.filename)
        with open(存储路径, 'wb') as 文件:
            文件内容 = await 图片.read()
            文件.write(文件内容)

    函数名 = inspect.stack()[0][3]
    return 函数名 + " 保存成功"


# 暂时无法使用
# @快捷应用程序接口.get("/你只看一次/分类列表")
# def 上传你只看一次数据(项目名: str):
#     标记 = 仍是一种标记语言类(项目名, '你只看一次')
#     标记.打开()
#     return 标记.获得分类列表()

# @快捷应用程序接口.get("/你只看一次/分类列表")
# def 获得你只看一次分类列表(项目名: str):
#     图片目录路径 = os.path.join('项目文件屋', 项目名, '智能间', '你只看一次')
#     分类列表 = os.listdir(图片目录路径)
#     return 分类列表


@快捷应用程序接口.get("/你只看一次/图片列表")
def 获取你只看一次图片列表(项目名: str, 分类名: str):
    图片目录路径 = os.path.join('项目文件屋', 项目名, '智能间', '你只看一次', 分类名, 'images')
    图片列表 = os.listdir(图片目录路径)
    return 图片列表


@快捷应用程序接口.get("/你只看一次/分类")
def 增加你只看一次分类(项目名: str, 分类名: str):
    标记 = 你只看一次的仍是一种标记语言类(项目名, 分类名, '你只看一次')
    标记.打开()
    标记.增加分类()
    return '增加分类成功'


@快捷应用程序接口.post("/你只看一次/上传数据")
async def 上传你只看一次数据(图片列表: list[UploadFile], 标签列表: list[UploadFile], 项目名: str, 分类名: str):
    图片目录路径 = os.path.join('项目文件屋', 项目名, '智能间', '你只看一次', 分类名, 'images')
    # 不存在目录就创建目录，存在的话就不要报错了
    os.makedirs(图片目录路径, exist_ok=True)

    标签目录路径 = os.path.join('项目文件屋', 项目名, '智能间', '你只看一次', 分类名, 'labels')
    # 不存在目录就创建目录，存在的话就不要报错了
    os.makedirs(标签目录路径, exist_ok=True)

    数量 = len(os.listdir(图片目录路径))

    for i in range(len(图片列表)):
        数量 += 1
        数量文字 = str(数量)
        # 前端会直接指定图片名的
        存储路径 = os.path.join(图片目录路径, 数量文字 + '.jpg')
        with open(存储路径, 'wb') as 文件:
            文件内容 = await 图片列表[i].read()
            文件.write(文件内容)

        # 前端会直接指定图片名的
        存储路径 = os.path.join(标签目录路径, 数量文字 + '.txt')
        with open(存储路径, 'wb') as 文件:
            文件内容 = await 标签列表[i].read()
            文件.write(文件内容)

    函数名 = inspect.stack()[0][3]
    return 函数名 + " 保存成功"


@快捷应用程序接口.get("/你只看一次/训练")
def 训练你只看一次(项目名: str, 分类名: str, 轮回数: int):
    数据目录 = os.path.join('项目文件屋', 项目名, '智能间', '你只看一次', 分类名)
    # 重置你只看一次的配置文件为默认值
    # settings.reset()
    # 设置数据目录到当前文件夹中 查看设置命令：yolo settings
    settings.update({'datasets_dir': 数据目录})
    time.sleep(1)


    模型操作 = 模型操作类(项目名, 分类名, '你只看一次')
    配置 = 你只看一次的仍是一种标记语言类(项目名, 分类名, '你只看一次')

    设备 = 'cpu'
    if torch.cuda.is_available():
        设备 = list(range(torch.cuda.device_count()))
    # 设置参数
    字典 = dict(
        模型路径=模型操作.最佳模型路径(),
        项目目录=模型操作.模型箱目录,
        配置路径=配置.项目配置文件路径,
        轮回数=轮回数,
        设备=设备
    )
    # 开始训练
    你只看一次类.训练(**字典)

    return '训练完毕'


@快捷应用程序接口.get("/你只看一次/分类预测")
def 你只看一次分类预测(项目名: str, 模拟器的ip和端口: str, 分类名: str, 置信度: float):
    # 模型的存储路径需要更改，因为追加训练会导致原先训练的消失，要么选择一次性训练多个，要么只训练一个的同时，保存一个。
    模型操作 = 模型操作类(项目名, 分类名)
    # 直接拿训练的第一张图片去判断
    我的模拟器 = 安卓指令类(模拟器的ip和端口)
    我的图片 = 我的模拟器.截屏()
    图片 = Image.open(我的图片)
    # 载入图片
    # 图片 = Image.open(图片路径)

    # 自动设定预测的设备
    设备 = 'cpu'
    if torch.cuda.is_available():
        设备 = list(range(torch.cuda.device_count()))

    字典 = dict(
        图片=图片,
        模型路径=模型操作.最佳模型路径(),
        # 模型路径='ceshi2.pt',
        # 模型路径='best.pt',
        # 这里分类序号是固定的，具体可以查看配置.yaml文件
        分类序号=80,
        置信度=置信度,
        设备=设备
    )
    图片流 = 你只看一次类.分类预测(**字典)

    return StreamingResponse(图片流, media_type="image/jpg")


# 该方法无法使用，除非一次性训练所有模型，所以当前无法使用了
# @快捷应用程序接口.get("/你只看一次/全类预测")
# def 你只看一次全类预测(项目名: str, 模拟器的ip和端口: str, 置信度: float):
#     模型操作 = 模型操作类(项目名)
#     # 直接拿训练的第一张图片去判断
#     # 图片路径 = os.path.join(数据目录, 'images', '1.jpg')
#     我的模拟器 = 安卓指令类(模拟器的ip和端口)
#     我的图片 = 我的模拟器.截屏()
#     图片 = Image.open(我的图片)
#     # 载入图片
#     # 图片 = Image.open(图片路径)
#     设备 = 'cpu'
#     if torch.cuda.is_available():
#         设备 = list(range(torch.cuda.device_count()))
#
#     字典 = dict(
#         图片=图片,
#         模型路径=模型操作.项目模型存放路径,
#         置信度=置信度,
#         设备=设备
#     )
#     图片流 = 你只看一次类.全类预测(**字典)
#
#     return StreamingResponse(图片流, media_type="image/jpg")


@快捷应用程序接口.post("/方法/二值转化")
async def 二值转化图片(图片: UploadFile, 阈值: int, 阈值类型: int):
    图片内容 = await 图片.read()
    图片 = 上传图转二值图片(图片内容, 阈值, 阈值类型)
    return StreamingResponse(图片, media_type="image/jpg")


# 保存数据到相应的csv表格中
# 注意数据类型有着以多包少，多的要放前面
@快捷应用程序接口.post("/方法/添加")
def 添加方法数据(数据: Union[
    多图匹配数据类, 图片匹配数据类, 图片二值化匹配数据类, 匹配再匹配数据类, 无图匹配数据类, 你只看一次数据类],
                 项目名: str,
                 方法名: str):
    表格目录 = os.path.join('项目文件屋', 项目名, '方法间')
    # 不存在目录就创建目录，存在的话就不要报错了
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
@快捷应用程序接口.post("/方法/修改")
async def 修改方法表格(数据: Union[你只看一次数据类], 项目名: str, 方法名: str):
    表格目录 = os.path.join('项目文件屋', 项目名, '方法间')
    # 不存在目录就创建目录，存在的话就不要报错了
    os.makedirs(表格目录, exist_ok=True)
    # 完整路径
    文件完整路径 = os.path.join(表格目录, 方法名 + '.csv')
    数据字典 = 数据.model_dump()
    新字典 = {}
    for 索引 in 数据字典.keys():
        新字典[索引] = [数据字典[索引]]

    表格 = 表格处理类(文件完整路径, 新字典)
    表格.修改数据(数据.序号)
    return "修改成功"


# 覆盖csv文件
@快捷应用程序接口.put("/方法/覆盖")
async def 覆盖方法表格(csv文件: UploadFile, 项目名: str, 方法名: str):
    表格目录 = os.path.join('项目文件屋', 项目名, '方法间')
    # 不存在目录就创建目录，存在的话就不要报错了
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
def 获取表格(项目名: str, 文件名: str):
    文件名 = 文件名 + '.csv'
    文件路径 = os.path.join('项目文件屋', 项目名, '方法间', 文件名)
    if os.path.exists(文件路径):
        return FileResponse(文件路径, media_type="csv/text", filename=文件名)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="表格文件没有找到！",
        )


# 获取csv文件最后一行数据的序号
@快捷应用程序接口.get("/方法/序号尾巴")
def 获得序号尾巴(项目名: str, 文件名: str):
    文件路径 = os.path.join('项目文件屋', 项目名, '方法间', 文件名 + '.csv')
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
    表格目录 = os.path.join('项目文件屋', 项目名, '步骤间')
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
    表格目录 = os.path.join('项目文件屋', 项目名, '步骤间')
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
    文件目录 = os.path.join('项目文件屋', 项目名, '步骤间', 文件名 + '.csv')
    if os.path.exists(文件目录):
        os.remove(文件目录)
        return "删除成功"
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件没有找到！",
        )


@快捷应用程序接口.get("/步骤/表格")
def 获得步骤文件(项目名: str, 文件名: str):
    文件名 = 文件名 + '.csv'
    文件路径 = os.path.join('项目文件屋', 项目名, '步骤间', 文件名)
    if os.path.exists(文件路径):
        return FileResponse(文件路径, media_type="csv/text", filename=文件名)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="表格文件没有找到！",
        )


@快捷应用程序接口.put("/步骤/覆盖")
async def 覆盖步骤表格(csv文件: UploadFile, 项目名: str, 文件名: str):
    表格目录 = os.path.join('项目文件屋', 项目名, '步骤间')
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
def 添加步骤数据(数据: 步骤数据类, 项目名: str, 文件名: str):
    表格目录 = os.path.join('项目文件屋', 项目名, '步骤间')
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


# 获取csv文件最后一行数据的序号
@快捷应用程序接口.get("/步骤/序号尾巴")
def 获得步骤尾巴(项目名: str, 文件名: str):
    文件路径 = os.path.join('项目文件屋', 项目名, '步骤间', 文件名 + '.csv')
    if os.path.exists(文件路径):
        表格 = 表格处理类(文件路径)
        # fastapi无法直接返回numpy.*的数据，所以添加了item来转换成 python 类型
        return 表格.序号尾巴.item()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="表格文件没有找到！",
        )


@快捷应用程序接口.put("/任务/创建")
async def 创建任务表格(csv文件: UploadFile, 项目名: str, 文件名: str):
    表格目录 = os.path.join('项目文件屋', 项目名, '任务间')
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
    表格目录 = os.path.join('项目文件屋', 项目名, '任务间')
    if os.path.exists(表格目录):
        文件列表 = os.listdir(表格目录)
        return ORJSONResponse(文件列表)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件没有找到！",
        )


@快捷应用程序接口.get("/任务/表格")
def 获得任务文件(项目名: str, 文件名: str):
    文件名 = 文件名 + '.csv'
    文件路径 = os.path.join('项目文件屋', 项目名, '任务间', 文件名)
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
    表格目录 = os.path.join('项目文件屋', 项目名, '任务间')
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
def 添加任务数据(数据: 任务数据类, 项目名: str, 文件名: str):
    表格目录 = os.path.join('项目文件屋', 项目名, '任务间')
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
    文件目录 = os.path.join('项目文件屋', 项目名, '任务间', 文件名 + '.csv')
    if os.path.exists(文件目录):
        os.remove(文件目录)
        return "删除成功"
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件没有找到！",
        )


@快捷应用程序接口.post("/执行/测试步骤")
def 测试步骤(步骤数据: 测试步骤数据类):
    # 使用类接收数据需要使用post方法
    我的模拟器 = 安卓指令类(步骤数据.模拟器的ip和端口)
    委托对象类.注册(步骤数据.项目名, 我的模拟器)
    # 用于全局停止执行
    委托对象类.注册(步骤数据.项目名 + '停止', False)
    # 任务名为空，因为不是必须的
    任务 = 任务类(步骤数据.项目名, '')
    步骤信息 = {
        '名称': 步骤数据.名称,
        '编号': 步骤数据.编号,
    }
    if 步骤数据.编号 == 0:
        任务.步骤组(步骤信息)
    else:
        任务.步骤(步骤信息)

    return '执行完毕。'


@快捷应用程序接口.post("/执行/测试任务")
def 测试任务(任务数据: 测试任务数据类):
    # 使用类接收数据需要使用post方法
    我的模拟器 = 安卓指令类(任务数据.模拟器的ip和端口)
    委托对象类.注册(任务数据.项目名, 我的模拟器)
    # 用于全局停止执行
    委托对象类.注册(任务数据.项目名 + '停止', False)

    任务 = 任务类(任务数据.项目名, 任务数据.任务名)
    任务.获取数据()
    任务.执行任务()
    return '执行完毕'


@快捷应用程序接口.get("/执行/停止")
def 停止执行(项目名: str):
    # 用于全局停止执行
    委托对象类.注册(项目名 + '停止', True)

    return '停止执行'


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
        "旧图路径": os.path.join('项目文件屋', '测试项目', '图片间', '应用中心.jpg'),
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
    委托对象类.注册(任务数据.项目名, 我的模拟器)
    # 用于全局停止执行
    委托对象类.注册(任务数据.项目名 + '停止', False)

    for 任务名 in 任务数据.任务列表:
        任务 = 任务类(任务数据.项目名, 任务名)

        任务.获取数据()
        任务.执行任务()
    return '执行完毕'


# 提供两个参数，第一个是主机地址，第二个是端口地址。
def 设置服务配置():
    # 日志配置 = {
    #     "version": 1,
    #     "disable_existing_loggers": True,
    #     "handlers": {
    #         "file_handler": {
    #             "class": "logging.FileHandler",
    #             "filename": "logfile.log",
    #         },
    #     },
    #     "root": {
    #         "handlers": ["file_handler"],
    #         "level": "INFO",
    #     },
    # }

    if len(sys.argv) == 2:
        return uvicorn.Config("接入口:快捷应用程序接口", host=sys.argv[1], port=8888, reload=False)
        # return uvicorn.Config("接入口:快捷应用程序接口", host=sys.argv[1], port=8888, reload=False,log_config=日志配置)
    elif len(sys.argv) == 3:
        return uvicorn.Config("接入口:快捷应用程序接口", host=sys.argv[1], port=int(sys.argv[2]),
                              reload=False)
    else:
        return uvicorn.Config("接入口:快捷应用程序接口", host='127.0.0.1', port=8888, reload=False)


# uvicorn 接入口:快捷应用程序接口 --reload --port 8888
# pip install python-multipart 可能出现报错需要安卓
if __name__ == "__main__":
    print("小犬正在狂奔......")
    服务配置 = 设置服务配置()
    服务 = uvicorn.Server(服务配置)
    服务.run()
