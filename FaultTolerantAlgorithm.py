from __future__ import division
from InitWSN import *

"""
    This algorithm is proposed by Cao Dong-lei in
    <A Fault-Tolerant Algorithm for Event Region Detection in Wireless Sensor Network>
"""


def event_Region_Detection(node_list, a, m, T, R, E, V, C, event_index):
    for i in range(len(node_list)):  # for each sensor
        if i in event_index:
            status = node_list[i].check_event(a, m, T, R, E, V, C, 2)
        #else:
            #status = node_list[i].check_event(a, m, T, R, E, V, C)
            count = 0
            neighbor_list = node_list[i].neighbor_list
            if status == 1:
                if len(neighbor_list) != 0:
                    for j in range(len(neighbor_list)):                # broadcasting status to all neighbors
                        if neighbor_list[j].ID in event_index:
                            nstatus = neighbor_list[j].check_event(a, m, T, R, E, V, C, 2)
                        elif neighbor_list[j].status == 0:
                            nstatus = neighbor_list[j].check_event(a, m, T, R, E, V, C)
                        else:
                            nstatus = neighbor_list[j].status
                        if nstatus == 1:
                            count += 1

            if count >= len(neighbor_list) / 2:
                if status == 0:
                    node_list[i].last_status = 4
                else:
                    node_list[i].last_status = 3
            else:
                if status != 0:
                    node_list[i].last_status = 4

        else:
            status = node_list[i].check_event(a, m, T, R, E, V, C)
            neighbor_list = node_list[i].neighbor_list
            count = 0
            if status == 1:
                if len(neighbor_list) != 0:
                    for j in range(len(neighbor_list)):                # broadcasting status to all neighbors
                        if neighbor_list[j].status == 0:
                            nstatus = neighbor_list[j].check_event(a, m, T, R, E, V, C)
                        else:
                            nstatus = neighbor_list[j].status
                        if nstatus == 1:
                            count += 1

            if count >= len(neighbor_list) / 2:
                if status == 0:
                    node_list[i].last_status = 4
                else:
                    node_list[i].last_status = 3
            else:
                if status != 0:
                    node_list[i].last_status = 4



    return node_list


# Event Area
def event_Region(node_list, x1, y1, x2, y2):   # x1 < x2   y1 < y2
    event_index = []
    for i in range(len(node_list)):
        x, y = node_list[i].get_pos()
        if x1 <= x <= x2 and y1 <= y <= y2:
            event_index.append(i)
    return event_index


def calculate_event1(node_list, event_index):
    # Event Area detection probability = Detected event sensors / Total sensor in the event area
    count = 0
    for i in event_index:
        if node_list[i].last_status == 3:
            count += 1
    print("FTA-Event:", count / len(event_index))
    return count / len(event_index)


def calculate_error1(node_list):
    count = 0
    e = 0
    for i in range(len(node_list)):
        if node_list[i].last_status == 4 and node_list[i].NodeFlag == 1:
            count += 1
        elif node_list[i].NodeFlag == 1:
            e += 1
    print("FTA-Fault:", count / (e + count))
    return count / (e + count)


def event_detection_rate1(node_list, event_index):
    count = 0
    error = 0
    for i in event_index:
        if node_list[i].last_status == 3 and node_list[i].NodeFlag == 0:
            count += 1
        if node_list[i].NodeFlag == 1:
            error += 1
    print("actual and check out event node", count)
    print("actual error node", error)
    print("event total node", len(event_index))
    print("event detection rate:", count / (len(event_index)-error))
    return count / (len(event_index)-error)


def event_false_alarm_rate1(node_list, event_index):
    event = 0
    count = 0
    error = 0
    for i in event_index:
        if node_list[i].last_status == 3 and node_list[i].NodeFlag == 0:
            count += 1
        if node_list[i].NodeFlag == 1:
            error += 1
        if node_list[i].last_status == 3:
            event += 1
    print("actual and check out event node", count)
    print("check out event node", event)
    print("error node", error)
    print("event total node", len(event_index))
    print("false alarm  rate:", (event-count) / (len(event_index) - error))
    return (event-count) / (len(event_index) - error)


def fault_detection_rate1(node_list):
    count = 0
    error = 0
    for i in range(len(node_list)):
        if node_list[i].last_status == 4 and node_list[i].NodeFlag == 1:
            count += 1
        if node_list[i].NodeFlag == 1:
            error += 1
    print("actual and check out error node", count)
    print("actual error node", error)
    print("error detection rate:", count / error)
    return count / error


def fault_false_alarm_rate1(node_list):
    check_error = 0
    count = 0
    actual_error = 0
    for i in range(len(node_list)):
        if node_list[i].last_status == 4 and node_list[i].NodeFlag == 1:
            count += 1
        if node_list[i].NodeFlag == 1:
            actual_error += 1
        if node_list[i].last_status == 4:
            check_error += 1
    print("actual and check out error node", count)
    print("check out error node", check_error)
    print("error node", actual_error)
    print("false alarm  rate:", (check_error-count) / actual_error)
    return (check_error-count) / check_error


if __name__ == "__main__":
    node_list = init_WSN(1024, 32, 0.25,  math.sqrt(2))  # a, m, T, R, E, V, C, x1, y1, x2, y2
    a = 1.96
    m = 10
    T = 1.0
    R = 30
    E = 100
    V = 10
    C = 8
    x1 = 17
    y1 = 5
    x2 = 27
    y2 = 15
    event_index = event_Region(node_list, x1, y1, x2, y2)
    node_list = event_Region_Detection(node_list, a, m, T, R, E, V, C, event_index)
    event = event_detection_rate1(node_list, event_index)
    err = fault_detection_rate1(node_list)
    print(event, err)
