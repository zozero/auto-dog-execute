class 结果类:
    # 是否找到了
    状态: bool
    # 需要执行点击操作触发的位置
    位置: tuple
    最高相似度: float
    # （宽，高）
    图片尺寸: tuple

    def __dict__(self):
        return {
            "状态": self.状态,
            "位置": self.位置,
            '最高相似度': self.最高相似度,
            '图片尺寸': self.图片尺寸,
        }
