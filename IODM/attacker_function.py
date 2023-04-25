
from platform import node
import numpy as np
import random
import math
import copy
from defender_function import *
# np.random.seed(0)
# random.seed(0)
display = False

attack_name = ['Vulnerability_Scanning', 'Phishing', 'Exploit_Public_Facing_Application', 'Previlage_Escalation', 'Brute_Force', 'Data_Manipulation', 'DDoS', 'Automated_Exfiltration']
# attack_name = ['Vulnerability_Scanning', 'Phishing', 'Exploit_Public_Facing_Application', 'Previlage_Escalation', 'Brute_Force', 'Data_Manipulation', 'DDoS']
def att_strategy_cost(strategy_number, G, node):
    global attack_name
    # print(node)
    # attack_cost_domain = np.array([1, 3, 4, 6, 6, 4, 5])/7
    attack_cost_domain = np.array([1, 3, 4, 6, 6, 4, 5, 7])/7
    if node is None:
        return attack_cost_domain
#      preset cost
    omega = 0.5
    attack_cost = np.zeros(strategy_number)
    # print(node)
    for i in range(strategy_number):
        # for n in G.nodes:
        # print(G[node], node)
        # print(nx.get_node_attributes(G, node))
        # print((G.nodes[node]['ess_'+attack_name[i]] / 7))
        attack_cost[i] += (G.nodes[node]['ess_'+attack_name[i]])
            # print(n)
    
    attack_cost = omega * attack_cost + (1 - omega) * attack_cost_domain
    return attack_cost

def att_strategy_option_matrix(subgame_number, strategy_number):
        strat_option = np.zeros((subgame_number, strategy_number))
        # R
        strat_option[0, 0] = 1
        strat_option[0, 1] = 1
        strat_option[0, 2] = 1
        # D
        strat_option[1, 0] = 1
        strat_option[1, 1] = 1
        strat_option[1, 2] = 1
        strat_option[1, 3] = 1
        strat_option[1, 4] = 1
        # E
        strat_option[2, 0] = 1
        strat_option[2, 1] = 1
        strat_option[2, 2] = 1
        strat_option[2, 5] = 1
        strat_option[2, 6] = 1
        strat_option[2, 7] = 1

        # strat_option[3, 0] = 1
        # strat_option[3, 1] = 1
        # strat_option[3, 2] = 1
        # strat_option[3, 3] = 1
        # strat_option[3, 4] = 1
        # strat_option[3, 5] = 1
        # strat_option[3, 6] = 1
        
        return strat_option



def vulnerabilityScanning(G_real, G_att, G_def, node_info_list, monit_time):
    attack_result = {"attack_cost": 1, "ids": []}
    
    node_id_set = list(G_att.nodes())
    # print(node_id_set)
    node_id_set.remove("ccs")
    # weights = [0.017] * 20 + [0.033] * 10 + [0.066] * 5
    weights = [0.0125] * 20 + [0.0025] * 10 + [0.1] * 5
    
    not_get_one = True
    while not_get_one:
        random_id = random.choices(node_id_set, weights = weights, k=1)[0]
        # if random_id == 'ccs':
        #     continue
        if G_real.nodes[random_id]["evicted"] == 0:
            not_get_one = False
            # print(random_id)
            if random.random() <= G_real.nodes[random_id]["NV"]:  # success rate is based on real graph
                # G_att.nodes[random_id]["combined_vulnerability"] = G_real.nodes[random_id]["combined_vulnerability"] 
                # G_att.nodes[random_id]["vulnerability"] = G_real.nodes[random_id]["vulnerability"] 
                node_info_list.append(G_att.nodes[random_id]['id'])
                
    return attack_result

