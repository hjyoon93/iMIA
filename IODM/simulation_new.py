#!/usr/bin/env python
# coding: utf-8


# # solve Jupyter runtime error
# import nest_asyncio
# nest_asyncio.apply()


import concurrent.futures
from curses.ascii import NL
from email.errors import FirstHeaderLineIsContinuationDefect
import multiprocessing
import os
import pandas as pd
import matplotlib.pyplot as plt
   
import matplotlib
matplotlib.use( 'tkagg' )
import networkx as nx
import numpy as np
from itertools import count
import random
import math
import copy
import time
import pickle
from imageai.Detection import ObjectDetection
import os
import matplotlib.pyplot as plt
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
import numpy as np
import skimage.io as io
import pylab
from mean_average_precision import MetricBuilder
import csv
import pandas as pd

from graph_function import *
from attacker_function import *
from defender_function import *
display = False

dataDir='./input/coco/valid'
dataType='val2014'
annFile = '_annotations.coco.json'
cocoGt=COCO(os.path.join(dataDir, annFile))

# np.random.seed(2)
# random.seed(2)
execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path ,'models', "yolov3.pt"))
detector.loadModel()

pylab.rcParams['figure.figsize'] = (10.0, 8.0)

def bb_intersection_over_union(boxA, boxB):
	# determine the (x, y)-coordinates of the intersection rectangle
    # print(boxA, boxB)

    # print(boxA, boxB)
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[0] + boxB[2])
    yB = min(boxA[3], boxB[1] + boxB[3])
	# compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
	# compute the area of both the prediction and ground-truth
	# rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[0] + boxB[2] - boxB[0] + 1) * (boxB[1] + boxB[3] - boxB[1] + 1)
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
	# return the intersection over union value
    return iou

