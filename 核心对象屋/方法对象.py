import os

from 公共函数屋.字符转换 import 字符串转换, 范围转换
from 公共函数屋.工具函数 import 限制范围
from 数据类型屋.结果类型 import 结果类
from 核心对象屋.可视对象 import 计算机可视化开源类
from 通用对象屋.委托对象 import 委托对象类
from 通用对象屋.消息对象 import 消息提示类
from 通用对象屋.表格对象 import 逗号分隔符类
from 通用对象屋.默认对象 import 目录名称对象


class 匹配方法类:
    @staticmethod
    def 图片匹配(**参数列表) -> 结果类:
        """
        用于在新图中找到和旧图相似的图。
        :param 参数列表:
        新图：
        旧图路径：
        :return:
        """
        新图 = 计算机可视化开源类.转成灰度图(参数列表['新图'])

        旧图 = 计算机可视化开源类.读取图片(参数列表['旧图路径'])
        旧图 = 计算机可视化开源类.转成灰度图(旧图)

        返回值 = 计算机可视化开源类.匹配模板(新图, 旧图, 参数列表['算法'], 参数列表['最低相似度'], 参数列表['额外补充'])
        # 修改相对图片的位置为相对屏幕的位置
        返回值.位置 = (
            返回值.位置[0] + 参数列表['范围'][0],
            返回值.位置[1] + 参数列表['范围'][1]
        )
        return 返回值

    @staticmethod
    def 二值图片匹配(**参数列表):
        参数列表['新图'] = 计算机可视化开源类.二值化图片(参数列表['新图'], 阈值=参数列表['阈值'],
                                                         阈值类型=参数列表['阈值类型'])

        匹配图片 = 计算机可视化开源类.读取图片(参数列表['旧图路径'])
        匹配图片 = 计算机可视化开源类.二值化图片(匹配图片, 阈值=参数列表['阈值'], 阈值类型=参数列表['阈值类型'])

        返回值 = 计算机可视化开源类.匹配模板(参数列表['新图'], 匹配图片, 参数列表['算法'], 参数列表['最低相似度'])
        # 修改相对图片的位置为相对屏幕的位置
        返回值.位置 = (
            返回值.位置[0] + 参数列表['范围'][0],
            返回值.位置[1] + 参数列表['范围'][1]
        )
        return 返回值

    @staticmethod
    def 匹配再匹配(**参数列表):
        if 参数列表['初次结果'].状态 is False:
            return 参数列表['初次结果']
        else:
            # 其实已经匹配过一次了，只不过根据之前匹配的位置，
            # 再计算得出新的匹配范围，但它会在方法预处理类实现，所以这里只需要这样。
            # 位置已经进行处理，无需再次增加。
            返回值 = 参数列表['后函数字典']['函数实例'](**参数列表['后参数字典'])
            return 返回值

    @staticmethod
    def 无图匹配(**参数列表):
        结果 = 结果类()
        结果.状态 = True
        结果.位置 = (参数列表['X轴'], 参数列表['Y轴'])
        结果.最高相似度 = 1.0
        结果.图片尺寸 = (0, 0)
        return 结果

    @staticmethod
    def 多图匹配(**参数列表):
        结果 = 结果类()
        结果.状态 = False
        for 旧图路径 in 参数列表['旧图路径列表']:
            参数列表['旧图路径'] = 旧图路径
            结果 = 匹配方法类.图片匹配(**参数列表)
            if 结果.状态:
                break
            else:
                continue
        return 结果

    @staticmethod
    def 分配函数(编码) -> dict:
        """
        主要是为了获取文件名和函数实例方法
        :param 编码:
        :return:
        """
        # 返回旧图的文件目录和相应方法的函数
        match 编码:
            case 'A':
                return {
                    '文件名': '图片匹配',
                    '函数实例': 匹配方法类.图片匹配
                }
            case 'B':
                return {
                    '文件名': '二值图片匹配',
                    '函数实例': 匹配方法类.二值图片匹配
                }
            case 'C':
                return {
                    '文件名': '匹配再匹配',
                    '函数实例': 匹配方法类.匹配再匹配
                }
            case 'D':
                return {
                    '文件名': '无图匹配',
                    '函数实例': 匹配方法类.无图匹配
                }
            case 'E':
                return {
                    '文件名': '多图匹配',
                    '函数实例': 匹配方法类.多图匹配
                }


