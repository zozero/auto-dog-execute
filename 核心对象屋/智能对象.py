import io
import os.path
from typing import Union
import base64

import cv2
import numpy as np
from PIL import Image, ImageDraw
from torch import tensor

import easyocr

from ultralytics import YOLO
from 数据类型屋.结果类型 import 结果类
from 核心对象屋.可视对象 import 计算机可视化开源类


class 你只看一次类:
    @staticmethod
    def 训练(模型路径: str, 配置路径: str, 项目目录: str, 轮回数: int = 160, 设备: Union[list, int, str] = 0) -> dict:
        你只看一次模型 = YOLO(模型路径)
        # 这里project就是存储训练结果目录的目录，还可以添加name来自定义结果的目录名
        结果: dict = 你只看一次模型.train(data=配置路径, epochs=轮回数, imgsz=640, device=设备, project=项目目录)
        return 结果

    @staticmethod
    def 预测(模型路径: str, 图片, 置信度: float = 0.2, 设备: Union[list, int, str] = 0):
        你只看一次模型 = YOLO(模型路径)
        结果列表: list = 你只看一次模型.predict(图片, show_labels=False, show_conf=False, show_boxes=False, conf=置信度,
                                                device=设备)
        # 返回识别出的结果，是一个二维数组，例如：shape: torch.Size([2, 6])
        # 需要把值放到cpu中才能取到。
        return 结果列表[0], 结果列表[0].boxes.data.cpu()
        # for 结果 in :
        #     位置 = 结果.boxes
        #     print("--------结果开始--------")
        #     print(结果['names'][位置['cls'][0]])
        #     print("--------结果结束--------")
        #
        #     print("--------位置开始--------")
        #     print(位置)
        #     print("--------位置结束--------")
        #
        #     指定分类索引 = np.where(np.array(位置['cls']) == 80)
        #
        #     结果.show()
        #     # 结果.save(filename='result.jpg')  # save to disk
        #     return 结果

    @staticmethod
    def 分类预测(图片, 模型路径: str, 分类序号: int = 80, 置信度: float = 0.2,
                 设备: Union[list, int, str] = 0) -> tensor:
        你只看一次模型 = YOLO(模型路径)
        结果列表: list = 你只看一次模型.predict(图片, show_labels=False, show_conf=False, show_boxes=False, conf=置信度,
                                                device=设备)
        结果 = 结果列表[0]
        结果盒子列表 = 结果列表[0].boxes.data.cpu()
        指定分类索引列表 = np.where(结果盒子列表 == 分类序号)[0]
        # 将当前的figure转换为图片数组
        # 返回的是BGR的图片数组，现在转成RGB的格式显示
        图片数组 = 计算机可视化开源类.转换颜色通道(结果.orig_img, cv2.COLOR_BGR2RGB)
        图片 = Image.fromarray(图片数组)
        # 找到了就绘制矩形
        if len(指定分类索引列表) > 0:
            # 绘制边框
            draw = ImageDraw.Draw(图片)
            for 盒子 in 结果盒子列表[指定分类索引列表]:
                # 绘制所有识别到的物体边框。
                draw.rectangle(盒子[0:4].tolist(), fill=None, outline='red', width=3)
        # 转换格式返回数据
        图片流 = io.BytesIO()
        # 一定要加格式
        图片.save(图片流, 'JPEG')
        图片流.seek(0)
        return 图片流

    # 已经无效了因为每个分类都会创建一个新的模型
    @staticmethod
    def 全类预测(图片, 模型路径: str, 置信度: float = 0.2, 设备: Union[list, int, str] = 0) -> tensor:
        你只看一次模型 = YOLO(模型路径)
        结果列表: list = 你只看一次模型.predict(图片, show_labels=False, show_conf=False, show_boxes=False, conf=置信度,
                                                device=设备)
        结果 = 结果列表[0]
        结果盒子列表 = 结果列表[0].boxes.data.cpu()

        # 将当前的figure转换为图片数组
        # 返回的是BGR的图片数组，现在转成RGB的格式显示
        图片数组 = 计算机可视化开源类.转换颜色通道(结果.orig_img, cv2.COLOR_BGR2RGB)
        图片 = Image.fromarray(图片数组)
        # 绘制边框
        绘画 = ImageDraw.Draw(图片)
        for 盒子 in 结果盒子列表:
            # 绘制所有识别到的物体边框。第一个参数是左上右下的四个数字列表。
            绘画.rectangle(盒子[0:4].tolist(), fill=None, outline='red', width=3)
        # 转换格式返回数据
        图片流 = io.BytesIO()
        # 一定要加格式
        图片.save(图片流, 'JPEG')
        图片流.seek(0)
        return 图片流


class 简单光学字符识别类:
    @staticmethod
    def 识别(图片, 文本: str, 语种: str = 'ch_sim', 最低相似度: float = 0.1) -> 结果类:
        print("简单光学字符识别类")
        # 返回值
        返回值 = 结果类()
        返回值.状态 = False
        返回值.图片尺寸 = (图片.shape[1], 图片.shape[0])
        返回值.最高相似度 = 0
        返回值.位置 = (0, 0)

        语言列表 = [语种, 'en']
        模型存放目录 = os.path.join('资源存放屋', '简单光学字符识别')
        读者 = easyocr.Reader(语言列表, model_storage_directory=模型存放目录)
        结果列表 = 读者.readtext(图片)
        for 结果 in 结果列表:
            if 结果[2] < 最低相似度:
                continue
            if 文本 in 结果[1]:
                返回值.状态 = True
                返回值.位置 = (int((结果[0][0][0] + 结果[0][2][0]) / 2), int((结果[0][0][1] + 结果[0][2][1]) / 2))
                返回值.最高相似度 = round(结果[2], 3)

        return 返回值

    @staticmethod
    def 识别测试(图片: np.ndarray, 语种: str = 'ch_sim'):
        语言列表 = [语种, 'en']
        模型存放目录 = os.path.join('资源存放屋', '简单光学字符识别')
        读者 = easyocr.Reader(语言列表, model_storage_directory=模型存放目录)
        结果列表 = 读者.readtext(图片)
        返回列表 = []
        for 结果 in 结果列表:
            # item()是为了将numpy的数据读取出来成为常规的python数据格式，便于fastapi返回。
            返回列表.append([(int(结果[0][0][0]), int(结果[0][0][1]), int(结果[0][2][0]), int(结果[0][2][1])), 结果[1],
                             round(结果[2], 2)])

        图片 = Image.fromarray(图片)
        # 绘制边框
        绘画 = ImageDraw.Draw(图片)
        for 结果 in 返回列表:
            # 绘制所有识别到的物体边框。第一个参数是左上右下的四个数字列表。
            绘画.rectangle(结果[0], fill=None, outline='red', width=3)

        # 转换格式返回数据
        图片流 = io.BytesIO()
        # 一定要加格式
        图片.save(图片流, 'JPEG')
        图片流.seek(0)
        图片字符串 = base64.b64encode(图片流.getvalue())

        return 图片字符串, 返回列表