def Phishing(G_real, G_att, node_info_list, attacker_location):

    attack_result = {"attack_cost": 1, "ids": []}
    # print(node_info_list)
    target_node_id = attacker_location
    if attacker_location is None:
        if node_info_list:
            # print(node_info_list)
            target_node_id = random.choice(node_info_list)
            if random.random(
            ) < G_real.nodes[target_node_id]["NV"] and not G_real.nodes[target_node_id]['dynamic_analysis'] and G_real.nodes[target_node_id]["evicted"] == 0:
                attack_result["ids"].append(target_node_id)
                G_real.nodes[target_node_id]["compromised"] = True
                G_att.nodes[target_node_id]["compromised"] = True
        return attack_result
    elif G_real.nodes[target_node_id]["compromised"]:
        if display:
            print("Phishing unsuccessful on", target_node_id, "node already compromised")
        return attack_result
    # target_node_id = random.choice(node_info_list)
    # while G_att.nodes[target_node_id]["compromised"] == True:
    #     target_node_id = random.choice(node_info_list)
    
    # compromise attempt
    if random.random() < G_real.nodes[target_node_id]["NV"] and not G_real.nodes[target_node_id]['dynamic_analysis'] and G_real.nodes[target_node_id]["evicted"] == 0:
        attack_result["ids"].append(target_node_id)
        # set it compromised
        G_real.nodes[target_node_id]["compromised"] = True
        G_att.nodes[target_node_id]["compromised"] = True
    else:
        if display:
            print("Phishing unsuccessful on", target_node_id, "with vul",
                G_real.nodes[target_node_id]["NV"])

    return attack_result

def exploitPublicFacingApplications(G_real, G_att, node_info_list, attacker_location):
    attack_result = {"attack_cost": 1, "ids": []}

    target_node_id = attacker_location
    if attacker_location is None:
        if node_info_list:
            target_node_id = random.choice(node_info_list)
            if random.random(
            ) < G_real.nodes[target_node_id]["SV"] and G_real.nodes[target_node_id]["evicted"] == 0:
                attack_result["ids"].append(target_node_id)
                G_real.nodes[target_node_id]["compromised"] = True
                G_att.nodes[target_node_id]["compromised"] = True
#                 G_def.nodes[target_node_id]["compromised"] = True
        return attack_result
    elif G_real.nodes[target_node_id]["compromised"]:
        if display:
            print("Exploiting Public Facing Vulnerability unsuccessful on", target_node_id, "node already compromised")
        return attack_result

    target_node_id = attacker_location

    # while G_att.nodes[target_node_id]["evicted"] != 0:
    #     target_node_id = random.choice(node_info_list)
    
    # compromise attempt
    if random.random() < G_real.nodes[target_node_id]["SV"] and G_real.nodes[target_node_id]["evicted"] == 0:
        attack_result["ids"].append(target_node_id)
        # set it compromised
        G_real.nodes[target_node_id]["compromised"] = True
        G_att.nodes[target_node_id]["compromised"] = True
#         G_def.nodes[max_APV_id]["compromised"] = True
    else:
        if display:
            print("Exploiting Public Facing Vulnerability unsuccessful on", target_node_id, "with vul",
                G_real.nodes[target_node_id]["SV"])

    return attack_result

def previlageEscalation(G_real, G_att, attacker_location):
    attack_result = {"attack_cost": 2, "ids": []}
    # target_node_id = random.choice(node_info_list)
    target_node_id = attacker_location
    if attacker_location is None:
        node_list = list(G_att.nodes)
        random.shuffle(node_list)
        node_list.remove('ccs')
        target_node_id = None
        found = False
        for n in node_list:
            if G_att.nodes[n]["compromised"] and G_real.nodes[n]["evicted"] == 0:
                found = True
                target_node_id = n
                break
        
        if not found:
            if display:
                print("Previlage Escalation unsuccessful: No compromised nodes")
            return attack_result
    elif not G_att.nodes[target_node_id]["compromised"] or G_real.nodes[target_node_id]["evicted"] != 0:
        if display:
            print("Previlage Escalation unsuccessful: Node", target_node_id, "not compromised or evicted!")
        return attack_result
    # compromise attempt
    if random.random() < G_real.nodes[target_node_id]["NV"]:
        attack_result["ids"].append(target_node_id)
        # increase vulnerability
        G_real.nodes[target_node_id]["UV"] = min(
                G_real.nodes[target_node_id]["UV"] * 1.1, 1)
        # set it compromised
        # G_real.nodes[target_node_id]["compromised"] = True
        # G_att.nodes[target_node_id]["compromised"] = True
    else:
        if display:
            print("Previlage Escalation unsuccessful on", target_node_id, "with vul",
                G_real.nodes[target_node_id]["NV"])

    return attack_result


