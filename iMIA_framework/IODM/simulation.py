import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import json 

from graph_function import *

def save_graph(G):
    all_nodes = list(G.nodes())
    nodes = [{'name': str(i), 'group': G.nodes[i]["type"], 'compromised': G.nodes[i]["compromised"], 'centrality': G.nodes[i]["centrality"], 'vulnerability': G.nodes[i]["vulnerability"]}
            for i in G.nodes()]
    links = [{'source': all_nodes.index(u[0]), 'target': all_nodes.index(u[1]), 'value':0, 'size':1}
            for u in G.edges()]
    with open('static/graph.json', 'w') as f:
        json.dump({'nodes': nodes, 'links': links}, f, indent=4,)

if __name__ == '__main__':
    G = create_graph()
    set_type(G)
    set_compromised(G)
    set_centrality(G)
    set_vulnerability(G)
    
    # while steps > 0:

    save_graph(G)
    # print(G.edges())
    # print(G)
        # print(nx.cycle_basis(G.to_undirected()))
    # cmap = []

    # for node in G:
    #     if 'IoT' in node:
    #         cmap.append('green')
    #     elif 'Edge' in node:
    #         cmap.append('red')
    #     elif 'MEC' in node:
    #         cmap.append('skyblue')
    #     else:
    #         cmap.append('yellow')
    

    # nx.draw(G, node_color = cmap)
    # plt.tight_layout()
    # plt.show()
    # plt.savefig("Graph.png", format="PNG")