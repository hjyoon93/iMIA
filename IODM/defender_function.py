
import random
import numpy as np
import graph_function
import math
import copy
import attacker_function
from graph_function import *
# np.random.seed(0)
# random.seed(0)
display = False

def def_strategy_cost(strategy_number):
    defend_cost = np.zeros(strategy_number)
    defend_cost[0] = 0.25
    defend_cost[1] = 0.25
    defend_cost[2] = 0.5
    defend_cost[3] = 0.5
    defend_cost[4] = 1
    defend_cost[5] = 1

    
    return defend_cost


def defender_uncertainty_update(att_detect, def_monit_time, def_strategy_number, uncertain_scheme, mu):
    
    uncertainty = 1-math.exp((-mu) *1/def_monit_time)

    if uncertain_scheme:
        return uncertainty
    else:
        return 0


def defender_class_choose_strategy(self, att_choose_strategy, att_strategy_number,
                                   attack_cost_record, attack_impact_record):
    # print(att_strategy_number)
    S_j = np.zeros(att_strategy_number)
    for j in range(att_strategy_number):
        for k in range(self.subgame_number + 1):
            # print(j, k)
            S_j[j] += self.P_subgame[k] * self.prob_believe_opponent[k][j]

    if display: print(f"S_j in def is {S_j}, sum is {sum(S_j)}")

    # eq. 19 (Uncertainty g)
    g = self.uncertainty
    # print(self.impact_record.shape, attack_impact_record[att_choose_strategy+1].shape, self.chosen_strategy, att_choose_strategy)
    # Update defense impact
    if display: print(self.impact_record.shape, self.chosen_strategy, attack_impact_record.shape, att_choose_strategy)
    self.impact_record[self.chosen_strategy] = 1 - attack_impact_record[att_choose_strategy]

    # eq. 17
    utility = np.zeros((self.strategy_number, att_strategy_number))
    for i in range(self.strategy_number):
        for j in range(att_strategy_number):
            utility[i, j] = (self.impact_record[i] +
                          attack_cost_record[j] / 3) - (
                              self.strat_cost[i] / 3 + attack_impact_record[j])
            
    # normalization range
    a = 1
    b = 10
    
    # eq. 8
    EU_C = np.zeros(self.strategy_number)
    for i in range(self.strategy_number):
        for j in range(att_strategy_number):
            # print(i, j)
            # print(EU_C.shape,S_j.shape, utility.shape )
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
#     HEU = np.zeros(self.strategy_number)
#     for index in range(self.strategy_number):
#         HEU[index] = ((1 - g) * EU_C[index]) + (g * EU_CMS[index])
    HEU = EU_C
    self.HEU = HEU  # uncertainty case doesn't consider as real HEU
#     if random.random() > g:
        
#     else:
#         HEU = np.ones(self.strategy_number)


    # eq. 23
    DHEU = np.zeros(self.strategy_number)
    if random.random() > g:
        self.DHEU = HEU
        for index in range(self.strategy_number):
            
            DHEU[index] = HEU[index] * self.strat_option[
                self.subgame_position, index]  # for Table 4
    else:
        HEU = np.ones(self.strategy_number)
        self.DHEU = HEU
        for index in range(self.strategy_number):
            # print(DHEU.shape, HEU.shape, self.strat_option.shape)
            DHEU[index] = HEU[index] * self.strat_option[
                3, index]  # for Table 4
    
    if display: print("DHEU:", DHEU)
    def_chosen_strategy = random.choices(range(self.strategy_number),
                                         weights=DHEU,
                                         k=1)[0]
    
    self.chosen_strategy = def_chosen_strategy
    # if self.chosen_strategy == 4 or self.chosen_strategy == 5 or self.chosen_strategy == 6 or self.chosen_strategy == 7:
        # self.deception_tech_used = True
    self.dec = def_strategy_cost(self.strategy_number)[self.chosen_strategy]
    # else:
    #     self.dec = 0

    return def_chosen_strategy

def dynamicAnalysis(G_real, G_att, G_def, P_da):
    for n in G_real.nodes():
        if random.random() < P_da:
            G_real.nodes[n]["dynamic_analysis"] = True
            G_def.nodes[n]["dynamic_analysis"] = True
    

def softwareUpdate(G_real, G_att, G_def, P_su):

    # for index in range(sv):
    for n in G_real.nodes():
        if random.random() < P_su:
            G_real.nodes[n]["SV"] = max(
                G_real.nodes[n]["SV"] * 0.95, 0)
            G_def.nodes[n]["SV"] = max(
                G_def.nodes[n]["SV"] * 0.95, 0)
        
    # for in G_real.nodes():
    #     G_att.nodes[n]["vulnerability"] = max(
    #         G_att.nodes[n]["vulnerability"] * 0.9, 0)

    # for n in G_real.nodes():