def Bruteforce(G_real, G_att, attacker_location):
    # node_id_set = list(G_att.nodes())
    attack_result = {"attack_cost": 2, "ids": []}
    # target_node_id = random.choice(node_info_list)

    # while G_att.nodes[target_node_id]["compromised"] == True:
    #     target_node_id = random.choice(node_info_list)
    target_node_id = attacker_location
    if attacker_location is None:
        # print(G_att.nodes)
        node_list = list(G_att.nodes)
        random.shuffle(node_list)
        node_list.remove('ccs')
        # print(node_list)
        target_node_id = None
        found = False
        for n in node_list:
            # print(n)
            if G_att.nodes[n]["compromised"] and G_real.nodes[n]["evicted"] == 0:
                found = True
                target_node_id = n
                break
        
        if not found:
            if display:
                print("Bruteforce unsuccessful: No compromised nodes")
            return attack_result
    elif not G_real.nodes[target_node_id]["compromised"] or G_real.nodes[target_node_id]["evicted"]!=0:
        if display:
            print("Bruteforce unsuccessful on", target_node_id, "Not compromised or evicted")
        return attack_result
    # else:
    # compromise attempt
    if random.random() < G_real.nodes[target_node_id]["EV"]:
        attack_result["ids"].append(target_node_id)
        # increase vulnerability
        G_real.nodes[target_node_id]["EV"] = min(
        G_real.nodes[target_node_id]["EV"] * 1.1, 10)
        # set it compromised
        # G_real.nodes[target_node_id]["compromised"] = True
        # G_att.nodes[target_node_id]["compromised"] = True
    else:
        if display:
            print("Bruteforce unsuccessful on", target_node_id, "with vul",
                G_real.nodes[target_node_id]["EV"])

    return attack_result

