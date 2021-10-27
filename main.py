import numpy as np
import matplotlib.pyplot as plt
import math

# Importing process data into arrays
P1 =[5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 5]
P2 =[4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8]
P3 =[8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6]
P4 =[3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3]
P5 =[16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4]
P6 =[11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8]
P7 =[14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10]
P8 =[4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6]

processDataList = [P1,P2,P3,P4,P5,P6,P7,P8]

# Creating the process data objects
class proccessObj:
    def __init__(self, proccessList : np.ndarray):
        self.processList = proccessList
        self.CPUBurst = self.processList[0]
        self.IOBurst = 0
        self.waitTime = 0
        self.TRTime = 0

# Creating Queues as objects
class queueObj:
    def __init__(self, choice):
        self.choice = choice
        self.qTime = 0
        self.readyQueue = []
        self.runQueue = []
        self.IOQueue = []
        self.createQue()

    def createQue(self):
        queType = choice
        # FCFS Queue Object
        if(queType == 0):
           print("test")

        def fillReadyQue(self, processDataList):
            FCFSProcceses = []
            for i in range(len(processDataList)):
                FCFSProcceses.append(proccessObj(processDataList[i]))

            for i in range(len(FCFSProcceses)):
                print(FCFSProcceses[i].processList[0])

choice = int(input("Enter 0:FCFC || 1:SJH || 2:RR  "))
FCFSQue = queueObj(choice)
