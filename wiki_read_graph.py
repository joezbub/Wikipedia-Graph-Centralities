import numpy as np
import settings

def get_labels():
    f = open(settings.labels_filename, 'r')
    labels = {}
    line_num = 0
    for x in f:
        labels[line_num] = x
        line_num += 1
    return labels

def get_graph():
    f = open(settings.graph_filename, 'r')
    edges = []
    for x in f:
        edges.append([int(x.split()[0]), int(x.split()[1])])
    edges = np.array(edges)
    matrix = np.zeros((settings.N, settings.N))
    matrix[edges[:,0], edges[:,1]] = 1
    return edges, matrix