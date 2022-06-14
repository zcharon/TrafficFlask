"""
进行视频检测,程序主接口
nodel_data:存放训练权重文件
out_viseo:存放检测后的完成品
video:存放待检测文件
yolo.py:构建yoloV4模型，在此可以更改权重文件路径
"""
from YOLO.yolo import YOLO
from PIL import Image
import numpy as np
import cv2
from YOLO.traffic_time import draw_vehicle_flow
import datetime
import threading
from sql import Sql


def save_video(path, i):
    """
    启动YOLO检测程序，检测视频并保存检测后的图像。
    :param path: 视频地址
    :param i: 当前线程标号
    :return:
    """
    str_info = "线程" + str(i) + "：save_video启动"
    print(str_info)
    yolo = YOLO()  # 导入YOLOV4模型
    cv2.namedWindow('video' + str(i), 2)
    capture = cv2.VideoCapture(path)

    # 保存检测的视频
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # 定义视频保存格式
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获得视频的相关信息
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # fps = capture.get(cv2.CAP_PROP_FPS)  # 获得帧率
    out = cv2.VideoWriter("YOLO/out_video/traffic_flow" + str(i) + ".avi",
                          fourcc, 20, (width, height))  # 确定预测视频保存路径

    # 打开视频失败，输出失败信息
    if not capture.isOpened():
        print("Error opening video stream or file")

    # count = 0  # 计数器

    persons = []
    vehicles = []
    seconds = []
    second_draw = []
    persons_second = []
    vehicles_second = []

    start = datetime.datetime.now()  # 获取当前运行系统时间
    before = datetime.datetime.now()
    sql = Sql()  # 创建数据库对象
    while capture.isOpened():  # 循环播放视频
        # t = []
        # 读取某一帧
        ref, frame = capture.read()
        if ref is True:
            image = frame.copy()  # 复制frame
            # 格式转变，BGRtoRGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 转变成Image
            frame = Image.fromarray(np.uint8(frame))
            # 进行检测, 返回绘制预测框后的视频，预测框，预测标签
            # classes: 对应预测框的类别; boxs: 预测框
            # frame绘制完预测框的图片帧(此时frame格式为PIL，转为image需要frame = np.array(frame))
            frame, classes, boxs = yolo.detect_image(frame)
            # 绘制路口实时车流量，并返回两个bool参数
            # draw, 是否进行了这1s的车流量统计
            # con, 当前道路是否发生了拥堵
            draw, con = draw_vehicle_flow(frame, classes, start, seconds,
                                          vehicles, persons, vehicles_second, persons_second, second_draw)
            if draw:
                # 数据清空
                now = datetime.datetime.now()
                seconds = []
                if (now - before).seconds > 1:
                    sql.add_record(now, i, vehicles_second[-1], persons_second[-1])
                    before = now
                # print(persons_second[-1])
                # print(vehicles_second[-1])
                persons_second = []
                vehicles_second = []
            # 将Image转变为numpy
            frame = np.array(frame)
            # 格式转变，RGBtoBGR
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
            cv2.imshow('video' + str(i), frame)
            if cv2.waitKey(10) & 0xff == ord('q'):
                break
        else:
            break

    # 进行销毁工作
    capture.release()
    # out.release()
    yolo.close_session()
    cv2.destroyAllWindows()
    print("over")


if __name__ == '__main__':
    path1 = "video/video1.mp4"
    path2 = "video/video1.mp4"
    thread1 = threading.Thread(target=save_video, args=(path1, 1,))
    thread2 = threading.Thread(target=save_video, args=(path2, 2,))
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()