def DoS(G_real, G_att, timestep, attacker_location):
    node_info_list = list(G_att.nodes())
    node_info_list.remove('ccs')
    attack_result = {"attack_cost": 2, "ids": []}
    target_node_id = attacker_location

    # node_list = random.shuffle(G_att.nodes)
    if target_node_id is None:
        target_node_id = random.choice(node_info_list)
        attack_result["ids"].append(target_node_id)
        if G_real.nodes[target_node_id]["evicted"] == 0:
            if G_real.nodes[target_node_id]["available"] == 0:
                if display:
                    print("DoS:", target_node_id)
                G_real.nodes[target_node_id]["available"] = timestep
                G_att.nodes[target_node_id]["available"] = timestep
                # print("ACCCC", G_real.nodes[target_node_id]["asset_capacity"] * 0.5, G_real.nodes[target_node_id]["asset_capacity"])
                # G_real.nodes[target_node_id]["asset_capacity"] = max(G_real.nodes[target_node_id]["asset_capacity"] * 0.5, 0)
                # G_att.nodes[target_node_id]["asset_capacity"] = max(G_att.nodes[target_node_id]["asset_capacity"] * 0.5, 0) 
                G_real.nodes[target_node_id]["memory"] = max(G_real.nodes[target_node_id]["memory"] * 0.5, 0)
                G_att.nodes[target_node_id]["memory"] = max(G_att.nodes[target_node_id]["memory"] * 0.5, 0) 
                G_real.nodes[target_node_id]["cpu"] = max(G_real.nodes[target_node_id]["cpu"] * 0.5, 0)
                G_att.nodes[target_node_id]["cpu"] = max(G_att.nodes[target_node_id]["cpu"] * 0.5, 0) 
    # while G_att.nodes[target_node_id]["compromised"] == True:
    #     target_node_id = random.choice(node_info_list)
        return attack_result
    
    # compromise attempt
    att_neighbors = []
    for n in G_att[target_node_id]:
        if 'ccs' in n or G_real.nodes[n]["evicted"] !=0:
            continue
        att_neighbors.append(n)
    # att_neighbors = [n for n in G_att[target_node_id]]

    # if 'ccs' in att_neighbors:
    #     att_neighbors.remove('ccs')
    if (len(att_neighbors)) == 0:
        target_node_id = random.choice(node_info_list)
        attack_result["ids"].append(target_node_id)
        if G_real.nodes[target_node_id]["evicted"] == 0:
            if G_real.nodes[target_node_id]["available"] == 0:
                if display:
                    print("DoS:", target_node_id)
                G_real.nodes[target_node_id]["available"] = timestep
                G_att.nodes[target_node_id]["available"] = timestep
                # print("ACCCC", G_real.nodes[target_node_id]["asset_capacity"] * 0.5, G_real.nodes[target_node_id]["asset_capacity"])
                # G_real.nodes[target_node_id]["asset_capacity"] = max(G_real.nodes[target_node_id]["asset_capacity"] * 0.5, 0)
                # G_att.nodes[target_node_id]["asset_capacity"] = max(G_att.nodes[target_node_id]["asset_capacity"] * 0.5, 0) 
                G_real.nodes[target_node_id]["memory"] = max(G_real.nodes[target_node_id]["memory"] * 0.5, 0)
                G_att.nodes[target_node_id]["memory"] = max(G_att.nodes[target_node_id]["memory"] * 0.5, 0) 
                G_real.nodes[target_node_id]["cpu"] = max(G_real.nodes[target_node_id]["cpu"] * 0.5, 0)
                G_att.nodes[target_node_id]["cpu"] = max(G_att.nodes[target_node_id]["cpu"] * 0.5, 0) 

        return attack_result
            
    node_id = random.choice(att_neighbors)
    target_node_id = node_id
    # decide which node to compromise
    # for node_id in att_neighbors:
        # if random.random() < G_real.nodes[node_id]["combined_vulnerability"]:
    attack_result["ids"].append(node_id)
    # increase vulnerability

    if G_real.nodes[node_id]["available"] == 0:
        if display:
            print("DoS:", node_id)
        G_real.nodes[target_node_id]["available"] = timestep
        G_att.nodes[target_node_id]["available"] = timestep
        # G_real.nodes[node_id]["asset_capacity"] = max(G_real.nodes[node_id]["asset_capacity"] * 0.5, 0)
        # G_att.nodes[node_id]["asset_capacity"] = max(G_att.nodes[node_id]["asset_capacity"] * 0.5, 0)
        G_real.nodes[target_node_id]["memory"] = max(G_real.nodes[target_node_id]["memory"] * 0.5, 0)
        G_att.nodes[target_node_id]["memory"] = max(G_att.nodes[target_node_id]["memory"] * 0.5, 0) 
        G_real.nodes[target_node_id]["cpu"] = max(G_real.nodes[target_node_id]["cpu"] * 0.5, 0)
        G_att.nodes[target_node_id]["cpu"] = max(G_att.nodes[target_node_id]["cpu"] * 0.5, 0)  
    
    return attack_result


def dataManipulation(G_real, G_att, timestep, attacker_location):
    attack_result = {"attack_cost": 2, "ids": []}
    target_node_id = attacker_location

    # while G_att.nodes[target_node_id]["evicted"] != 0:
    #     target_node_id = random.choice(node_info_list)
    if attacker_location is None or not 'MEC' in attacker_location:
        # print(G_att.nodes)
        node_list = list(G_att.nodes)
        random.shuffle(node_list)
        node_list.remove('ccs')
        target_node_id = None
        found = False
        for n in node_list:
            if not 'MEC' in n:
                continue
            if G_att.nodes[n]["compromised"] and G_real.nodes[n]["evicted"] == 0:
                found = True
                target_node_id = n
                break
        
        if not found:
            if display:
                print("Data Manipulation unsuccessful: No compromised nodes")
            return attack_result, attacker_location
    elif not G_real.nodes[target_node_id]["compromised"] or G_real.nodes[target_node_id]["evicted"]!=0:
        if display:
            print("Data Manipulation unsuccessful on", target_node_id, "Not compromised or evicted")
        return attack_result, attacker_location
    # if 

    # compromise attempt
    if random.random() < G_real.nodes[target_node_id]["NV"]:
        attack_result["ids"].append(target_node_id)
        # increase vulnerability

        if G_real.nodes[target_node_id]["poisoned"] == 0:
            G_real.nodes[target_node_id]["poisoned"] = timestep
            G_att.nodes[target_node_id]["poisoned"] = timestep
        if display:
            print("Poisoned:", target_node_id)
        # set it compromised
        # print("poisoned")
        # G_real.nodes[target_node_id]["compromised"] = True
        # G_att.nodes[target_node_id]["compromised"] = True
    else:
        if display:
            print("Data Manipulation unsuccessful on", target_node_id, "with vul",
                G_real.nodes[target_node_id]["NV"])

    return attack_result, target_node_id

