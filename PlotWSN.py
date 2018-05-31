import matplotlib.pyplot as plt
import numpy as np



########################################################################################################################
# This function can be used to plot the random graph, normal nodes and their edges will be shows as grey dots and lines.
# error nodes and their edges will be shown as red dots and lines.
# sink nodes and their edges will be shown as green dots and lines.
########################################################################################################################

def plot_WSN(node_list, number_of_node, fnode_indexs, length):
    ii = -1
    x1 = np.zeros(number_of_node)
    y1 = np.zeros(number_of_node)

    #plt.figure(figsize=(length, length))

    for i in range(number_of_node):
        ii += 1
        x1[ii] = node_list[i].x
        y1[ii] = node_list[i].y
        """for iii in xrange(node_list[i].node_degree):
            #color = '#eeefff'
            xx = [node_list[i].x, node_list[i].neighbor_list[iii].x]
            yy = [node_list[i].y, node_list[i].neighbor_list[iii].y]
            plt.plot(xx, yy, color='grey')"""

    x2 = np.zeros(len(fnode_indexs))
    y2 = np.zeros(len(fnode_indexs))
    ii = -1
    for i in fnode_indexs:
        ii += 1
        x2[ii] = node_list[i].x
        y2[ii] = node_list[i].y
        """for iii in xrange(node_list[i].node_degree):
            xx = [node_list[i].x, node_list[i].neighbor_list[iii].x]
            yy = [node_list[i].y, node_list[i].neighbor_list[iii].y]
            plt.plot(xx, yy, color='grey')"""

    """x3 = np.zeros(len(enode_indexs))
    y3 = np.zeros(len(enode_indexs))
    ii = -1
    for i in enode_indexs:
        ii += 1
        x3[ii] = node_list[i].x
        y3[ii] = node_list[i].y"""

    fig = plt.figure(figsize=(length, length))
    ax = fig.add_subplot(111)
    ax.plot(x1, y1, color='k', linestyle='', marker='1', markersize=10.0, markeredgewidth=1.0, label="normal")
    ax.plot(x2, y2, color='k', linestyle='', marker='o', markersize=10.0, markeredgewidth=1.0,
    markerfacecolor='k', markeredgecolor='black', label="fault")
    #ax.plot(x3, y3, color='green', linestyle='', marker='o', markersize=10.0, markeredgewidth=1.0,
    #         markerfacecolor='green', markeredgecolor='black', label="error")
    plt.title('Sensor Network')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.xlim(-0.5, length*1.05)
    plt.ylim(-0.5, length*1.05)
    #plt.savefig("wsn_400.png", dpi=300, bbox_inches='tight')
    #plt.cla()
    #plt.clf()
    #plt.close()
    plt.show()


