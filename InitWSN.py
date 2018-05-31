from __future__ import division
import random as rnd
import numpy as np
import math
from Node import *
from PlotWSN import *
import pickle

"""
    number_of_node : all number node of wsn
    length : length of wsn
    percentage_of_errornode : the percentage of the error node in all nodes (<1)
    distance : Communication distance
"""


def init_WSN(number_of_node=1024, length=32, percentage_of_errornode=0.1, distance=math.sqrt(2)):

    fault_num = int(number_of_node * percentage_of_errornode)    # number of error node (percentage of  all node)
    fnode_indexs = rnd.sample(range(0, number_of_node), fault_num)  # generation of random indices for fault node
    
    node_list = []                                               # list of references to node objects

    positions = np.zeros((number_of_node, 2))                    # matrix containing info on all node positions
    
  
    # -- NETWORK INITIALIZATION --
    #  nodes
    for i in range(number_of_node):            # for 0 to n indices
        x = rnd.uniform(0.0, length)         # random coordinate x
        y = rnd.uniform(0.0, length)         # random coordinate y
        node_list.append(Node(i, x, y, 0))    # create node
        positions[i, :] = [x, y]

    # Generation of fault nodes
    for i in fnode_indexs:                      # for on fault node position indices
        x, y = node_list[i].get_pos()
        node_list[i] = Node(i, x, y, 1)  # create fault node
        positions[i, :] = [x, y]

   
    # Find  neighbours using euclidean distance
    for i in range(number_of_node):           # cycle on all nodes
        dmax = distance * distance             # The square of the distance
        for j in range(number_of_node):       # compare each node with all the others
            x = positions[i, 0] - positions[j, 0]  # compute x distance between node i and node j
            y = positions[i, 1] - positions[j, 1]  # compute y distance between node i and node j
            dis = x * x + y * y                # compute distance square
            if dis <= dmax:                    # check if distance square is less or equal the max coverage dis
                if dis != 0:                   # avoid considering self node as neighbor
                    node_list[i].neighbor_writer(node_list[j])

   

    #output = open('wsn_0.1.pkl', 'wb')

    # Pickle dictionary using protocol 0.
    # pickle.dump(node_list, output)

    # Pickle the list using the highest protocol available.
    #pickle.dump(node_list, output, -1)

    #output.close()

    # Plot the network topology
    #print("Wait a moment, drawing the wsn.")
    #plot_WSN(node_list, number_of_node, fnode_indexs, length)

    return node_list

if __name__ == "__main__":
   node_list = init_WSN(400, 32, 0.1, math.sqrt(2))
