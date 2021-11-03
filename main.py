import numpy as np
import matplotlib.pyplot as plt
import math
import copy
#TODO ADD RR Scheduling (major changes only in run state)
#TODO MLFQ (major changes only in run state: three diff queues in run state RR5 RR10 FCFS)

# Creating the process data objects
class proccessListObj:
    def __init__(self, processDataList : np.ndarray, procName):
        self.processList = processDataList.copy()
        self.CPUBurst = -1
        if(self.CPUBurst == -1):
            self.CPUBurst = self.processList.pop(0)
        self.IOBurst = 0
        self.waitTime = 0
        self.startTime = -1
        self.endTime = -1
        self.TRTime = 0
        self.procName = procName

class queueObj:
    # Creating Queues as objects
    def __init__(self, choice, processObjList):
        self.choice = choice
        self.processObjList = copy.deepcopy(processObjList)
        self.qTime = 0
        self.clock = 0
        self.nonCPUUtil = 0
        self.readyQueue = []
        self.runQueue = []
        self.IOQueue = []
        self.avgWait = 0
        self.avgTRTime = 0
        self.avgResponseTime = 0
        self.actualCPUUtil = 0
        self.type = ""
        self.contextFlag = 1

        if choice == 0:
            # FCFS procedure
            self.type = "FCFS"
            self.populateFCFS()
            while len(self.runQueue) != 0 or len(self.IOQueue) != 0 or len(self.readyQueue) != 0:
                self.schedularFCFS()
            self.calcResults()
            self.printResults()
        elif choice == 1:
            # SJF procedure
            self.type = "SJF"
            self.populateSJF()
            while len(self.runQueue) != 0 or len(self.IOQueue) != 0 or len(self.readyQueue) != 0:
                self.schedularSJF()
            self.calcResults()
            self.printResults()
        elif choice == 2:
            # RR procedure
            print()
        elif choice == 3:
            # MLFQ procedure
            print()

    def printResults(self):
        print("\n===========================================================================")
        print(self.type, " CPU utilization: %", "%.2f" % self.actualCPUUtil, " Tw: ", self.avgWait, " Ttr: ",
              self.avgTRTime,
              " Tr: ", self.avgResponseTime)
        print("===========================================================================")

    def calcResults(self):
        for i in range(len(procObjList)):
            self.avgWait += self.processObjList[i].waitTime
            self.avgTRTime += self.processObjList[i].endTime - self.processObjList[i].startTime
            self.avgResponseTime += self.processObjList[i].startTime
        self.avgWait /= len(self.processObjList)
        self.avgTRTime /= len(self.processObjList)
        self.avgResponseTime /= len(self.processObjList)
        self.actualCPUUtil = (self.clock - self.nonCPUUtil)*100 / self.clock


    def populateFCFS(self):
        # FCFS Queue Object
        for i in range(len(self.processObjList)):
            self.readyQueue.append(self.processObjList[i])

    def populateSJF(self):
        #SJF Queue Object
        tmpObjList = copy.copy(self.processObjList)
        while len(self.readyQueue) < len(self.processObjList):
            minBurst = tmpObjList[0].CPUBurst
            x=0
            for i in range(len(tmpObjList)):
                if minBurst > tmpObjList[i].CPUBurst:
                    minBurst = tmpObjList[i].CPUBurst
                    x = i
            self.readyQueue.append(tmpObjList[x])
            tmpObjList.pop(x)


    def schedularSJF(self):
        current = []
        current.append(["==========================================================================="])
        current.append(["Current Execution Time: " + str(self.clock)])
        # Ready Queue Procedures
        current.append(["\nReady Queue:"])
        if self.clock == 300:
            print()
        # Changes CPU Burst from process list
        for i in range(len(self.readyQueue)):
            if self.readyQueue[i].CPUBurst == 0:
                self.readyQueue[i].CPUBurst = self.readyQueue[i].CPUBurst = self.readyQueue[i].processList.pop(0)
        # Checks if run que is empty and move first element in stack to run
        if len(self.runQueue) == 0 and len(self.readyQueue) != 0:
            self.runQueue.append(self.readyQueue.pop(0))
            self.contextFlag = 1
        # Adds wait time to each process in ready queue
        for i in range(len(self.readyQueue)):
            self.readyQueue[i].waitTime += 1
            current.append([str(self.readyQueue[i].procName) + " CPU Burst Time: " + str(self.readyQueue[i].CPUBurst)])

        # Run State Procedures
        if len(self.runQueue) != 0:
            if self.runQueue[0].CPUBurst == 0:
                if len(self.runQueue[0].processList) == 0:
                    self.runQueue[0].endTime = self.clock
                    self.runQueue.pop(0)
                    if len(self.readyQueue) != 0:
                        self.runQueue.append(self.readyQueue.pop(0))
                        self.contextFlag = 1
                else:
                    self.IOQueue.append(self.runQueue.pop(0))
                    if len(self.readyQueue) != 0:
                        self.runQueue.append(self.readyQueue.pop(0))
                        self.contextFlag = 1
        if len(self.runQueue) == 0:
            self.nonCPUUtil += 1
            current.append(["\nRunning process: None", " CPU Burst Time Remaining: N/A"])
        else:
            if self.runQueue[0].startTime == -1:
                self.runQueue[0].startTime = self.clock
            self.runQueue[0].CPUBurst -= 1
            current.append(["\nRunning process: " + str(
                self.runQueue[0].procName) + " CPU Burst Time Remaining: " + str(self.runQueue[0].CPUBurst + 1)])

        # IO Queue Procedures
        current.append(["\nI/O Queue:"])
        if self.clock == 527:
            print()
        IOQue = len(self.IOQueue)
        j = 0
        if self.clock == 107:
            print()
        while j < IOQue:
            self.IOQueue[j].IOBurst -= 1
            if self.IOQueue[j].IOBurst == -1:
                self.IOQueue[j].IOBurst = self.IOQueue[j].processList.pop(0)
            current.append([str(self.IOQueue[j].procName) + " IO Burst Time: " + str(self.IOQueue[j].IOBurst)])
            if self.IOQueue[j].IOBurst == 0:
                # Moves to ready queue after finishing IO burst
                x =0
                minBurst = self.IOQueue[j].processList[0]
                for i in range(len(self.readyQueue)):
                    if minBurst > self.readyQueue[i].CPUBurst:
                        x += 1
                self.readyQueue.insert(x,self.IOQueue.pop(j))
                self.readyQueue[x].CPUBurst = self.readyQueue[x].processList.pop(0)
                IOQue = len(self.IOQueue)
                j -= 1
            j += 1
        # One clock cycle ends here
        for i in range(len(current)):
            print(", ".join(current[i]))
        self.contextFlag = 0
        self.clock += 1

    def schedularFCFS(self):
        current = []
        current.append(["==========================================================================="])
        current.append(["Current Execution Time: "+ str(self.clock)])
        # Ready Queue Procedures
        current.append(["\nReady Queue:"])
        for i in range(len(self.readyQueue)):
            if self.readyQueue[i].CPUBurst == 0:
                self.readyQueue[i].CPUBurst = self.readyQueue[i].CPUBurst = self.readyQueue[i].processList.pop(0)
        if len(self.runQueue) == 0 and len(self.readyQueue) != 0:
            self.runQueue.append(self.readyQueue.pop(0))
            self.contextFlag = 1
        for i in range(len(self.readyQueue)):
            self.readyQueue[i].waitTime += 1
            current.append([str(self.readyQueue[i].procName)+ " CPU Burst Time: "+ str(self.readyQueue[i].CPUBurst)])

        # Run State Procedures
        if len(self.runQueue) != 0:
            if self.runQueue[0].CPUBurst == 0:
                if len(self.runQueue[0].processList) == 0:
                    self.runQueue[0].endTime = self.clock
                    self.runQueue.pop(0)
                    if len(self.readyQueue) != 0:
                        self.runQueue.append(self.readyQueue.pop(0))
                        self.contextFlag = 1
                else:
                    self.IOQueue.append(self.runQueue.pop(0))
                    if len(self.readyQueue) != 0:
                        self.runQueue.append(self.readyQueue.pop(0))
                        self.contextFlag = 1
        if len(self.runQueue) == 0:
            self.nonCPUUtil += 1
            current.append(["\nRunning process: None", " CPU Burst Time Remaining: N/A"])
        else:
            if self.runQueue[0].startTime == -1:
                self.runQueue[0].startTime = self.clock
            self.runQueue[0].CPUBurst -= 1
            current.append(["\nRunning process: "+ str(self.runQueue[0].procName)+ " CPU Burst Time Remaining: "+ str(self.runQueue[0].CPUBurst+1)])

        # IO Queue Procedures
        current.append(["\nI/O Queue:"])
        if self.clock == 527:
            print()
        IOQue = len(self.IOQueue)
        j = 0
        while j < IOQue:
            self.IOQueue[j].IOBurst -= 1
            if self.IOQueue[j].IOBurst == -1:
                self.IOQueue[j].IOBurst = self.IOQueue[j].processList.pop(0)
            current.append([str(self.IOQueue[j].procName)+ " IO Burst Time: "+ str(self.IOQueue[j].IOBurst)])
            if self.IOQueue[j].IOBurst == 0:
                self.readyQueue.append(self.IOQueue.pop(j))
                IOQue = len(self.IOQueue)
                j -= 1
            j += 1
        # One clock cycle ends here
        if self.contextFlag == 1:
            for i in range(len(current)):
                print(", ".join(current[i]))
        self.contextFlag = 0
        self.clock += 1


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
procObjList = []
for i in range(len(processDataList)):
    procName = "P"+str(i+1)
    procObjList.append(proccessListObj(processDataList[i],procName))

choice = 1#int(input("Enter 0:FCFC || 1:SJH || 2:RR  "))

# Creating queue process lists for different queues

TmpQue = queueObj(choice,procObjList)