class game_class:
    def __init__(self, simulation_id, DD_using, uncertain_scheme, web_data_upper_vul, vuln, Th_risk, _lambda,
                 mu, SF_thres_1, SF_thres_2, att_detect_UpBod, training, scheme):
        self.lifetime = 1
        self.subgame_number = 3
        self.strategy_number = 7
        self.DD_using = DD_using
        self.iot_sv_mean = vuln
        self.edge_sv_mean = vuln
        self.mec_sv_mean = vuln
        self.iot_ev_mean = vuln
        self.edge_ev_mean = vuln
        self.mec_ev_mean = vuln
        self.iot_uv_mean = vuln
        self.edge_uv_mean = vuln
        self.mec_uv_mean = vuln
        self.vuln_std = 0.05
        if training:
            self.vuln_mean_std = 0.5
        else:
            self.vuln_mean_std = 0
        self.graph = graph_class(self.iot_sv_mean, self.edge_sv_mean, self.mec_sv_mean, self.iot_ev_mean, self.edge_ev_mean, self.mec_ev_mean, self.iot_uv_mean, self.edge_uv_mean, self.mec_uv_mean, self.vuln_std, self.vuln_mean_std)
        # print("LOL")
        self.uncertain_scheme = uncertain_scheme
        self.att_detect_UpBod = att_detect_UpBod
        self.attacker = attacker_class(self, self.uncertain_scheme, self.att_detect_UpBod)
        self.attacker_number = 1
        self.defender = defender_class(self, self.uncertain_scheme)
        self.game_over = False
        self.FN = 10  # False Negative for Beta distribution
        self.TP = 90  # True Positive
        self.TN = 99
        self.FP = 1
        self.scheme = scheme
        

        # self.rewire_network = 0.01
        




        self.def_uncertainty_history = []
        self.att_uncertainty_history = []
        self.pre_attacker_number = 0
        self.att_HEU_history = []
        self.def_HEU_history = []
        self.att_strategy_counter = []
        self.def_strategy_counter = []
        self.FPR_history = []
        self.TPR_history = []
        self.att_cost_history = []
        self.def_cost_history = []
        self.def_per_strat_cost = np.zeros((1,8))
        self.def_succ_counter = np.zeros((6,8))
        self.def_fail_counter = np.zeros((6,8))
        self.criticality_hisotry = np.zeros(100000)  # np.zeros(10000)
        self.evict_reason_history = np.zeros(2)
        self.SysFail = [False] * 3
        self.att_EU_C = np.zeros(8)
        self.att_EU_CMS = np.zeros(8)
        self.def_EU_C = np.zeros(8)
        self.def_EU_CMS = np.zeros(8)
        self.att_impact = np.zeros(8)
        self.def_impact = np.zeros(8)
        self.att_HEU_DD_IPI = np.zeros(8)
        self.def_HEU_DD_IPI = np.zeros(8)
        self.NIDS_eviction = np.zeros(4)  # [# of bad, # of good]
        self.NIDS_Th_risk = Th_risk
        self._lambda = _lambda
        self.mu = mu
        self.SF_thres_1 = SF_thres_1
        self.SF_thres_2 = SF_thres_2
        self.hitting_result = []
        # print("LOL")
        self.test_images = 1000
        self.miou = 0
        self.num_iot = 0
        self.num_edge = 0
        self.num_mec = 0
        self.processed = 0
        self.timely = 0
        self.ious = pd.read_csv('./static/iou_new.csv')
        # print(len(self.ious))
        self.ious.drop_duplicates(subset=None, keep="first", inplace=True)
        # print(len(self.ious))
        # print(self.ious)
        for n in self.graph.network.nodes:
            if "IoT" in n:
                self.num_iot+=1

        for n in self.graph.network.nodes:
            if "Edge" in n:
                self.num_edge+=1
        
        for n in self.graph.network.nodes:
            if "MEC" in n:
                self.num_mec+=1
        
        self.avg_availibility = 0

        self.avg_timeliness = 0
        self.results = None


    def attacker_round(self, simulation_id, t, type="ebm"):
        if display: print(f"attacker location: {self.attacker.location}")
        if self.game_over:
            print(f"Sim {simulation_id} GAME OVER")
            return
        if display:
            print("Attacker Subgame:", self.attacker.subgame_position)
            print("Defender Subgame:", self.defender.subgame_position)
        self.attacker.observe_opponent(self.defender.subgame_position,
                                       self.defender.chosen_strategy)
        if type=='ebm':
            self.attacker.choose_strategy(self.defender.strategy_number,
                                      self.defender.strat_cost,
                                      self.defender.impact_record)
        elif type=='random':
            # weights = [0.3, 0.15, 0.15, 0.15, 0.15, 0.05, 0.05]
            # self.attacker.chosen_strategy = random.choices(np.arange(7), weights = weights, k=1)[0]
            self.attacker.chosen_strategy = np.random.randint(8)
            if self.attacker.chosen_strategy in [0,1,2]:
                self.attacker.subgame_position = 0
            elif self.attacker.chosen_strategy in [3,4]:
                self.attacker.subgame_position = 1
            elif self.attacker.chosen_strategy in [5,6,7]:
                self.attacker.subgame_position = 2
            self.attacker.subgame_position= np.random.randint(3)
        elif type=='path':
            # print('lol')
            # print(self.attacker.in_system_time, self.attacker.in_system_time -1 % 12)
            if (self.attacker.in_system_time - 1) % 9 in [0,1,2]:
                self.attacker.chosen_strategy = random.choice([0,1,2])
                self.attacker.subgame_position = 0
            elif (self.attacker.in_system_time - 1) % 9 in [3,4,5]:
                self.attacker.chosen_strategy = random.choice([0,1,2,3,4])
                self.attacker.subgame_position = 1
            elif (self.attacker.in_system_time - 1) % 9 in [6,7,8]:
                # weights = [0.2, 0.15, 0.15, 0.25, 0.25]
                # self.attacker.chosen_strategy = random.choices([0,1,2,5,6], weights=weights, k=1)[0]
                self.attacker.chosen_strategy = random.choice([0,1,2,5,6,7])
                self.attacker.subgame_position = 2
            # elif (self.attacker.in_system_time - 1) % 11 in [8,9,10]:
            #     self.attacker.chosen_strategy = random.choice([5,6])
            #     self.attacker.subgame_position = 2
            # print(self.attacker.in_system_time)


        if display:
            print(f"attacker choose: {self.attacker.attack_name[self.attacker.chosen_strategy]}")
        attack_result = self.attacker.execute_strategy(
            self.graph.network, self.defender.network, t)
        self.attacker.update_attribute(self.defender.dec, self._lambda)
        self.graph.update_graph(self.defender.network, self.attacker.network)
        if attack_result:
            self.def_succ_counter[self.attacker.subgame_position, self.defender.chosen_strategy] += 1
        else:
            self.def_fail_counter[self.attacker.subgame_position, self.defender.chosen_strategy] += 1
        if self.attacker.location is None:
            self.attacker.random_moving(self.graph.network)
            if display:
                print(f"attacker move, new location: {self.attacker.location}")
        elif attack_result:
            if self.attacker.chosen_strategy == 0:
                pass  # This avoid inside attacker increase stage when Strategy 1 success
            elif self.attacker.chosen_strategy == 7:
                print("Data Exfiltration Success")
                self.new_attacker()
            elif self.attacker.subgame_position == 2:
                self.attacker.random_moving(self.graph.network)
                if display:
                    print(f"attacker move, new location: {self.attacker.location}")
            else:
                # print('lol')
                self.attacker.next_stage()
        else:
            self.attacker.random_moving(self.graph.network)
            if display:
                print(f"attacker move, new location: {self.attacker.location}")

        return attack_result

    def defender_round(self, t):
        self.defender.observe_opponent(self.attacker.impact_record,
                                       self.attacker.subgame_position,
                                       self.attacker.chosen_strategy)
        result = self.defender.decide_subgame_posi(self.attacker.detect_prob,
                                               self.attacker.subgame_position)

        if result:
            if display:
                print("defender guess subgame correct")
        else:
            if display:
                print("defender guess subgame wrong")

        self.defender.choose_strategy(self.attacker.chosen_strategy,
                                      self.attacker.strategy_number,
                                      self.attacker.strat_cost,
                                      self.attacker.impact_record)
        if display:
            print(f"defender choose: {self.defender.chosen_strategy + 1}")
        success = self.defender.execute_strategy(self.attacker.network,
                                                 self.graph,
                                                 self.attacker.location, t)
        self.defender.update_attribute(self.attacker.detect_prob, self.mu, self.attacker.impact_record, self.attacker.strat_cost)
        self.graph.update_graph(self.defender.network, self.attacker.network)

    def attacker_round_random(self, simulation_id, tt):
        if display: print(f"attacker location: {self.attacker.location}")
        # if self.game_over:
        #     print(f"Sim {simulation_id} GAME OVER")
        #     return

        # self.attacker.observe_opponent(self.defender.subgame_position,
        #                                self.defender.chosen_strategy)

        self.attacker.chosen_strategy = np.random.randint(7)
        if display:
            print(f"attacker choose: {self.attacker.attack_name[self.attacker.chosen_strategy]}")
        attack_result = self.attacker.execute_strategy(
            self.graph.network, self.defender.network, tt, random_strategy=True)
        # self.attacker.update_attribute(self.defender.dec, self._lambda)
        self.graph.update_graph(self.defender.network, self.attacker.network)
        # if attack_result:
        #     self.def_succ_counter[self.attacker.subgame_position, self.defender.chosen_strategy] += 1
        # else:
        #     self.def_fail_counter[self.attacker.subgame_position, self.defender.chosen_strategy] += 1
        # if attack_result:
        #     if (self.attacker.chosen_strategy == 0
        #             and self.attacker.subgame_position != 0):
        #         pass  # This avoid inside attacker increase stage when Strategy 1 success
        #     else:
        #         self.attacker.next_stage()
        # else:
        self.attacker.random_moving(self.graph.network)

        if display:
            print(f"attacker move, new location: {self.attacker.location}")

        return attack_result

    def attacker_round_path(self, simulation_id, tt):
        if display: print(f"attacker location: {self.attacker.location}")
        # if self.game_over:
        #     print(f"Sim {simulation_id} GAME OVER")
        #     return

        # self.attacker.observe_opponent(self.defender.subgame_position,
        #                                self.defender.chosen_strategy)
        # print(self.attacker.in_system_time)
        if self.attacker.in_system_time - 1 % 16 in [0,1,2]:
            self.attacker.chosen_strategy = 0
        elif self.attacker.in_system_time - 1 % 16 in [4,5,6]:
            self.attacker.chosen_strategy = 1 if random.random()<0.5 else 2
        elif self.attacker.in_system_time - 1 % 16 in [7,8,9]:
            self.attacker.chosen_strategy = 3 if random.random()<0.5 else 4
        elif self.attacker.in_system_time - 1 % 16 in [10,11,12,13,14,15]:
            self.attacker.chosen_strategy = 5 if random.random()<0.5 else 6
            # elif self.attacker.in_system_time % 21 in []:
            # self.attacker.chosen_strategy = 1

        # self.attacker.chosen_strategy = min(self.attacker.in_system_time % 3, 6)
        if display:
            print(f"attacker choose: {self.attacker.attack_name[self.attacker.chosen_strategy]}")
        attack_result = self.attacker.execute_strategy(
            self.graph.network, self.defender.network, tt, random_strategy=True)
        # self.attacker.update_attribute(self.defender.dec, self._lambda)
        self.graph.update_graph(self.defender.network, self.attacker.network)
        # print(self.attacker.in_system_time)
        self.attacker.in_system_time+=1
        # if attack_result:
        #     self.def_succ_counter[self.attacker.subgame_position, self.defender.chosen_strategy] += 1
        # else:
        #     self.def_fail_counter[self.attacker.subgame_position, self.defender.chosen_strategy] += 1
        # if attack_result:
        #     if (self.attacker.chosen_strategy == 0
        #             and self.attacker.subgame_position != 0):
        #         pass  # This avoid inside attacker increase stage when Strategy 1 success
        #     else:
        #         self.attacker.next_stage()
        # else:
        self.attacker.random_moving(self.graph.network)

        if display:
            print(f"attacker move, new location: {self.attacker.location}")

        return attack_result
    
    def defender_round_random(self, t):
        self.defender.chosen_strategy = np.random.randint(6)
        if display:
            print(f"defender choose: {self.defender.defense_name[self.defender.chosen_strategy]}")
        success = self.defender.execute_strategy(self.attacker.network,
                                                 self.graph,
                                                 self.attacker.location, t)
        self.graph.update_graph(self.defender.network, self.attacker.network)

    def NIDS_detect(self):
        # Warning: False Positive evict too many nodes
        # false negative rate
        false_neg_prob = self.FN / (self.TP + self.FN)
        false_pos_prob = self.FP / (self.TN + self.FP)
        Th_risk = self.NIDS_Th_risk

        #         for index in self.graph.network.nodes:
        all_nodes = list(self.graph.network.nodes(data=False))
        experiment_index_record = 0
        for index in all_nodes:
            if is_node_evicted(self.graph.network,
                               index):  # ignore evicted node for saving time
                continue

            # detect is node compromised
            node_is_compromised = False
            if self.graph.network.has_node(index):
                if self.graph.network.nodes[index]["compromised_status"]:
                    if random.random() > false_neg_prob:
                        node_is_compromised = True
                        self.defender.network.nodes[index]["compromised_status"] = True
                        experiment_index_record = 0
                    else:
                        if display: print("False Negative to compromised node")
                else:
                    if random.random() < false_pos_prob:
                        if display: print("False Positive to good node")
                        node_is_compromised = True
                        self.defender.network.nodes[index]["compromised_status"] = True
                        experiment_index_record = 1

            if node_is_compromised:
                # No-DD means NIDS doesn't remain attacker in system
                if not self.DD_using:
                    if display: print(f"Evict node {index}, No DD using")
                    evict_a_node(index, self.graph.network,
                                 self.defender.network, self.attacker.network)
                    self.NIDS_eviction[experiment_index_record] += 1
                    continue
                if self.graph.network.has_node(index):
                    if self.graph.network.nodes[index]["criticality"] > Th_risk:
                        if display:
                            print(f"Evict node {index}, criticality > Th_risk")
                        evict_a_node(index, self.graph.network,
                                     self.defender.network,
                                     self.attacker.network)
                        self.NIDS_eviction[experiment_index_record] += 1
                        continue
                    else:
                        if is_system_fail(self.graph):
                            if display:
                                print(
                                    f"Evict node {index}, compromise cause SF")
                            evict_a_node(index, self.graph.network,
                                         self.defender.network,
                                         self.attacker.network)
                            self.NIDS_eviction[experiment_index_record] += 1
    
    def update_graph(self):
        self.graph.update_graph()
        self.attacker.update_graph()
        self.defender.update_graph()

    def prepare_for_next_game(self):
        self.lifetime += 1

        # Beta distribution
        # if self.graph.using_honeynet:
        #     self.TP += 5
        #     self.TN += 5

        # else:
        #     if self.defender.chosen_strategy == 4 or self.defender.chosen_strategy == 5 or self.defender.chosen_strategy == 6 or self.defender.chosen_strategy == 7:
        #         self.TP += 5
        #         self.TN += 5

        # rewire graph
        rewire_network(self.graph.network, self.attacker.network,
                       self.defender.network, self.rewire_network)

        # reconnect non-evicted node to server or databse
        node_reconnect(self.graph.network, self.attacker.network,
                       self.defender.network, self.graph.connect_prob)

        # update defender impact
        self.defender.impact_record[
            self.defender.chosen_strategy] = 1 - self.attacker.impact_record[
            self.attacker.chosen_strategy]

        # clean honeypot after each game
        # if self.graph.using_honeynet:
        #     clean_honeynet(self.graph.network, self.attacker.network,
        #                    self.defender.network)
        #     self.graph.using_honeynet = False

        # remove honeypot in comrpomised list
        for index in self.attacker.compromised_nodes:
            if not self.graph.network.has_node(index):
                self.attacker.compromised_nodes.remove(index)
        # remove honeypot in collection list
        for index in self.attacker.collection_list:
            if not self.graph.network.has_node(index):
                self.attacker.collection_list.remove(index)

    def new_attacker(self, simulation_id):
        self.attacker_number += 1
        if display:
            print(
                f"\033[93m Sim {simulation_id} Creating attacker #{self.attacker_number} \033[0m"
            )
        # new attacker
        self.attacker = attacker_class(self, self.uncertain_scheme, self.att_detect_UpBod)
        # reset defender
        self.defender.reset_attribute(self.attacker.impact_record,
                                      self.subgame_number)

    def get_observations(self):
        available = 0
        for n in self.graph.network.nodes:
            if self.graph.network.nodes[n]["available"]:
                print(n, "Unavailable")
            elif self.graph.network.nodes[n]["integrity"] == 0:
                print(n, "Incorrect results")
            else:
                print(n, "Works!!!")

    def init(self):
        
        imgIds=sorted(cocoGt.getImgIds())[:]

        # print(imgIds)
        each = self.test_images//self.num_iot
        # print(each)
        start = 0
        for i in range(self.num_iot):
            for j in range(start, start+each):
                self.graph.network.nodes["IoT"+str(i+1)]["pool"].append([imgIds[j],"IoT"+str(i+1)])
            start=j
        
        # for i in range(self.num_iot):
        #     print(self.graph.network.nodes["IoT"+str(i+1)]["pool"])
        

    def mission_timestep(self, t):
        # for n in self.graph.network.nodes:
            # print(n)
        
        results = []
        available = 0
        poisoned = 0
        self.available = 0
        for n in self.graph.network.nodes:
            
            if 'ccs' in n:
                continue
            
            # if self.graph.network.nodes[n]['evicted']!=0:
            #     print(n)
            # if self.graph.network.nodes[n]['memory']!=1:
            #     print(n, self.graph.network.nodes[n]['memory'], self.graph.network.nodes[n]['cpu'])
            lamda = 0.5 * self.graph.network.nodes[n]['memory'] + 0.5 * self.graph.network.nodes[n]['cpu']
            # print(self.graph.network.nodes[n]['memory'], self.graph.network.nodes[n]['memory'],lamda)
            if lamda == 1:
                self.graph.network.nodes[n]['asset_capacity'] = 1
            else:
                self.graph.network.nodes[n]['asset_capacity'] = np.exp(-0.35/lamda)
            # if self.graph.network.nodes[n]['memory']==0.5:
            # if self.graph.network.nodes[n]['asset_capacity'] <1:
            #     print(t, n, self.graph.network.nodes[n]['asset_capacity'], self.graph.network.nodes[n]["available"])
            # print(self.graph.network.nodes[n]['asset_capacity'])
            # self.graph.network.nodes[n]['asset_capacity'] = self.graph.network.nodes[n]['asset_capacity'] * np.exp(-t * self.graph.network.nodes[n]['lamda'] / 25000)
            # results.append({"node":n +"_AC", "success": 1 if self.graph.network.nodes[n]['asset_capacity']>0.75 else 0})
            # print(results)
            self.defender.network.nodes[n]["compromised"] = False
            if self.graph.network.nodes[n]["available"] != 0:
                # print(n, t, self.graph.network.nodes[n]["available"], self.graph.network.nodes[n]["asset_capacity"])
                if t - self.graph.network.nodes[n]["available"] >= 5:
                    self.graph.network.nodes[n]["available"] = 0
                    self.attacker.network.nodes[n]["available"] = 0
                    self.graph.network.nodes[n]['memory'] = 1
                    self.graph.network.nodes[n]['cpu'] = 1
                    self.attacker.network.nodes[n]['memory'] = 1
                    self.attacker.network.nodes[n]['cpu'] = 1
            
            if self.graph.network.nodes[n]["poisoned"] != 0:
                # print(n,"Poisoned for:", t - self.graph.network.nodes[n]["poisoned"])
                if t - self.graph.network.nodes[n]["poisoned"] >= 20:
                    self.graph.network.nodes[n]["poisoned"] = 0
                    self.attacker.network.nodes[n]["poisoned"] = 0
                    # print(n,"Poisoned for:", t - self.graph.network.nodes[n]["poisoned"])
            
            # if self.graph.network.nodes[n]["poisoned"] == 0:
                
            if self.graph.network.nodes[n]["evicted"] != 0:
                if t - self.graph.network.nodes[n]["evicted"] >= 5:
                    self.graph.network.nodes[n]["evicted"] = 0
                    self.defender.network.nodes[n]["evicted"] = 0
                    self.attacker.network.nodes[n]["evicted"] = 0
                    self.graph.network.nodes[n]['memory'] = 1
                    self.graph.network.nodes[n]['cpu'] = 1
                    self.attacker.network.nodes[n]['memory'] = 1
                    self.attacker.network.nodes[n]['cpu'] = 1

            if self.graph.network.nodes[n]["dynamic_analysis"]:    
                self.graph.network.nodes[n]["dynamic_analysis"] = False
                self.defender.network.nodes[n]["dynamic_analysis"] = False
            
            if self.graph.network.nodes[n]['available']==0 and self.graph.network.nodes[n]['evicted']==0 and self.graph.network.nodes[n]['poisoned']==0:
                self.available += 1
            if self.graph.network.nodes[n]['poisoned']!=0:
                poisoned = 1
            # else:
            #     print()
            #     print(n, self.graph.network.nodes[n]['available'], self.graph.network.nodes[n]['evicted'], self.graph.network.nodes[n]['poisoned'])
        # print("Available:", available)
        res_cnt = 0
        rtt = 0
        
        or_iot_edge = [0]*self.num_edge
        or_edge_mec = [0]*self.num_mec
        or_mec_obj = 0
        or_edge_iot = 0
        timely = 0
        processed = 0
        miou = 0
        zero_miou = 0
        miou_cnt = 0
        for i in range(self.num_iot):
            if self.graph.network.nodes["IoT"+str(i+1)]["available"] == 0 and self.graph.network.nodes["IoT"+str(i+1)]["evicted"] == 0:
                
                results.append({"node":"IoT"+str(i+1)+"_asset", "success": 1})
                # results.append({"node":"IoT"+str(i+1)+"_service", "success": 0})
                # or_iot = 0
                # continue
                # if random.random() <
                if random.random() < self.graph.network.nodes["IoT"+str(i+1)]["asset_capacity"]:
                    
                    results.append({"node":"IoT"+str(i+1)+"_Edge_service", "success": 1})
                    results.append({"node":"IoT"+str(i+1)+"_Edge", "success": 1})
                    or_iot_edge[int(np.floor(i/2))] += 1
                    if len(self.graph.network.nodes["IoT"+str(i+1)]["pool"]) !=0:
                        if len(self.graph.network.nodes[list(self.graph.network.edges("IoT"+str(i+1)))[0][1]]["recieved"]) >=10:
                            continue
                        id = self.graph.network.nodes["IoT"+str(i+1)]["pool"].pop(0)
                        # msg = [id, t]
                        id.insert(0, t)
                        # self.graph.network.nodes[list(self.graph.network.edges("IoT"+str(i+1)))[0][1]]["recieved"].append(t)
                        # print("IoT"+str(i+1),list(self.graph.network.edges("IoT"+str(i+1))))
                        self.graph.network.nodes[list(self.graph.network.edges("IoT"+str(i+1)))[0][1]]["recieved"].append(id)

                    if len(self.graph.network.nodes["IoT"+str(i+1)]["recieved"]) !=0:
                        # results.append({"node":"IoT"+str(i+1)+"_Edge", "success": 1})
                        while len(self.graph.network.nodes["IoT"+str(i+1)]["recieved"])!=0:
                            # res_cnt+=1
                            result = self.graph.network.nodes["IoT"+str(i+1)]["recieved"].pop(0)
                            # print("Res", t- result[1])
                            # res_cnt +=1
                            # print("Res cnt:", res_cnt)
                            # if i+1 == 13:
                            # print("IoT"+str(i+1), t-result[1])
                            if t-result[1] < 20:
                                timely += 1
                                self.timely += 1
                            # print(result)
                            self.processed += 1
                            processed+=1
                            # print(result)
                            self.miou += result[0]
                    # else:
                    #     results.append({"node":"IoT"+str(i+1)+"_Edge", "success": 0})
                else:
                    results.append({"node":"IoT"+str(i+1)+"_Edge_service", "success": 0})
                    results.append({"node":"IoT"+str(i+1)+"_Edge", "success": 0})
                    # print("Res", t - result[1])
                    # print("Res", result)
                    # print(len(self.graph.network.nodes["IoT"+str(i+1)]["pool"]), len(self.graph.network.nodes[list(self.graph.network.edges("IoT"+str(i+1)))[0][1]]["recieved"]))
            else:
                results.append({"node":"IoT"+str(i+1)+"_asset", "success": 0})
                results.append({"node":"IoT"+str(i+1)+"_Edge_service", "success": 0})
                results.append({"node":"IoT"+str(i+1)+"_Edge", "success": 0})
        for i in range(self.num_edge):
            if self.graph.network.nodes["Edge"+str(i+1)]["available"] == 0 and self.graph.network.nodes["Edge"+str(i+1)]["evicted"] == 0:
                results.append({"node":"Edge"+str(i+1)+"_asset", "success": 1})
                if random.random() < self.graph.network.nodes["Edge"+str(i+1)]["asset_capacity"]:
                    results.append({"node":"Edge"+str(i+1)+"_MEC_service", "success": 1})
                    results.append({"node":"Edge"+str(i+1)+"_MEC", "success": 1})
                    or_edge_mec[int(np.floor(i/2))] += 1
                    if len(self.graph.network.nodes["Edge"+str(i+1)]["recieved"]) !=0:
                        # results.append({"node":"Edge"+str(i+1)+"_MEC", "success": 1})
                        for j in list(self.graph.network.edges("Edge"+str(i+1))):
                            if "MEC" in j[1]:
                                break
                        # if self.graph.network.nodes[j[1]]["32zxrftm"] != 0:
                        # print(j[1])
                        id = self.graph.network.nodes["Edge"+str(i+1)]["recieved"].pop(0)
                        id.append("Edge"+str(i+1))
                        # print(id)
                        # print(self.graph.network.nodes[j[1]])
                        self.graph.network.nodes[j[1]]['recieved'].append(id)
                    # else:
                    #     results.append({"node":"Edge"+str(i+1)+"_MEC", "success": 0})
                else:
                    results.append({"node":"Edge"+str(i+1)+"_MEC_service", "success": 0})
                    results.append({"node":"Edge"+str(i+1)+"_MEC", "success": 0})
  
                    # self.graph.network.nodes[j[1]]["recieved"].append(id)
                if random.random() < self.graph.network.nodes["Edge"+str(i+1)]["asset_capacity"]:
                    results.append({"node":"Edge"+str(i+1)+"_IoT_service", "success": 1})
                    results.append({"node":"Edge"+str(i+1)+"_IoT", "success": 1})
                    or_edge_iot += 1
                    if len(self.graph.network.nodes["Edge"+str(i+1)]["pool"]) !=0:
                        # results.append({"node":"Edge"+str(i+1)+"_IoT", "success": 1})
                        iot = self.graph.network.nodes["Edge"+str(i+1)]['pool'][0][3]
                        # if self.graph.network.nodes[iot]["available"] != 0:
                        #     continue
                        id = self.graph.network.nodes["Edge"+str(i+1)]["pool"].pop(0)
                        # iot = id[2]
                        self.graph.network.nodes[iot]["recieved"].append(id)
                    # else:
                    #     results.append({"node":"Edge"+str(i+1)+"_IoT", "success": 0})
                else:
                    results.append({"node":"Edge"+str(i+1)+"_IoT_service", "success": 0})
                    results.append({"node":"Edge"+str(i+1)+"_IoT", "success": 0})
            else:
                results.append({"node":"Edge"+str(i+1)+"_service", "success": 0})
                results.append({"node":"Edge"+str(i+1)+"_MEC", "success": 0})  
                results.append({"node":"Edge"+str(i+1)+"_IoT", "success": 0})

        for i in range(self.num_mec):
            if self.graph.network.nodes["MEC"+str(i+1)]["poisoned"] == 0:
                or_mec_obj += 1
                results.append({"node":"MEC"+str(i+1)+"_obj", "success": 1})
            else:    
                results.append({"node":"MEC"+str(i+1)+"_obj", "success": 0})
                
            if self.graph.network.nodes["MEC"+str(i+1)]["available"] == 0 and self.graph.network.nodes["MEC"+str(i+1)]["evicted"] == 0:
                results.append({"node":"MEC"+str(i+1)+"_asset", "success": 1})
                if random.random() < self.graph.network.nodes["MEC"+str(i+1)]["asset_capacity"]:
                    results.append({"node":"MEC"+str(i+1)+"_obj_service", "success": 1})
                    # results.append({"node":"MEC"+str(i+1)+"_", "success": 1})
                    l = 2
                    while l>0 and len(self.graph.network.nodes["MEC"+str(i+1)]["recieved"]) !=0:
                        # print('lol0') 
                        if len(self.graph.network.nodes["MEC"+str(i+1)]["recieved"]) !=0:
                            # print("lol")
                            # print(self.graph.network.nodes["MEC"+str(i+1)]["recieved"])
                            testimg = self.graph.network.nodes["MEC"+str(i+1)]["recieved"].pop(0)
                            # print(self.ious.loc[self.ious['ID'] == testimg[1]].values[0][1])
                            if len(self.ious.loc[self.ious['ID'] == testimg[1]]) == 0:
                                maxiou = 0
                            else:
                                if self.graph.network.nodes["MEC"+str(i+1)]["poisoned"] !=0:
                                    maxiou = 0
                                    zero_miou+=1
                                else:
                                    maxiou = self.ious.loc[self.ious['ID'] == testimg[1]].values[0][1]
                            miou += maxiou
                            miou_cnt += 1
                            testimg.insert(0, maxiou)
                            self.graph.network.nodes["MEC"+str(i+1)]["pool"].append(testimg)
                            # print(testimg)
                            
                            if len(self.graph.network.nodes["MEC"+str(i+1)]["recieved"]) !=0:
                                testimg = self.graph.network.nodes["MEC"+str(i+1)]["recieved"].pop(0)
                                # print(testimg)
                                if len(self.ious.loc[self.ious['ID'] == testimg[1]].values) ==0:

                                    maxiou = 0
                            # img = cocoGt.loadImgs(testimg[1])[0]
                            # annotation_id = cocoGt.getAnnIds(imgIds=testimg[1])
                            # # print(imgId)

                            # ann = cocoGt.loadAnns(annotation_id)
                            # # print(img)
                            
                            # detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path, 'input' , 'coco', 'valid', img['file_name']), output_image_path=os.path.join(execution_path , "imagenew.jpg"), minimum_percentage_probability=30)
                            # # for a in ann:
                            # #     print(a)
                            # # print(testimg)
                            # # print(detections)
                            # if len(detections) == 0:
                            #     continue
                            # # results = []
                            # maxarea = 0
                            # maxbox = 0
                            # # cnt +=1
                            # for eachObject in detections:
                            #     if self.graph.network.nodes["MEC"+str(i+1)]["poisoned"] != 0:
                            #         eachObject['box_points'][0] = 0
                            #         eachObject['box_points'][1] = 0
                            #         eachObject['box_points'][2] = 0
                            #         eachObject['box_points'][3] = 0
                            #     if (eachObject['box_points'][2] - eachObject['box_points'][0]) * (eachObject['box_points'][3] - eachObject['box_points'][1]) >= maxarea:
                            #         maxarea = (eachObject['box_points'][2] - eachObject['box_points'][0]) * (eachObject['box_points'][3] - eachObject['box_points'][1])
                            #         maxbox = eachObject['box_points']
                            # maxiou = 0
                            # for a in ann:
                            #     maxiou = max(maxiou, bb_intersection_over_union(maxbox, a['bbox']))
                            # re = dict()
                            # re['ID'] = testimg[1]
                            # re['iou'] = maxiou
                            # testimg.insert(0, maxiou)
                            # # self.graph.network.nodes["MEC"+str(i+1)]["pool"].append(testimg)
                            # with open('iou_new.csv','a') as f:
                            #     w =  csv.DictWriter(f, re.keys())
                            #     w.writerow(re)
                            # # self.miou += maxiou
                            # # print(len(self.graph.network.nodes["MEC"+str(i+1)]["pool"]))
                            # self.graph.network.nodes["MEC"+str(i+1)]["pool"].append(testimg)
                                    # print(testimg)
                                    # print(len(self.graph.network.nodes["MEC"+str(i+1)]["pool"]))
                                else:
                                    if self.graph.network.nodes["MEC"+str(i+1)]["poisoned"] !=0:
                                        maxiou = 0
                                        zero_miou+=1
                                    else:
                                        maxiou = self.ious.loc[self.ious['ID'] == testimg[1]].values[0][1]
                                miou += maxiou
                                miou_cnt += 1
                                testimg.insert(0, maxiou)
                                self.graph.network.nodes["MEC"+str(i+1)]["pool"].append(testimg)
                        l-=1
                else:
                    results.append({"node":"MEC"+str(i+1)+"_obj_service", "success": 0})
                    # if self.graph.network.nodes["MEC"+str(i+1)]["poisoned"] != 0:
                    #     results.append({"node":"MEC"+str(i+1)+"_obj", "success": 0})
                    # else:
                    #     results.append({"node":"MEC"+str(i+1)+"_obj", "success": 1})
                #     results.append({"node":"MEC"+str(i+1)+"_obj", "success": 0})
                        # accuracy += maxiou
                        # print(maxiou)
                
                if random.random() < self.graph.network.nodes["MEC"+str(i+1)]["asset_capacity"]:
                    # results.append({"node":"MEC"+str(i+1)+"_Edge"+str(2*i+2), "success": 1})
                    results.append({"node":"MEC"+str(i+1)+"_Edge_service", "success": 1})
                    results.append({"node":"MEC"+str(i+1)+"_Edge", "success": 1})
                    b = 2
                    while b>0 and len(self.graph.network.nodes["MEC"+str(i+1)]["pool"]) !=0:
                        # print('lol', b)
                        b-=1
                        if len(self.graph.network.nodes["MEC"+str(i+1)]["pool"]) !=0:
                            # print(self.graph.network.nodes["MEC"+str(i+1)]["pool"][0])
                            edge = self.graph.network.nodes["MEC"+str(i+1)]["pool"][0][4]
                            if self.graph.network.nodes[edge]['available'] !=0:
                                continue
                            res = self.graph.network.nodes["MEC"+str(i+1)]["pool"].pop(0)
                            # edge = res[3]
                            res.pop(4)
                            self.graph.network.nodes[edge]["pool"].append(res)
                            if len(self.graph.network.nodes["MEC"+str(i+1)]["pool"]) !=0:
                                # results.append({"node":"MEC"+str(i+1)+"_Edge", "success": 1})
                                edge = self.graph.network.nodes["MEC"+str(i+1)]["pool"][0][4]
                                if self.graph.network.nodes[edge]['available'] !=0:
                                    continue
                                res = self.graph.network.nodes["MEC"+str(i+1)]["pool"].pop(0)
                                # edge = res[3]
                                res.pop(4)
                                self.graph.network.nodes[edge]["pool"].append(res)
                            # else:
                            #     break
                    # if b==2:
                    #     results.append({"node":"MEC"+str(i+1)+"_Edge", "success": 0})
                    # else:
                    #     results.append({"node":"MEC"+str(i+1)+"_Edge", "success": 1})
                        
                else:
                    results.append({"node":"MEC"+str(i+1)+"_Edge_service", "success": 0})
                    results.append({"node":"MEC"+str(i+1)+"_Edge", "success": 0})
            else:
                results.append({"node":"MEC"+str(i+1)+"_asset", "success": 0})
                results.append({"node":"MEC"+str(i+1)+"_obj_service", "success": 0})
                results.append({"node":"MEC"+str(i+1)+"_Edge_service", "success": 0})
                # results.append({"node":"MEC"+str(i+1)+"_obj", "success": 0})
                # if self.graph.network.nodes["MEC"+str(i+1)]["poisoned"] != 0:
                #     results.append({"node":"MEC"+str(i+1)+"_obj", "success": 0})
                # else:
                #     results.append({"node":"MEC"+str(i+1)+"_obj", "success": 1})
                results.append({"node":"MEC"+str(i+1)+"_Edge", "success": 0})
                # print(j[1], len(self.graph.network.nodes["Edge"+str(i+1)]["recieved"]))
                # print()
                # print(len(self.graph.network.nodes[j[1]]["recieved"]))
        
        # for n in self.graph.network.nodes:
            # print(n, "Pool:", len(self.graph.network.nodes[n]["pool"]), "Recieved:", len(self.graph.network.nodes[n]["recieved"]))
        # for i in or_iot_edge:
        #     print(i)
        # print(or_iot_edge)
        edge_mec_cnt = 0
        edge_iot_cnt = 0
        iot_cnt = 0
        mec_cnt = 0
        mec_obj = 0
        edge_iot_service = 0
        edge_mec_service = 0
        mec_obj_service = 0
        mec_edge_service = 0
        iot_service = 0
        for r in results:
            if r['success']==1:
                if '_Edge' in r['node'] and 'IoT' in r['node']:
                    iot_cnt+=1
                if '_MEC' in r['node']:
                    edge_mec_cnt+=1
                if '_IoT' in r['node']:
                    edge_iot_cnt+=1
                if '_Edge' in r['node'] and 'MEC' in r['node']:
                    mec_cnt+=1
                if '_obj' in r['node']:
                    mec_obj+=1
                if 'IoT_service' in r['node'] and 'Edge' in r['node']:
                    edge_iot_service+=1
                if 'MEC_service' in r['node'] and 'Edge' in r['node']:
                    edge_mec_service+=1
                if 'obj_service' in r['node'] and 'MEC' in r['node']:
                    mec_obj_service+=1
                if 'Edge_service' in r['node'] and 'MEC' in r['node']:
                    mec_edge_service+=1
                if 'Edge_service' in r['node'] and 'IoT' in r['node']:
                    iot_service+=1     
        # print("IoT service:", iot_service)
        # print("Edge MEC service:", edge_mec_service)
        # print("Edge IoT service:", edge_iot_service)
        # print("MEC obj service:", mec_obj_service)
        # print("MEC Edge service:", mec_edge_service)
        # print("IoT service:", iot_service)
        # if processed!=0:
        # print("Edge MEC send:", edge_mec_cnt)
        # print("Edge IoT send:", edge_iot_cnt)
        # print("IoT send:", iot_cnt)
        # print("MEC send:", mec_cnt)
        # print("Object Detection:", mec_obj)
        # print("Availibility:", self.available/35)
        # print("Edge Service:", edge_service)
        # print("MEC Service:", mec_service)
        # print("IoT Service:", iot_service)
        # print("Timeliness:", timely/(processed+0.001), timely, processed)
        # # print("Old Timeliness:", self.timely/(self.processed+1))
        # if poisoned:
        #     print("Poisoned MIOU:", miou/(miou_cnt+0.001), miou_cnt, zero_miou)
        # else:
        #     print("Non Poisoned MIOU:", miou/(miou_cnt+0.001), miou_cnt, zero_miou)
        # print("Old MIOU:", self.miou/(self.processed+0.001))
        # for r in results:
        #     print(r['node'], ":", r['success'], end=' ')
        or_iot_edge_cnt = 0
        for i in range(len(or_iot_edge)):
            results.append({"node":"OR_Edge"+str(i+1), "success": 0 if or_iot_edge[i]!=2 else 1})
            if or_iot_edge[i]==2:
                or_iot_edge_cnt += 1
        or_edge_mec_cnt = 0
        for i in range(len(or_edge_mec)):
            results.append({"node":"OR_MEC"+str(i+1), "success": 0 if or_edge_mec[i]!=2 else 1})
            if or_edge_mec[i]==2:
                or_edge_mec_cnt += 1   
        # results.append({"node":"Edge_MEC_OR", "success": 1 if mec_service>=4 else 0})
        # results.append({"node":"IoT_Edge_OR", "success": 1 if iot_service>=19 else 0})
        results.append({"node":"IoT_Edge_OR", "success": 1 if iot_service>=18 else 0})
        results.append({"node":"Edge_MEC_OR", "success": 1 if edge_mec_service>9 else 0})
        results.append({"node":"MEC_obj_OR", "success": 1 if mec_obj_service>4 else 0})
        results.append({"node":"MEC_Edge_OR", "success": 1 if mec_edge_service>4 else 0})
        results.append({"node":"Edge_IoT_OR", "success": 1 if edge_iot_service>9 else 0})
        # results.append({"node":"Edge_IoT_OR", "success": 1 if edge_iot_service>=9 else 0})
        results.append({"node":"Obj_OR", "success": 1 if or_mec_obj>4 else 0})
        # results.append({"node":"Edge_iot_OR", "success": 1 if edge_service>=9 else 0})
        # results.append({"node":"AND", "success": 1 if or_mec_obj>=2 and or_edge_iot>=5 else 0})
        # timeliness = self.timely/(self.processed + 0.001) if self.timely != 0 else 1
        # mission_performance = self.miou/self.processed if self.miou != 0 else 1
        # print(self.miou, self.processed)
        # results.append({"node":"timeliness", "success": 1 if timeliness>0.875 else 0})
        # results.append({"node":"mission_performance", "success": 1 if mission_performance>0.75 else 0}) 
        timeliness = (edge_iot_service + edge_mec_service + mec_obj_service + mec_edge_service + iot_service)/50
        # timeliness = (edge_iot_service + edge_mec_service + mec_obj_service + mec_edge_service + iot_service)/50
        # print("Timeliness:", timeliness)
        # availability  = self.available/35
        # self.avg_availibility += (edge_iot_service + edge_mec_service + mec_obj_service + mec_edge_service + iot_service)/50
        self.avg_timeliness += timeliness
        # print(self.available, availability) 
        # self.timely = timely
        # self.processed = processed
        mission_performance = miou/(miou_cnt+0.001) if miou_cnt != 0 else 1
        # print(mission_performance, self.miou/(self.processed+0.001), zero_miou)
        results.append({"node":"timeliness", "success": 1 if timeliness>0.80 else 0})
        # results.append({"node":"mission_performance", "success": 1 if mission_performance>0.65 else 0}) 
        # results.append({"node":"timeliness", "success": 1 if availability>0.9 else 0})
        results.append({"node":"mission_performance", "success": 1 if mission_performance>0.75 else 0})
        success = 0 if timeliness<0.8 or mission_performance<0.75 else 1
        results.append({"node":"mission", "success": success})
        # if len(results)!=104:
        #     print(len(results))
        #     print(results)
        resu = dict()
        # print(results)
        for r in results:
            resu[str(r["node"])] = r["success"]
        if self.results is None:
            self.results = resu
        else:
            for key in self.results:
                if key in resu:
                    self.results[key] += resu[key]
                else:
                    pass
        # resu = dict(resu)
        # print(res)
        # results = dict(results)
        # somedict = dict(raymond='red', rachel='blue', matthew='green')
        # with open('./results/training_path.csv','a') as f:
        #     w =  csv.DictWriter(f, res.keys())
        #     w.writeheader()
        # with open('ebm_train.csv','a') as f:
            # print(resu.keys())
            # w =  csv.DictWriter(f, resu.keys())
            # if t>5 and 0 in res:
            # w.writerow(res)
            # res = dict(res)
            # print(res.items())
        # with open('test_fin.csv','a') as f:    
        #     w =  csv.DictWriter(f, resu.keys())
            # w.writeheader()
            # w.writerow(resu)
        return rtt, res_cnt

    def mission_completed(self):
        for n in self.graph.network.nodes:
            if len(self.graph.network.nodes[n]["pool"]) !=0 or len(self.graph.network.nodes[n]["recieved"]) !=0:
                return False
            
        return True
        
    def experiment_saving(self):
        self.def_uncertainty_history.append(self.defender.uncertainty)
        self.att_uncertainty_history.append(self.attacker.uncertainty)

        # Att/Def HEU
        self.att_HEU_history.append(
            self.attacker.HEU[self.attacker.chosen_strategy])
        self.def_HEU_history.append(
            self.defender.HEU[self.defender.chosen_strategy])
        # Att/Def Strategy
        self.att_strategy_counter.append(self.attacker.chosen_strategy)
        self.def_strategy_counter.append(self.defender.chosen_strategy)
        # FP & TP for ROC curve
        self.FPR_history.append(1 - self.TN /
                                (self.TN + self.FP))  # FPR using preset value
        self.TPR_history.append(1 - self.FN / (self.FN + self.TP))
        # Att/Def Cost
        self.att_cost_history.append(
            self.attacker.strat_cost[self.attacker.chosen_strategy])
        self.def_cost_history.append(
            self.defender.strat_cost[self.defender.chosen_strategy])
        def_cost_temp = np.zeros(8)
        def_cost_temp[self.defender.chosen_strategy] = self.defender.strat_cost[self.defender.chosen_strategy]

        self.def_per_strat_cost = np.append(self.def_per_strat_cost, np.reshape(def_cost_temp, (1, -1)), axis=0)


        # Criticality
        criti_list = (np.array(
            list(
                nx.get_node_attributes(self.graph.network,
                                       "criticality").values())) *
                      1000).astype(int)
        for value in criti_list:
            self.criticality_hisotry[value] += 1
        # EU_C & EU_CMS
        self.att_EU_C = np.vstack((self.att_EU_C, self.attacker.EU_C))
        self.att_EU_CMS = np.vstack((self.att_EU_CMS, self.attacker.EU_CMS))
        self.def_EU_C = np.vstack((self.def_EU_C, self.defender.EU_C))
        self.def_EU_CMS = np.vstack((self.def_EU_CMS, self.defender.EU_CMS))
        # attacker/defender impact
        self.att_impact = np.vstack(
            (self.att_impact, self.attacker.impact_record))
        self.def_impact = np.vstack(
            (self.def_impact, self.defender.impact_record))
        # HEU in DD IPI
        self.att_HEU_DD_IPI = np.vstack(
            (self.att_HEU_DD_IPI, self.attacker.HEU))
        self.def_HEU_DD_IPI = np.vstack(
            (self.def_HEU_DD_IPI, self.defender.HEU))

        # Hitting Ratio
        hit = False
        att_AHEU_str_index = random.choice(np.where(self.attacker.AHEU == max(self.attacker.AHEU))[0])
        att_DHEU_str_index = random.choice(np.where(self.attacker.att_guess_DHEU == max(self.attacker.att_guess_DHEU))[0])

        def_AHEU_str_index = random.choice(np.where(self.defender.def_guess_AHEU == max(self.defender.def_guess_AHEU))[0])
        # def_DHEU_str_index = random.choice(np.where(attacker.defender_HEU == max(attacker.defender_HEU))[0])
        def_DHEU_str_index = random.choice(np.where(self.defender.DHEU == max(self.defender.DHEU))[0])
        if att_AHEU_str_index == def_AHEU_str_index and att_DHEU_str_index == def_DHEU_str_index:
            self.hitting_result.append(True)
        else:
            self.hitting_result.append(False)


