import numpy as np


def linear_activation(x):
    return x


def sigmoid_activation(x):
    return 1 / (1 + np.exp(-x))


def tanh_activation(x):
    return np.tanh(x)


def relu_activation(x):
    return np.maximum(0, x)
