import settings
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import mplcursors
from wiki_read_graph import get_labels, get_graph
import operator

def compute():
    edges, _ = get_graph()
    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    closeness_centralities = nx.closeness_centrality(graph)
    return closeness_centralities
