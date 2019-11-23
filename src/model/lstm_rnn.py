# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow

class Train(object):
    """
        训练类
    """
    time_step = 20
    rnn_unit = 10
    batch_size = 60
    input_size = 1
    output_size = 1
    lr = 0.0006
    train_x = []
    train_y = []
    def __init__(self, filename):
        """
            init method
        """
        with open(filename) as f:
            df = pd.read_csv(f)
            data = np.array(df['最高价'])
            data = data[:: -1]
            #以折线图展示data
            plt.figure()
            plt.plot(data)
            plt.show()

            normalize_data = (data - np.mean(data)) / np.std(data)  #标准化
            normalize_data = normalize_data[:, np.newaxis]  #增加维度
            for i in range(len(normalize_data) - time_step - 1):
                x = normalize_data[i : i + time_step]
                y = normalize_data[i + 1 : i + time_step + 1]
                self.train_x.append(x.tolist())
                self.train_y.append(y.tolist())
        return

if __name__ == '__main__':
train = Train('stock_dataset.csv')
