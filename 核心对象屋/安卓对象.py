import io
import os
import re
import subprocess
import time

import cv2
import numpy as np
from PIL import Image

from 公共函数屋.字符转换 import 范围转换
from 数据类型屋.结果类型 import 结果类
from 通用对象屋.委托对象 import 委托对象类
from 通用对象屋.消息对象 import 消息提示类


# 这个类包含了各种各样的安卓指令，通过这些指令来完成指定任务。
class 安卓指令类:
    def __init__(self, ip端口):
        self.__空格 = r' '
        self.__安卓调试桥路径 = os.path.join('.', '安卓工具屋', 'adb.exe') + self.__空格
        print(self.__安卓调试桥路径)
        # print(self.__安卓调试桥路径)
        # self.__安卓调试桥路径 = r"./安卓平台工具/adb.exe" + self.__空格
        self.__安卓连接地址 = ip端口
        # 华为手机adb
        # self.__安卓连接地址 = r"192.168.3.22:5555"
        # 返回的数据编码格式
        # self.__编码 = 'GBK'
        self.__编码 = 'UTF-8'
        # 华为刘海 75 像素
        # self.__刘海高度 = 75
        self.__刘海高度 = 0
        self.__连接安卓()

    def __连接安卓(self):
        命令 = self.__安卓调试桥路径 + "connect" + self.__空格 + self.__安卓连接地址
        输出 = self.__执行命令(命令)
        输出 = self.__解码(输出)
        if len(输出) != 0 and 'connected' in 输出:
            print(self.__安卓连接地址 + '\t连接成功')
            self.__安卓调试桥路径 = self.__安卓调试桥路径 + "-s" + self.__空格 + self.__安卓连接地址 + self.__空格
            # 输出 = self.__执行命令(命令)
        else:
            raise Exception(self.__安卓连接地址 + '\t连接失败')

    def 敲击屏幕(self, 位置: tuple, 休眠时间=0.8, **参数字典):
        if 位置 is not None and 位置 != '':
            x的增量, y的增量 = self.__计算增量()
            命令 = self.__安卓调试桥路径 + 'shell input tap' + self.__空格 + str(
                x的增量 + 位置[0]) + self.__空格 + str(
                y的增量 + 位置[1])
            self.__执行命令(命令)
            self.间隙时间(休眠时间)

    def 滑动屏幕(self, 位置: tuple, 滑动量=(0, 20), 休眠时间=1.5, **参数字典):
        """

        :param 位置: 按住的位置，例如(50,50)
        :param 滑动量:
        :param 休眠时间:
        :return:
        """
        if 滑动量 is not None and 滑动量 != '':
            x的增量, y的增量 = self.__计算增量()
            命令 = self.__安卓调试桥路径 + "shell input swipe" + self.__空格 + str(
                x的增量 + 位置[0]) + self.__空格 + str(
                y的增量 + 位置[1]) + self.__空格 + str(x的增量 + 位置[0] + 滑动量[0]) + self.__空格 + str(
                y的增量 + 位置[1] + 滑动量[1])
            self.__执行命令(命令)
            self.间隙时间(休眠时间)

    def 返回(self, 休眠时间=0.8, **参数字典):
        命令 = self.__安卓调试桥路径 + "shell input keyevent KEYCODE_BACK"
        self.__执行命令(命令)
        self.间隙时间(休眠时间)

    def 主界面(self, 休眠时间=0.8, **参数字典):
        命令 = self.__安卓调试桥路径 + "shell input keyevent KEYCODE_HOME"
        self.__执行命令(命令)
        self.间隙时间(休眠时间)

    def __计算增量(self):
        """
        用于计算由于刘海屏导致的点击错位复原
        :return:
        """
        x的增量 = 0
        y的增量 = 0
        屏幕方向 = self.__获取屏幕方向()
        if 屏幕方向 == 0:
            y的增量 = y的增量 + self.__刘海高度
        elif 屏幕方向 == 1:
            x的增量 = x的增量 + self.__刘海高度

        return x的增量, y的增量

    def 打开游戏(self, 游戏启动名, 休眠时间=0.5):
        """
        直接启动游戏
        运行adb shell dumpsys window | findstr mCurrentFocus 用于查找应用启动入口
        :param 游戏启动名:
        :param 休眠时间:
        :return:
        """
        命令 = self.__安卓调试桥路径 + "shell am start -n" + self.__空格 + 游戏启动名
        self.间隙时间()
        self.__执行命令(命令)
        self.间隙时间(休眠时间)

    def 获取手机屏幕尺寸(self):
        命令 = self.__安卓调试桥路径 + "shell wm size"
        输出 = self.__执行命令(命令)
        输出 = self.__解码(输出)
        输出 = re.findall(r"\d+", 输出)
        输出 = tuple(map(int, 输出[:]))
        屏幕方向 = self.__获取屏幕方向()
        if 屏幕方向 == 0 or 屏幕方向 == 2:
            return 输出[-2], 输出[-1] - self.__刘海高度
        else:
            return 输出[-1] - self.__刘海高度, 输出[-2]

    def 裁剪图片(self, 范围=(0, 0, 10, 10), 完整相对路径='垃圾堆放屋/临时', 是否保存=True):
        # 将图片转换成opencv专用的格式后，在转成opencv的格式不过这个图片是BGR的顺序的。
        # 现在是多次一举的。暂时注释，后期可能删除。
        # 图片 = cv.imdecode(np.asarray(bytearray(输出), dtype=np.uint8), cv.IMREAD_COLOR)
        # if self.__刘海高度 != 0:
        #     图片 = self.__图片去刘海(图片)
        #
        # 图片 = cv2.cvtColor(图片, cv2.COLOR_BGR2RGB)
        # 该函数可以直接打开BytesIO对象
        图片 = Image.open(self.截屏())
        # 后续转成jpg格式，这样没有透明度
        图片 = 图片.convert('RGB')
        图片 = 图片.crop(范围)
        # 保存是同步执行的，可能会导致阻塞

        完整相对路径 = 完整相对路径 + '.jpg'
        if 是否保存:
            图片.save(完整相对路径)
        # 换成这个格式是专门为了对应opencv的处理函数，这是必须的。
        图片 = cv2.cvtColor(np.asarray(图片), cv2.COLOR_RGB2BGR)

        return 完整相对路径, 图片

        # 返回模拟器整个屏幕的图片数据

    def 截屏(self):
        命令 = self.__安卓调试桥路径 + "shell screencap -p"
        输出 = self.__执行命令(命令).replace(b'\r\n', b'\n')
        # 将从模拟器返回的数据转为io.BytesIO对象，它可以直接成流式数据
        图片 = io.BytesIO(输出)
        return 图片

    def __图片去刘海(self, 图片):
        屏幕方向 = self.__获取屏幕方向()
        if 屏幕方向 == 0:
            图片 = 图片[self.__刘海高度:]
        elif 屏幕方向 == 2:
            图片 = 图片[:- self.__刘海高度]
        elif 屏幕方向 == 1:
            图片 = 图片[:, self.__刘海高度:]
        elif 屏幕方向 == 3:
            图片 = 图片[:, :- self.__刘海高度]
        return 图片

    def __获取屏幕方向(self):
        """

        :return: 0：纵向   1：横向
        """
        命令 = self.__安卓调试桥路径 + "shell dumpsys input"
        输出 = self.__执行命令(命令)
        输出 = self.__解码(输出)
        输出 = 输出.split('\r\n')

        方向字符串 = ''
        for 字符串 in 输出:
            下标 = 字符串.find('SurfaceOrientation')
            if 下标 != -1:
                方向字符串 = 字符串
                break
        if 方向字符串 != '':
            输出 = re.findall(r"\d+", 方向字符串)
            输出 = tuple(map(int, 输出[:]))
            return 输出[0]
        else:
            Exception('未知错误：未找到屏幕方向的所在位置')

    def __解码(self, 标准输出: bytes):
        """
        把bytes转换为str
        :param 标准输出:
        :return:
        """
        输出 = 标准输出.decode(self.__编码)
        return 输出

    @staticmethod
    def __执行命令(命令: str):
        # 命令=命令.split(' ')
        进程 = subprocess.Popen(
            命令,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        标准输出, 标准错误 = 进程.communicate()
        if 进程.returncode > 0:
            raise Exception(进程.returncode, 标准错误)
        return 标准输出

    def __del__(self):
        pass
        # self.__执行命令(self.__安卓调试桥路径 + 'kill-server')

    def 断开连接(self):
        # adb disconnect 手机ip //断开指定IP
        # adb disconnect //断开所有
        pass

    @staticmethod
    def 间隙时间(时间=0.5):
        time.sleep(时间)


class 安卓预处理类:
    def __init__(self, 项目名: str, 编码列表, 判断结果: 结果类):
        self.项目名 = 项目名
        self.编码列表 = 编码列表
        self.判断结果 = 判断结果
        self.参数字典 = {}
        match 编码列表[0]:
            case 'A':
                self.预处理点击()
            case 'B':
                self.预处理滑动()
            case 'C':
                self.预处理返回()
            case 'D':
                self.预处理主界面()

    def 预处理点击(self):
        self.参数字典['行为函数'] = 委托对象类.字典[self.项目名].敲击屏幕
        self.参数字典['位置'] = self.判断结果.位置

    def 预处理滑动(self):
        print(self.编码列表)
        self.参数字典['行为函数'] = 委托对象类.字典[self.项目名].滑动屏幕
        self.参数字典['位置'] = self.判断结果.位置
        滑动量 = [0, 0]
        if len(self.编码列表) == 2:
            滑动量 = [self.编码列表[1], self.编码列表[1]]
        elif self.编码列表[2] == 'X':
            滑动量[0] = self.编码列表[1]
        elif self.编码列表[2] == 'Y':
            滑动量[1] = self.编码列表[1]
        self.参数字典['滑动量'] = tuple(滑动量)

    def 预处理返回(self):
        self.参数字典['行为函数'] = 委托对象类.字典[self.项目名].返回
        self.参数字典['位置'] = self.判断结果.位置

    def 预处理主界面(self):
        self.参数字典['行为函数'] = 委托对象类.字典[self.项目名].主界面
        self.参数字典['位置'] = self.判断结果.位置
