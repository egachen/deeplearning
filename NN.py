"""
Neural Network , it's a generic neural network class, the layers number and size can be defined
It's an exercise from https://iamtrask.github.io/2015/07/12/basic-python-network/
"""
import numpy as np

def sigmoid(inX):
    return 1/(1 + np.exp(-inX))
    
def derivative(inX):
    return inX*(1 - inX)
    
class NN:
    def __init__(self, NNSize):
        self.NNSize = NNSize    
        self.weightsList = []
        self.alpha = 0.3 
        self.setupNN()
    
    def setupNN(self):
        """
        Initial NN stucture, currently, only weight list
        """
        for i in range(len(self.NNSize)-1):
            np.random.seed(1)
            # add a bais node for each layer except output layer
            # refer to https://www.quora.com/In-artificial-neural-networks-what-actually-is-bias-unit
            # the weights matrix will be like [n+1,m]
            weights = 2*np.random.random((self.NNSize[i] + 1, self.NNSize[i+1])) - 1
            self.weightsList.append(weights)
        
    def feedDataSet(self, dataMat):
        """
        adapt input dataset and feed it into NN
        """
        for index,data in enumerate(dataMat):
            X = np.array(data[0]).T
            Y = np.array(data[1]).T
            self.train(X, Y)


    def predict(self, inX, layerList):
        """
        feed input inX into NN, and get output in layerList
        """
        # add one bais node for input layer
        inX = np.append(inX, [[1]], 1)
        layerList[0] = inX
        for i in range(len(self.NNSize)-1):
            # 1. get weights between layers
            weights = self.weightsList[i]         
            # 2. multiply input layer and weights
            layerList[i+1] =  sigmoid(inX.dot(weights))
            # 3. add a bais node
            if (i+1) < (len(self.NNSize) - 1):
                layerList[i+1] = np.append(layerList[i+1], [[1]], 1)
            inX = layerList[i+1]

    def evaluate(self, testData):
        """
        evaluate the trained NN; input testData and get successful rate
        """
        success = 0
        for x,y in testData:
           x = x.T
           # add bias node
           x = np.append(x, [[1]], 1)
           for i in range(len(self.NNSize)-1):
               weights = self.weightsList[i]
               x = sigmoid(x.dot(weights))
               if i < len(self.NNSize) - 2:
                   x = np.append(x, [[1]], 1)
           if np.argmax(x) == y:
              success += 1
        return success/float(len(testData))
    
        
    def train(self, X, Y):
        """
        train NN with input X, at first it use predict() to feed forward
        then, it use backpropagate to update weights
        """
        layerList = []
        for i in range(len(self.NNSize)):
            layerList.append(X)
        # forward
        self.predict(X, layerList)

        # backward
        inError = Y - layerList[-1]
        for i in range(len(layerList)-1, 0, -1):
            delta = self.alpha*inError*derivative(layerList[i])
            if i < len(layerList) - 1:
                # remove bias node from delta because no input for bias node when forward
                delta = np.delete(delta, -1, 1)
            inError = delta.dot(self.weightsList[i-1].T)
            self.weightsList[i-1] += layerList[i-1].T.dot(delta)

        return layerList