def localFilePermissions(G_real, G_att, G_def):

    for n in G_real.nodes():
        if G_real.nodes[n]["compromised"]:
            G_real.nodes[n]["UV"] = max(
                G_real.nodes[n]["UV"] * 0.95, 0)
            G_def.nodes[n]["UV"] = max(
                G_def.nodes[n]["UV"] * 0.95, 0)
        
    # for in G_real.nodes():
    #     G_att.nodes[n]["vulnerability"] = max(
    #         G_att.nodes[n]["vulnerability"] * 0.9, 0)

    # for n in G_real.nodes():

def Encryption(G_real, G_att, G_def):

    for n in G_real.nodes():
        if random.random() < 1-G_real.nodes[n]["EV"]:
            G_real.nodes[n]["EV"] = max(
                G_real.nodes[n]["EV"] * 0.95, 0)
            G_def.nodes[n]["EV"] = max(
                G_def.nodes[n]["EV"] * 0.95, 0)
        
    # for in G_real.nodes():
    #     G_att.nodes[n]["vulnerability"] = max(
    #         G_att.nodes[n]["vulnerability"] * 0.9, 0)

    # for n in G_real.nodes():
        

def networkTrafficFiletering(G_real, G_att, G_def, attacker_location, t, P_ntf):
    if attacker_location is None:
        return
    if random.random() < P_ntf:
        evict_a_node(attacker_location, G_real, G_def, G_att, t)
        update_criticality(G_real)
        update_criticality(G_att)
        update_criticality(G_def)

def networkTrafficCommunityDeviation(G_real, G_att, G_def, t):
    if random.random()<0.5:
        return 
    FN = 20  # False Negative for Beta distribution
    TP = 80  # True Positive
    TN = 90
    FP = 10
    false_neg_prob = FN / (TP + FN)
    false_pos_prob = FP / (TN + FP)
    Th_risk = 0.3

    #         for index in self.graph.network.nodes:
    all_nodes = list(G_real.nodes(data=False))
    experiment_index_record = 0
    for index in all_nodes:
        if is_node_evicted(G_real,
                            index):  # ignore evicted node for saving time
            continue

        # detect is node compromised
        node_is_compromised = False
        if G_real.has_node(index):
            if G_real.nodes[index]["compromised"]:
                if random.random() > false_neg_prob:
                    node_is_compromised = True
                    G_def.nodes[index]["compromised"] = True
                    experiment_index_record = 0
                else:
                    if display: print("False Negative to compromised node")
            else:
                if random.random() < false_pos_prob:
                    if display: print("False Positive to good node")
                    node_is_compromised = True
                    G_def.nodes[index]["compromised"] = True
                    experiment_index_record = 1

        if node_is_compromised:
            if G_real.has_node(index):
                # if G_real.network.nodes[index]["criticality"] > Th_risk:
                if display:
                    # print("Evict node", index, ", criticality > Th_risk")
                    print(f"Evict node {index}")
                evict_a_node(index, G_real,
                                    G_def,
                                    G_att, t)
                    # self.NIDS_eviction[experiment_index_record] += 1
                    # continue
                # else:
                #     if is_system_fail(self.graph, [None], self.SF_thres_1, self.SF_thres_2):
                #         if display:
                #             print(
                #                 f"Evict node {index}, compromise cause SF")
                #         evict_a_node(index, self.graph.network,
                #                         self.defender.network,
                #                         self.attacker.network)
                #         self.NIDS_eviction[experiment_index_record] += 1



# In[15]:
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

def def_strategy_option_matrix(subgame_number, strategy_number, DD_using):
    strat_option = np.zeros(
        (subgame_number + 1, strategy_number))  # last one is full game
    
    strat_option[0, 0] = 1
    strat_option[0, 1] = 1
    # D
    strat_option[1, 2] = 1
    strat_option[1, 3] = 1
    # E
    strat_option[2, 4] = 1
    strat_option[2, 5] = 1

    
    strat_option[3, 0] = 1
    strat_option[3, 1] = 1
    strat_option[3, 2] = 1
    strat_option[3, 3] = 1
    strat_option[3, 4] = 1
    strat_option[3, 5] = 1

    return strat_option

def defender_class_execute_strategy(self, G_att, graph, attacker_location, t):

    return_value = False
    if self.chosen_strategy == 0:
        dynamicAnalysis(graph.network, G_att, self.network, P_da=0.25)
        return_value = True
    elif self.chosen_strategy == 1:
        softwareUpdate(graph.network, G_att, self.network, P_su=0.25)
        return_value = True
    elif self.chosen_strategy == 2:
        localFilePermissions(graph.network, G_att, self.network)
        return_value = True
    elif self.chosen_strategy == 3:
        Encryption(graph.network, G_att, self.network)
        return_value = True
    elif self.chosen_strategy == 4:
        networkTrafficFiletering(graph.network, G_att, self.network, attacker_location, t, P_ntf=0.25)
        return_value = True
    elif self.chosen_strategy == 5:
        networkTrafficCommunityDeviation(graph.network, G_att, self.network, t)
        return_value = True
    

    return return_value