def Automated_Exfiltration(G_real, G_att, timestep, location, compromised_nodes):
    attack_result = {"attack_cost": 3, "ids": []}
    
    # node_id_set = list(G_att.nodes())
    # # print(node_id_set)
    # node_id_set.remove("ccs")
    # # weights = [0.017] * 20 + [0.033] * 10 + [0.066] * 5
    # weights = [0.0125] * 20 + [0.0025] * 10 + [0.1] * 5
    
    # not_get_one = True
    total_compromised_importance = 0
    for node_id in compromised_nodes:
        if G_real.has_node(node_id):
            if G_real.nodes[node_id]["compromised"]:
                if "MEC" in node_id:
                    importance = 5
                elif "Edge" in node_id:
                    importance = 3
                elif "IoT" in node_id:
                    importance = 1
                total_compromised_importance += importance

    if total_compromised_importance > 10:
        if display: print("Data exfiltration success")
        if display:
            print("total collected importance is",
                  total_compromised_importance)
        attack_result["data_exfiltrated"] = True
    else:
        if display: print("Data exfiltration failed")
        attack_result["data_exfiltrated"] = False

    return attack_result
            
    return attack_result


def attacker_class_choose_strategy(self, def_strategy_number,
                                   defend_cost_record, defend_impact_record):

    # attacker is 100% sure of subgame subgame
    P_subgame = np.zeros(self.subgame_number + 1)
    P_subgame[self.subgame_position] = 1
    S_j = np.zeros(def_strategy_number)
    for j in range(def_strategy_number):
        for k in range(self.subgame_number + 1):
            S_j[j] += P_subgame[k] * self.prob_believe_opponent[k][j]

    if display: print(f"S_j in att is {S_j}")

    # eq. 19 (Uncertainty g)
    g = self.uncertainty
    
    # eq. 17
    utility = np.zeros((self.strategy_number, def_strategy_number))
    for i in range(self.strategy_number):
        for j in range(def_strategy_number):
            utility[i,j] = (self.impact_record[i] +
                          defend_cost_record[j] / 3) - (
                              self.strat_cost[i] / 3 + defend_impact_record[j])
            
    # normalization range
    a = 1
    b = 10
    
    # eq. 8
    EU_C = np.zeros(self.strategy_number)
    for i in range(self.strategy_number):
        for j in range(def_strategy_number):
            EU_C[i] += S_j[j] * utility[i, j]
    # Normalization
    if (max(EU_C)-min(EU_C)) != 0:
        EU_C = a + (EU_C-min(EU_C))*(b-a)/(max(EU_C)-min(EU_C))
    self.EU_C = EU_C

    
    # eq. 9
    EU_CMS = np.zeros(self.strategy_number)
    for i in range(self.strategy_number):
        w = np.argmin(utility[i])  # min utility index
        EU_CMS[i] = self.strategy_number * S_j[w] * utility[i][w]
    # Normalization
    if (max(EU_CMS)-min(EU_CMS)) != 0:
        EU_CMS = a + (EU_CMS- min(EU_CMS))*(b-a)/(max(EU_CMS)-min(EU_CMS))
    self.EU_CMS = EU_CMS
    
    # eq. 7
    HEU = np.zeros(self.strategy_number)
    for index in range(self.strategy_number):
        HEU[index] = ((1 - g) * EU_C[index]) + (g * EU_CMS[index])
#     
    # if random.random() > g:
    #     HEU = EU_C
    #     self.HEU = HEU  # uncertainty case doesn't consider as real HEU
    # else:
    #     HEU = np.ones(self.strategy_number)
    # HEU = (1-g) * EU_C + g * EU_CMS
    # self.AHEU = (1-g) * EU_C + g * EU_CMS
    self.AHEU = HEU

    # eq. 23
    AHEU = np.zeros(self.strategy_number)
    for index in range(self.strategy_number):
        AHEU[index] = HEU[index] * self.strat_option[
            self.subgame_position, index]  # for Table 4
    if display:
        print("AHEU:", AHEU)
    self.chosen_strategy = random.choices(range(self.strategy_number),
                                          weights=AHEU,
                                          k=1)[0]
    return self.chosen_strategy


