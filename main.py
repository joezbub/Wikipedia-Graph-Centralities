import settings
import numpy as np
import networkx as nx
import operator
import matplotlib.pyplot as plt
import mplcursors
import wiki_degree_centrality as degree_centrality
import wiki_pagerank_centrality as pagerank
import wiki_eigen_centrality as eigen_centrality
import wiki_katz_centrality as katz_centrality
from wiki_read_graph import get_labels, get_graph

def get_subgraph(edges, nodes):
    subgraph_edges = []
    nodes = set(nodes)
    for edge in edges:
        if edge[0] in nodes and edge[1] in nodes:
            subgraph_edges.append(edge)
    return subgraph_edges

def plot(graph, pos, all_centralities, title):
    centralities = [all_centralities[node] for node in graph]
    max_centrality = max(centralities)
    centralities = [centrality / max_centrality for centrality in centralities] # normalize
    nodes = nx.draw_networkx_nodes(graph, pos=pos, node_color=centralities, vmin=0, vmax=1, cmap=plt.cm.Reds, node_size=100)
    # nx.draw_networkx_labels(graph, pos, font_color='yellow')
    nx.draw_networkx_edges(graph, pos, edgelist=subgraph_edges, edge_color='black')

    def update_annot(sel):
        if sel == None:
            return
        node_index = sel.index
        node_name = list(graph.nodes)[node_index]
        text = labels[node_name] + " " + str(centralities[node_index])
        sel.annotation.set_text(text)

    cursor = mplcursors.cursor(nodes, hover=True)
    cursor.connect('add', update_annot)
    ax = plt.gca()
    ax.set_title(title)    
    plt.show()

def get_degree_stats(matrix):
    outdeg = np.matmul(matrix, np.ones(settings.N).transpose())
    indeg = np.matmul(matrix.transpose(), np.ones(settings.N).transpose())
    print(sorted(enumerate(outdeg), key=lambda x:x[1], reverse=True)[0:5])
    print(sorted(enumerate(indeg), key=lambda x:x[1], reverse=True)[0:5])

    plt.hist(outdeg, bins=25)
    plt.show()

    plt.hist(indeg, bins=25)
    plt.show()

settings.init()

labels = get_labels()
edges, matrix = get_graph()

# get_degree_stats(matrix)

pageranks = pagerank.compute()
eigen_centralities = eigen_centrality.compute()
katz_centralities = katz_centrality.compute()
degree_centralities = degree_centrality.compute()

subgraph_nodes = sorted(pageranks, key=pageranks.get, reverse=True)[:settings.subgraph_size]
subgraph_edges = get_subgraph(edges, subgraph_nodes)

graph = nx.DiGraph()
graph.add_nodes_from(subgraph_nodes)
graph.add_edges_from(subgraph_edges)
pos = nx.spring_layout(graph)

plot(graph, pos, pageranks, title="Pageranks")
plot(graph, pos, eigen_centralities, title="Eigenvector centralities")
plot(graph, pos, katz_centralities, title="Katz centralities")
plot(graph, pos, degree_centralities, title="Degree centralities")
