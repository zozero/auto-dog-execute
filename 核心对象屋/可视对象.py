import os
import cv2
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim

from 数据类型屋.结果类型 import 结果类
from 通用对象屋.消息对象 import 消息提示类


# 该类是对opencv的封装，加额外的自定义函数。
class 计算机可视化开源类:
    @staticmethod
    def 匹配模板(新图, 旧图, 算法, 最低相似度=0.8, 补充判断=0) -> 结果类:
        """
        用于在新图中找到和旧图相似的图。
        :param 新图: 刚刚截取下来的图片，后续会使用旧图在新图中找到似类旧图的图像位置。
        :param 旧图: 之前截屏后流程端截取保存的图片，用它在新图中找到类似的旧图。
        :param 算法:
                    cv.TM_SQDIFF_NORMED
                    cv.TM_CCORR_NORMED
                    cv.TM_CCOEFF_NORMED
                    链接：https://docs.opencv.org/4.x/df/dfb/group__imgproc__object.html#ga586ebfb0a7fb604b35a23d85391329be
        :param 最低相似度: 对于相似度的最低要求
        :param 补充判断: 0 不补充    1 结构相似度
        :return: 返回结果类
        """
        高, 宽 = 旧图.shape[:2]
        匹配结果 = cv2.matchTemplate(新图, 旧图, 算法)
        最差值, 最高值, 最差位置, 最佳位置 = cv2.minMaxLoc(匹配结果)
        # 返回值
        返回值 = 结果类()
        返回值.状态 = False
        返回值.图片尺寸 = (旧图.shape[1], 旧图.shape[0])
        返回值.位置 = (最佳位置[0] + int(返回值.图片尺寸[0] / 2), 最佳位置[1] + int(返回值.图片尺寸[1] / 2))
        返回值.最高相似度 = round(最高值, 3)

        if 最高值 >= 最低相似度:
            返回值.状态 = True
        else:
            返回值.状态 = False
        if 补充判断 == 1:
            y数组, x数组 = np.where(匹配结果 >= 最低相似度)
            返回值.状态, 返回值.位置 = 计算机可视化开源类.最佳结构相似度(旧图, 新图, y数组, x数组, 高, 宽)

        return 返回值

    @staticmethod
    def 最佳结构相似度(旧图, 新图, y数组, x数组, 高, 宽):
        for y, x in zip(y数组, x数组):
            图片2 = 新图[y:y + 高, x:x + 宽]
            状态 = 计算机可视化开源类.计算结构相似度(图片2, 旧图)
            if 状态:
                return 状态, (x + 宽, y + 高)
            else:
                continue
        return False, (-1, -1)

    @staticmethod
    def 计算结构相似度(图片1, 图片2, 相似度=0.8):
        """
        防止误判而额外增加的一层计算方法。
        :param 图片1:
        :param 图片2:
        :param 相似度:
        :return:
        """
        返回值 = ssim(图片1, 图片2)
        if 返回值 > 相似度:
            返回值 = True
        else:
            返回值 = False
        return 返回值

    @staticmethod
    def 读取图片(图片路径):
        if os.path.isfile(图片路径):
            图片数组 = Image.open(图片路径)
            图片数组 = 计算机可视化开源类.转换颜色通道(np.asarray(图片数组), cv2.COLOR_RGB2BGR)
            # self.显示图片(图片数组)
            return 图片数组
        else:
            消息提示类.致命错误('计算机可视化开源类-读取图片 %s' % 图片路径, '图片载入失败。')

    @staticmethod
    def 转换颜色通道(图片数组, 通道码):
        """

        :param 图片数组:
        :param 通道码: 转换通道的编码 https://docs.opencv.org/4.x/d8/d01/group__imgproc__color__conversions.html#ga4e0972be5de079fed4e3a10e24ef5ef0
        :return:
        """
        return cv2.cvtColor(图片数组, 通道码)

    @staticmethod
    def 转成灰度图(图片数组):
        灰度图数组 = cv2.cvtColor(图片数组, cv2.COLOR_BGR2GRAY)
        return 灰度图数组

    @staticmethod
    def 二值化图片(图片数组, 阈值, 最大值=255, 阈值类型=cv2.THRESH_BINARY):
        """
        :param 图片数组:
        :param 阈值:
        :param 最大值:
        :param 阈值类型: https://docs.opencv.org/4.5.5/d7/d1b/group__imgproc__misc.html#gaa9e58d2860d4afa658ef70a9b1115576
        :return:
        """
        灰度图数组 = 计算机可视化开源类.转成灰度图(图片数组)
        二值化 = cv2.threshold(灰度图数组, 阈值, 最大值, 阈值类型)[1]
        return 二值化

    @staticmethod
    def 测试(参数):
        print(参数, " 这是用来测试的函数")
