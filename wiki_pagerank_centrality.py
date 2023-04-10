import settings
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import mplcursors
from wiki_read_graph import get_labels, get_graph
import operator

def compute():
    labels = get_labels()
    edges, matrix = get_graph()
    outdeg = np.matmul(matrix, np.ones(settings.N).transpose())

    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    pagerank_centralities = nx.pagerank(graph)
    return pagerank_centralities
# pos = nx.spring_layout(graph)

