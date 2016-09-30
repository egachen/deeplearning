import mnist_loader
from NN import *

training_data, validation_data, test_data = mnist_loader.load_data_wrapper()


def testBasicNN():
    myNN = NN([784, 30, 10])

    for j in range(30):
        myNN.feedDataSet(training_data)
        print("Basic NN with MNIST, round: %d, successful rate: %f" %\
             (j, myNN.evaluate(test_data)))

def main():
    testBasicNN()

if __name__ == "__main__":
    main()
