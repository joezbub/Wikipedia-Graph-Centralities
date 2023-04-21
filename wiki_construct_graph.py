import numpy as np
import requests
import re
from functools import lru_cache

N = 1000
root = 'https://en.wikipedia.org/wiki/Complex_system'
prefix = 'https://en.wikipedia.org'

@lru_cache
def get_real_url(url):
    """
    Recursively requests url to get real url after redirects
    """
    r = requests.get(url)
    s = r.text
    link_section = re.search("<link rel=\"canonical\" href=\"(.*?)\"/>", s)
    ret = link_section.group(1)
    if "#" in ret:
        ret = get_real_url(ret[:ret.index("#")])
    return ret

def extract_link_section(url):
    """
    Find "See also" section of article in the HTML
    """
    r = requests.get(url)
    s = r.text

    see_also = re.search("id=\"See_also\"(.|\n)", s)
    if not see_also:
        return ""
    start = see_also.end()
    s = s[start:]

    table_ind = re.search("<table>", s)
    ul_ind = re.search("<ul>", s)

    if table_ind and table_ind.start() < ul_ind.start(): # Table formatted
        s = s[table_ind.end():]
        start_pos = re.search("<ul>", s).end()
        end_pos = re.search("</table>", s).start()
        s = s[start_pos:end_pos]
    else: # ul formatted
        start_pos = ul_ind.end()
        s = s[start_pos:]
        end_pos = re.search("</ul>", s).start()
        s = s[:end_pos]
    return s

def extract_links(url):
    """
    Extracts valid links in "See also" section of article
    """
    section = extract_link_section(url)
    tmp = re.search("<a href=\"(.*?)\"", section)
    links = []
    while tmp:
        link = tmp.group(1)
        if "#" in link:
            link = link[:link.index("#")]
        if len(link) == 0:
            pass
        elif link[0] == '/':
            links.append(prefix + link)
        else:
            links.append(link)
        section = section[tmp.end():]
        tmp = re.search("<a href=\"(.*?)\"", section)
    return links

def bfs(root):
    """
    Run BFS until network is grown to 1000 nodes
    """
    queue = [root]
    vis = set(queue)
    level_order = []
    while (len(level_order) < N):
        curr_url = queue.pop(0)
        print(curr_url)
        level_order.append(curr_url)
        outlinks = extract_links(curr_url)
        print(len(outlinks))
        for url in outlinks:
            real_url = get_real_url(url)
            if real_url != None and real_url not in vis:
                vis.add(real_url)
                queue.append(real_url)
    return level_order

def get_edges(nodes):
    """
    After nodes are found, extract links again to identify edges within desired graph
    """
    adj_matrix = np.zeros((N, N))
    node_to_index = {}
    
    for i in range(len(nodes)):
        node_to_index[nodes[i]] = i

    for i in range(len(nodes)):
        outlinks = extract_links(nodes[i])
        for url in outlinks:
            real_url = get_real_url(url)
            if real_url in node_to_index:
                adj_matrix[i][node_to_index[real_url]] = 1
    return adj_matrix

nodes = bfs(root)
with open("nodes.txt", "w") as f:
    for node in nodes:
        f.write(node + '\n')

matrix = get_edges(nodes)
with open("edges.txt", "w") as f:
    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 1:
                f.write("%d %d\n" % (i, j))

with open("edges-labelled.txt", "w") as f:
    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 1:
                f.write("%s %s\n" % (nodes[i], nodes[j]))