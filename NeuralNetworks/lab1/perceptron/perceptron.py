import numpy as np


class Perceptron:

    def __init__(self, input_size, activation_func):
        self.weights = np.random.rand(input_size)
        self.bias = np.random.rand()
        self.activation_func = activation_func

    def predict(self, inputs):
        # Weighted sum
        weighted_sum = np.dot(inputs, self.weights) + self.bias
        # Activation function
        return self.activation_func(weighted_sum) >= 0.5
