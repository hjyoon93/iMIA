#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import copy
import torch
from torch import nn
from collections import OrderedDict


#FedAvg for non-iid
def FedAvg(w, data_length):

    w_avg = copy.deepcopy(w[0])

    #print("data length:", data_length[0])
    #print("length of this:", len(w[0]))
    #print("length of this:", len(w[1]))
    #print("length of this:", len(w[2]))
    #print("length of this:", w[0])

    #print("aaaaaaa:", w[0])
    if len(data_length) <= 1:

        for k in w_avg.keys():
            #print("first:",w_avg[k])
            w_avg[k] = torch.mul(w_avg[k], data_length[0])
            #print("first output:",w_avg[k])

    if len(data_length) > 1:

        for k in w_avg.keys():
            #print("first:",w_avg[k])
            w_avg[k] = torch.mul(w_avg[k], data_length[0])
            #print("first output:",w_avg[k])

        index = 1
        for k in w_avg.keys():
            for i in range(1, len(w)):
                w_avg[k] += torch.mul(w[i][k], data_length[index])
                index += 1
            index = 1
            #w_avg[k] = torch.div(w_avg[k], len(w))
    return w_avg



    
    #index = 0
    #for k in w_avg.keys():
    #    for i in range(0, len(w)):
    #        w_avg[k] += w[i][k]
    #    w_avg[k] = torch.div(w_avg[k], len(w))
    #return w_avg

    #print("aaaaaaa:", torch.mul(2,4))
    #if len(data_length) <= 1:
    #    w_avg = copy.deepcopy(w[0])
    #    for i in w_avg:
    #        print(i)
    #if len(data_length) > 1:
    #    w_avg = data_length[0] * copy.deepcopy(w[0])
    #    i = 1
    #    for j in range(1, len(w)):
    #        w_avg += w[j] * data_length[i]
    #        i += 1
    #return w_avg





