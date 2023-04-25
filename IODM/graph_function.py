import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import json
import random 
import math
# np.random.seed(0)
# random.seed(0)

display = False



# def set_reachability(G):
#     if not nx.get_node_attributes(G, "reachability"):
#         nx.set_node_attributes(G, 0, "reachability")
#     reachability = nx.betweenness_centrality(G)
#     for n in G.nodes():
#         G.nodes[n]["reachability"] = reachability[n]
def set_centrality(G):
        H = G.copy(as_view = False)
        
        H.remove_node("ccs")
        # print(H.nodes[0])
        h_nodes = list(H.nodes)
        for n in h_nodes:
            # print('xddz')
            if H.nodes[n]['evicted'] == True:
                H.remove_node(n)
        # print('xdd')
        pr = nx.pagerank(H, alpha=0.9)
        values = pr.values()
        min_ = min(values)
        max_ = max(values)

        normalized_pr = {key: ((v - min_ ) / (max_ - min_) )  for (key, v) in pr.items() }
        
        # if not nx.get_node_attributes(G, "centrality"):
        nx.set_node_attributes(G, 0, "centrality")
        # print(len(normalized_pr))
        for n in normalized_pr:
            if n == 'ccs':
                continue
            # print(n)
            G.nodes[n]["centrality"] = normalized_pr[n]

def update_criticality(G):

    if not nx.get_node_attributes(G, "criticality"):
        nx.set_node_attributes(G, 1, "criticality")
    
    set_centrality(G)
    
    for n in G.nodes():
        G.nodes[n]["criticality"] = (G.nodes[n]["type"] + 1) * G.nodes[n]["centrality"]


def evict_a_node(remove_id, G_real, G_def, G_att, t):
    
    node_neighbor = list(G_def.neighbors(remove_id))
    
    # remove edge to adjacent nodes
    # for neighbor_index in node_neighbor:
    # G_real[remove_id]['evicted'] = True
    # G_def[remove_id]['evicted'] = True
    # G_real[remove_id]['evicted'] = True

        # if G_real.has_edge(remove_id,neighbor_index): G_real.remove_edge(remove_id,neighbor_index)
        # if G_def.has_edge(remove_id,neighbor_index): G_def.remove_edge(remove_id,neighbor_index)
        # if G_att.has_edge(remove_id,neighbor_index): G_att.remove_edge(remove_id,neighbor_index)
    
    # change evict mark
    G_real.nodes[remove_id]["evicted"] = t
    G_def.nodes[remove_id]["evicted"] = t
    G_att.nodes[remove_id]["evicted"] = t
        
    # update criticality
    update_criticality(G_real)
    update_criticality(G_def)
    update_criticality(G_att)

def update_normalized_vulnerability(G):
    for n in G.nodes():
        G.nodes[n]["NV"] = (G.nodes[n]["SV"] + G.nodes[n]["UV"] + G.nodes[n]["EV"])/3

def is_node_evicted(G, target_id):
    return G.nodes[target_id]["evicted"] != 0

def update_vul(G):
    # if not nx.get_node_attributes(G, "vulnerability"):
    #     nx.set_node_attributes(G, 0, "vulnerability")
    # if not nx.get_node_attributes(G, "combined_vulnerability"):
    #     nx.set_node_attributes(G, 0, "combined_vulnerability")
    for n in G.nodes():
        G.nodes[n]["combined_vulnerability"] = ((G.nodes[n]["vulnerability"] + G.nodes[n]["centrality"] * 10)/2)

def update_en_vul(G, ev_lambda, T_rekey):
    T_rekey += 1
    for n in G.nodes():
        # for index in range(ev):
        G.nodes[n]["EV"] = G.nodes[n][
                "original_EV"] * math.exp(
                    -ev_lambda / T_rekey)

def update_dynamaic_analysis(G):
    for n in G.nodes():
        G.nodes[n]["dynamic_analysis"] = False