def is_system_fail(G):
    total = len(list(G.nodes))
    evicted = 0
    for n in G.nodes:
        if G.node[n]["evicted"]:
            evicted += 1
        
    if evicted/total > 70:
        return True
    return False



def game_start(t, simulation_id=0,
               DD_using=True,
               uncertain_scheme=True,
               web_data_upper_vul=7,
               Iot_upper_vul=5, Th_risk=0.3, _lambda=1, mu=8, SF_thres_1=1 / 3, SF_thres_2=1 / 2, att_detect_UpBod=0.5, scheme='ebm'):
    print(
        f"Start Simulation {simulation_id}, DD_using={DD_using}, uncertain_scheme={uncertain_scheme}, web_data_upper_vul={web_data_upper_vul}, Iot_upper_vul={Iot_upper_vul}"
    )
    np.seterr(divide='ignore',
              invalid='ignore')  # for remove divide zero warning

    # game_continue = True
    vuln = Iot_upper_vul
    game = game_class(simulation_id, DD_using, uncertain_scheme,
                      web_data_upper_vul, vuln, Th_risk, _lambda, mu, SF_thres_1, SF_thres_2, att_detect_UpBod, False, scheme)
    # print("Lol")
    game.init()
    tt = 0
    # print("lol")
    # for k in range(game.num_iot):
    #     print("IoT"+str(k+1), len(game.graph.network.nodes["IoT"+str(k+1)]["pool"]), len(game.graph.network.nodes["IoT"+str(k+1)]["recieved"]))
    # while (not game.game_over):
    # print(game.graph.network.edges)
    available_list = []
    timeliness_list = []
    while tt<5000:
        # print(game.lifetime)
        # if display:
        #     print(f"attacker subgame: {game.attacker.subgame_position + 1}")
        # print("Timestep", tt, "Processed:", game.processed)
        # for k in range(game.num_iot):
        #     print("IoT"+str(k+1), len(game.graph.network.nodes["IoT"+str(k+1)]["pool"]), len(game.graph.network.nodes["IoT"+str(k+1)]["recieved"]))
        # for k in range(game.num_edge):
        #     print("Edge"+str(k+1), len(game.graph.network.nodes["Edge"+str(k+1)]["pool"]), len(game.graph.network.nodes["Edge"+str(k+1)]["recieved"]))
        # for k in range(game.num_mec):
        #     print("MEC"+str(k+1), len(game.graph.network.nodes["MEC"+str(k+1)]["pool"]), len(game.graph.network.nodes["MEC"+str(k+1)]["recieved"]))
        game.available = 0
        rtt, res_cnt = game.mission_timestep(tt)
        
        # print("RTT and Count:", tt, rtt/(res_cnt+1))
        # print("mIoU:", game.miou/(game.processed + 1))
        # print("Timeliness:", game.timely/(game.processed + 1))
        # with open('./iou/'+scheme+'_mIoU_'+str(t)+'.csv','a') as f:
        #     w =  csv.DictWriter(f, ["timestep", "meanIoU"])
        #     w.writerow({"timestep":tt, "meanIoU": game.miou/(game.processed + 1)})
        # with open('./timeliness_lol/'+scheme+'_timely'+str(t)+'.csv','a') as f:
        #     w =  csv.DictWriter(f, ["timestep", "Timeliness"])
        #     w.writerow({"timestep": tt, "Timeliness": game.timely/(game.processed + 1)})
        # with open('./availability.csv','a') as f:
        #     w =  csv.DictWriter(f, ["timestep", "Availability"])
        #     w.writerow({"timestep": tt, "Availability": game.available/35})

        # with open('./timeliness.csv','a') as f:
        #     w =  csv.DictWriter(f, ["timestep", "Timeliness"])
        #     w.writerow({"timestep": tt, "Timeliness": game.timely/(game.processed + 0.001)})

        available_list.append(game.available/35)
        timeliness_list.append(0.95)
        evicted = 0
        for n in game.graph.network.nodes:
            if game.graph.network.nodes[n]["evicted"] !=0:
                evicted +=1
        # print("Evicted:", evicted)

        if game.mission_completed():
            break
        game.defender_round(tt)
        # if game.graph.network[game.attacker.location]["evicted"]!=0:
        #     game.attacker.location = None
        evicted = False
        if game.attacker.location is not None:
            att_outside = is_node_evicted(game.graph.network,
                                        game.attacker.location)
            if att_outside:
                game.new_attacker(simulation_id)
                for n in game.graph.network.nodes:
                    game.graph.network.nodes[n]['compromised'] = False
                    game.attacker.network.nodes[n]['compromised'] = False
                    game.defender.network.nodes[n]['compromised'] = False
                evicted = True
            # else:
        if not evicted:
            attack_result = game.attacker_round(simulation_id, tt, type=game.scheme)
        
        # print('lol')
        tt+=1
    resu = dict()
        # print(results)
    for r in game.results:
        if 'mission_performance' in r:
            thresh = 0.6
        elif 'timeliness' in r:
            thresh = 0.75
        elif 'OR_Edge' in r:
            thresh = 0.9
        elif 'OR_MEC' in r:
            thresh = 0.85
        elif 'Obj_OR' in r:
            thresh = 0.86
        elif 'IoT_Edge_OR' in r:
            print('here')
            thresh = 0.85
        elif 'Edge_MEC_OR' in r:
            thresh = 0.85
        elif 'MEC_obj_OR' in r:
            thresh = 0.92
        elif 'MEC_Edge_OR' in r:
            thresh = 0.92
        elif 'Edge_IoT_OR' in r:
            thresh = 0.85
        elif 'IoT' in r and 'asset' in r:
            thresh = 0.9
        elif 'Edge' in r and 'asset' in r:
            thresh = 0.9
        elif 'MEC' in r and 'asset' in r:
            thresh = 0.9
        elif 'IoT' in r and '_Edge'in r and 'service' in r:
            thresh = 0.9
        elif 'Edge' in r and '_MEC' in r and 'service' in r:
            thresh = 0.9
        elif 'Edge' in r and '_IoT' in r and 'service' in r:
            thresh = 0.9
        elif 'MEC' in r and '_Edge' in r and 'service' in r:
            thresh = 0.9
        elif 'MEC' in r and '_obj' in r and 'service' in r:
            thresh = 0.9
        elif 'IoT' in r and '_Edge' in r and not 'service' in r:
            thresh = 0.9
        elif 'Edge' in r and '_MEC' in r and not 'service' in r:
            thresh = 0.9
        elif 'Edge' in r and '_IoT' in r and not 'service' in r:
            thresh = 0.9
        elif 'MEC' in r and '_obj' in r and not 'service' in r:
            thresh = 0.9
        elif 'MEC' in r and '_Edge' in r and not 'service' in r:
            thresh = 0.9
        # print(r, game.results[r]/tt)
        if 'mission_performance' in r:
            resu[r] = (1 if game.miou/(game.processed + 0.001) > 0.75 else 0)
        # elif 'timeliness' in r:
        #     resu[r] = (1 if game.timely/(game.processed + 0.001) > 0.9 else 0)
        elif 'mission' in r:
            resu[r] = (1 if game.miou/(game.processed + 0.001) > 0.75 and game.timely/(game.processed + 0.001) > 0.9 else 0)
        else:
            resu[r] = (1 if game.results[r]/tt > thresh else 0)
    for r in game.results:
        game.results[r]/=tt
    # print(game.results)
    # with open('test_fin.csv','a') as f:    
        #     w =  csv.DictWriter(f, resu.keys())
            # w.writeheader()
            # w.writerow(resu)
    # for r in game.results:
    #     print(r,":", game.results[r], resu[r])
    # for k in range(game.num_iot):
    #     print("IoT"+str(k+1), len(game.gra
    # ph.network.nodes["IoT"+str(k+1)]["pool"]), len(game.graph.network.nodes["IoT"+str(k+1)]["recieved"]))
    print("Timesteps:", tt)
    print("mIoU:", game.miou/(game.processed + 0.001))
    # print("Timeliness:", game.avg_timeliness/(tt + 0.001))
    print("Timeliness:", game.avg_timeliness/tt)

    # plt.plot(np.arange(len(available_list)-2), available_list[2:], label='Availability')
    # plt.plot(np.arange(len(timeliness_list)-2), timeliness_list[2:], label='Timeliness')
    # plt.legend()
    # plt.savefig("comparision.png")
    # with open('./'+scheme+'_timely_final'+'.csv','a') as f:
    #     w =  csv.DictWriter(f, ["timestep", "Timeliness"])
    #     w.writerow({"timestep": vuln, "Timeliness": game.timely/(game.processed + 0.001)})
    
    # with open('./'+scheme+'_timely_final_'+str(vuln)+'.csv','a') as f:
    #     w =  csv.DictWriter(f, ["timestep", "Timeliness"])
    #     w.writerow({"timestep": vuln, "meanIoU": game.timely/(game.processed + 0.001)})
        
    # with open('./miou_true_random/'+scheme+'_miou_'+str(vuln)+'.csv','a') as f:
    #     w =  csv.DictWriter(f, ["timestep", "meanIoU"])
    #     w.writerow({"timestep": vuln, "meanIoU": game.miou/(game.processed + 0.001)})
    
    # with open('./timely_true_random/'+scheme+'_timely_'+str(vuln)+'.csv','a') as f:
    #     w =  csv.DictWriter(f, ["timestep", "Timeliness"])
    #     w.writerow({"timestep": vuln, "Timeliness": game.timely/(game.processed + 0.001)})
    
    # with open('./availability_true_random/'+scheme+'_availability_'+str(vuln)+'.csv','a') as f:
    #     w =  csv.DictWriter(f, ["timestep", "Availability"])
    #     w.writerow({"timestep": vuln, "Availability": game.avg_availibility/(tt + 0.001)})
    
    # with open('./avg_timely_true_random/'+scheme+'_avg_timely_'+str(vuln)+'.csv','a') as f:
    #     w =  csv.DictWriter(f, ["timestep", "Average Timeliness"])
    #     w.writerow({"timestep": vuln, "Average Timeliness": game.avg_timeliness/(tt + 0.001)})

    return game