# In[51]:


def attacker_class_execute_strategy(self, G_real, G_def, timestep, random_strategy=False):
    return_value = False
    attack_result = {"attack_cost": 0, "ids": []}

    if self.chosen_strategy == 0:

        attack_result = vulnerabilityScanning(G_real, self.network, G_def,
                                    self.collection_list, self.monit_time)
        return_value = True
    elif self.chosen_strategy == 1:
        attack_result = Phishing(G_real, self.network, self.collection_list, self.location)
        if attack_result["ids"]:
            self.compromised_nodes.extend(attack_result["ids"])

            #  decrease collection list
            if self.location is None:
                self.collection_list.remove(attack_result["ids"][0])

            return_value = True
        else:
            if display: print("attack 2 failed")

    elif self.chosen_strategy == 2:
        attack_result = exploitPublicFacingApplications(G_real, self.network, self.collection_list, self.location)
        if attack_result["ids"]:
            self.compromised_nodes.extend(attack_result["ids"])
            return_value = True
        else:
            if display: print("attack 3 failed")

    elif self.chosen_strategy == 3:
        attack_result = previlageEscalation(G_real, self.network, self.location)
        if attack_result["ids"]:
            # self.compromised_nodes.extend(attack_result["ids"])
            return_value = True
        else:
            if display: print("attack 4 failed")

    elif self.chosen_strategy == 4:
        attack_result = Bruteforce(G_real, self.network, self.location)
        if attack_result["ids"]:
            # self.compromised_nodes.extend(attack_result["ids"])
            return_value = True
        else:
            if display: print("attack 5 failed")

    elif self.chosen_strategy == 5:
        attack_result, location = dataManipulation(G_real, self.network, timestep, self.location)
        if attack_result["ids"]:
            # self.compromised_nodes.extend(attack_result["ids"])
            return_value = True
            self.location = location
        else:
            if display: print("attack 6 failed")

    elif self.chosen_strategy == 6:
        attack_result = DoS(G_real, self.network, timestep, self.location)
        if attack_result["ids"]:
            # self.compromised_nodes.extend(attack_result["ids"])
            return_value = True
        else:
            if display: print("attack 7 failed")
    
    elif self.chosen_strategy == 7:
        attack_result = Automated_Exfiltration(G_real, self.network, timestep, self.location, self.compromised_nodes)
        if attack_result["data_exfiltrated"]:
            # self.compromised_nodes.extend(attack_result["ids"])
            return_value = True
        else:
            if display: print("attack 8 failed")
    
        # if attack_result["data_exfiltrated"]:
        #     if display: print("attacker exfiltrate data")
        #     return_value = True
        # else:
        #     if display: print("attack 8 failed")
    if random_strategy == False:
        # print("LOL")
        self.impact_record[self.chosen_strategy] = attack_impact(
            G_real, attack_result["ids"], self.attack_name[self.chosen_strategy])
        
        self.strat_cost = att_strategy_cost(self.strategy_number, G_real, self.location)
    # if attack_result["ids"]:
    # self.location = None
    # node_list = list(G_real.nodes)
    # random.shuffle(node_list)
    # node_list.remove('ccs')
    # for n in node_list:
    #     if G_real.nodes[n]["evicted"]!=0 or G_real.nodes[n]["compromised"]:
    #         continue
    #     self.location = n
    # self.location = random.choice(self.compromised_nodes)
    if display:
        print("Compromised nodes:", self.compromised_nodes)
        print("Scanned node:", self.collection_list)

    return return_value

def attack_impact(G, new_compromised_list, strategy_choosen):
    
    omega = 0.5
    if len(new_compromised_list) == 0:
        return 0
    # print("SDDD")
    # print(new_compromised_list)
    N = G.number_of_nodes()
    
    impact_iss = 0
    total_criticality = 0
    for n in new_compromised_list:
        # print(G.nodes[n]['iss_'+strategy_choosen])
        impact_iss += G.nodes[n]['iss_'+strategy_choosen]
        total_criticality += G.nodes[n]["criticality"]
    ai = total_criticality/N
    
    ai = omega * impact_iss + (1 - omega) * ai

    # impact = 0
    return ai

