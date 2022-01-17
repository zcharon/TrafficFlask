import numpy as np
import pandas as pd


def toNdarrya(persons, vehicles):
    # 先转换为二维数组，再转换为ndarray
    n = len(persons)
    tmp = []
    maxPersons = 0
    maxVehicles = 0

    # 遍历车、人流量列表，将车、人流量的最大值多为该路口的特征
    for i in range(n):
        if maxPersons < persons[i]:
            maxPersons = persons[i]
        if maxVehicles < vehicles[i]:
            maxVehicles = vehicles[i]
    tmp.append([maxVehicles, maxPersons])
    tmp_nd = np.array(tmp)

    # 将车、人流量信息存储成ndarray
    dataset = pd.DataFrame(tmp_nd)
    dataset.to_csv('./export_file/K.csv', mode='a', header=False)
