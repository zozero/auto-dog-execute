import io

from PIL import Image


def 保存图片(图片, 保存路径: str):
    图片 = io.BytesIO(图片)
    图片 = Image.open(图片)
    图片.save(保存路径)
