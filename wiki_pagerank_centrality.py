import settings
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from wiki_read_graph import get_labels, get_graph

def compute():
    edges, _ = get_graph()
    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    pagerank_centralities = nx.pagerank(graph)
    return pagerank_centralities