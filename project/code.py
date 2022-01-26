#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 14:02:49 2021

@author: 3679695
"""
#%%
from random import randint, uniform
import networkx as nx
import matplotlib.pyplot as plt
def add_link(my_link, my_graph):
    '''
    add_link((node1, node2), my_graph)
    
    Add the link ('node1', 'node2') in the graph 'my_graph'
        Parameters:
            (node1, node2) (int, int) : the link  that will be added
            my_graph (dictionary of lists) : the graph that will contain the link
        Returns:    
    '''
    node1, node2 = my_link
    if node1 in my_graph:
        my_graph[node1].append(node2)
    else:
        my_graph[node1] = [node2]
    if node2 in my_graph:
        my_graph[node2].append(node1)
    else:
        my_graph[node2] = [node1]
    return

def erdos(node_count, link_count):
    '''
    erdos(node_count, link_count)
    
    Generates a graph with 'node_count' nodes and 'link_count' links
        Parameters:
            node_count (int)
            link_count (int)
        Returns:
            my_graph (dictionary of lists) : 
    '''
    my_graph = {}
    for node in range(node_count):
        my_graph[node] = []
    current_link_count = 0
    while current_link_count <= link_count:
        node1 = randint(0, node_count -1)
        node2 = randint(0, node_count -1)
        link_exists = node1 in my_graph and node2 in my_graph
        link_exists = link_exists and node1 in my_graph[node2] # node 1 is a neighbour of node 2
        link_exists = link_exists and node2 in my_graph[node1] # node 2 is a neighbour of node 1
        if not link_exists:
            add_link((node1, node2), my_graph)
            current_link_count += 1
    return my_graph

import copy
def sum_degree(my_graph):
    '''
    sum_degree(my_graph)
    
    Compute the sum of the degree of the nodes in the graph 'my_graph'
        Parameters:
            my_graph (dictionary of lists)
        Returns:
            my_sum_degree (int) : the sum of the degree of the nodes
    '''
    my_sum_degree = 0
    for node in my_graph:
        my_sum_degree += len(my_graph[node])
    return my_sum_degree
def barabasi(graph_size, my_graph, alpha):
    '''
    barabasi(graph_size, base_graph, alpha)
    
    Generates a Barabasi-Albert graph starting with the graph 'base_graph' and adding nodes until
    the graph's size equal to 'graph_size'. The added nodes should have degree equal to 'alpha'
        Parameters:
            graph_size (int) : the size of the graph that will be generated
            base_graph (dictionary of list): the graph that will be used as the base
            alpha (int): the degree of the nodes that will be added
        Returns
    '''
    base_graph = copy.deepcopy(my_graph)
    origin_size = len(base_graph)
    for new_node in range(origin_size + 1, graph_size + 1):
        
       # print(f"\r Loading the barabasi graph : {new_node} / {graph_size}",end = "", flush = True)
        node_odd = []
        my_sum_degree = sum_degree(base_graph)
        cumul = 0
        for node in base_graph: # Compute the odds for each node to be linked to the new node
            cumul += len(base_graph[node]) / my_sum_degree
            node_odd.append((node, cumul))
        base_graph[new_node] = [] # New node added to graph
        degree_new_node = 0
        while degree_new_node < alpha:
            tmp = uniform(0,1)
            neighbour_node = None
            for (node, odd) in node_odd:
                if tmp < odd:
                    neighbour_node = node
                    break
            link_exist = neighbour_node in base_graph[new_node] and new_node in base_graph[neighbour_node] 
            if not link_exist:
                add_link((new_node, neighbour_node), base_graph)
                degree_new_node += 1
    return base_graph
def bfs_modified(my_graph):
   
    my_cc = {}
    cc_index = 0
    for source in my_graph.keys():
        if source not in my_cc:
            my_queue = [source]
            marked_node = [source]
            while my_queue:
                node1 = my_queue.pop(0)
                my_cc[node1] = cc_index
                for node2 in my_graph[node1]:
                    if node2 not in marked_node:
                        my_queue.append(node2)
                        marked_node.append(node2)
            cc_index += 1
    
    cc_sets = {}
    for node in my_cc:
        cc_index = my_cc[node]
        if cc_index in cc_sets:
            cc_sets[cc_index].add(node)
        else:
            
            cc_sets[cc_index] = {node}
    cc_max = 0
    for cc_index in cc_sets:
        if len(cc_sets[cc_index]) >= len(cc_sets[cc_max]):
            cc_max = cc_index
    return cc_sets[cc_max]

def si_model(lcc, my_graph, p):
    '''
    Return a dictionary representing the evolution of the number of
    infected according to the number of steps
        Parameters:
            lcc (set) : A set containing all the nodes of the largest component connected
            my_graph (dictionary of lists) : the graph
            p (float) : probability of infection
        Returns:
            my_evolution (dictionary)
    '''
    max_infected = len(lcc)
    infecteds = {lcc.pop()}
    step = 0
    my_evolution = {step : len(infecteds)}
    while len(infecteds) < max_infected:
        step += 1
        new_infected = set()
        for infected in infecteds:
            for neighbour in my_graph[infected]:
                tmp = uniform(0,1)
                if tmp < p:
                    new_infected.add(neighbour)
        infecteds = infecteds.union(new_infected)
        my_evolution[step] = len(infecteds)
    return my_evolution
def visualize(graph, file):
    my_graph = nx.Graph()
    for node in graph:
        for neighbour in graph[node]:
            my_graph.add_edge(node, neighbour)
    nx.draw(my_graph, node_size = 50)
    plt.savefig(file)
if __name__ == "__main__":
    print("start")
    erdos_graph = erdos(5,2)
    n_barabasi = 30
    my_barabasi1 = barabasi(n_barabasi, erdos_graph, 1)
    #my_barabasi2 = barabasi(n_barabasi, erdos_graph, 2)
    #my_barabasi3 = barabasi(n_barabasi, erdos_graph, 20)
    p = 0.01
    barabasi_list = []
    x = []
    y = []
    for i in range(1,1, 1):
        my_barabasi = barabasi(n_barabasi, erdos_graph, i)
        barabasi_list.append(my_barabasi)
        barabasi_evolution = si_model(bfs_modified(my_barabasi), my_barabasi, p)
        #print("i", i, " ; Time used" , max(barabasi_evolution.keys()))
        x.append(i)
        y.append(max(barabasi_evolution.keys()))
        #plt.plot(barabasi_evolution.keys(), barabasi_evolution.values(), label = i)
        #plt.xlabel("time")
        #plt.ylabel("nodes infected")
        #plt.legend()
    '''plt.xlabel("alpha")
    plt.ylabel("time to infect all nodes")
    plt.scatter(x,y)'''
        


    
    #visualize(erdos_graph, 'erdos.png')
    visualize(my_barabasi1, 'barabasi.png')