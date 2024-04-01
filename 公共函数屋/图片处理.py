import io

import cv2
import numpy as np
from PIL import Image

from 核心对象屋.可视对象 import 计算机可视化开源类


def 保存图片(图片, 保存路径: str):
    图片 = io.BytesIO(图片)
    图片 = Image.open(图片)
    图片.save(保存路径)


def 上传图转二值图片(图片, 阈值: int, 阈值类型: int):
    # 读取后的上传图片用pil打开
    图片数组 = Image.open(io.BytesIO(图片))
    # 转换颜色通道，后用于opencv处理
    图片数组 = 计算机可视化开源类.转换颜色通道(np.asarray(图片数组), cv2.COLOR_RGB2BGR)
    图片数组 = 计算机可视化开源类.二值化图片(图片数组, 阈值=阈值, 阈值类型=阈值类型)
    # 再次转换颜色通道回去
    图片数组 = 计算机可视化开源类.转换颜色通道(图片数组, cv2.COLOR_BGR2RGB)
    # 对图片进行编码，获得缓冲区的内容
    成功, 缓冲区 = cv2.imencode(".jpg", 图片数组)
    # 转换成可返回的数据格式
    图片 = io.BytesIO(缓冲区)
    return 图片
