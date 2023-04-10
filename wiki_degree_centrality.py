import settings
import numpy as np
from wiki_read_graph import get_labels, get_graph

def compute():
    _, matrix = get_graph()
    indeg = np.matmul(matrix.transpose(), np.ones(settings.N).transpose())
    return {k: v for k, v in enumerate(indeg)}
