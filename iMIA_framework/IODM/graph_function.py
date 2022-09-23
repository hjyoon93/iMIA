import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import json
import random 

def create_graph():
    num_iot = np.random.randint(15, 20)
    iot_devices = {}
    for i in range(num_iot):
        iot_devices['IoT'+str(i+1)] = {'connected': False}

    num_edge = np.random.randint(8, 15)
    edge_devices = {}
    for i in range(num_edge):
        edge_devices['Edge'+str(i+1)] = {'connected_mec': False, 'connected_iot': False}

    num_mec = np.random.randint(3, 8)
    mec_devices = {}
    for i in range(num_mec):
        mec_devices['MEC'+str(i+1)] = {'connected': False}

    ccs = {'ccs': {'connected': False}}

    conn = []

    for j in range(num_edge):
        i = np.random.randint(num_iot)
        while iot_devices['IoT'+str(i+1)]['connected']:
            i = np.random.randint(num_iot)
        conn.append(('IoT'+str(i+1), 'Edge'+str(j+1)))
        iot_devices['IoT'+str(i+1)]['connected'] = True
        edge_devices['Edge'+str(j+1)]['connected_iot'] = True

    for i in range(num_iot):
        l = np.random.randint(num_edge)
        if iot_devices['IoT'+str(i+1)]['connected'] == False:
            conn.append(('IoT'+str(i+1), 'Edge'+str(l+1)))
            iot_devices['IoT'+str(i+1)]['connected'] = True
        edge_devices['Edge'+str(l+1)]['connected_iot'] = True

    for j in range(num_mec):
        i = np.random.randint(num_edge)
        while edge_devices['Edge'+str(i+1)]['connected_mec']:
            i = np.random.randint(num_edge)
        conn.append(('MEC'+str(j+1), 'Edge'+str(i+1)))
        conn.append(('MEC'+str(j+1), 'ccs'))
        mec_devices['MEC'+str(j+1)]['connected'] = True
        edge_devices['Edge'+str(i+1)]['connected_mec'] = True

    for i in range(num_edge):
        l = np.random.randint(num_mec)
        if edge_devices['Edge'+str(i+1)]['connected_mec'] == False:
            conn.append(('Edge'+str(i+1), 'MEC'+str(l+1)))
            edge_devices['Edge'+str(i+1)]['connected_mec'] = True
        mec_devices['MEC'+str(l+1)]['connected'] = True

    ccs['ccs']['connected'] = True

    G=nx.Graph()
    G.add_nodes_from(iot_devices.keys())
    G.add_nodes_from(edge_devices.keys())
    G.add_nodes_from(mec_devices.keys())
    G.add_nodes_from(ccs.keys())
    G.add_edges_from(conn)
    return G

def set_type(G):
    nx.set_node_attributes(G, 0, "type")
    for n in G.nodes:
        if 'IoT' in n:
            G.nodes[n]["type"] = 0
        elif 'Edge' in n:
            G.nodes[n]["type"] = 1
        elif 'MEC' in n:
            G.nodes[n]["type"] = 2
        else:
            G.nodes[n]["type"] = 4

def set_compromised(G):
    if not nx.get_node_attributes(G, "compromised"):
        nx.set_node_attributes(G, False, "compromised")

def set_centrality(G):
    H = G.copy(as_view = False)
    H.remove_node("ccs")
    pr = nx.pagerank(H, alpha=0.9)
    values = pr.values()
    min_ = min(values)
    max_ = max(values)

    normalized_pr = {key: ((v - min_ ) / (max_ - min_) )  for (key, v) in pr.items() }
    
    if not nx.get_node_attributes(G, "centrality"):
        nx.set_node_attributes(G, 0, "centrality")
    
    for n in G.nodes:
        if n == 'ccs':
            continue
        G.nodes[n]["centrality"] = normalized_pr[n]

def set_vulnerability(G):
    nx.set_node_attributes(G, 0, "vulnerability")
    
    for n in G.nodes:
        if "IoT" in n:
            G.nodes[n]["vulnerability"] = (random.randint(1, 10) * G.nodes[n]["centrality"]) / 10
        elif "Edge" in n:
            G.nodes[n]["vulnerability"] = (random.randint(1, 10) * G.nodes[n]["centrality"]) / 10
        elif "MEC" in n:
            G.nodes[n]["vulnerability"] = (random.randint(1, 10) * G.nodes[n]["centrality"]) / 10

def set_integrity(G):
    if not nx.get_node_attributes(G, "integrity"):
        nx.set_node_attributes(G, 1, "integrity")

def set_confidentiality(G):
    if not nx.get_node_attributes(G, "confidentiality"):
        nx.set_node_attributes(G, 1, "confidentiality")