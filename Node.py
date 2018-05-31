from __future__ import division
from numpy import random
import numpy as np

"""
    node
"""


class Node(object):
    def __init__(self, ID, x, y, NodeFlag=0, status=0, sink=0):
        self.ID = ID  # ID of the node
        self.x = x  # position
        self.y = y  # position
        self.NodeFlag = NodeFlag  # 0 normal  1 fault   2 event
        self.sink = sink  # 0 not sink node   1 sink node
        self.status = status  # 0 may be in normal area  1 may be in event area
        # 2 Error may occur  3 Event detected  4 Error occurred
        self.last_status = 0
        self.neighbor_list = []  # list of references for neighbor nodes
        self.node_degree = 0  # number of neighbors

        # self.linksink_list = []                                # list of Nodes communicating with sink
        # self.sink_degree = 0                                   # number of Nodes communicating with sink

        self.normal_list = []  # Save N normal Historical Data

    def get_pos(self):  # return positions, DEPRECATED
        return self.x, self.y

    def neighbor_writer(self, neighbor):
        self.neighbor_list.append(neighbor)  # list of reference for neighbors node
        self.node_degree += 1  # increase neighbor number at each insertion

    def linksink_writer(self, linksink):
        self.linksink_list.append(linksink)  # list of reference for sink node
        self.sink_degree += 1

    def data_acquiste(self, NodeFlag=0):
        if (NodeFlag == 0 and self.NodeFlag == 0):
            return random.uniform(28, 30)
        elif (self.NodeFlag == 1):
            return random.uniform(30, 100)
        elif (NodeFlag == 2 and self.NodeFlag == 0):
            return random.normal(100, 10)

    # Fault Tolerant Algorithm
    def check_event(self, a, m, T, R, E, V, C, NodeFlag=0):
        """phase one-Upon detecting the occurrence of the event
        :param a:  Assumed thresholds for test conditions
        :param m:  Sampling times
        :param T:  Event duration
        :param R:  Reading threshold
        :param E:  Event expectations
        :param V:  Event Variance
        :param C:  Assumed thresholds for test conditions
        :param NodeFlag:
        :return: status
        """
        count = 0
        c = []
        r = self.data_acquiste(NodeFlag)  # t-moment node readings
        c.append(r)
        if r < (R + np.mean(c)) / 2:
            self.status = 0
            return self.status
        t = t1 = T / m  # sampling interval
        while t < T:
            # print(self.NodeFlag, r, (R + np.mean(c)) / 2, abs(r - np.mean(c) + E), a * (np.var(c) + V * V))
            if r > (R + np.mean(c)) / 2:  # statistical hypothesis test
                if abs(r - np.mean(c)) < a * (np.std(c) + V):
                    count += 1
            t += t1
            r = self.data_acquiste(NodeFlag)
            c.append(r)
        if count > C:
            self.status = 1
        else:
            self.status = 2
        return self.status


    # Spatio-Temporal algorithm

    def history_data(self, n):  # Save the most recent n data
        for i in range(n - len(self.normal_list)):
            self.normal_list.append(random.uniform(28, 30))

        return self.normal_list

    def confidence_intervals(self, data, t_value):  # Calculating confidence intervals
        # data.sort()
        n = len(data)
        med = np.median(data)
        min_interval = med - (np.std(data) / np.sqrt(n) * t_value) * np.sqrt(1 + n)
        max_interval = med + (np.std(data) / np.sqrt(n) * t_value) * np.sqrt(1 + n)
        # print(min_interval, max_interval)
        return min_interval, max_interval

    def check_event1(self, n, t_value, NodeFlag=0):
        normal_list = self.history_data(n)
        nmin_interval, nmax_interval = self.confidence_intervals(normal_list, t_value)
        val = self.data_acquiste(NodeFlag)
        if nmin_interval <= val <= nmax_interval:
            self.normal_list.pop(0)
            self.normal_list.append(val)
            self.status = 0
        else:
            self.status = 1
        return self.status

    def check_event2(self, n, t_value, NodeFlag=0):
        normal_list = self.history_data(n)
        min_interval, max_interval = self.confidence_intervals(normal_list, t_value)
        c = []
        val = self.data_acquiste(NodeFlag)
        c.append(val)
        t = t1 = 0.1
        if min_interval <= val <= max_interval:
            self.normal_list.pop(0)
            self.normal_list.append(val)
            self.status = 0
        else:
            total = 0
            while t < 1:
                # print((30 + np.mean(c)) / 2/(max_interval-min_interval))
                total += (val - max_interval) / (max_interval - min_interval)
                val = self.data_acquiste(NodeFlag)
                c.append(val)
                if c[-1] == c[-2]:
                    self.status = 2
                    return self.status
                t += t1
            if total / 10 < 1:
                self.status = 5
            elif total / 10 < (30 + np.mean(c)) / 2 / (max_interval - min_interval):
                self.status = 2
            else:
                self.status = 1
        return self.status



    def check_event3(self, n, t_value, NodeFlag=0):
        normal_list = self.history_data(n)
        min_interval, max_interval = self.confidence_intervals(normal_list, t_value)
        val = self.data_acquiste(NodeFlag)
        t = t1 = 0.1
        if min_interval <= val <= max_interval:
            self.normal_list.pop(0)
            self.normal_list.append(val)
            self.status = 0
        else:
            if (val - max_interval) / (max_interval - min_interval) < 1 or (val - min_interval) / (
                        max_interval - min_interval) < 1:
                self.status = 5

        return self.status


if __name__ == "__main__":
    node = Node(1, 10, 20, 1)
    """a, b = node.history_data(60)
    min_interval, max_interval = node.confidence_intervals(a, 2.000)
    k = node.data_acquiste(0)
    if min_interval < k < max_interval:
        print("True")
    else:
        print("False")
    print(k)"""
    for i in range(20):
        node.check_event1(30, 2.756)
