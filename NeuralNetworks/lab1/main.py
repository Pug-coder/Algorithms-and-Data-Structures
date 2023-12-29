import numpy as np
import matplotlib.pyplot as plt

from perceptron.perceptron import Perceptron
from perceptron.activation_funcs import (
    sigmoid_activation,
    tanh_activation,
    relu_activation,
    linear_activation,
)
from char_templates.templates import test_data, training_data

LR = 0.01
SHOTS = 40


def calculate_accuracy(predictions, labels):
    correct_predictions = np.sum(predictions == labels)
    total_predictions = len(labels)
    accuracy = correct_predictions / total_predictions
    return accuracy


def calculate_binary_cross_entropy(predictions, labels):
    epsilon = 1e-15
    predictions = np.clip(predictions, epsilon, 1 - epsilon)
    loss = - (labels * np.log(predictions) + (1 - labels) * np.log(1 - predictions))
    return np.mean(loss)


def main():
    training_inputs, training_labels = training_data()
    test_inputs = test_data()

    # Define activation functions
    activation_functions = [
        sigmoid_activation,
        tanh_activation,
        relu_activation,
        linear_activation,
    ]

    all_accuracy_values = []
    all_loss_values = []

    for activation_func in activation_functions:
        # Create a Perceptron with the current activation function
        perceptron = Perceptron(input_size=len(training_inputs[0]), activation_func=activation_func)

        accuracy_values = []
        loss_values = []

        # Train the Perceptron
        for epoch in range(SHOTS):
            for inputs, label in zip(training_inputs, training_labels):
                prediction = perceptron.predict(inputs)
                error = label - prediction
                perceptron.weights += LR * error * inputs
                perceptron.bias += LR * error

            # Test the Perceptron on the test data
            predictions = np.array([perceptron.predict(inputs) for inputs in test_inputs])

            # Calculate accuracy and loss
            accuracy = calculate_accuracy(predictions, training_labels)
            loss = calculate_binary_cross_entropy(predictions, training_labels)

            accuracy_values.append(accuracy)
            loss_values.append(loss)

        all_accuracy_values.append(accuracy_values)
        all_loss_values.append(loss_values)

    # Plot all accuracies
    plt.figure()
    for i, activation_func in enumerate(activation_functions):
        plt.plot(range(SHOTS), all_accuracy_values[i], label=f"{activation_func.__name__} Accuracy")
    plt.title("All Accuracies")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.savefig("all_accuracies.png")

    # Plot all losses
    plt.figure()
    for i, activation_func in enumerate(activation_functions):
        plt.plot(range(SHOTS), all_loss_values[i], label=f"{activation_func.__name__} Loss")
    plt.title("All Losses")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.savefig("all_losses.png")

    # Show all the plots
    plt.show()


if __name__ == "__main__":
    main()
