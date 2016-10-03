import numpy as np
import math

def vectorDist(v1, v2):
    """
    return distance between two vectors
    """
    return math.sqrt(np.sum((v1-v2)**2))

def splitDist(d1, d2):
    return abs(d1 - d2)

class KdNode:
    """
    The class for kd tree node
    """
    def __init__(self, vector, split, left=None, right=None):
        self.vector = np.array(vector)  #the actual vector for this node
        self.split = split   #init dimension value for split number
        self.left = left  # left tree 
        self.right = right   #right ree

class KdTree:
    """
    Construct a kd tree
    """
    def __init__(self):
        self.kdTree = None 

    def createKdTree(self, vectorList):
        """
        function to create kd tree, vectorList is the list of all vectors
        """
        if len(vectorList) == 0:
           return None

        if len(vectorList) == 1:
           return KdNode(vectorList[0], 0)

        # compute variance for each dimension, get the index of max variance
        vectorArr = np.array(vectorList)
        varList = [np.var(vectorArr[:,[x]]) for x in range(len(vectorList[0]))]
        split = np.argmax(varList)
        # sort with the order of dimension split
        vectorList.sort(key=lambda v:v[split])
        # find middle vector in the sorted list
        mid = len(vectorList)/2
        
        left = vectorList[:mid]
        if (mid+1) == len(vectorList):
            right = [] 
        else:
            right = vectorList[mid+1:]
        kdNode = KdNode(vectorList[mid], split)
        kdNode.left = self.createKdTree(left) 
        kdNode.right = self.createKdTree(right)
        return kdNode

    def searchKdTree(self, target):
        if self.kdTree is None:
            return None
        
        # init search
        kdNode = self.kdTree
        nearest = self.kdTree
        searchPath = []
        minDist = np.inf

        # loop untile kdNode is none
        while kdNode is not None:
            # append each node into search path for back search
            searchPath.append(kdNode)    

            nearestDist = vectorDist(nearest.vector, target)
            currentDist = vectorDist(kdNode.vector, target)
            # if current dist less than nearest dist, update
            if nearestDist > currentDist:
                nearest = kdNode
                minDist = currentDist

            split = kdNode.split
   
            # compare target dimenion s and current node dimension s
            if target[split] <= kdNode.vector[split]:
                kdNode = kdNode.left
            else:
                kdNode = kdNode.right             

        while searchPath:
            backPoint = searchPath.pop()
            kdNode = None 
            split = backPoint.split

            if splitDist(target[split], backPoint.vector[split]) < minDist:
                # if minDist is less than the distance between s dimension of 
                # target and backpoint, that means we should check right/left tree
                if target[split] <= backPoint.vector[split]:
                    kdNode = backPoint.right
                else:
                    kdNode = backPoint.left 

            if kdNode is None:
                continue

            # add this node into search path since it might be a new path
            searchPath.append(kdNode)
            currentDist = vectorDist(kdNode.vector, target)
            if minDist > currentDist:
                 nearest = kdNode
                 minDist = currentDist 

        return nearest, minDist

def testKdTree():
    testData = [[2,3], [5,4], [9,6], [4,7], [8,1],[7,2]]
    kd = KdTree()
    kd.kdTree = kd.createKdTree(testData)
    print("Try to search =========")
    print(kd.searchKdTree([2.1, 4.5]).vector)