class graph_class:
    def __init__(self, iot_ev_m, edge_ev_m, mec_ev_m, iot_sv_m, edge_sv_m, mec_sv_m, iot_uv_m, edge_uv_m, mec_uv_m, vuln_s, vuln_m_err):
        self.attack_strategies = ['Vulnerability_Scanning', 'Phishing', 'Exploit_Public_Facing_Application', 'Previlage_Escalation', 'Brute_Force', 'DDoS', 'Data_Manipulation', 'Automated_Exfiltration']
        # self.attack_strategies = ['Vulnerability_Scanning', 'Phishing', 'Exploit_Public_Facing_Application', 'Previlage_Escalation', 'Brute_Force', 'DDoS', 'Data_Manipulation']
        self.network = None
        self.honey_net = None
        self.using_honeynet = False
        self.network_size_factor = 5 #5
        self.node_number = 10*self.network_size_factor#100  # number of nodes
        self.connect_prob = 0.05  # connection probability
        self.SF_thres = 0.3  # A threshold for SF
        self.low_inter = 10*self.network_size_factor #10  # number of low interaction honeypots
        self.high_inter = 5*self.network_size_factor #5  # number of high interaction honeypots
        self.inter_per_node = 3 # one honeypot connect to 3 nodes
        self.N_ws = 5*self.network_size_factor #5  # number of Web servers
        self.N_db = 5*self.network_size_factor #5  # number of databases
        self.N_iot = self.node_number - self.N_ws - self.N_db  # number of IoT nodes
        self.ev = 5  # encryption vulnerability
        self.sv = 5  # software vulnerability
        self.uv = 1  # unknown vulnerability
        self.ev_lambda = 1 # λ for normalize encryption vulnerability
        self.T_rekey = 1 # rekey time for encryption vulnerability
        self.iot_sv_mean = iot_sv_m
        self.edge_sv_mean = edge_sv_m
        self.mec_sv_mean = mec_sv_m
        self.iot_ev_mean = iot_ev_m
        self.edge_ev_mean = edge_ev_m
        self.mec_ev_mean = mec_ev_m
        self.iot_uv_mean = iot_uv_m
        self.edge_uv_mean = edge_uv_m
        self.mec_uv_mean = mec_uv_m
        self.vuln_std = vuln_s
        self.vuln_mean_error = vuln_m_err

        # print(self.mec_ev_mean)
        # self.web_data_upper_vul = web_data_upper_vul
        # self.Iot_upper_vul = Iot_upper_vul
        
        if display: print("create graph")
        self.create_graph()
        
        # print("gg",self.network)
        self.set_graph_attributes(self.network, self.attack_strategies)
        # print("gg",self.network.nodes['IoT1'])
        # print("lol11")
        
        self.save_graph(self.network, self.attack_strategies)
        
        # print("lol22")
        
    def T_rekey_reset(self):
        self.T_rekey = 1

        # while steps > 0:
    def update_graph(self, G_def, G_att):
        update_criticality(self.network)
        update_criticality(G_def)
        update_criticality(G_att)
        update_normalized_vulnerability(self.network)
        update_normalized_vulnerability(G_def)
        update_normalized_vulnerability(G_att)
        update_dynamaic_analysis(self.network)
        update_dynamaic_analysis(G_att)
        update_dynamaic_analysis(G_def)
        update_en_vul(G_att, 1, self.T_rekey)
        update_en_vul(G_def, 1, self.T_rekey)
        update_en_vul(self.network, 1, self.T_rekey)
    
    def set_type(self, G):
    
    # print('lol')
    # print(G.nodes)
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
        
    # print('lol')

    def set_compromised(self, G):
        if not nx.get_node_attributes(G, "compromised"):
            nx.set_node_attributes(G, False, "compromised")

    def set_software_vulnerability(self, G):
        nx.set_node_attributes(G, 0, "SV")
        for n in G.nodes:
            noise = random.random()/20
            if "IoT" in n:
                G.nodes[n]["SV"] = np.clip(np.random.normal(np.clip(np.random.normal(self.iot_sv_mean, self.vuln_mean_error), 0, 10), self.vuln_std)/10, 0, 1)
            elif "Edge" in n:
                G.nodes[n]["SV"] = np.clip(np.random.normal(np.clip(np.random.normal(self.edge_sv_mean, self.vuln_mean_error), 0, 10), self.vuln_std)/10, 0, 1)
            elif "MEC" in n:
                G.nodes[n]["SV"] = np.clip(np.random.normal(np.clip(np.random.normal(self.mec_sv_mean, self.vuln_mean_error), 0, 10), self.vuln_std)/10, 0, 1)

    def set_unknown_vulnerability(self, G):
        nx.set_node_attributes(G, 0, "UV")
        
        for n in G.nodes:
            noise = random.random()/20
            if "IoT" in n:
                G.nodes[n]["UV"] = np.clip(np.random.normal(np.clip(np.random.normal(self.iot_uv_mean, self.vuln_mean_error), 0, 10), self.vuln_std)/10, 0, 1)
            elif "Edge" in n:
                G.nodes[n]["UV"] = np.clip(np.random.normal(np.clip(np.random.normal(self.edge_uv_mean, self.vuln_mean_error), 0, 10), self.vuln_std)/10, 0, 1)
            elif "MEC" in n:
                G.nodes[n]["UV"] = np.clip(np.random.normal(np.clip(np.random.normal(self.mec_uv_mean, self.vuln_mean_error), 0, 10), self.vuln_std)/10, 0, 1)

    def set_encryption_vulnerability(self, G):
        nx.set_node_attributes(G, 0, "EV")
        nx.set_node_attributes(G, 0, "original_EV")
        for n in G.nodes:
            noise = random.random()/20
            if "IoT" in n:
                # print()
                G.nodes[n]["EV"] = np.clip(np.random.normal(np.clip(np.random.normal(self.iot_ev_mean, self.vuln_mean_error), 0, 10), self.vuln_std)/10, 0, 1)
            elif "Edge" in n:
                G.nodes[n]["EV"] = np.clip(np.random.normal(np.clip(np.random.normal(self.edge_ev_mean, self.vuln_mean_error), 0, 10), self.vuln_std)/10, 0, 1)
            elif "MEC" in n:
                G.nodes[n]["EV"] = np.clip(np.random.normal(np.clip(np.random.normal(self.mec_ev_mean, self.vuln_mean_error), 0, 10), self.vuln_std)/10, 0, 1)
            G.nodes[n]["original_EV"] = G.nodes[n]["EV"]

    def set_ess(self, G, attack_strategies):
        for i in range(len(attack_strategies)):
            # print(attack_strategies[i])
            nx.set_node_attributes(G, 0, "ess_"+attack_strategies[i])
            
            for n in G.nodes:
                if "IoT" in n:
                    G.nodes[n]["ess_"+attack_strategies[i]] = np.clip(np.random.normal(5, 1)/10, 0, 1)
                elif "Edge" in n:
                     G.nodes[n]["ess_"+attack_strategies[i]] = np.clip(np.random.normal(7, 1)/10, 0, 1)
                elif "MEC" in n:
                     G.nodes[n]["ess_"+attack_strategies[i]] = np.clip(np.random.normal(9, 1)/10, 0, 1)

    def set_iss(self, G, attack_strategies):
        for i in range(len(attack_strategies)):
            nx.set_node_attributes(G, 0, "iss_"+attack_strategies[i])
            
            for n in G.nodes:
                if "IoT" in n:
                    G.nodes[n]["iss_"+attack_strategies[i]] = np.clip(np.random.normal(5, 1)/10, 0, 1)
                elif "Edge" in n:
                    G.nodes[n]["iss_"+attack_strategies[i]] = np.clip(np.random.normal(7, 1)/10, 0, 1)
                elif "MEC" in n:
                    G.nodes[n]["iss_"+attack_strategies[i]] = np.clip(np.random.normal(9, 1)/10, 0, 1)

    def set_lamda(self, G):
        nx.set_node_attributes(G, 0, "lamda")
            
        for n in G.nodes:
            if "IoT" in n:
                G.nodes[n]["lamda"] = np.clip(np.random.normal(1, 0.2), 0, 1)
            elif "Edge" in n:
                G.nodes[n]["lamda"] = np.clip(np.random.normal(0.5, 0.2), 0, 1)
            elif "MEC" in n:
                G.nodes[n]["lamda"] = np.clip(np.random.normal(0.25, 0.2), 0, 1)
            
    def set_asset_capacity(self, G):
        if not nx.get_node_attributes(G, "asset_capacity"):
            nx.set_node_attributes(G, 1, "asset_capacity")
    
    def set_memory(self, G):
        if not nx.get_node_attributes(G, "memory"):
            nx.set_node_attributes(G, 1, "memory")
    
    def set_cpu(self, G):
        if not nx.get_node_attributes(G, "cpu"):
            nx.set_node_attributes(G, 1, "cpu")

    def set_poisoned(self, G):
        if not nx.get_node_attributes(G, "poisoned"):
            nx.set_node_attributes(G, 0, "poisoned")

    def set_available(self, G):
        if not nx.get_node_attributes(G, "available"):
            nx.set_node_attributes(G, 0, "available")
        
    def set_evicted(self, G):
        if not nx.get_node_attributes(G, "evicted"):
            nx.set_node_attributes(G, 0, "evicted")

    def set_integrity(self, G):
        if not nx.get_node_attributes(G, "integrity"):
            nx.set_node_attributes(G, 1, "integrity")

    def set_pool(self, G):
        nx.set_node_attributes(G,{ n: [] for n in G.nodes() },"pool")
        # nx.set_node_attributes(G, [], "pool")

    def set_recieved(self, G):
        nx.set_node_attributes(G,{ n: [] for n in G.nodes() },"recieved")
        # nx.set_node_attributes(G, [], "recieved")
    
    def set_model_updated(self, G):
        nx.set_node_attributes(G, 0, "model_updated")
    
    def set_dynamic_analysis(self, G):
        nx.set_node_attributes(G, 0, "dynamic_analysis")

    def set_id(self, G):
        nx.set_node_attributes(G, 0, "id")
        for n in G.nodes:
            G.nodes[n]["id"] = n
            
    def set_graph_attributes(self, G, attack_strategies):
        self.set_type(G)
        self.set_id(G)
        self.set_compromised(G)
        self.set_lamda(G)
        self.set_evicted(G)
        set_centrality(G) 
        
        # print('xd')
        self.set_integrity(G) 
        self.set_software_vulnerability(G)
        self.set_encryption_vulnerability(G)
        self.set_unknown_vulnerability(G)
        self.set_ess(G, attack_strategies)
        self.set_iss(G, attack_strategies)
        self.set_asset_capacity(G)
        self.set_memory(G)
        self.set_cpu(G)
        self.set_poisoned(G)
        self.set_available(G)
        self.set_pool(G)
        self.set_recieved(G)
        self.set_dynamic_analysis(G)
    
    
    def save_graph(self, G, attack_strategies):
        all_nodes = list(G.nodes())
        nodes = [{'name': str(i), 'group': G.nodes[i]["type"], 'compromised': G.nodes[i]["compromised"],
                'centrality': G.nodes[i]["centrality"], 'vulnerability': G.nodes[i]["SV"], 
                'asset_capacity': G.nodes[i]["asset_capacity"],
                'SV': G.nodes[i]["SV"],
                'poisoned': G.nodes[i]["poisoned"], 'available':  G.nodes[i]["available"],
                'evicted' : G.nodes[i]["evicted"],
                'ess_'+attack_strategies[0]: G.nodes[i]["ess_"+attack_strategies[0]], 
                'ess_'+attack_strategies[1]: G.nodes[i]["ess_"+attack_strategies[1]], 
                'ess_'+attack_strategies[2]: G.nodes[i]["ess_"+attack_strategies[2]],
                'ess_'+attack_strategies[3]: G.nodes[i]["ess_"+attack_strategies[3]],
                'ess_'+attack_strategies[4]: G.nodes[i]["ess_"+attack_strategies[4]],
                'ess_'+attack_strategies[5]: G.nodes[i]["ess_"+attack_strategies[5]],
                'iss_'+attack_strategies[0]: G.nodes[i]["iss_"+attack_strategies[0]], 
                'iss_'+attack_strategies[1]: G.nodes[i]["iss_"+attack_strategies[1]], 
                'iss_'+attack_strategies[2]: G.nodes[i]["iss_"+attack_strategies[2]],
                'iss_'+attack_strategies[3]: G.nodes[i]["iss_"+attack_strategies[3]],
                'iss_'+attack_strategies[4]: G.nodes[i]["iss_"+attack_strategies[4]],
                'iss_'+attack_strategies[5]: G.nodes[i]["iss_"+attack_strategies[5]]
                }
                for i in G.nodes()]
        links = [{'source': all_nodes.index(u[0]), 'target': all_nodes.index(u[1]), 'value':0, 'size':1}
                for u in G.edges()]
        with open('static/graph.json', 'w') as f:
            json.dump({'nodes': nodes, 'links': links}, f, indent=4,)
    
        
    def create_graph(self):
        num_iot = 20 #np.random.randint(15, 20)
        iot_devices = {}
        for i in range(num_iot):
            iot_devices['IoT'+str(i+1)] = {'connected': False}

        num_edge = 10 # np.random.randint(8, 15)
        edge_devices = {}
        for i in range(num_edge):
            edge_devices['Edge'+str(i+1)] = {'connected_mec': False, 'connected_iot': False}

        num_mec = 5 #np.random.randint(3, 8)
        mec_devices = {}
        for i in range(num_mec):
            mec_devices['MEC'+str(i+1)] = {'connected': False}

        ccs = {'ccs': {'connected': False}}

        conn = []

        for j in range(num_edge):
            # i = np.random.randint(num_iot)
            # while iot_devices['IoT'+str(i+1)]['connected']:
            #     i = np.random.randint(num_iot)
            conn.append(('IoT'+str(2*j+1), 'Edge'+str(j+1)))
            conn.append(('IoT'+str(2*j+2), 'Edge'+str(j+1)))
            iot_devices['IoT'+str(2*j+1)]['connected'] = True
            iot_devices['IoT'+str(2*j+1)]['connected'] = True
            edge_devices['Edge'+str(j+1)]['connected_iot'] = True

        # for i in range(num_iot):
        #     l = np.random.randint(num_edge)
        #     if iot_devices['IoT'+str(i+1)]['connected'] == False:
        #         conn.append(('IoT'+str(i+1), 'Edge'+str(l+1)))
        #         iot_devices['IoT'+str(i+1)]['connected'] = True
        #     edge_devices['Edge'+str(l+1)]['connected_iot'] = True

        for j in range(num_mec):
            # i = np.random.randint(num_edge)
            # while edge_devices['Edge'+str(i+1)]['connected_mec']:
            #     i = np.random.randint(num_edge)
            conn.append(('MEC'+str(j+1), 'Edge'+str(2*j+1)))
            conn.append(('MEC'+str(j+1), 'Edge'+str(2*j+2)))
            conn.append(('MEC'+str(j+1), 'ccs'))
            mec_devices['MEC'+str(j+1)]['connected'] = True
            edge_devices['Edge'+str(2*j+1)]['connected_mec'] = True
            edge_devices['Edge'+str(2*j+2)]['connected_mec'] = True

        # for i in range(num_edge):
        #     l = np.random.randint(num_mec)
        #     if edge_devices['Edge'+str(i+1)]['connected_mec'] == False:
        #         conn.append(('Edge'+str(i+1), 'MEC'+str(l+1)))
        #         edge_devices['Edge'+str(i+1)]['connected_mec'] = True
        #     mec_devices['MEC'+str(l+1)]['connected'] = True

        ccs['ccs']['connected'] = True

        self.network = nx.Graph()
        self.network.add_nodes_from(iot_devices.keys())
        self.network.add_nodes_from(edge_devices.keys())
        self.network.add_nodes_from(mec_devices.keys())
        self.network.add_nodes_from(ccs.keys())
        self.network.add_edges_from(conn)

            