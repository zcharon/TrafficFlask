# @Time : 2021/6/16 21:46
# @Author : guanghao zhou
# @File : app.py
# Software : PyCharm
from flask import Flask, render_template, Response, request, flash, redirect
import cv2
from sql import Sql
from video import save_video
import threading

# flask实例化
app = Flask(__name__)
# 设置安全密匙，不设置flash用不了
app.secret_key = 'THIS-A-KEY'
sql = Sql()


# 摄像头
class VideoCamera(object):
    def __init__(self, i):
        # 通过opencv获取实时视频流
        self.video = cv2.VideoCapture('video/video' + i + '.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        """
        将OpenCV的image类转化为byte，以供html显示
        :return:
        """
        success, image = self.video.read()
        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


# 用户登录
@app.route('/')
def login():
    return render_template('login.html')


@app.route('/video', methods=['POST', 'GET'])
def video():
    wd = request.args.get('i')
    location = sql.select_distinct(d_id=int(wd))
    return render_template('video.html', index=int(wd), loca=location)


@app.route('/information', methods=['POST', 'GET'])
def information():
    loca = request.args.get('location')
    d_id = request.args.get('d_id')
    record = sql.select_record(d_id=d_id)
    return render_template('information.html', datas=record, loca=loca)


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/site', methods=['POST', 'GET'])
def site():
    district = sql.select_distinct_all()

    return render_template('site.html', sites=district)


# 用户信息验证
@app.route('/userInfo', methods=['POST'])
def userInfo():
    """
    用户登录验证
    :return: None
    """
    form = request.form
    id = form.get('id')
    password = form.get('email')
    if not id:
        flash("请输入账号")
        return render_template("login.html")
    manager = sql.select_manager(username=id, password=password)
    if manager is not None and password == manager.password:
        return redirect('/site')
    else:
        flash("账号密码不正确,请重新输入")
        return render_template('login.html')


def gen(camera):
    """
    迭代器，返回当前视频帧
    :param camera:
    :return:
    """
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed', methods=["GET", "POST"])
def video_feed():
    wd = request.args.get('i')
    return Response(gen(VideoCamera(wd)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def Yolo_video_thread():
    path = "video/video"
    threads = []
    size = int(sql.find_len_district())  # 从数据库中读取数据条数，从而开启线程
    print(size)
    # 创建多线程
    # for i in range(size):
    for i in range(2):
        path_video = path + str(i + 1) + ".mp4"
        threads.append(threading.Thread(target=save_video, args=(path_video, i + 1,)))

    # 开启多线程
    # for i in range(size):
    for i in range(2):
        threads[i].start()


Yolo_video_thread()


if __name__ == '__main__':
    app.run()

