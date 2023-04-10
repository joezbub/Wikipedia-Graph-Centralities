import settings
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import mplcursors
from wiki_read_graph import get_labels, get_graph
import operator
import scipy

def compute():
    edges, matrix = get_graph()
    _, vec = scipy.sparse.linalg.eigs(-matrix.transpose(), k = 1)
    normalizedVec = vec / sum(vec)
    return {k: v for k, v in enumerate(normalizedVec)}
    

