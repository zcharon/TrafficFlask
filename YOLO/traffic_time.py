"""
统计实时车流量
返回车流与人流
"""
from PIL import ImageFont, ImageDraw
import numpy as np
import datetime


def draw_vehicle_flow(image, classes, start, second, vehicles, persons, vehicles_second, persons_second, second_draw):
    """
    在视频中绘制车流量信息。
    :param image:
    :param classes:
    :param start:
    :param second:
    :param vehicles:
    :param persons:
    :param vehicles_second:
    :param persons_second:
    :param second_draw:
    :return:
    """
    vehicle = 0
    person = 0
    for class_ in classes:
        if class_ == 0:
            person += 1
        elif 1 <= class_ <= 8:
            vehicle += 1

    now = datetime.datetime.now()
    second_now = (now-start).seconds

    if len(second) == 0:
        second.append(second_now)

    tag = True
    if second_now > second[-1]:
        per = 0
        veh = 0
        for p in persons_second:
            per += p
        for v in vehicles_second:
            veh += v

        per /= len(persons_second)
        veh /= len(vehicles_second)

        # with open("..date/traffic_flow.csv", "a+") as f:
        #     writer = csv.writer(f)
        #     writer.writerow([second_now, veh])
        vehicles.append(int(veh))

        # with open("..data/person_flow.csv", "a+") as f:
        #     writer = csv.writer(f)
        #     writer.writerow([second_now, per])
        persons.append(int(per))
        second_draw.append(second_now)

    else:
        second.append(second_now)
        vehicles_second.append(int(vehicle))
        persons_second.append(int(person))
        tag = False

    congestion = False

    if len(persons) > 0 and len(vehicles):
        font = ImageFont.truetype(font='font/simhei.ttf',
                                  size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
        label_person = 'person {:}'.format(persons[-1])
        label_person = label_person.encode('utf-8')
        label_vehicle = 'vehicle {:}'.format(vehicles[-1])
        label_vehicle = label_vehicle.encode('utf-8')

        color = (255, 255, 255)

        if vehicles[-1] >= 18:
            congestion = True
            color = (255, 0, 0)

        draw = ImageDraw.Draw(image)
        draw.text((50, 110), str(label_person, 'UTF-8'), fill=color, font=font)
        draw.text((50, 140), str(label_vehicle, 'UTF-8'), fill=color, font=font)

    return tag, congestion,
