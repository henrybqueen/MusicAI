import numpy as np
import os


def create_dataset(data, seq_len=1):
    xs, ys = [], []
    for i in range(len(data) - seq_len):
        v = data[i:(i + seq_len)]
        xs.append(v)
        ys.append(data[i + seq_len])
    return np.array(xs), np.array(ys)


def main(dir_in):

    X, Y = [], []

    new_dir = dir_in + "_DataArrays"
    os.mkdir(new_dir)

    for file in os.listdir(dir_in):
        path = dir_in + "/" + file

        with open(path, "r") as f:
            lines = f.readlines()

        lines = [x[:-1] for x in lines]

        data = np.array(lines)

        x, y = create_dataset(data, 60)

        X.append(x)
        Y.append(y)

    X = np.array(X)
    Y = np.array(Y)

    X = X[0]
    Y = Y[0]

    X = X.reshape((X.shape[0], X.shape[1], 1))

    array_name = new_dir + "/"

    np.save(array_name+"X", X)
    np.save(array_name+"Y", Y)

