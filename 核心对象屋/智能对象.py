from typing import Union

from ultralytics import YOLO


class 你只看一次类:
    @staticmethod
    def 训练(模型存放路径: str, 配置文件路径: str, 轮回数: int = 160, 设备: Union[list, int, str] = 0) -> dict:
        你只看一次模型 = YOLO(模型存放路径)

        结果: dict = 你只看一次模型.train(data=配置文件路径, epochs=轮回数, imgsz=640, device=设备,save_dir=模型存放路径)
        return 结果

    @staticmethod
    def 预测(模型存放路径: str, 图片, 置信度: float = 0.8, 设备: Union[list, int, str] = 0) :
        你只看一次模型 = YOLO(模型存放路径)
        结果列表:list= 你只看一次模型.predict(图片, show_labels=False, show_conf=False, show_boxes=False, conf=置信度, device=设备)
        for 结果 in 结果列表:
            位置 = 结果.boxes
            print("--------位置开始--------")
            print(位置)
            print("--------位置结束--------")
            结果.show()
            # 结果.save(filename='result.jpg')  # save to disk
            # return 结果