class 方法预处理类:
    """
    主要是为了准备匹配方法的参数

    """

    def __init__(self, 编码, 参数字典):
        self.编码 = 编码
        self.参数字典 = 参数字典
        self.对照编码(编码)

    def 对照编码(self, 编码):
        match 编码:
            case 'A':
                self.预处理图片匹配()
            case 'B':
                self.预处理二值图片匹配()
            case 'C':
                self.预处理匹配再匹配()
            case 'D':
                self.预处理无图匹配()
            case 'E':
                self.预处理多图匹配()

    def 预处理图片匹配(self):
        # 旧图路径需要放在这里，之后可以无图匹配的方式
        self.参数字典['旧图路径'] = os.path.join(self.参数字典['项目路径'], 目录名称对象['图片目录'],
                                                 self.参数字典['图片名'] + '.jpg')
        # 截取范围是左上和右下的坐标
        屏幕尺寸 = 委托对象类.字典[self.参数字典['项目名']].获取手机屏幕尺寸()
        范围 = 范围转换(self.参数字典['范围'], 屏幕尺寸)
        范围 = 限制范围(范围, 屏幕尺寸)
        图片路径, 图片 = 委托对象类.字典[self.参数字典['项目名']].裁剪图片(范围)
        self.参数字典['新图'] = 图片
        self.参数字典['新图路径'] = 图片路径
        self.参数字典['范围'] = 范围

    def 预处理二值图片匹配(self):
        self.参数字典['旧图路径'] = os.path.join(self.参数字典['项目路径'], 目录名称对象['图片目录'],
                                                 self.参数字典['图片名'] + '.jpg')
        # 截取范围是左上和右下的坐标
        屏幕尺寸 = 委托对象类.字典[self.参数字典['项目名']].获取手机屏幕尺寸()
        范围 = 范围转换(self.参数字典['范围'], 委托对象类.字典[self.参数字典['项目名']].获取手机屏幕尺寸())
        范围 = 限制范围(范围, 屏幕尺寸)
        图片路径, 图片 = 委托对象类.字典[self.参数字典['项目名']].裁剪图片(范围)
        self.参数字典['新图'] = 图片
        self.参数字典['新图路径'] = 图片路径
        self.参数字典['范围'] = 范围

    def 预处理匹配再匹配(self):
        # 使用前编码设置参数
        函数字典, 前参数字典 = self.识别匹配('前编码')
        # 先去执行前编码的匹配，返回结果
        判断结果: 结果类 = 函数字典['函数实例'](**前参数字典)
        # 用于再方法匹配中直接查询结果返回
        self.参数字典['初次结果'] = 判断结果
        # 如果初次寻找没找到就直接返回
        if 判断结果.状态 is False:
            return
        # 屏幕坐标的坐标位置
        x = int(判断结果.位置[0] - 判断结果.图片尺寸[0] / 2)
        y = int(判断结果.位置[1] - 判断结果.图片尺寸[1] / 2)
        宽 = 判断结果.图片尺寸[0]
        高 = 判断结果.图片尺寸[1]

        x2 = x + 宽 + int(self.参数字典['X偏移'])
        if x > x2:
            临时x = x2
            x2 = x
            x = 临时x
        y2 = y + 高 + int(self.参数字典['Y偏移'])
        if y > y2:
            临时y = y2
            y2 = y
            y = 临时y

        # 设置范围
        范围 = (x, y, x2, y2)
        # 截取范围是左上和右下的坐标
        屏幕尺寸 = 委托对象类.字典[self.参数字典['项目名']].获取手机屏幕尺寸()
        范围 = 限制范围(范围, 屏幕尺寸)
        print("范围",范围)
        # 使用后编码获取相应的参数，之后会在匹配方法类中去执行匹配
        函数字典, 后参数字典 = self.识别匹配('后编码')
        后参数字典['范围'] = 范围

        # 必须重新根据新的范围重新裁剪图片才行
        图片路径, 图片 = 委托对象类.字典[self.参数字典['项目名']].裁剪图片(范围)
        后参数字典['新图'] = 图片
        后参数字典['新图路径'] = 图片路径

        self.参数字典['后参数字典'] = 后参数字典
        self.参数字典['后函数字典'] = 函数字典



    # 用于匹配再匹配的识别前编码和后编码
    def 识别匹配(self, 类型: str):
        编码列表 = 字符串转换(self.参数字典[类型])
        if 编码列表 and len(编码列表) == 2:
            # 获取匹配方法
            函数字典 = 匹配方法类.分配函数(编码列表[0])
            项目路径 = os.path.join(目录名称对象['表格目录'], self.参数字典['项目名'])
            文件路径 = os.path.join(str(项目路径), 目录名称对象['方法目录'], 函数字典['文件名'] + '.csv')

            表格文件 = 逗号分隔符类(文件路径)
            # 编码列表[1]是指第几行数据，拿出来后直接生成一个字典类型。
            临时参数字典 = 表格文件.数据列表[编码列表[1]].to_dict()
            临时参数字典['项目名'] = self.参数字典['项目名']
            临时参数字典['项目路径'] = 项目路径
            # 预处理各种参数，之后用于给匹配方法传参
            预处理 = 方法预处理类(编码列表[0], 临时参数字典)
            # 判断结果: 结果类 = 函数字典['函数实例'](**预处理.参数字典)
            return 函数字典, 预处理.参数字典
        else:
            消息提示类.致命错误('预处理匹配再匹配', '编码不正确或者不存在。')

    def 预处理无图匹配(self):
        pass

    def 预处理多图匹配(self):
        # 旧图路径需要放在这里，之后可以无图匹配的方式
        self.参数字典['旧图路径列表'] = []
        for i in range(self.参数字典['数量']):
            self.参数字典['旧图路径列表'].append(os.path.join(self.参数字典['项目路径'], 目录名称对象['图片目录'],
                                                              self.参数字典['图片名'] + '-' + str(i + 1) + '.jpg'))

        # 截取范围是左上和右下的坐标
        屏幕尺寸 = 委托对象类.字典[self.参数字典['项目名']].获取手机屏幕尺寸()
        范围 = 范围转换(self.参数字典['范围'], 屏幕尺寸)
        范围 = 限制范围(范围, 屏幕尺寸)
        图片路径, 图片 = 委托对象类.字典[self.参数字典['项目名']].裁剪图片(范围)
        self.参数字典['新图'] = 图片
        self.参数字典['新图路径'] = 图片路径
        self.参数字典['范围'] = 范围
