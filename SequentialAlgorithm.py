from __future__ import division
from InitWSN import *
import pickle


def confidence_intervals1(node_list, event_index, n, t_value):
    for i in range(len(node_list)):
        if i in event_index:
            status = node_list[i].check_event2(n, t_value, 2)
            if status == 1:
                node_list[i].last_status = 3
            elif status == 2:
                node_list[i].last_status = 4
            elif status == 5:
                node_list[i].last_status = 5
            else:
                node_list[i].last_status = 0

        else:
            status = node_list[i].check_event2(n, t_value)
            if status == 1:
                node_list[i].last_status = 3
            elif status == 2:
                node_list[i].last_status = 4
            elif status == 5:
                node_list[i].last_status = 5
            else:
                node_list[i].last_status = 0

    return node_list


def confidence_intervals(node_list, event_index, n, t_value):
    for i in range(len(node_list)):  # for each sensor
        if i in event_index:
            status = node_list[i].check_event1(n, t_value, 2)
        #else:
            #status = node_list[i].check_event(a, m, T, R, E, V, C)
            neighbor_list = node_list[i].neighbor_list
            count = 0
            if status == 1:
                if len(neighbor_list) != 0:
                    for j in range(len(neighbor_list)):                # broadcasting status to all neighbors
                        if neighbor_list[j].ID in event_index:
                            nstatus = neighbor_list[j].check_event1(n, t_value, 2)
                        elif neighbor_list[j].status == 0:
                            nstatus = neighbor_list[j].check_event1(n, t_value)
                        else:
                            nstatus = neighbor_list[j].check_event1(n, t_value)
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
            status = node_list[i].check_event1(n, t_value)
            neighbor_list = node_list[i].neighbor_list
            count = 0
            if status == 1:
                if len(neighbor_list) != 0:
                    for j in range(len(neighbor_list)):                # broadcasting status to all neighbors
                        if neighbor_list[j].status == 0:
                            nstatus = neighbor_list[j].check_event1(n, t_value)
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


def calculate_event2(node_list, event_index):
    # Event Area detection probability = Detected event sensors / Total sensor in the event area
    count = 0
    err = 0
    caerr = 0
    for i in event_index:
        if node_list[i].last_status == 3:
            count += 1
        if node_list[i].last_status == 4:
            err += 1
        if node_list[i].NodeFlag == 1:
            caerr += 1
    print("error:", err)
    print("totalerror:", caerr)
    print("evevnt:", count)
    print("total:", len(event_index))
    print("STA-Event:", count / len(event_index))
    return count / len(event_index)


def calculate_error2(node_list):
    count = 0
    e = 0
    for i in range(len(node_list)):
        if node_list[i].last_status == 4 and node_list[i].NodeFlag == 1:
            count += 1
        elif node_list[i].NodeFlag == 1:
            e += 1
    print("STA-Fault:", count / (e + count))
    return count / (e + count)


def event_detection_rate2(node_list, event_index):
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


def event_false_alarm_rate2(node_list, event_index):
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


def fault_detection_rate2(node_list):
    count = 0
    error = 0
    for i in range(len(node_list)):
        if node_list[i].last_status == 4 and node_list[i].NodeFlag == 1:
            count += 1
        if node_list[i].NodeFlag == 1:
            error += 1
    print("actual and check out fault node", count)
    print("actual fault node", error)
    print("fault detection rate:", count / error)
    return count / error


def fault_false_alarm_rate2(node_list):
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
    print("actual and check out fault node", count)
    print("check out fault node", check_error)
    print("false node", actual_error)
    print("false alarm  rate:", (check_error-count) / actual_error)
    return (check_error-count) / check_error


def error_false_recognition_rate(node_list):
    count = 0
    actual_error = 0
    for i in range(len(node_list)):
        if node_list[i].last_status == 5:
            count += 1
        if node_list[i].NodeFlag == 1:
            actual_error += 1
    print("check out error node", count)
    print("normal node", len(node_list)-actual_error)
    print("false alarm  rate:", count / (len(node_list)-actual_error))
    return count / (len(node_list)-actual_error)


def choice_sample():
    t = 0
    evdr = 0
    evfar = 0
    erdr = 0
    erfar = 0
    efrr = 0
    while t < 100:
        pkl_file = open('wsn_0.1.pkl', 'rb')
        node_list = pickle.load(pkl_file)
        pkl_file.close()
        # node_list = init_WSN(1024, 32, 0.05,  math.sqrt(2))
        x1 = 17
        y1 = 5
        x2 = 27
        y2 = 15
        n = 40
        t_value = 2.704
        event_index = event_Region(node_list, x1, y1, x2, y2)
        confidence_intervals1(node_list, event_index, n, t_value)
        evdr += event_detection_rate2(node_list, event_index)
        evfar += event_false_alarm_rate2(node_list, event_index)
        erdr += fault_detection_rate2(node_list)
        erfar += fault_false_alarm_rate2(node_list)
        efrr += error_false_recognition_rate(node_list)
        t += 1
    return evdr, evfar, erdr, erfar, efrr

if __name__ == "__main__":
    """pkl_file = open('efe_400.pkl', 'rb')
    node_list = pickle.load(pkl_file)
    pkl_file.close()
    #node_list = init_WSN(400, 32, 0.1,  math.sqrt(2))
    x1 = 17
    y1 = 5
    x2 = 27
    y2 = 15
    n = 30
    t_value = 2.756
    event_index = event_Region(node_list, x1, y1, x2, y2)
    confidence_intervals1(node_list, event_index, n, t_value)
    edr2 = event_detection_rate2(node_list, event_index)
    efar2 = event_false_alarm_rate2(node_list, event_index)
    fdr2 = fault_detection_rate2(node_list)
    ffar2 = fault_false_alarm_rate2(node_list)
    print(edr2, efar2)
    print(fdr2, ffar2)"""
    evdr, evfar, erdr, erfar, efrr = choice_sample()
    print("event_detection_rate:", evdr/100, "event_false_alarm_rate:", evfar/100)
    print("fault_detection_rate:", erdr/100, "fault_false_alarm_rate:", erfar/100)
    print("error_recognition_rate:", efrr / 100)
