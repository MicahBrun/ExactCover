# Micah Brown 2021
import numpy as np
import collections

def algorithmX(cover, reqLst = [], axis = 0):
    """
    Function takes a matrix representation of the cover problem, returns a list of sets that solve the problem.

    Parameters
    ------------------------
    cover : a numpy matrix representation of the cover problem, by default the sets are defined on the second index
    reqList : a list containing the indices of the sets that are required to exist in the final solution, is empty by default
    axis : defines which index coresponds to the sets and which to the elements, by default this is set to 0 meaning the sets are defined on the second index
    
    Returns
    ------------------------
    A list of the indices of the sets which solve to problem
    """

    if axis == 1:
        #If the axis is 0, the sets are defined on the second index, if 1, they are defined on the first
        cover = cover.transpose()

    numberOfEle, numberOfSets = cover.shape

    treeLoc = collections.deque([0]) #Will function as a stack with information on the order in the tree one is

    arrRemainingEle = np.arange(numberOfEle)
    arrRemainingSets = np.arange(numberOfSets)

    [arrRemainingEle, arrRemainingSets] = removeReq(cover, arrRemainingEle, arrRemainingSets, reqLst)

    treeArrs = [[arrRemainingEle,arrRemainingSets]] #Holds the remeining Elements and remaining Sets for each level of the tree, will work like a stack    
    
    treeSetsWithEle = collections.deque([]) #finds the index of the first row (element) with the lowest number of 1s
    setsWithEle = findMinIdxAndEle(cover, arrRemainingEle, arrRemainingSets)
    treeSetsWithEle.append(setsWithEle)

    finalListOfSets = collections.deque([])
    
    #if there are no more elements, so the sets cover all the elements, return the list of sets
    if treeArrs[-1][0].size == 0:
        return list(finalListOfSets)
    
    while 1:        

        #if the minimum number of 1s is 0 the problem isn't solved and we must go back up the tree
        if setsWithEle.size == 0:

            #goes through the tree, if all branches have been looked at it goes back up the tree until it can find a new branch
            for i in range(len(treeLoc)):
                if treeLoc[-1] < len(treeSetsWithEle[-1]) -1:
                    treeLoc[-1] = treeLoc[-1] +1
                    break
                treeLoc.pop()
                treeSetsWithEle.pop()
                treeArrs.pop()
                finalListOfSets.pop()
            
            setsWithEle = findMinIdxAndEle(cover, treeArrs[-1][0], treeArrs[-1][1])

        else: #if the minimum number of ones is not 0 continue onto the next level of Tree
            setIdx = treeSetsWithEle[-1][ treeLoc[-1] ] #Takes the matrix index of the set that we decided is in the solution
            finalListOfSets.append(setIdx)
            treeArrs.append( removeEleSet(cover, treeArrs[-1][0], treeArrs[-1][1], setIdx) )
            if treeArrs[-1][0].size == 0:
                return list(finalListOfSets)
            setsWithEle = findMinIdxAndEle(cover, treeArrs[-1][0], treeArrs[-1][1])
            treeSetsWithEle.append(setsWithEle)
            treeLoc.append(0)


def removeEleSet(cover, arrRemainingEle, arrRemainingSets, setIdx):
    #Performs the deletion part of Algorithm X which involves deleting all
    #elements that are in a set from our list as well as any set that contains these elements

    corEleWith1 = np.nonzero( cover[arrRemainingEle, setIdx] )[0] #for the given setIdx (column) finds all the elements that are in that set
    for ele in corEleWith1: #for each element that is in the set
        corSetWith1 = np.nonzero( cover[arrRemainingEle[ele],arrRemainingSets])[0] #find all the sets (columns) that contain this element
        arrRemainingSets = np.delete(arrRemainingSets, corSetWith1) #And delete them
    arrRemainingEle = np.delete(arrRemainingEle, corEleWith1) #Then remove all the elements (rows) that are in the set we chose

    return [arrRemainingEle, arrRemainingSets] #return the remaining Elements and Sets in an vector array

def findMinIdxAndEle(cover, arrRemainingEle, arrRemainingSets):
    #Count all the ones and find the first element with the lowest number of ones
    count1s = np.count_nonzero( cover[arrRemainingEle,:][:, arrRemainingSets] , axis = 1 )
    #take the index of this element
    min1sEleIdx = arrRemainingEle[np.argmin(count1s)]

    #Give a list of all the elements with this index
    setsWithEle = arrRemainingSets[np.nonzero(cover[min1sEleIdx,arrRemainingSets])[0]]

    return setsWithEle

def removeReq(cover, arrRemainingEle,arrRemainingSets, reqlist):

    for setIdx in reqlist:
        [arrRemainingEle, arrRemainingSets] = removeEleSet(cover, arrRemainingEle, arrRemainingSets, setIdx)
        _ = findMinIdxAndEle(cover, arrRemainingEle, arrRemainingSets)
    
    return [arrRemainingEle, arrRemainingSets]