class defender_class:
    def __init__(self, game, uncertain_scheme):
        if display: print("create defender")
        self.network = copy.deepcopy(game.graph.network)  # defender's view
        self.strategy_number = 6
        self.key_time = 1
        self.monit_time = 1
        self.dec = 0
        self.strat_cost = def_strategy_cost(self.strategy_number)
        self.impact_record = np.ones(self.strategy_number)
        self.P_fake = 0  # fake key for DS7
        self.subgame_position = 4  # 6 means full game
        self.subgame_number = game.subgame_number 
        self.strat_option = def_strategy_option_matrix(
            game.subgame_number, self.strategy_number, game.DD_using)  # Table 4
        self.chosen_strategy = random.randint(0, self.strategy_number)
        self.prob_believe_opponent = np.zeros(
            (game.subgame_number + 1, game.attacker.strategy_number))
        self.obs_oppo_strat_history = np.zeros(
            (game.subgame_number + 1, game.attacker.strategy_number))
        self.P_subgame = np.zeros(game.subgame_number + 1)  # Eq. 5: belief context
        self.subgrame_history = np.zeros(game.subgame_number + 1)
        self.deception_tech_used = False
        self.uncertain_scheme = uncertain_scheme
        if self.uncertain_scheme:
            self.uncertainty = 1  #1 # 100% uncertainty at beginning  (scheme change here!)
        else:
            self.uncertainty = 0
        self.HEU = np.zeros(self.strategy_number)
        self.EU_C = None
        self.EU_CMS = None
        self.DHEU = np.zeros(self.strategy_number)
        self.def_guess_AHEU = np.zeros(self.strategy_number)
        self.chosen_strategy_record = np.zeros(self.strategy_number)
        self.attacker_observation = np.zeros(self.strategy_number)
        self.attacker_strat_cost = attacker_function.att_strategy_cost(7, self.network, None)
        self.defense_name = ["Dynamic Analysis", "Software Update", "Local File Permissions", "Encryption", "Network Traffic Filerting", "NIDS"]
    
    
    def observe_opponent(self, attack_impact_record, attack_subgame,
                         attack_strategy):
        # Observe strategy
        self.obs_oppo_strat_history[attack_subgame, attack_strategy] += 1
        self.prob_believe_opponent = update_strategy_probability(
            self.obs_oppo_strat_history)

        # belief context
        self.subgrame_history[attack_subgame] += 1
        self.P_subgame = self.subgrame_history / (sum(self.subgrame_history))

    def update_attribute(self, att_detect, mu, attack_impact, attack_cost):
        # key_time
        self.key_time += 1
        # monitor time
        self.monit_time += 1
        # uncertainty
        self.uncertainty = defender_uncertainty_update(att_detect,
                                                       self.monit_time,
                                                       self.strategy_number,
                                                       self.uncertain_scheme, mu)
        self.def_guess_AHEU = self.def_guess_att_EU_C(attack_impact)
        self.attacker_observation[self.chosen_strategy] += 1
        self.attacker_strat_cost = attack_cost

    def def_guess_att_EU_C(self, attack_impact):
        # defender observe itself
        self.chosen_strategy_record[self.chosen_strategy] += 1

        if np.sum(self.attacker_observation) == 0:
            strat_prob = np.zeros(self.strategy_number)
        else:
            strat_prob = self.chosen_strategy_record / np.sum(self.chosen_strategy_record)

        utility = np.zeros((self.strategy_number, self.strategy_number))
        for i in range(self.strategy_number):
            for j in range(self.strategy_number):
                utility[i, j] = (attack_impact[i] +
                                 self.strat_cost[j] / 3) - (self.attacker_strat_cost[i] / 3 + self.impact_record[j])
        EU_C = np.zeros(self.strategy_number)
        for i in range(self.strategy_number):
            for j in range(self.strategy_number):
                EU_C[i] += strat_prob[j] * utility[i, j]
        # Normalization
        a = 1
        b = 10
        if (max(EU_C) - min(EU_C)) != 0:
            EU_C = a + (EU_C - min(EU_C)) * (b - a) / (max(EU_C) - min(EU_C))
        return EU_C

    def reset_attribute(self, attack_impact_record, subgame_number):
        self.key_time = 1
        self.monit_time = 1
        self.P_fake = 0
        self.impact_record = np.ones(self.strategy_number)
        self.belief_context = [1 / (subgame_number + 1)] * (subgame_number + 1)
        self.obs_oppo_strat_history = np.zeros((
            self.obs_oppo_strat_history.shape[0], self.obs_oppo_strat_history.shape[1]))
        self.dec = 0
        self.deception_tech_used = False
        if self.uncertain_scheme:
            self.uncertainty = 1  #(scheme change here!)
        else:
            self.uncertainty = 0

    choose_strategy = defender_class_choose_strategy
    execute_strategy = defender_class_execute_strategy

    def decide_subgame_posi(self, att_detect, att_subgame_stage):
        g = self.uncertainty
        # print(g)
        if random.random() > g:
            self.subgame_position = att_subgame_stage
            return True
        else:
            self.subgame_position = 3  # full game
            return False