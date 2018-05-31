# coding=utf-8
from __future__ import division

import matplotlib

from FaultTolerantAlgorithm import *
from SequentialAlgorithm import *
import math
import matplotlib.pyplot as plt
import pickle


def reset(node_list):
    for i in range(len(node_list)):
        node_list[i].status = 0
        node_list[i].last_status = 0
    return node_list


def comparison_algorithm():
    sevcor = []                    # Sequential algorithm event check out rate
    sevfar = []                    # Sequential algorithm event false alarm rate
    fevcor = []
    fevfar = []
    sercor = []                    # Sequential algorithm error check out rate
    serfar = []                    # Sequential algorithm error false alarm rate
    fercor = []
    ferfar = []
    ratio = [0.05, 0.1, 0.15, 0.2, 0.25]
    #ratio = [300, 400, 500, 600, 700, 800, 900, 1024]
    file_name = ["wsn_0.05.pkl", "wsn_0.1.pkl", "wsn_0.15.pkl", "wsn_0.2.pkl", "wsn_0.25.pkl"]
    #file_name = ["wsn_300.pkl", "wsn_400.pkl", "wsn_500.pkl", "wsn_600.pkl", "wsn_700.pkl", "wsn_800.pkl", "wsn_900.pkl", "wsn_1024.pkl"]
    for i in range(len(file_name)):
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
        number_of_node = 1024
        length = 32
        distance = math.sqrt(2)
        pkl_file = open(file_name[i], 'rb')
        node_list = pickle.load(pkl_file)
        pkl_file.close()
        #node_list = init_WSN(number_of_node, length, ratio[i], distance)
        event_index = event_Region(node_list, x1, y1, x2, y2)
        event_Region_Detection(node_list, a, m, T, R, E, V, C, event_index)

        fevent = event_detection_rate1(node_list, event_index)
        fevcor.append(fevent)
        ferr = event_false_alarm_rate1(node_list, event_index)
        fevfar.append(ferr)

        fevent = fault_detection_rate1(node_list)
        fercor.append(fevent)
        ferr = fault_false_alarm_rate1(node_list)
        ferfar.append(ferr)

        node_list = reset(node_list)

        n = 30                                         # 20  2.11
        t_value = 2.756                                 # 30  2.756
        confidence_intervals(node_list, event_index, n, t_value)

        sevent = event_detection_rate2(node_list, event_index)
        sevcor.append(sevent)
        serr = event_false_alarm_rate2(node_list, event_index)
        sevfar.append(serr)

        sevent = fault_detection_rate2(node_list)
        sercor.append(sevent)
        serr = fault_false_alarm_rate2(node_list)
        serfar.append(serr)

    return fevcor, fevfar, fercor, ferfar, sevcor, sevfar, sercor, serfar, ratio


