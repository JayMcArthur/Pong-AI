import numpy as np
import scipy.special
import random
import os
#pylint: disable=no-member
os.system('cls')

class neuralNetwork:

    def __init__(self, inputNodes, hiddenHeight, hiddenLength, outputNodes, learningRate):
        # Save Size
        self.iNodes = inputNodes
        self.hNodes = [hiddenHeight, hiddenLength]
        self.oNodes = outputNodes

        # Save Learning Rate
        self.lr = learningRate

        # activation function is the sigmoid function

        self.activation_function = lambda x: scipy.special.expit(x)
        
        self.weights = []

        # Create Weights (Normally distributed)
        # Input to Hidden
        self.weights.append(np.random.normal(0.0, pow(self.iNodes, -0.5), (self.hNodes[0], self.iNodes)))
        # Hidden to Hidden
        if (self.hNodes[1] > 1):
            for i in range(self.hNodes[1]-1):
                self.weights.append(np.random.normal(min(0.0,i), pow(self.hNodes[0], -0.5), (self.hNodes[0], self.hNodes[0])))
        # Hidden to Output
        self.weights.append(np.random.normal(0.0, pow(self.hNodes[0], -0.5), (self.oNodes, self.hNodes[0])))

    def train(self, inputs_list, target_list):
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(target_list, ndmin=2).T
        node_inputs = [None,]
        node_outputs = [None,]
        node_errors = [None,]

        # Solve
        # Input to Hidden
        node_inputs[0] = np.dot(self.weights[0], inputs)
        node_outputs[0] = self.activation_function(node_inputs[0])
        # Hidden to Final
        for i in range(1, len(self.weights)):
            node_inputs.append(np.dot(self.weights[i], node_outputs[i-1]))
            node_outputs.append(self.activation_function(node_inputs[i]))
            node_errors.append(None)

        # Find Error
        # Hidden to Output
        node_errors[len(node_errors)-1] = targets -  node_outputs[len(node_outputs)-1]
        # Input to Hidden
        for i in range(len(node_errors)-2, -1, -1):
            node_errors[i] = np.dot(self.weights[i+1].T,  node_errors[i+1])

        # Update Weights
        # Hidden to Output
        for i in range(len(self.weights)-1, 0, -1):
            self.weights[i] += self.lr * np.dot((node_errors[i] * node_outputs[i] * (1.0 - node_outputs[i])), np.transpose(node_outputs[i-1]))
        # Input to Hidden
        self.weights[0] += self.lr * np.dot((node_errors[0] * node_outputs[0] * (1.0 - node_outputs[0])), np.transpose(inputs))

    def query(self, inputs_list):
        inputs = np.array(inputs_list, ndmin=2).T
        node_inputs = [None,]
        node_outputs = [None,]

        # Solve
        # Input to Hidden
        node_inputs[0] = np.dot(self.weights[0], inputs)
        node_outputs[0] = self.activation_function(node_inputs[0])
        # Hidden to Final
        for i in range(1, len(self.weights)):
            node_inputs.append(np.dot(self.weights[i], node_outputs[i-1]))
            node_outputs.append(self.activation_function(node_inputs[i]))

        return node_outputs[len(node_outputs)-1]


'''
input_nodes = 3
hidden_height = 2
hidden_length = 2
output_nodes = 3

learning_rate = 0.3

network = neuralNetwork(input_nodes, hidden_height, hidden_length, output_nodes, learning_rate)

#print(output)
#print("")



for i in range(10000):
    y = random.randrange(1,101) / 100
    z = random.randrange(1,101) / 100
    if (z > y):
        network.train([y,random.randrange(1,101)/100,z], [0.99,0.01,0.01])
        network.train([z,random.randrange(1,101)/100,z], [0.01,0.99,0.01])
    elif (z == y):
        network.train([y,random.randrange(1,101)/100,z], [0.01,0.99,0.01])
    elif (z < y):
        network.train([z,random.randrange(1,101)/100,z], [0.01,0.99,0.01])
        network.train([y,random.randrange(1,101)/100,z], [0.01,0.01,0.99])

def find(array):
    if array[0] > array[1] and array[0] > array[2]:
        return "Move Up"
    elif array[1] > array[0] and array[1] > array[2]:
        return "Stay"
    elif array[2] > array[1] and array[2] > array[0]:
        return "Move Down"



output = network.query([0.75, 0.5, 1])
#print(output)
print(find(output))
output = network.query([0.5, 1, 0.5])
#print(output)
print(find(output))
output = network.query([1, 0.5, 0.75])
#print(output)
print(find(output))



'''