"""
使用SLTM循环神将网络进行车流量预测（预测时间为视频播放后10min）
"""
import csv
import os
from keras.callbacks import ReduceLROnPlateau, EarlyStopping
from numpy import array
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
import matplotlib.pyplot as plt


def readFile():
    """
    获取数据借口，并将数据转化为x_train, y_train
    :return:[], []
    """
    x = []
    y = []
    # 读取csv文件，以，分割
    with open("./export_file/traffic_flow.csv", mode='r') as f:
        read = csv.reader(f)
        for row in read:
            if len(row) >= 2:
                x.append(int(row[0]))
                y.append(int(float(row[1])))
    return x, y


def split_sequence(x_input, y_input, n_steps):
    """
    数据进行datatime分类
    :param x_input:
    :param y_input:
    :param n_steps:
    :return:
    """
    X, y = list(), list()
    for i in range(len(x_input)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the sequence
        if end_ix > len(x_input)-1:
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = x_input[i:end_ix], y_input[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)


def split_test(x_input, n_steps):
    X = list()
    for i in range(len(x_input)):
        end_ix = i + n_steps
        if end_ix > len(x_input)-1:
            break
        seq_x = x_input[i:end_ix]
        X.append(seq_x)
    return array(X)


def lstm(x_input, y_input):
    """
    将数据导入并进行LSTM训练
    :param x_input:
    :param y_input:
    :return:
    """
    n_steps = 3

    X, y = split_sequence(x_input, y_input, n_steps)
    n_features = 1
    X = X.reshape((X.shape[0], X.shape[1], n_features))
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(n_steps, n_features), return_sequences=True))  # 隐藏层，输入，特征维
    model.add(LSTM(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    weights_path = "./model_data/flow_lstm.h5"
    if os.path.exists(weights_path):
        model.load_weights(weights_path, by_name=True)
    # 早停法，acc三次不下降就降低学习率
    # 学习率下降的方式，acc三次不下降就下降学习率继续训练
    reduce_lr = ReduceLROnPlateau(
        monitor='loss',
        factor=0.5,
        patience=3,
        verbose=1
    )

    # 是否需要早停，当val_loss一直不下降的时候意味着模型基本训练完毕，可以停止
    early_stopping = EarlyStopping(
        monitor='loss',
        min_delta=0,
        patience=10,
        verbose=1
    )

    # fit model
    model.fit(X, y, epochs=70, batch_size=16, verbose=1, callbacks=[reduce_lr, early_stopping])

    log_dir = "./model_data/"
    model.save_weights(log_dir + 'flow_lstm.h5')
    x = list(range(x_input[-1], x_input[-1] + 600))
    x_test = split_test(x, n_steps)
    x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], n_features))
    y_test = model.predict(x_test, 1)
    predit_fraw(y_test)


def predit_fraw(yhat):
    plt.subplots()
    plt.title(r'traffic flow predit', fontsize=20)
    plt.plot(yhat, label='vehicles', color='b')
    plt.savefig("./export_file/fraffic_predit.png")
    plt.show()


def flow_lstm():
    x_train, y_train = readFile()
    lstm(x_train, y_train)


if __name__ == "__main__":
    flow_lstm()