if __name__ == "__main__":
    fevcor100, fevfar100, fercor100, ferfar100, sevcor100, sevfar100, sercor100, serfar100 = [], [], [], [], [], [], [], []
    for i in range(100):
        fevcor, fevfar, fercor, ferfar, sevcor, sevfar, sercor, serfar, ratio = comparison_algorithm()
        fevcor100.append(fevcor)
        fevfar100.append(fevfar)
        fercor100.append(fercor)
        ferfar100.append(ferfar)
        sevcor100.append(sevcor)
        sevfar100.append(sevfar)
        sercor100.append(sercor)
        serfar100.append(serfar)

    fevcor1, fevfar1, fercor1, ferfar1, sevcor1, sevfar1, sercor1, serfar1 = [], [], [], [], [], [], [], []
    for i in range(len(fevcor100[0])):
        sfevcor, sfevfar, sfercor, sferfar, ssevcor, ssevfar, ssercor, sserfar = 0, 0, 0, 0, 0, 0, 0, 0
        for j in range(100):
            #print(fevcor100[j][i])
            sfevcor += fevcor100[j][i]
            sfevfar += fevfar100[j][i]
            sfercor += fercor100[j][i]
            sferfar += ferfar100[j][i]
            ssevcor += sevcor100[j][i]
            ssevfar += sevfar100[j][i]
            ssercor += sercor100[j][i]
            sserfar += serfar100[j][i]
        fevcor1.append(sfevcor/100)
        fevfar1.append(sfevfar/100)
        fercor1.append(sfercor/100)
        ferfar1.append(sferfar/100)
        sevcor1.append(ssevcor/100)
        sevfar1.append(ssevfar/100)
        sercor1.append(ssercor/100)
        serfar1.append(sserfar/100)

    fevcor, fevfar, fercor, ferfar, sevcor, sevfar, sercor, serfar, ratio = comparison_algorithm()
    # Plot Event probability detection chart
    zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simkai.ttf')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(ratio, fevcor1, color='black', linestyle='-', marker='o', label="文献[13]方法")
    ax.plot(ratio, sevcor1, color='black', linestyle='-', marker='*', label="本文方法")
    #ax.set_ylim([-1.2, 1.2])
    plt.legend()
    plt.title('Event Node Checkout Rate diagram')
    plt.xlabel('Percentage of fault sensor')
    #plt.xlabel('The number of sensor')
    plt.ylabel('ETPR(%)')
    plt.legend(prop=zhfont1)
    #plt.savefig("rate_ETPR.png", dpi=500, bbox_inches='tight')
    #plt.savefig("number_ETPR.png", dpi=500, bbox_inches='tight')
    plt.show()
    #plt.cla()
    #plt.clf()
    #plt.close()


    # Draw sensor Error Identification rate chart
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(ratio, fevfar1, color='black', linestyle='-', marker='o', label="文献[13]方法")
    ax.plot(ratio, sevfar1, color='black', linestyle='-', marker='*', label="本文方法")
    plt.legend()
    plt.title('Event Node False Alarm Rate diagram')
    plt.xlabel('Percentage of fault sensor')
    #plt.xlabel('The number of sensor')
    plt.ylabel('EFPR(%)')
    plt.legend(prop=zhfont1)
    #plt.savefig("rate_EFPR.png", dpi=500, bbox_inches='tight')
    #plt.savefig("number_EFPR.png", dpi=500, bbox_inches='tight')
    plt.show()
    #plt.cla()
    #plt.clf()
    #plt.close()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(ratio, fercor1, color='black', linestyle='-', marker='o', label="文献[13]方法")
    ax.plot(ratio, sercor1, color='black', linestyle='-', marker='*', label="本文方法")
    # ax.set_ylim([-1.2, 1.2])
    plt.legend()
    plt.title('Fault Node Checkout Rate diagram')
    plt.xlabel('Percentage of fault sensor')
    #plt.xlabel('The number of sensor')
    plt.ylabel('FTPR(%)')
    plt.legend(prop=zhfont1)
    #plt.savefig("rate_FTPR.png", dpi=500, bbox_inches='tight')
    #plt.savefig("number_FTPR.png", dpi=500, bbox_inches='tight')
    plt.show()
    #plt.cla()
    #plt.clf()
    #plt.close()


    # Draw sensor Error Identification rate chart
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(ratio, ferfar1, color='black', linestyle='-', marker='o', label="文献[13]方法")
    ax.plot(ratio, serfar1, color='black', linestyle='-', marker='*', label="本文方法")
    plt.legend()
    plt.title('Fault Node False Alarm Rate diagram')
    plt.xlabel('Percentage of fault sensor')
    #plt.xlabel('The number of sensor')
    plt.ylabel('FFPR(%)')
    plt.legend(prop=zhfont1)
    #plt.savefig("rate_FFPR.png", dpi=500, bbox_inches='tight')
    #plt.savefig("rate_FFPR.png", dpi=500, bbox_inches='tight')
    plt.show()
    #plt.cla()
    #plt.clf()
    #plt.close()