def update_strategy_probability(opponent_strat_history):
    return_result = np.zeros((len(opponent_strat_history), len(opponent_strat_history[0])))
    sum_botton = np.sum(opponent_strat_history, axis=1)
    for k in range(len(opponent_strat_history)):
        for j in range(len(opponent_strat_history[0])):
            if sum_botton[k] == 0:
                return_result[k][j] = 1/len(opponent_strat_history[0])
            else:
                return_result[k][j] = opponent_strat_history[k][j]/sum_botton[k]
    
    return return_result 
# In[53]:

def attacker_uncertainty_update(att_in_system_time, att_detect, dec, uncertain_scheme, _lambda):
    # _lambda = 0.8 # was 2

    # df = 1 + (1-att_detect) * dec
    uncertainty = 1 - math.exp((-_lambda) * (1)/att_in_system_time)
    
# (scheme change here!) 
    if uncertain_scheme:
        return uncertainty
    else:
        return 0


class attacker_class:
    def __init__(self, game, uncertain_scheme, att_detect_UpBod):
        global attack_name
        # if display: print("create attacker")
        self.network = copy.deepcopy(game.graph.network)  # attacker's view
        # for n in self.network:
        #     print(self.network.nodes[n])
        self.strategy_number = 8
        self.collection_list = []
        self.location = None
        self.impact_record = np.ones(
            self.strategy_number
        )  # attacker believe all strategy have impact initially
        self.strat_cost = att_strategy_cost(self.strategy_number, self.network, self.location)
        self.strat_option = att_strategy_option_matrix(
            game.subgame_number, self.strategy_number)  # Table 4
        self.belief_context = [1 /
                               (game.subgame_number + 1)] * (game.subgame_number + 1)
        self.subgame_position = 0
        self.subgame_number = game.subgame_number
        self.prob_believe_opponent = np.zeros(
            (game.subgame_number + 1,
             6))  # 8 is defender strategy number # c_{\kappa}
        self.obs_oppo_strat_history = np.zeros(
            (game.subgame_number + 1, 6))  # 7 is defender strategy number
        self.in_system_time = 1
        self.monit_time = 1
        self.detect_prob = random.uniform(0, att_detect_UpBod)
        self.chosen_strategy = 0
        self.in_honeynet = False
        self.uncertain_scheme = uncertain_scheme
        if self.uncertain_scheme:
            self.uncertainty = 1  #1  # 100% uncertainty at beginning  (scheme change here!)
        else:
            self.uncertainty = 0
        self.attack_name = attack_name
        self.HEU = np.zeros(self.strategy_number)
        self.compromised_nodes = []
        self.EU_C = None
        self.EU_CMS = None
        self.AHEU = np.zeros(self.strategy_number)
        self.att_guess_DHEU = np.zeros(self.strategy_number)
        self.chosen_strategy_record = np.zeros(self.strategy_number)
        self.defender_observation = np.zeros(self.strategy_number)
        self.att_guess_def_impact = np.ones(self.strategy_number)
        self.observed_defen_strat = 0
        self.defender_strat_cost = def_strategy_cost(self.strategy_number)

    choose_strategy = attacker_class_choose_strategy

    execute_strategy = attacker_class_execute_strategy

    def reset_in_system_time(self):
        self.in_system_time = 1
        return self.in_system_time

    def next_stage(self):
        if self.subgame_position != 2:
            self.subgame_position += 1

    def reset_attribute(self):
        pass

    def observe_opponent(self, defend_subgame, defen_strategy):
        # Observe strategy
        self.obs_oppo_strat_history[defend_subgame, defen_strategy] += 1
        self.observed_defen_strat = defen_strategy
        self.prob_believe_opponent = update_strategy_probability(
            self.obs_oppo_strat_history)
        # print(self.prob_believe_opponent)

    def update_attribute(self, dec, _lambda):
        # monitor time
        self.monit_time += 1
        
        # if in_system
        # if self.subgame_position >= 1:
        self.in_system_time += 1

        # belief context
        self.belief_context[0] = 1 - sum(self.belief_context[1:])

        # uncertainty
        self.uncertainty = attacker_uncertainty_update(self.in_system_time,
                                                       self.detect_prob, dec,
                                                       self.uncertain_scheme, _lambda)
        # HNE Hitting Ratio
        self.defender_observation[self.chosen_strategy] += 1
        self.att_guess_DHEU = self.att_guess_def_EU_C()

    def att_guess_def_EU_C(self):
        # attacker observe itself
        self.chosen_strategy_record[self.chosen_strategy] += 1

        if np.sum(self.defender_observation) == 0:
            strat_prob = np.zeros(self.strategy_number)
        else:
            strat_prob = self.chosen_strategy_record / np.sum(self.chosen_strategy_record)
        xi = 5

        self.att_guess_def_impact[self.observed_defen_strat] = 1 - self.impact_record[self.chosen_strategy]

        utility = np.zeros((self.strategy_number, self.strategy_number))
        for i in range(self.strategy_number):
            for j in range(self.strategy_number):
                utility[i, j] = (self.att_guess_def_impact[i] +
                                 self.strat_cost[j] / 3) - (self.defender_strat_cost[i] / 3 + self.impact_record[j])
        EU_C = np.zeros(self.strategy_number)
        for i in range(self.strategy_number):
            for j in range(self.strategy_number):
                EU_C[i] += strat_prob[j] * utility[i, j]
        # Normalization
        a = 1
        b = 10
        if (max(EU_C) - min(EU_C)) != 0:
            EU_C = a + (EU_C - min(EU_C)) * (b - a) / (max(EU_C) - min(EU_C))
        self.EU_C = EU_C
        return EU_C

    def random_moving(self, G_real):
        # if self.location is None:
        #     return
        
        # node_list = self.compromised_nodes
        node_list = self.collection_list + list(set(self.compromised_nodes) - set(self.collection_list))
        # node_list = self.collection_list + self.compromised_nodes
        
        if len(node_list)==0:
            return

        imp_nodes = []
        iots = []
        for i in node_list:
            if "MEC" in i or "Edge" in i:
                imp_nodes.append(i)
            else:
                iots.append(i)
        # random.shuffle(node_list)
        # node_list.remove('ccs')
        if len(imp_nodes)!=0:
            if random.random() < 0.75:
                self.location = random.choice(imp_nodes)
            elif len(iots)!=0:
                self.location = random.choice(iots)
            else:
                self.location = random.choice(imp_nodes)
        else:
            self.location = random.choice(iots)
        
        # for n in node_list:
        #     if G_real.nodes[n]["evicted"]!=0 or not G_real.nodes[n]["compromised"]:
        #         continue
        #     self.location = n
        # neighbor_list = [i for i in self.network[self.location]]
        # compromised_neighbor_list = [self.location]  # allow attacker stands still
        # for index in neighbor_list:
        #     if self.network.nodes[index]["compromised"]:
        #         compromised_neighbor_list.append(index)

        # self.location = random.choice(compromised_neighbor_list)


    def random_moving_random(self, G_real):
        # if self.location is None:
        #     return
        node_list = self.collection_list + list(set(self.compromised_nodes) - set(self.collection_list))
        # node_list = self.collection_list + self.compromised_nodes
        
        if len(node_list)==0:
            return

        imp_nodes = []
        iots = []
        for i in node_list:
            if "MEC" in i or "Edge" in i:
                imp_nodes.append(i)
            else:
                iots.append(i)
        # random.shuffle(node_list)
        # node_list.remove('ccs')
        if len(imp_nodes)!=0:
            if random.random() < 0.5:
                self.location = random.choice(imp_nodes)
            elif len(iots)!=0:
                self.location = random.choice(iots)
            else:
                self.location = random.choice(imp_nodes)
        else:
            self.location = random.choice(iots)
        # for n in node_list:
        #     if G_real.nodes[n]["evicted"]!=0 or not G_real.nodes[n]["compromised"]:
        #         continue
        #     self.location = n
        # neighbor_list = [i for i in self.network[self.location]]
        # compromised_neighbor_list = [self.location]  # allow attacker stands still
        # for index in neighbor_list:
        #     if self.network.nodes[index]["compromised"]:
        #         compromised_neighbor_list.append(index)

        # self.location = random.choice(compromised_neighbor_list)
