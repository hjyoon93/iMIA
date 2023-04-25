#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import copy
import numpy as np
from torchvision import datasets, transforms
import torch
#torch.manual_seed(0) #always have the same results by seeding the same fixed value so the results will be reproducible ######### later uncomment it

from utils.sampling import mnist_iid, mnist_noniid, cifar_iid, traffic_iid
from utils.options import args_parser
from models.Update import LocalUpdate
from models.Update_dp import LocalUpdate_dp
from models.Nets import MLP, CNNMnist, CNNCifar, LeNet
from models.Fed import FedAvg
from models.test import test_img
from models.test_dp import test_img_dp
import loading_data as dataset
import random
from itertools import chain
import attacker_function
import itertools
import random
import math
import sys

from ast import literal_eval
import time


#getting a random number of image for each car to carry
def constrained_sum_sample_pos(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""

    dividers = sorted(random.sample(range(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

#ac


"""
rsu_asset = [[20, 15], [25, 10], [21, 11], [22, 8]]


def ac_rsu(c_r0, m_r0, c_r1, m_r1, c_r2, m_r2, c_r3, m_r3):
    # cpu load and memory load
    matrix_rsu = [
        [c_r0, m_r0],  # rsu0 1
        [c_r1, m_r1],  # rsu1 2
        [c_r2, m_r2],  # rsu2 3
        [c_r3, m_r3],  # rsu3 4
    ]

    # matrix_rsu = [
    #    [20, 15],  # rsu0 1
    #    [25, 10],  # rsu1 2
    #    [21, 11],  # rsu2 3
    #    [22, 8],  # rsu3 4
    # ]

    cpu_weight = 0.6
    memory_weight = 0.4

    min_cpu_rsu = min(matrix_rsu[0][0], matrix_rsu[1][0], matrix_rsu[2][0], matrix_rsu[3][0])
    min_memory_rsu = min(matrix_rsu[0][1], matrix_rsu[1][1], matrix_rsu[2][1], matrix_rsu[3][1])

    matrix_rsu[0][0] = (min_cpu_rsu / matrix_rsu[0][0]) * cpu_weight
    matrix_rsu[1][0] = min_cpu_rsu / matrix_rsu[1][0] * cpu_weight
    matrix_rsu[2][0] = min_cpu_rsu / matrix_rsu[2][0] * cpu_weight
    matrix_rsu[3][0] = min_cpu_rsu / matrix_rsu[3][0] * cpu_weight

    matrix_rsu[0][1] = min_memory_rsu / matrix_rsu[0][1] * memory_weight
    matrix_rsu[1][1] = min_memory_rsu / matrix_rsu[1][1] * memory_weight
    matrix_rsu[2][1] = min_memory_rsu / matrix_rsu[2][1] * memory_weight
    matrix_rsu[3][1] = min_memory_rsu / matrix_rsu[3][1] * memory_weight

    #print(matrix_rsu)

    for i in range(len(matrix_rsu)):
        matrix_rsu[i] = sum(matrix_rsu[i])

    return matrix_rsu

#ccs ac


ccs_asset = [[20, 7], [20, 10], [30, 15], [31, 12]]


def ac_ccs(c_ccs0, m_ccs0, c_ccs1, m_ccs1, c_ccs2, m_ccs2, c_ccs3, m_ccs3):
#cpu load and memory load
    matrix_ccs = [
        [c_ccs0, m_ccs0],  # rsu0 1
        [c_ccs1, m_ccs1],  # rsu1 2
        [c_ccs2, m_ccs2],  # rsu2 3
        [c_ccs3, m_ccs3],  # rsu3 4
    ]


    #matrix_rsu = [
    #    [20, 15],  # rsu0 1
    #    [25, 10],  # rsu1 2
    #    [21, 11],  # rsu2 3
    #    [22, 8],  # rsu3 4
    #]


    cpu_weight = 0.6
    memory_weight = 0.4

    min_cpu_rsu = min(matrix_ccs[0][0],matrix_ccs[1][0],matrix_ccs[2][0],matrix_ccs[3][0])
    min_memory_rsu = min(matrix_ccs[0][1],matrix_ccs[1][1],matrix_ccs[2][1],matrix_ccs[3][1])



    matrix_ccs[0][0] = (min_cpu_rsu/matrix_ccs[0][0]) * cpu_weight
    matrix_ccs[1][0] = min_cpu_rsu/matrix_ccs[1][0] * cpu_weight
    matrix_ccs[2][0] = min_cpu_rsu/matrix_ccs[2][0] * cpu_weight
    matrix_ccs[3][0] = min_cpu_rsu/matrix_ccs[3][0] * cpu_weight

    matrix_ccs[0][1] = min_memory_rsu/matrix_ccs[0][1] * memory_weight
    matrix_ccs[1][1] = min_memory_rsu/matrix_ccs[1][1] * memory_weight
    matrix_ccs[2][1] = min_memory_rsu/matrix_ccs[2][1] * memory_weight
    matrix_ccs[3][1] = min_memory_rsu/matrix_ccs[3][1] * memory_weight

    #print(matrix_ccs)

    for i in range(len(matrix_ccs)):
        matrix_ccs[i] = sum(matrix_ccs[i])


    return matrix_ccs



#end of ac
"""





def get_train_valid_loader(data_dir,
                           batch_size,
                           num_workers=0,
                           ):
    # Create Transforms
    transform = transforms.Compose([
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
        transforms.Normalize((0.3403, 0.3121, 0.3214),
                             (0.2724, 0.2608, 0.2669))
    ])

    # Create Datasets
    dataset_train = dataset.BelgiumTS(
        root_dir=data_dir, train=True,  transform=transform)
    dataset_test = dataset.BelgiumTS(
        root_dir=data_dir, train=False,  transform=transform)

    # Load Datasets
    return dataset_train, dataset_test

if __name__ == '__main__':
    # parse args

    args = args_parser()
    args.device = torch.device('cuda:{}'.format(args.gpu) if torch.cuda.is_available() and args.gpu != -1 else 'cpu')
    # load dataset and split users
    if args.dataset == 'mnist':
        trans_mnist = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
        dataset_train = datasets.MNIST('../data/mnist/', train=True, download=True, transform=trans_mnist)
        dataset_test = datasets.MNIST('../data/mnist/', train=False, download=True, transform=trans_mnist)
        # sample users
        if args.iid:
            dict_users = mnist_iid(dataset_train, args.num_users)
        else:
            dict_users = mnist_noniid(dataset_train, args.num_users)
    elif args.dataset == 'cifar':
        trans_cifar = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
        dataset_train = datasets.CIFAR10('../data/cifar', train=True, download=True, transform=trans_cifar)
        dataset_test = datasets.CIFAR10('../data/cifar', train=False, download=True, transform=trans_cifar)
        if args.iid:
            dict_users = cifar_iid(dataset_train, args.num_users)
        else:
            exit('Error: only consider IID setting in CIFAR10')
    elif args.dataset == 'traffic':
        dataset_train, dataset_test = get_train_valid_loader("",
            batch_size=32, num_workers=0)



        if args.iid:
            ######
            args.epochs = 20

            #with open('file_arg_four.txt', 'a') as file:
            #    file.write("%i\n" % args.epochs)
            #    file.close()
            print("this is the args:", args)
            #dict_users_copy = traffic_iid(dataset_train, args.num_users)
            dict_users = traffic_iid(dataset_train, args.num_users)
            #print(dict_users)

            #test code
            #print("this is it",dataset_train[0])
            #print("this is it", dataset_train[1])

            #print(type(dataset_train))


            #for i in range(len(dataset_train)):
            #    if dataset_train[i][1] == 37:
            #        dataset_train[i] = list(dataset_train[i])
            #        dataset_train[i][1] = 1
            #        dataset_train[i] = tuple(dataset_train[i])



            #        i[1] = 1
            #print(type(dataset_train[0][1])) #37
            #print(type(dataset_train[1][1])) #53
            #
            #print(type(dataset_train[2][1])) #41







            ##############

            #declaration of AC, EV, SV, UV
            #order: rsu0, rsu1, rsu2, rsu3, ccs
            #AC = [1.0, 1.0, 1.0, 1.0, 1.0] #Asset capacity
            #EV = [0.3, 0.4, 0.3, 0.5, 0.0] #encryption vulnerability
            #SV = [0.4, 0.4, 0.4, 0.4, 0.0] #cvss - software vulnerability
            #UV = [0.5, 0.4, 0.5, 0.4, 0.0] #unknown vulnerability

            #AC = [1.0, 1.0, 1.0, 1.0, 1.0]  # Asset capacity
            """
            EV_initial = [0.8, 0.9, 0.9, 0.7, 0.05]
            EV = [0.8, 0.9, 0.9, 0.7, 0.05]  # encryption vulnerability
            SV = [0.9, 0.8, 0.8, 0.9, 0.4]  # cvss - software vulnerability
            UV = [0.8, 0.8, 0.8, 0.7, 0.8]  # unknown vulnerability
            """
            # min(np.random.normal(0.7,0.1),1), min(np.random.normal(0.7,0.1),1)
            rsu0_ev = min(np.random.normal(0.4, 0.05), 1)
            while rsu0_ev < 0:
                rsu0_ev = min(np.random.normal(0.4, 0.05), 1)

            rsu1_ev = min(np.random.normal(0.4, 0.05), 1)
            while rsu1_ev < 0:
                rsu1_ev = min(np.random.normal(0.4, 0.05), 1)

            rsu2_ev = min(np.random.normal(0.4, 0.05), 1)
            while rsu2_ev < 0:
                rsu2_ev = min(np.random.normal(0.4, 0.05), 1)

            rsu3_ev = min(np.random.normal(0.5, 0.05), 1)
            while rsu3_ev < 0:
                rsu3_ev = min(np.random.normal(0.5, 0.05), 1)

            ccs_ev = min(np.random.normal(0.3, 0.05), 1)
            while ccs_ev < 0:
                ccs_ev = min(np.random.normal(0.3, 0.05), 1)

            rsu0_sv = min(np.random.normal(0.5, 0.05), 1)
            while rsu0_sv < 0:
                rsu0_sv = min(np.random.normal(0.5, 0.05), 1)

            rsu1_sv = min(np.random.normal(0.5, 0.05), 1)
            while rsu1_sv < 0:
                rsu1_sv = min(np.random.normal(0.5, 0.05), 1)

            rsu2_sv = min(np.random.normal(0.5, 0.05), 1)
            while rsu2_sv < 0:
                rsu2_sv = min(np.random.normal(0.5, 0.05), 1)

            rsu3_sv = min(np.random.normal(0.4, 0.05), 1)
            while rsu3_sv < 0:
                rsu3_sv = min(np.random.normal(0.4, 0.05), 1)

            ccs_sv = min(np.random.normal(0.2, 0.05), 1)
            while ccs_sv < 0:
                ccs_sv = min(np.random.normal(0.2, 0.05), 1)

            rsu0_uv = min(np.random.normal(0.5, 0.05), 1)
            while rsu0_uv < 0:
                rsu0_uv = min(np.random.normal(0.5, 0.05), 1)

            rsu1_uv = min(np.random.normal(0.4, 0.05), 1)
            while rsu1_uv < 0:
                rsu1_uv = min(np.random.normal(0.4, 0.05), 1)

            rsu2_uv = min(np.random.normal(0.3, 0.05), 1)
            while rsu2_uv < 0:
                rsu2_uv = min(np.random.normal(0.3, 0.05), 1)

            rsu3_uv = min(np.random.normal(0.4, 0.05), 1)
            while rsu3_uv < 0:
                rsu3_uv = min(np.random.normal(0.4, 0.05), 1)

            ccs_uv = min(np.random.normal(0.3, 0.05), 1)
            while ccs_uv < 0:
                ccs_uv = min(np.random.normal(0.3, 0.05), 1)




            #Made vulnerability changing
            #EV_initial = [0.4, 0.5, 0.6, 0.6, 0.05]
            EV = [rsu0_ev, rsu1_ev, rsu2_ev, rsu3_ev, ccs_ev]  # encryption vulnerability
            EV_initial = EV
            SV = [rsu0_sv, rsu1_sv, rsu2_sv, rsu3_sv, ccs_sv]  # cvss - software vulnerability
            UV = [rsu0_uv, rsu1_uv, rsu2_uv, rsu3_uv, ccs_uv]  # unknown vulnerability

            print("this is the EV:", EV)
            print("this is the EV_initial:", EV_initial)
            print("this is the SV:", SV)
            print("this is the UV:", UV)



            node_compromised = [False, False, False, False, False]

            node_compromised_NIDS = [None, None, None, None, None]


            #car asset capacity: whether to decide a given car was able to collect vehicles
            mu0, sigma0 = 0.85, 0.05  # mean and standard deviation
            car_ac = np.random.normal(mu0, sigma0, 56)
            print("car_ac:", car_ac)

            total_number_attacks = 0
            number_attack_success = 0

            #number_service_success / total_number_service
            total_number_service = 0
            number_service_success = 0


            #made car vulnerability changing
            #car vulnerability: whether dos will work or not
            mu1, sigma1 = 0.5, 0.05  # mean and standard deviation
            car_vulnerability = np.random.normal(mu1, sigma1, 56)
            print("car_vul:", car_vulnerability)

            #made car forwarding prob changing
            #car_forwarding_prob: forwarding probability
            mu2, sigma2 = 0.8, 0.01  # mean and standard deviation
            car_forwarding_prob = np.random.normal(mu2, sigma2, 56)

            print("car_forward:", car_forwarding_prob)


            #min(np.random.normal(0.7,0.1,1))
            #ccs_uv = min(np.random.normal(0.6, 0.1), 1)
            #while ccs_uv < 0:
            #    ccs_uv = min(np.random.normal(0.6, 0.1), 1)



            rsu0_cpu = min(np.random.normal(0.05, 0.05), 1)
            while rsu0_cpu < 0:
                rsu0_cpu = min(np.random.normal(0.05, 0.05), 1)



            rsu0_mem = min(np.random.normal(0.04, 0.05), 1)
            while rsu0_mem < 0:
                rsu0_mem = min(np.random.normal(0.04, 0.05), 1)

            rsu1_cpu = min(np.random.normal(0.06, 0.05), 1)
            while rsu1_cpu < 0:
                rsu1_cpu = min(np.random.normal(0.06, 0.05), 1)

            rsu1_mem = min(np.random.normal(0.05, 0.05), 1)
            while rsu1_mem < 0:
                rsu1_mem = min(np.random.normal(0.05, 0.05), 1)

            rsu2_cpu = min(np.random.normal(0.05, 0.05), 1)
            while rsu2_cpu < 0:
                rsu2_cpu = min(np.random.normal(0.05, 0.05), 1)


            rsu2_mem = min(np.random.normal(0.04, 0.05), 1)
            while rsu2_mem < 0:
                rsu2_mem = min(np.random.normal(0.04, 0.05), 1)

            rsu3_cpu = min(np.random.normal(0.06, 0.05), 1)
            while rsu3_cpu < 0:
                rsu3_cpu = min(np.random.normal(0.06, 0.05), 1)

            rsu3_mem = min(np.random.normal(0.03, 0.05), 1)
            while rsu3_mem < 0:
                rsu3_mem = min(np.random.normal(0.03, 0.05), 1)

            ccs_cpu = min(np.random.normal(0.05, 0.05), 1)
            while ccs_cpu < 0:
                ccs_cpu = min(np.random.normal(0.05, 0.05), 1)

            ccs_mem = min(np.random.normal(0.01, 0.05), 1)
            while ccs_mem < 0:
                ccs_mem = min(np.random.normal(0.01, 0.05), 1)



            #made AC changing
            rsu_asset = [[rsu0_cpu, rsu0_mem], [rsu1_cpu, rsu1_mem], [rsu2_cpu, rsu2_mem], [rsu3_cpu, rsu3_mem]]

            print("this is the rsu asset:", rsu_asset)


            #made AC changing
            ccs_asset = [[ccs_cpu, ccs_mem]]

            print("this is the ccs asset:", ccs_asset)




            def AC(cpu_load, memory_load):
                a = (0.5 * cpu_load) + (0.5 * memory_load)
                AC = min((1 * (math.exp(-a), 1)))
                return AC


            print(AC(rsu_asset[0][0], rsu_asset[0][1]), AC(rsu_asset[1][0], rsu_asset[1][1]),
                  AC(rsu_asset[2][0], rsu_asset[2][1]), AC(rsu_asset[3][0], rsu_asset[3][1]))
            print(AC(ccs_asset[0][0], ccs_asset[0][1]))


            # print(AC(rsu_asset[0][0], rsu_asset[0][1]))
            # print(AC(ccs_asset[0][0], ccs_asset[0][1]))

            def vulnerability(EV, SV, UV):
                my_list = [EV, SV, UV]
                A = list(map(sum, zip(*my_list)))
                myInt = 3
                vul = [x / myInt for x in A]
                return vul

            #dataset for one mission run
            List = []

            #new_adding V (v0-v55) #does the vehicle operate properly
            for i in range(56):
                List.append('true')
            #new_end of adding V (v0-v55) #is the vehicle active and present

            print("leng of list after v:", len(List))


            rsu_0 = [36,36,36,36,36,36,36,36,36,36,36,36,36,36]#constrained_sum_sample_pos(14, 504)
            print("rsu_0:", rsu_0)  # [16, 76, 14, 18, 60, 95, 11, 3, 69, 46, 46, 36, 3, 11]
            rsu_1 = [36,36,36,36,36,36,36,36,36,36,36,36,36,36]#constrained_sum_sample_pos(14, 504)
            print("rsu_1:", rsu_1)  # [16, 76, 14, 18, 60, 95, 11, 3, 69, 46, 46, 36, 3, 11]
            rsu_2 = [36,36,36,36,36,36,36,36,36,36,36,36,36,36]#constrained_sum_sample_pos(14, 504)
            print("rsu_2:", rsu_2)  # [16, 76, 14, 18, 60, 95, 11, 3, 69, 46, 46, 36, 3, 11]
            rsu_3 = [36,36,36,36,36,36,36,36,36,36,36,36,36,36]#constrained_sum_sample_pos(14, 504)
            print("rsu_3:", rsu_3)  # [16, 76, 14, 18, 60, 95, 11, 3, 69, 46, 46, 36, 3, 11]


            #new_adding S1 (s1_0-s1_55): does the vehicle have enough capacity to collect images before entering the service area?
            for i in car_ac:
                if random.random() < i:
                    List.append('true')
                    #number_service_success += 1
                else:
                    List.append('false')

            print("leng of list after s1:", len(List))



            #total_number_service += 56



            #new_ending S1: does the vehicle have enough capacity to collect images before entering the service area?

            track_image_collect = []
            #new_adding SV1 (SV1_0-SV1_55): does the vehicle collect images?
            for i in car_ac:
                if random.random() < i:
                    List.append('true')
                    track_image_collect.append('true')
                else:
                    List.append('false')
                    track_image_collect.append('false')
            #end_adding SV1: does the vehicle collect images?

            print("leng of list after sv1:",len(List))

            #track_image_collect = []
            #for i in car_ac:
            #    if random.random() < i:
            #        track_image_collect.append('true')
            #    else:
            #        track_image_collect.append('false')



            ####getting true and false for vehicles by forwarding prob and dos attack (0.3) success rate
            car_list = []
            for i in range(len(car_forwarding_prob)):
                #random.seed(i)
                if track_image_collect[i] == 'false':
                    car_list.append('0')
                elif track_image_collect[i] == 'true':
                    if random.random() < car_forwarding_prob[i]: #forward probability
                        if random.random() < 0.4:  #(i.e., frequency of the attack happening)
                            #total_number_attacks += 1
                            if random.random() < car_vulnerability[i]:
                                #number_attack_success += 1
                                car_list.append('0') #cannot forward
                            else:
                                car_list.append('1') #can forward
                        else:
                            car_list.append('1') #can forward
                    else:
                        car_list.append("0") #cannot forward
            print(car_list)


            #new_adding SD1 (sd1_0-sd1_55) (SEND TASK): does the vehicle send images to RSU
            for i in car_list:
                if i == '0':
                    List.append('false')
                else:
                    List.append('true')

            print("leng of list after sd1:", len(List))
            print(len(List))
            #new_end of adding SD1 (SEND TASK); does the vehicle send images to RSU


            #print("true:",List)
            #print(len(List))

            # writing to a file whether cars were able to send to rsu or not
            with open('input_four_test.txt', 'w') as f:
                for line in car_list:
                    f.write(f"{line}\n")
            ####end of getting true and false for vehicles by forwarding (0.9) success rate and dos attack (0.3) success rate


            ######Make the iid dataset an non-iid dataset
            #reading file
            for i in dict_users:
                dict_users[i] = list(dict_users[i])

            #print(len(dict_users[0]))
            #print(len(dict_users[1]))
            #print(len(dict_users[2]))
            #print(len(dict_users[3]))

            with open('input_four_test.txt') as f:
                a = f.read().splitlines()
                #a = a[:56]

            #rsu_0 = constrained_sum_sample_pos(14, 504)
            #print("rsu_0:", rsu_0) #[16, 76, 14, 18, 60, 95, 11, 3, 69, 46, 46, 36, 3, 11]
            #rsu_1 = constrained_sum_sample_pos(14, 504)
            #rsu_2 = constrained_sum_sample_pos(14, 504)
            #rsu_3 = constrained_sum_sample_pos(14, 504)

            mylist0 = []
            mylist1 = []
            mylist2 = []
            mylist3 = []
            for i in range(len(a)):
                if a[i] == '1':
                    continue
                elif a[i] == '0':
                    if i == 0 or i == 1 or i == 2 or i == 3 or i == 4 or i == 5 or i == 6 or i == 7 or i == 8 or i == 9 or i == 10 or i == 11 or i == 12 or i == 13:
                        if i == 0:
                            mylist0.append([*range(0,rsu_0[0],1)])
                        if i == 1:
                            mylist0.append([*range(rsu_0[0],rsu_0[0] + rsu_0[1],1)])
                        if i == 2:
                            mylist0.append([*range(rsu_0[0] + rsu_0[1], rsu_0[0] + rsu_0[1] + rsu_0[2],1)])
                        if i == 3:
                            mylist0.append([*range(rsu_0[0] + rsu_0[1] + rsu_0[2],rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3],1)])
                        if i == 4:
                            mylist0.append([*range(rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3], rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4],1)])
                        if i == 5:
                            mylist0.append([*range(rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4],rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4]+rsu_0[5],1)])
                        if i == 6:
                            mylist0.append([*range(rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4]+rsu_0[5],rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4]+rsu_0[5]+rsu_0[6],1)])
                        if i == 7:
                            mylist0.append([*range(rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4]+rsu_0[5]+rsu_0[6],rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4]+rsu_0[5]+rsu_0[6]+rsu_0[7],1)])
                        if i == 8:
                            mylist0.append([*range(rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4]+rsu_0[5]+rsu_0[6]+rsu_0[7],rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4]+rsu_0[5]+rsu_0[6]+rsu_0[7]+rsu_0[8],1)])
                        if i == 9:
                            mylist0.append([*range(rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4]+rsu_0[5]+rsu_0[6]+rsu_0[7]+rsu_0[8],rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4]+rsu_0[5]+rsu_0[6]+rsu_0[7]+rsu_0[8]+rsu_0[9],1)])
                        if i == 10:
                            mylist0.append([*range(rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4]+rsu_0[5]+rsu_0[6]+rsu_0[7]+rsu_0[8]+rsu_0[9],rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4]+rsu_0[5]+rsu_0[6]+rsu_0[7]+rsu_0[8]+rsu_0[9]+rsu_0[10],1)])
                        if i == 11:
                            mylist0.append([*range(rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4]+rsu_0[5]+rsu_0[6]+rsu_0[7]+rsu_0[8]+rsu_0[9]+rsu_0[10],rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4]+rsu_0[5]+rsu_0[6]+rsu_0[7]+rsu_0[8]+rsu_0[9]+rsu_0[10]+rsu_0[11],1)])
                        if i == 12:
                            mylist0.append([*range(rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4]+rsu_0[5]+rsu_0[6]+rsu_0[7]+rsu_0[8]+rsu_0[9]+rsu_0[10]+rsu_0[11],rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4]+rsu_0[5]+rsu_0[6]+rsu_0[7]+rsu_0[8]+rsu_0[9]+rsu_0[10]+rsu_0[11]+rsu_0[12],1)])
                        if i == 13:
                            mylist0.append([*range(rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4]+rsu_0[5]+rsu_0[6]+rsu_0[7]+rsu_0[8]+rsu_0[9]+rsu_0[10]+rsu_0[11]+rsu_0[12],rsu_0[0] + rsu_0[1] + rsu_0[2]+ rsu_0[3]+rsu_0[4]+rsu_0[5]+rsu_0[6]+rsu_0[7]+rsu_0[8]+rsu_0[9]+rsu_0[10]+rsu_0[11]+rsu_0[12]+rsu_0[13],1)])



                    if i == 14 or i == 15 or i == 16 or i ==17 or i == 18 or i == 19 or i ==20 or i == 21 or i == 22 or i ==23 or i == 24 or i == 25 or i ==26 or i == 27:
                        if i == 14:
                            mylist1.append([*range(0,rsu_1[0],1)])
                        if i == 15:
                            mylist1.append([*range(rsu_1[0],rsu_1[0]+rsu_1[1],1)])
                        if i == 16:
                            mylist1.append([*range(rsu_1[0]+rsu_1[1],rsu_1[0]+rsu_1[1]+rsu_1[2],1)])
                        if i == 17:
                            mylist1.append([*range(rsu_1[0]+rsu_1[1]+rsu_1[2],rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3],1)])
                        if i == 18:
                            mylist1.append([*range(rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3],rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4],1)])
                        if i == 19:
                            mylist1.append([*range(rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4],rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4]+rsu_1[5],1)])
                        if i == 20:
                            mylist1.append([*range(rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4]+rsu_1[5],rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4]+rsu_1[5]+rsu_1[6],1)])
                        if i == 21:
                            mylist1.append([*range(rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4]+rsu_1[5]+rsu_1[6],rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4]+rsu_1[5]+rsu_1[6]+rsu_1[7],1)])
                        if i == 22:
                            mylist1.append([*range(rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4]+rsu_1[5]+rsu_1[6]+rsu_1[7],rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4]+rsu_1[5]+rsu_1[6]+rsu_1[7]+rsu_1[8],1)])
                        if i == 23:
                            mylist1.append([*range(rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4]+rsu_1[5]+rsu_1[6]+rsu_1[7]+rsu_1[8],rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4]+rsu_1[5]+rsu_1[6]+rsu_1[7]+rsu_1[8]+rsu_1[9],1)])
                        if i == 24:
                            mylist1.append([*range(rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4]+rsu_1[5]+rsu_1[6]+rsu_1[7]+rsu_1[8]+rsu_1[9],rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4]+rsu_1[5]+rsu_1[6]+rsu_1[7]+rsu_1[8]+rsu_1[9]+rsu_1[10],1)])
                        if i == 25:
                            mylist1.append([*range(rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4]+rsu_1[5]+rsu_1[6]+rsu_1[7]+rsu_1[8]+rsu_1[9]+rsu_1[10],rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4]+rsu_1[5]+rsu_1[6]+rsu_1[7]+rsu_1[8]+rsu_1[9]+rsu_1[10]+rsu_1[11],1)])
                        if i == 26:
                            mylist1.append([*range(rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4]+rsu_1[5]+rsu_1[6]+rsu_1[7]+rsu_1[8]+rsu_1[9]+rsu_1[10]+rsu_1[11],rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4]+rsu_1[5]+rsu_1[6]+rsu_1[7]+rsu_1[8]+rsu_1[9]+rsu_1[10]+rsu_1[11]+rsu_1[12],1)])
                        if i == 27:
                            mylist1.append([*range(rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4]+rsu_1[5]+rsu_1[6]+rsu_1[7]+rsu_1[8]+rsu_1[9]+rsu_1[10]+rsu_1[11]+rsu_1[12],rsu_1[0]+rsu_1[1]+rsu_1[2]+rsu_1[3]+rsu_1[4]+rsu_1[5]+rsu_1[6]+rsu_1[7]+rsu_1[8]+rsu_1[9]+rsu_1[10]+rsu_1[11]+rsu_1[12]+rsu_1[13],1)])


                    if i == 28 or i == 29 or i == 30 or i ==31 or i == 32 or i == 33 or i ==34 or i == 35 or i == 36 or i ==37 or i == 38 or i == 39 or i ==40 or i == 41:
                        if i == 28:
                            mylist2.append([*range(0,rsu_2[0],1)])
                        if i == 29:
                            mylist2.append([*range(rsu_2[0],rsu_2[0]+rsu_2[1],1)])
                        if i == 30:
                            mylist2.append([*range(rsu_2[0]+rsu_2[1],rsu_2[0]+rsu_2[1]+rsu_2[2],1)])
                        if i == 31:
                            mylist2.append([*range(rsu_2[0]+rsu_2[1]+rsu_2[2],rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3],1)])
                        if i == 32:
                            mylist2.append([*range(rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3],rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4],1)])
                        if i == 33:
                            mylist2.append([*range(rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4],rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4]+rsu_2[5],1)])
                        if i == 34:
                            mylist2.append([*range(rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4]+rsu_2[5],rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4]+rsu_2[5]+rsu_2[6],1)])
                        if i == 35:
                            mylist2.append([*range(rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4]+rsu_2[5]+rsu_2[6],rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4]+rsu_2[5]+rsu_2[6]+rsu_2[7],1)])
                        if i == 36:
                            mylist2.append([*range(rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4]+rsu_2[5]+rsu_2[6]+rsu_2[7],rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4]+rsu_2[5]+rsu_2[6]+rsu_2[7]+rsu_2[8],1)])
                        if i == 37:
                            mylist2.append([*range(rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4]+rsu_2[5]+rsu_2[6]+rsu_2[7]+rsu_2[8],rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4]+rsu_2[5]+rsu_2[6]+rsu_2[7]+rsu_2[8]+rsu_2[9],1)])
                        if i == 38:
                            mylist2.append([*range(rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4]+rsu_2[5]+rsu_2[6]+rsu_2[7]+rsu_2[8]+rsu_2[9],rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4]+rsu_2[5]+rsu_2[6]+rsu_2[7]+rsu_2[8]+rsu_2[9]+rsu_2[10],1)])
                        if i == 39:
                            mylist2.append([*range(rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4]+rsu_2[5]+rsu_2[6]+rsu_2[7]+rsu_2[8]+rsu_2[9]+rsu_2[10],rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4]+rsu_2[5]+rsu_2[6]+rsu_2[7]+rsu_2[8]+rsu_2[9]+rsu_2[10]+rsu_2[11],1)])
                        if i == 40:
                            mylist2.append([*range(rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4]+rsu_2[5]+rsu_2[6]+rsu_2[7]+rsu_2[8]+rsu_2[9]+rsu_2[10]+rsu_2[11],rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4]+rsu_2[5]+rsu_2[6]+rsu_2[7]+rsu_2[8]+rsu_2[9]+rsu_2[10]+rsu_2[11]+rsu_2[12],1)])
                        if i == 41:
                            mylist2.append([*range(rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4]+rsu_2[5]+rsu_2[6]+rsu_2[7]+rsu_2[8]+rsu_2[9]+rsu_2[10]+rsu_2[11]+rsu_2[12],rsu_2[0]+rsu_2[1]+rsu_2[2]+rsu_2[3]+rsu_2[4]+rsu_2[5]+rsu_2[6]+rsu_2[7]+rsu_2[8]+rsu_2[9]+rsu_2[10]+rsu_2[11]+rsu_2[12]+rsu_2[13],1)])


                    if i == 42 or i == 43 or i == 44 or i == 45 or i == 46 or i == 47 or i == 48 or i == 49 or i == 50 or i ==51 or i == 52 or i == 53 or i ==54 or i == 55:
                        if i == 42:
                            mylist3.append([*range(0,rsu_3[0],1)])
                        if i == 43:
                            mylist3.append([*range(rsu_3[0],rsu_3[0]+rsu_3[1],1)])
                        if i == 44:
                            mylist3.append([*range(rsu_3[0]+rsu_3[1],rsu_3[0]+rsu_3[1]+rsu_3[2],1)])
                        if i == 45:
                            mylist3.append([*range(rsu_3[0]+rsu_3[1]+rsu_3[2],rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3],1)])
                        if i == 46:
                            mylist3.append([*range(rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3],rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4],1)])
                        if i == 47:
                            mylist3.append([*range(rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4],rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4]+rsu_3[5],1)])
                        if i == 48:
                            mylist3.append([*range(rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4]+rsu_3[5],rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4]+rsu_3[5]+rsu_3[6],1)])
                        if i == 49:
                            mylist3.append([*range(rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4]+rsu_3[5]+rsu_3[6], rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4]+rsu_3[5]+rsu_3[6]+rsu_3[7],1)])
                        if i == 50:
                            mylist3.append([*range(rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4]+rsu_3[5]+rsu_3[6]+rsu_3[7],rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4]+rsu_3[5]+rsu_3[6]+rsu_3[7]+rsu_3[8],1)])
                        if i == 51:
                            mylist3.append([*range(rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4]+rsu_3[5]+rsu_3[6]+rsu_3[7]+rsu_3[8],rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4]+rsu_3[5]+rsu_3[6]+rsu_3[7]+rsu_3[8]+rsu_3[9],1)])
                        if i == 52:
                            mylist3.append([*range(rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4]+rsu_3[5]+rsu_3[6]+rsu_3[7]+rsu_3[8]+rsu_3[9],rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4]+rsu_3[5]+rsu_3[6]+rsu_3[7]+rsu_3[8]+rsu_3[9]+rsu_3[10],1)])
                        if i == 53:
                            mylist3.append([*range(rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4]+rsu_3[5]+rsu_3[6]+rsu_3[7]+rsu_3[8]+rsu_3[9]+rsu_3[10],rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4]+rsu_3[5]+rsu_3[6]+rsu_3[7]+rsu_3[8]+rsu_3[9]+rsu_3[10]+rsu_3[11],1)])
                        if i == 54:
                            mylist3.append([*range(rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4]+rsu_3[5]+rsu_3[6]+rsu_3[7]+rsu_3[8]+rsu_3[9]+rsu_3[10]+rsu_3[11], rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4]+rsu_3[5]+rsu_3[6]+rsu_3[7]+rsu_3[8]+rsu_3[9]+rsu_3[10]+rsu_3[11]+rsu_3[12],1)])
                        if i == 55:
                            mylist3.append([*range(rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4]+rsu_3[5]+rsu_3[6]+rsu_3[7]+rsu_3[8]+rsu_3[9]+rsu_3[10]+rsu_3[11]+rsu_3[12],rsu_3[0]+rsu_3[1]+rsu_3[2]+rsu_3[3]+rsu_3[4]+rsu_3[5]+rsu_3[6]+rsu_3[7]+rsu_3[8]+rsu_3[9]+rsu_3[10]+rsu_3[11]+rsu_3[12]+rsu_3[13],1)])
            print("dictionary0", dict_users['0'])
            print("length before:", len(dict_users['0']))

            flat_mylist0 = itertools.chain(*mylist0)
            flat_mylist0 = list(flat_mylist0)

            print("this is is:",flat_mylist0)
            print("length in process :", len(flat_mylist0))

            flat_mylist1 = itertools.chain(*mylist1)
            flat_mylist1 = list(flat_mylist1)

            flat_mylist2 = itertools.chain(*mylist2)
            flat_mylist2 = list(flat_mylist2)

            flat_mylist3 = itertools.chain(*mylist3)
            flat_mylist3 = list(flat_mylist3)

            """
            for i in flat_mylist0:
                if i in dict_users['0']:
                    dict_users['0'].remove(i)

            for i in flat_mylist1:
                if i in dict_users['1']:
                    dict_users['1'].remove(i)

            for i in flat_mylist2:
                if i in dict_users['2']:
                    dict_users['2'].remove(i)

            for i in flat_mylist3:
                if i in dict_users['3']:
                    dict_users['3'].remove(i)
                    
            """
            dict_users["0"] = [v for i, v in enumerate(dict_users["0"]) if i not in flat_mylist0]
            dict_users["1"] = [v for i, v in enumerate(dict_users["1"]) if i not in flat_mylist1]
            dict_users["2"] = [v for i, v in enumerate(dict_users["2"]) if i not in flat_mylist2]
            dict_users["3"] = [v for i, v in enumerate(dict_users["3"]) if i not in flat_mylist3]
            print("this,:",dict_users['0'])
            print(len(dict_users["0"]))
            print(len(dict_users["1"]))
            print(len(dict_users["2"]))
            print(len(dict_users["3"]))

            print("length after effect:", len(dict_users['0']))


            if len(dict_users['0']) == 0 and len(dict_users['1']) == 0 and len(dict_users['2']) == 0 and len(dict_users['3']) == 0:
                args.num_users = 0
                del dict_users['0']
                del dict_users['1']
                del dict_users['2']
                del dict_users['3']

            elif len(dict_users['0']) == 0 and len(dict_users['1']) == 0 and len(dict_users['2']) == 0:
                args.num_users = 1
                del dict_users['0']
                del dict_users['1']
                del dict_users['2']

            elif len(dict_users['0']) == 0 and len(dict_users['1']) == 0 and len(dict_users['3']) == 0:
                args.num_users = 1
                del dict_users['0']
                del dict_users['1']
                del dict_users['3']


            elif len(dict_users['0']) == 0 and len(dict_users['2']) == 0 and len(dict_users['3']) == 0:
                args.num_users = 1
                del dict_users['0']
                del dict_users['2']
                del dict_users['3']

            elif len(dict_users['1']) == 0 and len(dict_users['2']) == 0 and len(dict_users['3']) == 0:
                args.num_users = 1
                del dict_users['1']
                del dict_users['2']
                del dict_users['3']



            elif len(dict_users['0']) == 0 and len(dict_users['1']) == 0:
                args.num_users = 2
                del dict_users['0']
                del dict_users['1']

            elif len(dict_users['0']) == 0 and len(dict_users['2']) == 0:
                args.num_users = 2
                del dict_users['0']
                del dict_users['2']

            elif len(dict_users['0']) == 0 and len(dict_users['3']) == 0:
                args.num_users = 2
                del dict_users['0']
                del dict_users['3']

            elif len(dict_users['1']) == 0 and len(dict_users['2']) == 0:
                args.num_users = 2
                del dict_users['1']
                del dict_users['2']

            elif len(dict_users['1']) == 0 and len(dict_users['3']) == 0:
                args.num_users = 2
                del dict_users['1']
                del dict_users['3']


            elif len(dict_users['2']) == 0 and len(dict_users['3']) == 0:
                args.num_users = 2
                del dict_users['2']
                del dict_users['3']

            elif len(dict_users['0']) == 0:
                args.num_users = 3

                del dict_users['0']

            elif len(dict_users['1']) == 0:
                args.num_users = 3
                del dict_users['1']

            elif len(dict_users['2']) == 0:
                args.num_users = 3
                del dict_users['2']

            elif len(dict_users['3']) == 0:
                args.num_users = 3
                del dict_users['3']

            #######end of Make the iid dataset an non-iid dataset

            users = []
            for i in dict_users:
                users.append(int(i))
            print("users:", users)
            print("num_users:", args.num_users)

            print(dict_users)
            print(len(dict_users))

            whole_length = 0
            #data_length = []
            data_length = {0: None, 1: None, 2: None, 3: None}
            data_length_list = []
            """
            
            data_length = {0: None, 1: None, 2: None, 3: None}
            data_length_list = []

            unique_keys = [0, 1, 2, 3]
            data_length_list = [11, 12, 13, 14]

            data_length.update({0: 1, 1: 1})

            data_length.update({2: 1, 3: 1})
            """
            print("afddsgsadgdsfadsfdsaf:", dict_users)
            for i in dict_users:
                whole_length += len(dict_users[i])

            for i in dict_users:
                data_length_list.append(len(dict_users[i])/whole_length)

            for i in range(len(data_length_list)):
                data_length.update({i:data_length_list[i]})



            if data_length[0] == None:
                del data_length[0]

            if data_length[1] == None:
                del data_length[1]

            if data_length[1] == None:
                del data_length[1]

            if data_length[1] == None:
                del data_length[1]


            print("hello:",data_length)

            data_length_copy = data_length.copy()

            print("hello1:",data_length_copy)



            print("this is the data_length:", data_length)


            print("this is the whole length:", whole_length)







            #a = {0: [1, 2, 3, 4], 1: [1, 2, 3, 4, 5], 2: [1, 2, 3, 4], 3: [1, 2, 3, 4]}

            #a[1] = a[2]
            #del a[2]

            #print(a)



            # converting iterable to list and printing


            #>> > oldlist = [2, 5, 7, 12, 13]
            #>> > indices = {3, 4}
            #>> > [v for i, v in enumerate(oldlist) if i not in indices]
            #[2, 5, 7]



                    #delete images due to dos

        else:
            exit('Error: only consider IID setting in Traffic')
    else:
        exit('Error: unrecognized dataset')

    #img_size = dataset_train[0][0].shape
    #print("this:",img_size)

    #print(len(dict_users[0]))
    #print(len(dict_users[1]))
    #print(len(dict_users[2]))
    #print(len(dict_users[3]))
    print("print_num", args.num_users)

    # build model
    if args.model == 'cnn' and args.dataset == 'cifar':
        net_glob = CNNCifar(args=args).to(args.device)
    elif args.model == 'cnn' and args.dataset == 'mnist':
        net_glob = CNNMnist(args=args).to(args.device)
    elif args.model == 'LeNet' and args.dataset == 'traffic':
        net_glob = LeNet(args=args).to(args.device)
        prev_net_glob = LeNet(args=args).to(args.device)
        #rsu0_glob = LeNet(args=args).to(args.device)
        #rsu1_glob = LeNet(args=args).to(args.device)
        #rsu2_glob = LeNet(args=args).to(args.device)
        #rsu3_glob = LeNet(args=args).to(args.device)
    elif args.model == 'mlp':
        len_in = 1
        for x in img_size:
            len_in *= x
        net_glob = MLP(dim_in=len_in, dim_hidden=200, dim_out=args.num_classes).to(args.device)
    else:
        exit('Error: unrecognized model')
    print(net_glob)
    net_glob.train() #get initial weights

    # copy weights
    w_glob = net_glob.state_dict() #assign initial global model weights to w_glob

    # training
    loss_train = []
    #cv_loss, cv_acc = [], []
    #val_loss_pre, counter = 0, 0
    #net_best = None
    #best_loss = None
    #val_acc_list, net_list = [], []

    #if prev_net_glob == net_glob:
    #    print("same")
    #else:
    #    print("different")
    #newline
    train_accuracy = []
    test_accuracy = []
    prev_acc_test = 0
    count = 0
    #until here
    since_rekey = 0
    #phish_recovered = True
    victims = []
    #victims_copy = []
    #ioc = [] #known attack pattern
    #attacker signature change probability 50%
    #dos_signature = ["d0", "d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "d10", "d11", "d12", "d13", "d14"]
    #phish_signature = ["p0", "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13", "p14"]
    #dp_signature = ["dp0", "dp1", "dp2", "dp3", "dp4", "dp5", "dp6", "dp7", "dp8", "dp9", "dp10", "dp11", "dp12", "dp13", "dp14"]
    #d_signature = "d0"
    #p_signature = "p0"
    #dp_signature = "dp0"
    mission_acc_condition = 0
    up_time = []
    ccs_dos_happend = 0
    #tp = 0.90
    #tn = 0.90
    #fn = 1 - tp
    #fp = 1 - tp
    #comp_interval = 0

    dp_success = 0
    dos_success = 0

    dp_twice = 0
    mp_twice = 0

    victim_dp = None
    victim_mp = None

    compromised = 0

    #has_rekeyed = 0

    #total_number_attacks = 0
    #number_attack_success = 0
    attack = None
    count_dp_test = 0
    test_train_cases = []
    test_train_cases_new = []

    test_train_cases_fn0 = []
    test_train_cases_new_fn0 = []


    test_train_cases_fn1 = []
    test_train_cases_new_fn1 = []

    test_train_cases_fn2 = []
    test_train_cases_new_fn2 = []

    test_train_cases_fn3 = []
    test_train_cases_new_fn3 = []

    rsu_participate = ["true", "true", "true", "true"]
    ccs_alive = "true"

    pd_rekey = 0.8
    pd_nf = 0.8
    pd_su = 0.7



    outcome = None


    print("length before fl", len(List))

    if args.all_clients:  #if aggregation over all clients
        print("Aggregation over all clients")
        w_locals = [w_glob for i in range(args.num_users)] #assign initial global weights to all local clients
    #print(args) checking all args values
    for iter in range(args.epochs):  #args.epochs is rounds of training. For every round of training
        print("length of List:", len(List))
        labels = []
        test_train_cases = []
        test_train_cases_new = []
        rsu_store = []
        rsu_service_success = []

        test_train_cases_fn0 = []
        test_train_cases_new_fn0 = []

        test_train_cases_fn1 = []
        test_train_cases_new_fn1 = []

        test_train_cases_fn2 = []
        test_train_cases_new_fn2 = []

        test_train_cases_fn3 = []
        test_train_cases_new_fn3 = []

        #print("total:", total_number_attacks)
        #print("success attack:", number_attack_success)


        #dataset_train = list(dataset_train)

        #del list(dataset_train[0])
        #del dataset_train[0][1]
        #print(dataset_train)

        """
        dataset_train = list(dataset_train)

        for i in range(len(dataset_train)):

            if i in dict_users[str(victim)]:
                test_train_cases.append(dataset_train[i])
        #print(test_train_cases[0:5])
        #print(len(test_train_cases))
        print(dict_users[str(victim)])

        for i in test_train_cases:
            if i[1] == 45 or i[1] == 30 or i[1] == 18 or i[1] == 41:
                test_train_cases_new.append(i)

        #print(len(test_train_cases_new))
        #print(test_train_cases_new)

        #print(type(test_train_cases_new))
        """

        #print(len(dict_users[str(0)]))
        #print(dict_users[str(0)])
        #print(len(test_train_cases))



        #print("this is the one:", dict_users[str(1)][0])
        #print("this is the one:", type(dict_users[str(1)][0]))
        #print("this is the two:", dict_users[str(1)])
        #print("this is the three:", len((dict_users[str(1)])))

        #total number of data poisoning attack performed
        """ 
        labels = []
        attack_rows = 0
        #print("this is the two:", dict_users[str(0)])
        for i in range(len(dict_users[str(0)])):
            #print("label:", dataset_train[dict_users[str(0)][i]][1])
            labels.append(dataset_train[dict_users[str(0)][i]][1])

        print(labels)

        for i in labels:
            if (i == 45 or i == 30 or i == 18 or i == 41):
                attack_rows += 1
        total_number_attacks = total_number_attacks + attack_rows
        print("dsfdsfdsfdsafdsafdsf:", attack_rows)
        
        """

        #node_compromised = [False, False, False, False, False]
        print("iterrrrrrrr",iter)
        data_length = data_length_copy.copy()

        print(len(data_length))
        print(data_length)
        print(len(data_length_copy))
        print(data_length_copy)

        #dp_success = 0
        #dos_success = 0


        #if iter == 0:
        #    whole_start = time.time()
        #    start = time.time()


        #if prev_net_glob == net_glob:
        #    print("it is same")
        #else:
        #    print("it is different")

        #print(prev_net_glob)
        #print(net_glob)

        #####newline
        #if iter != 0:

    #################################start of the rsu and ccs communication##########################################


        #new_adding a2 (ccs operate), s2 (enough ac to create initial global model), sv2 (did the task)?, #sd2 (send to rsu)?
        if iter == 0:
            List.append('true')
            List.append('true')
            List.append('true')
            total_number_service += 1
            number_service_success += 1
            print("leng of list after a2, s2, sv2 in iter1:", len(List))
        ####newline


        loss_locals = [] #create loss_locals
        if not args.all_clients:  # if not aggregation over all clients
            w_locals = []   #create a empty list for a list for weights of all clients
        m = max(int(args.frac * args.num_users), 1) #m is selected clients and in my work, all clients selected do successfully upload its local model
        #np.random.seed(iter)    #Reproducibility
        idxs_users = np.random.choice(users, m, replace=False)  #picking m clients randomly out of total num_users without replacement #range(args.num_users)
        print("newline:",idxs_users)
        idxs_users.sort()

        print("newline:", idxs_users)
        #hello = idxs_users.remove(1)
        #print("newnew:", hello)

        #adding r0, r1, r2, r3 - if rsu is alive and active
        # May perform dos or data poisoning
        #victim = random.choice(idxs_users)
        #print("victim:",victim)
        #print(type(victim))
        #print("what is the type:",type(idxs_users[0]))
        #print(idxs_users[0]+4)

        #if iter >= 1:
        #    since_rekey += 1
        #victim = None

        fn = []
        fp = []
        tn = []
        tp = []

        # done with NIDS (if detected as compromised then isolate it for one FL iteration and put it back to the network as benign)
        if iter >= 1:
            print("real:",node_compromised)
            print("nids:",node_compromised_NIDS)

            for i in range(len(node_compromised)): # if seeing compromised as compromised, putting back in the network
                if (node_compromised[i] == True and node_compromised_NIDS[i] == True):
                    node_compromised[i] = False

            for i in range(len(node_compromised)): #it was range(len(node_compromised))
                if node_compromised[i] == True: #for compromised nodes
                    if random.random() < 0.95: #TP
                        node_compromised_NIDS[i] = True #compromised as compromised = evicted
                        tp.append(i)
                    else: #FN
                        node_compromised_NIDS[i] = False #compromised as normal = alredy compromised (phished) so keep doing dp
                        fn.append(i)
                        #dp_twice = 1

                else: #for normal nodes
                    #random_num = random.random()
                    if random.random() < 0.99: #TN
                        node_compromised_NIDS[i] = False #normal as normal = good nodes that are not atttacked yet - should be targeted by attacker
                        tn.append(i)
                    else: #FP
                        node_compromised_NIDS[i] = True #normal as compromised = evicted
                        fp.append(i)

            for i in range(len(node_compromised_NIDS)-1):
                if node_compromised_NIDS[i] == True: #for any nodes (fp and tp) detected as compromised, isolate it for one iteration
                    del data_length[i]
                    idxs_users = np.delete(idxs_users, np.where(idxs_users == i))
                    #now remaining fn and tn

            #for i in fn: # remain only normal as normal - TN in available victim
            #    idxs_users = np.delete(idxs_users, np.where(idxs_users == i))
            #    print("users with normal as normal:", idxs_users)

            print("ground truth:", node_compromised)
            print("nids decided:", node_compromised_NIDS)


            if node_compromised_NIDS[4] == True: #if ccs is detected as compromised but it was always normal, then service-tasks are false and move to next iteration
                #everything is false
                # new_adding all false when dos attack to ccs
                for i in range(24):
                    List.append("false")
                print("leng of list after dos falsely compromised:", len(List))
                total_number_service += 5
                # new_adding all false when dos attack to ccs
                continue


            print("this is fn:", fn)
            print("this is fp:", fp)
            print("this is tn:", tn)
            print("this is tp:", tp)

            rsu_participate = []

            for i in range(len(node_compromised_NIDS)-1):
                print("number index:",i)
                #print(rsu_participate)

                if node_compromised_NIDS[i] == True:
                    rsu_participate.append("false")
                else:
                    rsu_participate.append("true")

            if node_compromised_NIDS[4] == True:
                ccs_alive = "false"
            else:
                ccs_alive = "true"


            #print("ground truth:", node_compromised)



        #done with NIDS
        """
        if iter >= 1:
            if compromised == 1:
                if random.random() <= 0.20: #FN: seeing compromised as normal; else would be TP
                    print("seeing compromised as normal - one more iteration of compromised state will go on")
                    #new code for compromised for two fl rounds
                    if dos_success == 1: #or attack == 4 or attack == 5:
                        #if dos on rsu or ccs
                        #data_length.pop(victim)
                        del data_length[victim]
                        index = np.argwhere(idxs_users == victim)  # the node compromised by dos
                        idxs_users = np.delete(idxs_users, index)

                        #####done
                    if dos_success == 6:  # or attack == 4 or attack == 5:
                        dos_success = 0
                        dp_success = 0
                        compromised = 0
                        continue

                        #####done
                    if dp_success == 1:
                        victim_dp = victim
                        #idxs_users.remove(victim_dp)
                        dp_twice = 1

                    if dp_success == 2:
                        victim_mp = victim
                        #idxs_users.remove(victim_mp)
                        mp_twice = 1
                else:
                    print("TP: correctly detected compromised node - ended with only one compromised iteration")
        """




                #end of new code for compromised for two fl rounds
            #else: #TP and TN: Correctly detected
            #    print("TP: compromised node detected correctly and stopped after 1 compromised iteration")
            #    print("TN: uncompromised node detected correctly so did nothing - let it be")


        dp_success = 0
        dos_success = 0
        compromised = 0

        #print("netnetnetnet:", net_glob)


                #test_train_cases_fn0 = []
                # test_train_cases_new_fn0 = []
        ########fn######

        for i in fn:
            if i == 0:
                dataset_train = list(dataset_train)

                for j in range(len(dataset_train)): #2016

                    if j in dict_users[str(0)]:
                        test_train_cases_fn0.append(dataset_train[j])
                # print(test_train_cases[0:5])
                # print(len(test_train_cases))
                print(dict_users[str(0)])


                for k in test_train_cases_fn0:
                    if k[1] == 45 or k[1] == 30 or k[1] == 18 or k[1] == 41:
                        test_train_cases_new_fn0.append(k)

                # this is for total_attack
                labels = []
                attack_rows = 0
                # print("this is the two:", dict_users[str(0)])
                for n in range(len(dict_users[str(0)])):
                    # print("label:", dataset_train[dict_users[str(0)][i]][1])
                    labels.append(dataset_train[dict_users[str(0)][n]][1])

                print(labels)

                for m in labels:
                    if (m == 45 or m == 30 or m == 18 or m == 41):
                                attack_rows += 1
                total_number_attacks = total_number_attacks + attack_rows
                print("attacked_row_0:", attack_rows)

            elif i == 1:
                dataset_train = list(dataset_train)

                for j in range(len(dataset_train)):  # 2016

                    if j in dict_users[str(1)]:
                        test_train_cases_fn1.append(dataset_train[j])
                # print(test_train_cases[0:5])
                # print(len(test_train_cases))
                print(dict_users[str(1)])

                for k in test_train_cases_fn1:
                    if k[1] == 45 or k[1] == 30 or k[1] == 18 or k[1] == 41:
                        test_train_cases_new_fn1.append(k)

                # this is for total_attack
                labels = []
                attack_rows = 0
                # print("this is the two:", dict_users[str(0)])
                for n in range(len(dict_users[str(1)])):
                    # print("label:", dataset_train[dict_users[str(0)][i]][1])
                    labels.append(dataset_train[dict_users[str(1)][n]][1])

                print(labels)

                for m in labels:
                    if (m == 45 or m == 30 or m == 18 or m == 41):
                        attack_rows += 1
                total_number_attacks = total_number_attacks + attack_rows
                print("attacked_row_1:", attack_rows)

            elif i == 2:
                dataset_train = list(dataset_train)

                for j in range(len(dataset_train)):  # 2016

                    if j in dict_users[str(2)]:
                        test_train_cases_fn2.append(dataset_train[j])
                # print(test_train_cases[0:5])
                # print(len(test_train_cases))
                print(dict_users[str(2)])

                for k in test_train_cases_fn2:
                    if k[1] == 45 or k[1] == 30 or k[1] == 18 or k[1] == 41:
                        test_train_cases_new_fn2.append(k)

                # this is for total_attack
                labels = []
                attack_rows = 0
                # print("this is the two:", dict_users[str(0)])
                for n in range(len(dict_users[str(2)])):
                    # print("label:", dataset_train[dict_users[str(0)][i]][1])
                    labels.append(dataset_train[dict_users[str(2)][n]][1])

                print(labels)

                for m in labels:
                    if (m == 45 or m == 30 or m == 18 or m == 41):
                        attack_rows += 1
                total_number_attacks = total_number_attacks + attack_rows
                print("attacked_row_fn2:", attack_rows)



            elif i == 3:
                dataset_train = list(dataset_train)

                for j in range(len(dataset_train)):  # 2016

                    if j in dict_users[str(3)]:
                        test_train_cases_fn3.append(dataset_train[j])
                # print(test_train_cases[0:5])
                # print(len(test_train_cases))
                print(dict_users[str(3)])

                for k in test_train_cases_fn3:
                    if k[1] == 45 or k[1] == 30 or k[1] == 18 or k[1] == 41:
                        test_train_cases_new_fn3.append(k)

                # this is for total_attack
                labels = []
                attack_rows = 0
                # print("this is the two:", dict_users[str(0)])
                for n in range(len(dict_users[str(3)])):
                    # print("label:", dataset_train[dict_users[str(0)][i]][1])
                    labels.append(dataset_train[dict_users[str(3)][n]][1])

                print(labels)

                for m in labels:
                    if (m == 45 or m == 30 or m == 18 or m == 41):
                        attack_rows += 1
                total_number_attacks = total_number_attacks + attack_rows
                print("attacked_row_fn3:", attack_rows)







        ########endoffn######
        """
        if (attack == 4):
            dataset_train = list(dataset_train)

            for i in range(len(dataset_train)):

                if i in dict_users[str(victim)]:
                    test_train_cases.append(dataset_train[i])
            # print(test_train_cases[0:5])
            # print(len(test_train_cases))
            print(dict_users[str(victim)])

            for i in test_train_cases:
                if i[1] == 45 or i[1] == 30 or i[1] == 18 or i[1] == 41:
                    test_train_cases_new.append(i)
        ########endoffn######
        """





        #print("this is the length of dataset train:",len(dataset_train))

        #random.choice([i for i in a if i not in [0,1,2]])


        if random.random() < 0.4: #60% chance of an attack happening
            #victim = random.choice(idxs_users)

            #print("this is the data_length:", data_length)

            #dos on rsu node = 1
            #dos on transmission from rsu to ccs = 2
            #dos on transmission from ccs to rsu = 3
            #label flipping = 4
            #local model poisoning = 5
            #dos on ccs itself = 6

            attack = None



            if iter == 0:
                #attacks = [4]
                attacks = [1, 2, 3, 4, 5]
                attack = random.choice(attacks)
            elif iter == 14:
                attacks = [1, 2, 3, 4, 5, 6]
                attack = random.choice(attacks)
            else:
                attacks = [1, 2, 3, 4, 5, 6]
                attack = random.choice(attacks)


            if attack != 6:
                victim = random.choice([i for i in idxs_users if i not in fn])
                print("this is the whole remaining nodes:", idxs_users)
                print("this is the chosen victim node:", victim)






            if (attack != 4 or attack != 5):
                total_number_attacks += 1



            if (attack == 4):
                dataset_train = list(dataset_train)

                for i in range(len(dataset_train)):

                    if i in dict_users[str(victim)]:
                        test_train_cases.append(dataset_train[i])
                # print(test_train_cases[0:5])
                # print(len(test_train_cases))
                print(dict_users[str(victim)])

                for i in test_train_cases:
                    if i[1] == 45 or i[1] == 30 or i[1] == 18 or i[1] == 41:
                        test_train_cases_new.append(i)

                # print(len(test_train_cases_new))
                # print(test_train_cases_new)

                # print(type(test_train_cases_new))




            print("this is the selected attack:", attack)

            vul = vulnerability(EV, SV, UV)  # this is the new version

            print("this is the EV:", EV)
            print("this is the SV:", SV)
            print("this is the UV:", UV)
            print("this is vul", vul)

            # start of attack 6
            if attack == 6: #random.random() < 0.5: #choose to perform either dos or phishing+dp
                if random.random() < vul[4]: #(SV[victim] * UV[victim]): #compromised; #########then node being attacked is compromised by dos
                    #have if/else for change key
                    number_attack_success += 1

                    print("dos attack to ccs itself")
                    compromised = 1
                    dos_success = 6
                    ccs_alive = "false"
                    rsu_participate = ["false, false", "false", "false"]
                    UV[4] += (UV[4] * 0.1)  # increase UV by 10%

                    # asset capacity update
                    ccs_asset[0][0] += (ccs_asset[0][0] * 0.3)
                    ccs_asset[0][1] += (ccs_asset[0][1] * 0.3)

                    #since_rekey += 1
                    #print("elapse:", since_rekey)
                    #EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                    #AC(ccs_asset[0][0], ccs_asset[0][1])

                    #consequence is no aggregation, no prediction on app, app is down until the end of current iteration.

                    #node_compromised[victim] = True
                    #UV[victim] += (UV[victim] * 0.1) #increase UV by 10%

                    #index = np.argwhere(idxs_users == victim) #the node compromised by dos
                    #idxs_users = np.delete(idxs_users, index)

                    #print("due to a compromised node by dos:",idxs_users)
                    #print("this is the victim:", victim)
                    #print("if dos happens:", np.sort(idxs_users))

                    #adding r
                    #all = np.array([0,1,2,3])
                    #for i in all:
                    #    if i in np.sort(idxs_users):
                    #        List.append('true')
                    #    else:
                    #        List.append('false')


                    defenses = ["rekey", "nf", "su"]
                    defense = random.choice(defenses)
                    if defense == "nf":
                        if random.random() < pd_nf:
                            print("perform Network Filtering")
                            UV = [i * 0.9 for i in UV]
                            since_rekey += 1
                            print("elapse:", since_rekey)
                            EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")

                    elif defense == "rekey":
                        if random.random() < pd_rekey:
                            print("perform rekeying")
                            #phish_recovered = True
                            node_compromised = [False, False, False, False, False]
                            victims.clear()
                            EV = [i * math.exp(-1 / 1) for i in EV_initial]
                            since_rekey = 0
                            print("elapse:", since_rekey)
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")

                        #EV[4] = EV[4] * math.exp(-1 / 1)
                    elif defense == "su":
                        if random.random() < pd_su:
                            SV = [i * 0.9 for i in SV]
                            since_rekey += 1
                            print("elapse:", since_rekey)
                            EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")


                    #new_adding all false when dos attack to ccs
                    for i in range(24):
                        List.append("false")
                    print("leng of list after ccs dos:", len(List))
                    # new_adding all false when dos attack to ccs

                    total_number_service += 5

                    continue
                    # everything is false
                    #print(List)
                    #print(len(List))

                else: #not compromised
                    #new_adding sd2: whether ccs send to rsu
                    if iter >= 1:
                        for i in range(len(node_compromised_NIDS)-1):
                            if node_compromised_NIDS[i] == False:
                                List.append('true')
                            elif node_compromised_NIDS[i] == True:
                                List.append('false')
                        print("leng of list after sd2:", len(List))
                    # new_ending sd2: whether ccs send to rsu

                    # ids
                    print("failed dos attack to ccs itself")
                    ccs_alive = "true"

                    #print("seeing normal as compromised - evict the node")  # app down
                    #dos_success = 6

                    #node_compromised[victim] = False
                    #UV[victim] += (UV[victim] * 0.1)  # increase UV by 10%
                    #print("this is the victim:", victim)
                    #nodeStatus[victim] = False
                    #UV[victim] += (UV[victim] * 0.1)  # increase UV by 10%

                    UV[4] += (UV[4] * 0.1)  # increase UV by 10%

                    #asset capacity update
                    ccs_asset[0][0] += (ccs_asset[0][0] * 0.3)
                    ccs_asset[0][1] += (ccs_asset[0][1] * 0.3)
                    #AC(ccs_asset[0][0], ccs_asset[0][1])

                    #consequence is nothing happen due to failure of ddos

                    #adding r
                    #all = np.array([0, 1, 2, 3])
                    #for i in all:
                    #    if i in np.sort(idxs_users):
                    #        List.append('true')
                    #    else:
                    #        List.append('false')

                    # if the defender performs
                    defenses = ["rekey", "nf", "su"]
                    defense = random.choice(defenses)
                    if defense == "nf":
                        if random.random() < pd_nf:
                            print("perform Network Filtering")
                            UV = [i * 0.9 for i in UV]
                            since_rekey += 1
                            print("elapse:", since_rekey)
                            EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")


                    elif defense == "rekey":
                        if random.random() < pd_rekey:
                            print("perform rekeying")
                            #phish_recovered = True
                            node_compromised = [False, False, False, False, False]
                            victims.clear()
                            EV = [i * math.exp(-1 / 1) for i in EV_initial]
                            since_rekey = 0
                            print("elapse:", since_rekey)
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")

                    elif defense == "su":
                        if random.random() < pd_su:
                            SV = [i * 0.9 for i in SV]
                            since_rekey += 1
                            print("elapse:", since_rekey)
                            EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")
            #end of attack 6



            #vul = vulnerability(EV, SV, UV) #this is the new version


            if attack == 1: #random.random() < 0.5: #choose to perform either dos or phishing+dp
                if random.random() < vul[victim]: #(SV[victim] * UV[victim]): #compromised; #########then node being attacked is compromised by dos
                    number_attack_success += 1
                    #newcode
                    victims.append(victim)
                    #end of newcode
                    print("node compromised by dos")
                    compromised = 1
                    dos_success = 1

                    rsu_participate[victim] = 'false'

                    # asset capacity update
                    rsu_asset[victim][0] += (rsu_asset[victim][0] * 0.3)
                    rsu_asset[victim][1] += (rsu_asset[victim][1] * 0.3)
                    #AC(rsu_asset[victim][0], rsu_asset[victim][1])

                    # new_adding SD2 (sending model ccs to rsu)
                    if iter == 0:
                        for i in range(4):
                            if i == victim:
                                List.append('true')
                            else:
                                List.append('true')
                        print("leng of list after sd2 in iter0:", len(List))

                    if iter >= 1:
                        for i in range(len(node_compromised_NIDS) - 1):
                            if node_compromised_NIDS[i] == False:
                                List.append('true')
                            elif node_compromised_NIDS[i] == True:
                                List.append('false')
                        print("leng of list after sd2:", len(List))
                    # new_end SD2 (sending model ccs to rsu)


                    #data_length.pop(victim)
                    del data_length[victim]
                    print("updated data_length:", data_length)

                    #node_compromised[victim] = True
                    UV[victim] += (UV[victim] * 0.1) #increase UV by 10%
                    #print(UV)
                    #print(victim)
                    index = np.argwhere(idxs_users == victim) #the node compromised by dos
                    idxs_users = np.delete(idxs_users, index)

                    #print("due to a compromised node by dos:",idxs_users)
                    #print("this is the victim:", victim)
                    #print("if dos happens:", np.sort(idxs_users))
                    #adding r
                    #all = np.array([0,1,2,3])
                    #for i in all:
                    #    if i in np.sort(idxs_users):
                    #        List.append('true')
                    #    else:
                    #        List.append('false')

                    defenses = ["rekey", "nf", "su"]
                    defense = random.choice(defenses)
                    if defense == "nf":
                        if random.random() < pd_nf:
                            print("perform Network Filtering")
                            UV = [i * 0.9 for i in UV]
                            since_rekey += 1
                            print("elapse:", since_rekey)
                            EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")

                    elif defense == "rekey":
                        if random.random() < pd_rekey:
                            print("perform rekeying")
                            node_compromised = [False, False, False, False, False]
                            #phish_recovered = True
                            victims.clear()
                            EV = [i * math.exp(-1 / 1) for i in EV_initial]
                            since_rekey = 0
                            print("elapse:", since_rekey)
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")
                    elif defense == "su":
                        if random.random() < pd_su:
                            SV = [i * 0.9 for i in SV]
                            since_rekey += 1
                            print("elapse:", since_rekey)
                            EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")
                        #EV = [i * math.exp(-1 / rekey) for i in EV] #EV = [math.exp((-1 * i) / rekey) for i in EV]
                    #print(List)
                    #print(len(List))

                else: #not compromised

                    #node_compromised[victim] = False

                    # asset capacity update
                    rsu_asset[victim][0] += (rsu_asset[victim][0] * 0.3)
                    rsu_asset[victim][1] += (rsu_asset[victim][1] * 0.3)
                    #AC(rsu_asset[victim][0], rsu_asset[victim][1])

                    print("only impacted by dos; not compromised")
                    rsu_participate[victim] = 'true'
                    print("this is the victim:", victim)
                    UV[victim] += (UV[victim] * 0.1)  # increase UV by 10%

                    # new_adding SD2 (sending model ccs to rsu)
                    if iter == 0:
                        for i in range(4):
                            if i == victim:
                                List.append('true')
                            else:
                                List.append('true')
                        print("leng of list after sd2 in iter0:", len(List))

                    if iter >= 1:
                        for i in range(len(node_compromised_NIDS) - 1):
                            if node_compromised_NIDS[i] == False:
                                List.append('true')
                            elif node_compromised_NIDS[i] == True:
                                List.append('false')
                        print("leng of list after sd2:", len(List))
                    # new_end SD2 (sending model ccs to rsu)

                    #adding r
                    #all = np.array([0, 1, 2, 3])
                    #for i in all:
                    #    if i in np.sort(idxs_users):
                    #        List.append('true')
                    #    else:
                    #        List.append('false')

                    # if the defender performs
                    defenses = ["rekey", "nf", "su"]
                    defense = random.choice(defenses)
                    if defense == "nf":
                        if random.random() < pd_nf:
                            print("perform Network Filtering")
                            UV = [i * 0.9 for i in UV]
                            since_rekey += 1
                            print("elapse:", since_rekey)
                            EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")

                    elif defense == "rekey":
                        if random.random() < pd_rekey:
                            print("perform rekeying")
                            node_compromised = [False, False, False, False, False]
                            #phish_recovered = True
                            victims.clear()
                            EV = [i * math.exp(-1 / 1) for i in EV_initial]
                            since_rekey = 0
                            print("elapse:", since_rekey)
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")

                    elif defense == "su":
                        if random.random() < pd_su:
                            SV = [i * 0.9 for i in SV]
                            since_rekey += 1
                            print("elapse:", since_rekey)
                            EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")

            #######NIDS DONE WITH ATTACK 1


            ######attack 2 (jamming attack between RSU and CCS)
            # attack 2: delete the local model trained by the RSU (i.e., sender) node from the w_local
            if attack == 2: #random.random() < 0.5: #choose to perform either dos or phishing+dp
                if random.random() < vul[victim]:
                    number_attack_success += 1
                    rsu_participate[victim] = 'true'


                    #have if/else for change key
                    dos_success = 2


                    print("jamming attack a path going from rsu to ccs")
                    #only consequence is not sending
                    #data_length.pop(victim)
                    del data_length[victim]

                    # new_adding SD2 (sending model ccs to rsu)
                    if iter == 0:
                        for i in range(4):
                            if i == victim:
                                List.append('true')
                            else:
                                List.append('true')
                        print("leng of list after sd2 in iter0:", len(List))

                    if iter >= 1:
                        for i in range(len(node_compromised_NIDS) - 1):
                            if node_compromised_NIDS[i] == False:
                                List.append('true')
                            elif node_compromised_NIDS[i] == True:
                                List.append('false')
                        print("leng of list after sd2:", len(List))
                    # new_end SD2 (sending model ccs to rsu)


                    print("updated data_length:", data_length)

                    #node_compromised[victim] = True
                    #UV[victim] += (UV[victim] * 0.1)  # increase UV by 10%
                    # print(UV)
                    # print(victim)

                    print("updated data_length:", data_length)

                    #node_compromised[victim] = True
                    UV[victim] += (UV[victim] * 0.1) #increase UV by 10%

                    #index = np.argwhere(idxs_users == victim) #the node compromised by dos
                    #idxs_users = np.delete(idxs_users, index)

                    #print("due to a compromised node by dos:",idxs_users)
                    print("this is the victim:", victim)
                    #print("if dos happens:", np.sort(idxs_users))
                    #adding r
                    #all = np.array([0,1,2,3])
                    #for i in all:
                    #    if i in np.sort(idxs_users):
                    #        List.append('true')
                    #    else:
                    #        List.append('false')

                    defenses = ["rekey", "nf", "su"]
                    defense = random.choice(defenses)
                    if defense == "nf":
                        if random.random() < pd_nf:
                            print("perform Network Filtering")
                            UV = [i * 0.9 for i in UV]
                            since_rekey += 1
                            print("elapse:", since_rekey)
                            EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")

                    elif defense == "rekey":
                        if random.random() < pd_rekey:
                            print("perform rekeying")
                            #phish_recovered = True
                            node_compromised = [False, False, False, False, False]
                            victims.clear()
                            EV = [i * math.exp(-1 / 1) for i in EV_initial]
                            since_rekey = 0
                            print("elapse:", since_rekey)
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")

                    elif defense == "su":
                        if random.random() < pd_su:
                            SV = [i * 0.9 for i in SV]
                            since_rekey += 1
                            print("elapse:", since_rekey)
                            EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")
                    #print(List)
                    #print(len(List))

                else:
                    print("jamming failed;")
                    print("this is the victim:", victim)
                    rsu_participate[victim] = 'true'
                    #node_compromised[victim] = False
                    #UV[victim] += (UV[victim] * 0.1)  # increase UV by 10%
                    UV[victim] += (UV[victim] * 0.1)  # increase UV by 10%

                    # new_adding SD2 (sending model ccs to rsu)
                    if iter == 0:
                        for i in range(4):
                            if i == victim:
                                List.append('true')
                            else:
                                List.append('true')
                        print("leng of list after sd2 in iter0:", len(List))

                    if iter >= 1:
                        for i in range(len(node_compromised_NIDS) - 1):
                            if node_compromised_NIDS[i] == False:
                                List.append('true')
                            elif node_compromised_NIDS[i] == True:
                                List.append('false')
                        print("leng of list after sd2:", len(List))
                    # new_end SD2 (sending model ccs to rsu)
                    #adding r
                    #all = np.array([0, 1, 2, 3])
                    #for i in all:
                    #    if i in np.sort(idxs_users):
                    #        List.append('true')
                    #    else:
                    #        List.append('false')

                    # if the defender performs
                    defenses = ["rekey", "nf", "su"]
                    defense = random.choice(defenses)
                    if defense == "nf":
                        if random.random() < pd_nf:
                            print("perform Network Filtering")
                            UV = [i * 0.9 for i in UV]
                            since_rekey += 1
                            print("elapse:", since_rekey)
                            EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")

                    elif defense == "rekey":
                        if random.random() < pd_rekey:
                            print("perform rekeying")
                            #phish_recovered = True
                            node_compromised = [False, False, False, False, False]
                            victims.clear()
                            EV = [i * math.exp(-1 / 1) for i in EV_initial]
                            since_rekey = 0
                            print("elapse:", since_rekey)
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")

                    elif defense == "su":
                        if random.random() < pd_su:
                            SV = [i * 0.9 for i in SV]
                            since_rekey += 1
                            print("elapse:", since_rekey)
                            EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")



            ######## NIDS FOR ATTACK 2 IS DONE


            # attack 3: have the RSU node (i.e., recipient) train with the local model it had for the previous iteration
            if attack == 3: #random.random() < 0.5: #choose to perform either dos or phishing+dp
                if random.random() < vul[victim]: #(SV[victim] * UV[victim]): #compromised; #########then node being attacked is compromised by dos
                    #have if/else for change key
                    number_attack_success += 1
                    rsu_participate[victim] = 'false'

                    del data_length[victim]
                    print("jamming attack to a path going from ccs to rsu")
                    dos_success = 3

                    UV[4] += (UV[4] * 0.1)  # increase UV by 10%

                    #new_adding SD2 (sending model ccs to rsu)
                    if iter == 0:
                        for i in range(4):
                            if i == victim:
                                List.append('false')
                            else:
                                List.append('true')
                        print("leng of list after sd2 in iter 0:", len(List))


                    if iter >= 1:
                        for i in range(len(node_compromised_NIDS)-1):
                            if node_compromised_NIDS[i] == False and i != victim:
                                List.append('true')
                            elif node_compromised_NIDS[i] == False and i == victim:
                                List.append('false')
                            elif node_compromised_NIDS[i] == True:
                                List.append('false')
                        print("leng of list after sd2 in iter 0:", len(List))
                    #new_end SD2 (sending model ccs to rsu)







                    #the only consequence is not being able to send

                    #node_compromised[victim] = True
                    #UV[victim] += (UV[victim] * 0.1) #increase UV by 10%

                    #index = np.argwhere(idxs_users == victim) #the node compromised by dos
                    #idxs_users = np.delete(idxs_users, index)

                    #print("due to a compromised node by dos:",idxs_users)
                    print("this is the victim:", victim)
                    #print("if dos happens:", np.sort(idxs_users))
                    #adding r

                    #all = np.array([0,1,2,3])
                    #for i in all:
                    #    if i in np.sort(idxs_users):
                    #        List.append('true')
                    #    else:
                    #        List.append('false')

                    defenses = ["rekey", "nf", "su"]
                    defense = random.choice(defenses)
                    if defense == "nf":
                        if random.random() < pd_nf:
                            print("perform Network Filtering")
                            UV = [i * 0.9 for i in UV]
                            since_rekey += 1
                            print("elapse:", since_rekey)
                            EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")

                    elif defense == "rekey":
                        if random.random() < pd_rekey:
                            print("perform rekeying")
                            #phish_recovered = True
                            node_compromised = [False, False, False, False, False]
                            victims.clear()
                            EV = [i * math.exp(-1 / 1) for i in EV_initial]
                            since_rekey = 0
                            print("elapse:", since_rekey)
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")

                    elif defense == "su":
                        if random.random() < pd_su:
                            SV = [i * 0.9 for i in SV]
                            since_rekey += 1
                            print("elapse:", since_rekey)
                            EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")
                    #print(List)
                    #print(len(List))

                else:
                    rsu_participate[victim] = 'true'
                    print("jamming failed")
                    UV[4] += (UV[4] * 0.1)  # increase UV by 10%
                    #consequence is nothing as jamming failed
                    print("this is the victim:", victim)
                    #node_compromised[victim] = False
                    #UV[victim] += (UV[victim] * 0.1)  # increase UV by 10%

                    # new_adding SD2 (sending model ccs to rsu)
                    if iter == 0:
                        for i in range(4):
                            if i == victim:
                                List.append('true')
                            else:
                                List.append('true')
                        print("leng of list after sd2 in iter0:", len(List))

                    if iter >= 1:
                        for i in range(len(node_compromised_NIDS)-1):
                            if node_compromised_NIDS[i] == False:
                                List.append('true')
                            elif node_compromised_NIDS[i] == True:
                                List.append('false')
                        print("leng of list after sd2:", len(List))
                    # new_end SD2 (sending model ccs to rsu)


                    #adding r
                    #all = np.array([0, 1, 2, 3])
                    #for i in all:
                    #    if i in np.sort(idxs_users):
                    #        List.append('true')
                    #    else:
                    #        List.append('false')

                    # if the defender performs
                    defenses = ["rekey", "nf", "su"]
                    defense = random.choice(defenses)
                    if defense == "nf":
                        if random.random() < pd_nf:
                            print("perform Network Filtering")
                            UV = [i * 0.9 for i in UV]
                            since_rekey += 1
                            print("elapse:", since_rekey)
                            EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")

                    elif defense == "rekey":
                        if random.random() < pd_rekey:
                            print("perform rekeying")
                            #phish_recovered = True
                            node_compromised = [False, False, False, False, False]
                            victims.clear()
                            EV = [i * math.exp(-1 / 1) for i in EV_initial]
                            since_rekey = 0
                            print("elapse:", since_rekey)
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")

                    elif defense == "su":
                        if random.random() < pd_su:
                            SV = [i * 0.9 for i in SV]
                            since_rekey += 1
                            print("elapse:", since_rekey)
                            EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                            print("EV:", EV)
                        else:
                            print("NO DEFENSE PERFORMED")



            #start of attack 6: dos attack on CCS itself: no aggregation, no prediction, traffic application is down.







            if attack == 4: #else: #perform phishing + data poisoning
                if node_compromised[victim] == False:#phish_recovered == True:
                    if random.random() < vul[victim]: #(SV[victim] * (EV[victim] + UV[victim])): #compromised; #########phising attack
                        if random.random() < vul[victim]: #SV[victim]: #still compromised; ########if data poisoning works after phishing suceeds
                            total_number_attacks += 1
                            number_attack_success += 1

                            rsu_asset[victim][0] += (rsu_asset[victim][0] * 0.3)
                            rsu_asset[victim][1] += (rsu_asset[victim][1] * 0.3)


                            rsu_participate[victim] = 'true'

                            # new_adding SD2 (sending model ccs to rsu)
                            if iter == 0:
                                for i in range(4):
                                    if i == victim:
                                        List.append('true')
                                    else:
                                        List.append('true')
                                print("leng of list after sd2 in iter0:", len(List))

                            if iter >= 1:
                                for i in range(len(node_compromised_NIDS) - 1):
                                    if node_compromised_NIDS[i] == False:
                                        List.append('true')
                                    elif node_compromised_NIDS[i] == True:
                                        List.append('false')
                                print("leng of list after sd2:", len(List))
                            # new_end SD2 (sending model ccs to rsu)

                            # this is for total_attack
                            labels = []
                            attack_rows = 0
                            # print("this is the two:", dict_users[str(0)])
                            for i in range(len(dict_users[str(victim)])):
                                # print("label:", dataset_train[dict_users[str(0)][i]][1])
                                labels.append(dataset_train[dict_users[str(victim)][i]][1])

                            print(labels)

                            for i in labels:
                                if (i == 45 or i == 30 or i == 18 or i == 41):
                                    attack_rows += 1
                            total_number_attacks = total_number_attacks + attack_rows
                            print("attacked_row:", attack_rows)


                            #put what many were misclassifed randomly for number_attack_success


                            compromised = 1
                            print("both phishing and dp succeeded")
                            print("this is the victim:", victim)
                            node_compromised[victim] = True

                            #adding r
                            #all = np.array([0, 1, 2, 3])
                            #for i in all:
                            #    if i in np.sort(idxs_users):
                            #        List.append('true')
                            #    else:
                            #        List.append('false')
                            #########data should be manipulated here
                            #if random.random() < 0.5: #it was 0.5
                            dp_success = 1

                            #print(dict_users[str(victim)])
                            #print(dict_users)
                            #phish_recovered = False


                            defenses = ["rekey", "nf", "su"]
                            defense = random.choice(defenses)
                            if defense == "nf":
                                if random.random() < pd_nf:
                                    print("perform Network Filtering")
                                    UV = [i * 0.9 for i in UV]
                                    since_rekey += 1
                                    print("elapse:", since_rekey)
                                    EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                    print("EV:", EV)
                                else:
                                    print("NO DEFENSE PERFORMED")

                            elif defense == "rekey":
                                if random.random() < pd_rekey:
                                    print("perform rekeying")
                                    #phish_recovered = True
                                    node_compromised = [False, False, False, False, False]
                                    victims.clear()
                                    EV = [i * math.exp(-1 / 1) for i in EV_initial]
                                    since_rekey = 0
                                    print("elapse:", since_rekey)
                                    print("EV:", EV)
                                else:
                                    print("NO DEFENSE PERFORMED")

                            elif defense == "su":
                                if random.random() < pd_su:
                                    SV = [i * 0.9 for i in SV]
                                    since_rekey += 1
                                    print("elapse:", since_rekey)
                                    EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                    print("EV:", EV)
                                else:
                                    print("NO DEFENSE PERFORMED")

                        else: #compromised
                            rsu_asset[victim][0] += (rsu_asset[victim][0] * 0.3)
                            rsu_asset[victim][1] += (rsu_asset[victim][1] * 0.3)



                            rsu_participate[victim] = 'true'
                            total_number_attacks += 1
                            number_attack_success += 1
                            print("only phishing succeeded")
                            compromised = 1
                            print("this is the victim:", victim)
                            node_compromised[victim] = True
                            #phish_recovered = False

                            # new_adding SD2 (sending model ccs to rsu)
                            if iter == 0:
                                for i in range(4):
                                    if i == victim:
                                        List.append('true')
                                    else:
                                        List.append('true')
                                print("leng of list after sd2 in iter0:", len(List))

                            if iter >= 1:
                                for i in range(len(node_compromised_NIDS) - 1):
                                    if node_compromised_NIDS[i] == False:
                                        List.append('true')
                                    elif node_compromised_NIDS[i] == True:
                                        List.append('false')
                                print("leng of list after sd2:", len(List))
                            # new_end SD2 (sending model ccs to rsu)

                            #adding r
                            #all = np.array([0, 1, 2, 3])
                            #for i in all:
                            #    if i in np.sort(idxs_users):
                            #        List.append('true')
                            #    else:
                            #        List.append('false')
                            # if the attacker performs phishing
                            print(dict_users[str(victim)])
                            print(dict_users)

                            defenses = ["rekey", "nf", "su"]
                            defense = random.choice(defenses)
                            if defense == "nf":
                                if random.random() < pd_nf:
                                    print("perform Network Filtering")
                                    UV = [i * 0.9 for i in UV]
                                    since_rekey += 1
                                    print("elapse:", since_rekey)
                                    EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                    print("EV:", EV)
                                else:
                                    print("NO DEFENSE PERFORMED")

                            elif defense == "rekey":
                                if random.random() < pd_rekey:
                                    print("perform rekeying")
                                    #phish_recovered = True
                                    node_compromised = [False, False, False, False, False]
                                    victims.clear()
                                    EV = [i * math.exp(-1 / 1) for i in EV_initial]
                                    since_rekey = 0
                                    print("elapse:", since_rekey)
                                    print("EV:", EV)
                                else:
                                    print("NO DEFENSE PERFORMED")

                            elif defense == "su":
                                if random.random() < pd_su:
                                    SV = [i * 0.9 for i in SV]
                                    since_rekey += 1
                                    print("elapse:", since_rekey)
                                    EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                    print("EV:", EV)
                                else:
                                    print("NO DEFENSE PERFORMED")

                    else: #uncompromised
                        #if phishing initially fails
                        rsu_participate[victim] = 'true'
                        total_number_attacks += 1
                        print("phishing failed")


                        node_compromised[victim] = False

                        # new_adding SD2 (sending model ccs to rsu)
                        if iter == 0:
                            for i in range(4):
                                if i == victim:
                                    List.append('true')
                                else:
                                    List.append('true')
                            print("leng of list after sd2 in iter0:", len(List))

                        if iter >= 1:
                            for i in range(len(node_compromised_NIDS) - 1):
                                if node_compromised_NIDS[i] == False:
                                    List.append('true')
                                elif node_compromised_NIDS[i] == True:
                                    List.append('false')
                            print("leng of list after sd2:", len(List))
                        # new_end SD2 (sending model ccs to rsu)



                        #adding r
                        #all = np.array([0, 1, 2, 3])
                        #for i in all:
                        #    if i in np.sort(idxs_users):
                        #        List.append('true')
                        #    else:
                        #        List.append('false')

                        # if the defender performs
                        defenses = ["rekey", "nf", "su"]
                        defense = random.choice(defenses)
                        if defense == "nf":
                            if random.random() < pd_nf:
                                print("perform Network Filtering")
                                UV = [i * 0.9 for i in UV]
                                since_rekey += 1
                                print("elapse:", since_rekey)
                                EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                print("EV:", EV)
                            else:
                                print("NO DEFENSE PERFORMED")

                        elif defense == "rekey":
                            if random.random() < pd_rekey:
                                print("perform rekeying")
                                #phish_recovered = True
                                node_compromised = [False, False, False, False, False]
                                victims.clear()
                                EV = [i * math.exp(-1 / 1) for i in EV_initial]
                                since_rekey = 0
                                print("elapse:", since_rekey)
                                print("EV:", EV)
                            else:
                                print("NO DEFENSE PERFORMED")

                        elif defense == "su":
                            if random.random() < pd_su:
                                SV = [i * 0.9 for i in SV]
                                since_rekey += 1
                                print("elapse:", since_rekey)
                                EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                print("EV:", EV)
                            else:
                                print("NO DEFENSE PERFORMED")

                elif victim in victims and node_compromised[victim] == True:#phish_recovered == False:
                    if random.random() < vul[victim]: #SV[victim]:  #still compromised;####### if data poisoning works as phishing already suceeded in the previous iteration
                        rsu_participate[victim] = 'true'

                        rsu_asset[victim][0] += (rsu_asset[victim][0] * 0.3)
                        rsu_asset[victim][1] += (rsu_asset[victim][1] * 0.3)

                        # new_adding SD2 (sending model ccs to rsu)
                        if iter == 0:
                            for i in range(4):
                                if i == victim:
                                    List.append('true')
                                else:
                                    List.append('true')
                            print("leng of list after sd2 in iter0:", len(List))

                        if iter >= 1:
                            for i in range(len(node_compromised_NIDS) - 1):
                                if node_compromised_NIDS[i] == False:
                                    List.append('true')
                                elif node_compromised_NIDS[i] == True:
                                    List.append('false')
                            print("leng of list after sd2:", len(List))
                        # new_end SD2 (sending model ccs to rsu)
                        # this is for total_attack
                        labels = []
                        attack_rows = 0
                        # print("this is the two:", dict_users[str(0)])
                        for i in range(len(dict_users[str(victim)])):
                            # print("label:", dataset_train[dict_users[str(0)][i]][1])
                            labels.append(dataset_train[dict_users[str(victim)][i]][1])

                        print(labels)

                        for i in labels:
                            if (i == 45 or i == 30 or i == 18 or i == 41):
                                attack_rows += 1
                        total_number_attacks = total_number_attacks + attack_rows
                        print("attacked_row:", attack_rows)

                        # put what many were misclassifed randomly for number_attack_success





                        #if random.random() < tp:  # seeing compromised as compromised - evict the node
                        #    print("Attack 4 : Seeing fn (seeing compromised as compromised): evict the node")
                        #    index = np.argwhere(idxs_users == victim)  # the node compromised by dos
                        #    idxs_users = np.delete(idxs_users, index)
                        #    data_length.pop(victim)
                        print("phishing already succeeded and dp succeeded")
                        compromised = 1
                        node_compromised[victim] = True


                        print("this is the victim:", victim)
                        #if random.random() < 0.5:
                        dp_success = 1
                        #else:
                            #dp_success = 2

                        #adding r
                        #all = np.array([0, 1, 2, 3])
                        #for i in all:
                        #    if i in np.sort(idxs_users):
                        #        List.append('true')
                        #    else:
                        #        List.append('false')

                        #########data should be manipulated here



                        print("perform dp")
                        print(dict_users[str(victim)])
                        print(dict_users)

                        defenses = ["rekey", "nf", "su"]
                        defense = random.choice(defenses)
                        if defense == "nf":
                            if random.random() < pd_nf:
                                print("perform Network Filtering")
                                UV = [i * 0.9 for i in UV]
                                since_rekey += 1
                                print("elapse:", since_rekey)
                                EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                print("EV:", EV)
                            else:
                                print("NO DEFENSE PERFORMED")

                        elif defense == "rekey":
                            if random.random() < pd_rekey:
                                print("perform rekeying")
                                #phish_recovered = True
                                node_compromised = [False, False, False, False, False]
                                victims.clear()
                                EV = [i * math.exp(-1 / 1) for i in EV_initial]
                                since_rekey = 0
                                print("elapse:", since_rekey)
                                print("EV:", EV)
                            else:
                                print("NO DEFENSE PERFORMED")

                        elif defense == "su":
                            if random.random() < pd_su:
                                SV = [i * 0.9 for i in SV]
                                since_rekey += 1
                                print("elapse:", since_rekey)
                                EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                print("EV:", EV)
                            else:
                                print("NO DEFENSE PERFORMED")

                    else:
                        rsu_participate[victim] = 'true'

                        rsu_asset[victim][0] += (rsu_asset[victim][0] * 0.3)
                        rsu_asset[victim][1] += (rsu_asset[victim][1] * 0.3)

                        # new_adding SD2 (sending model ccs to rsu)
                        if iter == 0:
                            for i in range(4):
                                if i == victim:
                                    List.append('true')
                                else:
                                    List.append('true')
                            print("leng of list after sd2 in iter0:", len(List))

                        if iter >= 1:
                            for i in range(len(node_compromised_NIDS) - 1):
                                if node_compromised_NIDS[i] == False:
                                    List.append('true')
                                elif node_compromised_NIDS[i] == True:
                                    List.append('false')
                            print("leng of list after sd2:", len(List))
                        # new_end SD2 (sending model ccs to rsu)
                        # this is for total_attack
                        labels = []
                        attack_rows = 0
                        # print("this is the two:", dict_users[str(0)])
                        for i in range(len(dict_users[str(victim)])):
                            # print("label:", dataset_train[dict_users[str(0)][i]][1])
                            labels.append(dataset_train[dict_users[str(victim)][i]][1])

                        print(labels)

                        for i in labels:
                            if (i == 45 or i == 30 or i == 18 or i == 41):
                                attack_rows += 1
                        total_number_attacks = total_number_attacks + attack_rows
                        print("attacked_row:", attack_rows)


                        #no successful attack

                        #we say attack was successful when it succeeds to change the label and also misclassify it to a random label data poisoning

                        compromised = 1

                        print("failed data poisoning (label flipping)")
                        print("this is the victim:", victim)
                        node_compromised[victim] = True
                        #phish_recovered = False


                        #adding r
                        #all = np.array([0, 1, 2, 3])
                        #for i in all:
                        #    if i in np.sort(idxs_users):
                        #        List.append('true')
                        #    else:
                        #        List.append('false')
                        # if the attacker performs phishing
                        print(dict_users[str(victim)])
                        print(dict_users)

                        defenses = ["rekey", "nf", "su"]
                        defense = random.choice(defenses)
                        if defense == "nf":
                            if random.random() < pd_nf:
                                print("perform Network Filtering")
                                UV = [i * 0.9 for i in UV]
                                since_rekey += 1
                                print("elapse:", since_rekey)
                                EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                print("EV:", EV)
                            else:
                                print("NO DEFENSE PERFORMED")

                        elif defense == "rekey":
                            if random.random() < pd_rekey:
                                print("perform rekeying")
                                #phish_recovered = True
                                node_compromised = [False, False, False, False, False]
                                victims.clear()
                                EV = [i * math.exp(-1 / 1) for i in EV_initial]
                                since_rekey = 0
                                print("elapse:", since_rekey)
                                print("EV:", EV)
                            else:
                                print("NO DEFENSE PERFORMED")

                        elif defense == "su":
                            if random.random() < pd_su:
                                SV = [i * 0.9 for i in SV]
                                since_rekey += 1
                                print("elapse:", since_rekey)
                                EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                print("EV:", EV)
                            else:
                                print("NO DEFENSE PERFORMED")

            #attack 5
            if attack == 5: #else: #perform phishing + data poisoning
                if node_compromised[victim] == False:#phish_recovered == True:
                    if random.random() < vul[victim]: #(SV[victim] * (EV[victim] + UV[victim])): #compromised; #########phising attack
                        if random.random() < vul[victim]: #SV[victim]: #still compromised; ########if data poisoning works after phishing suceeds
                            rsu_participate[victim] = 'true'

                            rsu_asset[victim][0] += (rsu_asset[victim][0] * 0.3)
                            rsu_asset[victim][1] += (rsu_asset[victim][1] * 0.3)


                            total_number_attacks += 2
                            number_attack_success += 2

                            # new_adding SD2 (sending model ccs to rsu)
                            if iter == 0:
                                for i in range(4):
                                    if i == victim:
                                        List.append('true')
                                    else:
                                        List.append('true')
                                print("leng of list after sd2 in iter0:", len(List))

                            if iter >= 1:
                                for i in range(len(node_compromised_NIDS) - 1):
                                    if node_compromised_NIDS[i] == False:
                                        List.append('true')
                                    elif node_compromised_NIDS[i] == True:
                                        List.append('false')
                                print("leng of list after sd2:", len(List))
                            # new_end SD2 (sending model ccs to rsu)

                            compromised = 1
                            print("phishing aand dp succeeded")

                            print("this is the victim:", victim)
                            node_compromised[victim] = True

                            #adding r
                            #all = np.array([0, 1, 2, 3])
                            #for i in all:
                            #    if i in np.sort(idxs_users):
                            #        List.append('true')
                            #    else:
                            #        List.append('false')
                            #########data should be manipulated here
                            #if random.random() < 0.5: #it was 0.5
                            #dp_success = 1
                            #else:
                            dp_success = 2


                            #print(dict_users[str(victim)])
                            #print(dict_users)
                            #phish_recovered = False

                            defenses = ["rekey", "nf", "su"]
                            defense = random.choice(defenses)
                            if defense == "nf":
                                if random.random() < pd_nf:
                                    print("perform Network Filtering")
                                    UV = [i * 0.9 for i in UV]
                                    since_rekey += 1
                                    print("elapse:", since_rekey)
                                    EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                    print("EV:", EV)
                                else:
                                    print("NO DEFENSE PERFORMED")

                            elif defense == "rekey":
                                if random.random() < pd_rekey:
                                    print("perform rekeying")
                                    #phish_recovered = True
                                    node_compromised = [False, False, False, False, False]
                                    victims.clear()
                                    EV = [i * math.exp(-1 / 1) for i in EV_initial]
                                    since_rekey = 0
                                    print("elapse:", since_rekey)
                                    print("EV:", EV)
                                else:
                                    print("NO DEFENSE PERFORMED")

                            elif defense == "su":
                                if random.random() < pd_su:
                                    SV = [i * 0.9 for i in SV]
                                    since_rekey += 1
                                    print("elapse:", since_rekey)
                                    EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                    print("EV:", EV)
                                else:
                                    print("NO DEFENSE PERFORMED")

                        else: #compromised
                            rsu_participate[victim] = 'true'

                            rsu_asset[victim][0] += (rsu_asset[victim][0] * 0.3)
                            rsu_asset[victim][1] += (rsu_asset[victim][1] * 0.3)

                            total_number_attacks += 1
                            number_attack_success += 1

                            # new_adding SD2 (sending model ccs to rsu)
                            if iter == 0:
                                for i in range(4):
                                    if i == victim:
                                        List.append('true')
                                    else:
                                        List.append('true')
                                print("leng of list after sd2 in iter0:", len(List))

                            if iter >= 1:
                                for i in range(len(node_compromised_NIDS) - 1):
                                    if node_compromised_NIDS[i] == False:
                                        List.append('true')
                                    elif node_compromised_NIDS[i] == True:
                                        List.append('false')
                                print("leng of list after sd2:", len(List))
                            # new_end SD2 (sending model ccs to rsu)

                            compromised = 1
                            print("only phishing succeeded")

                            print("this is the victim:", victim)
                            node_compromised[victim] = True
                            #phish_recovered = False

                            #adding r
                            #all = np.array([0, 1, 2, 3])
                            #for i in all:
                            #    if i in np.sort(idxs_users):
                            #        List.append('true')
                            #    else:
                            #        List.append('false')
                            # if the attacker performs phishing
                            print(dict_users[str(victim)])
                            print(dict_users)

                            defenses = ["rekey", "nf", "su"]
                            defense = random.choice(defenses)
                            if defense == "nf":
                                if random.random() < pd_nf:
                                    print("perform Network Filtering")
                                    UV = [i * 0.9 for i in UV]
                                    since_rekey += 1
                                    print("elapse:", since_rekey)
                                    EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                    print("EV:", EV)
                                else:
                                    print("NO DEFENSE PERFORMED")

                            elif defense == "rekey":
                                if random.random() < pd_rekey:
                                    print("perform rekeying")
                                    #phish_recovered = True
                                    node_compromised = [False, False, False, False, False]
                                    victims.clear()
                                    EV = [i * math.exp(-1 / 1) for i in EV_initial]
                                    since_rekey = 0
                                    print("elapse:", since_rekey)
                                    print("EV:", EV)
                                else:
                                    print("NO DEFENSE PERFORMED")

                            elif defense == "su":
                                if random.random() < pd_su:
                                    SV = [i * 0.9 for i in SV]
                                    since_rekey += 1
                                    print("elapse:", since_rekey)
                                    EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                    print("EV:", EV)
                                else:
                                    print("NO DEFENSE PERFORMED")

                    else: #uncompromised
                        #if phishing initially fails
                        # ids
                        rsu_participate[victim] = 'true'

                        # new_adding SD2 (sending model ccs to rsu)
                        if iter == 0:
                            for i in range(4):
                                if i == victim:
                                    List.append('true')
                                else:
                                    List.append('true')
                            print("leng of list after sd2 in iter0:", len(List))

                        if iter >= 1:
                            for i in range(len(node_compromised_NIDS) - 1):
                                if node_compromised_NIDS[i] == False:
                                    List.append('true')
                                elif node_compromised_NIDS[i] == True:
                                    List.append('false')
                            print("leng of list after sd2:", len(List))
                        # new_end SD2 (sending model ccs to rsu)

                        total_number_attacks += 1

                        print("phishing failed")

                        node_compromised[victim] = False

                        #adding r
                        #all = np.array([0, 1, 2, 3])
                        #for i in all:
                        #    if i in np.sort(idxs_users):
                        #        List.append('true')
                        #    else:
                        #        List.append('false')

                        # if the defender performs
                        defenses = ["rekey", "nf", "su"]
                        defense = random.choice(defenses)
                        if defense == "nf":
                            if random.random() < pd_nf:
                                print("perform Network Filtering")
                                UV = [i * 0.9 for i in UV]
                                since_rekey += 1
                                print("elapse:", since_rekey)
                                EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                print("EV:", EV)
                            else:
                                print("NO DEFENSE PERFORMED")

                        elif defense == "rekey":
                            if random.random() < pd_rekey:
                                print("perform rekeying")
                                #phish_recovered = True
                                node_compromised = [False, False, False, False, False]
                                victims.clear()
                                EV = [i * math.exp(-1 / 1) for i in EV_initial]
                                since_rekey = 0
                                print("elapse:", since_rekey)
                                print("EV:", EV)
                            else:
                                print("NO DEFENSE PERFORMED")

                        elif defense == "su":
                            if random.random() < pd_su:
                                SV = [i * 0.9 for i in SV]
                                since_rekey += 1
                                print("elapse:", since_rekey)
                                EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                print("EV:", EV)
                            else:
                                print("NO DEFENSE PERFORMED")

                elif victim in victims and node_compromised[victim] == True:#phish_recovered == False:
                    if random.random() < vul[victim]: #SV[victim]:  #still compromised;####### if data poisoning works as phishing already suceeded in the previous iteration
                        rsu_participate[victim] = 'true'

                        rsu_asset[victim][0] += (rsu_asset[victim][0] * 0.3)
                        rsu_asset[victim][1] += (rsu_asset[victim][1] * 0.3)

                        # new_adding SD2 (sending model ccs to rsu)
                        if iter == 0:
                            for i in range(4):
                                if i == victim:
                                    List.append('true')
                                else:
                                    List.append('true')
                            print("leng of list after sd2 in iter0:", len(List))

                        if iter >= 1:
                            for i in range(len(node_compromised_NIDS) - 1):
                                if node_compromised_NIDS[i] == False:
                                    List.append('true')
                                elif node_compromised_NIDS[i] == True:
                                    List.append('false')
                            print("leng of list after sd2:", len(List))
                        # new_end SD2 (sending model ccs to rsu)

                        total_number_attacks += 1
                        number_attack_success += 1

                        compromised = 1
                        node_compromised[victim] = True
                        print("data poisoning succeeded (model poisoning)")
                        print("this is the victim:", victim)
                        #if random.random() < 0.5:
                        #dp_success = 1
                        #else:
                        dp_success = 2

                        #adding r
                        #all = np.array([0, 1, 2, 3])
                        #for i in all:
                        #    if i in np.sort(idxs_users):
                        #        List.append('true')
                        #    else:
                        #        List.append('false')

                        #########data should be manipulated here



                        print("perform dp")
                        print(dict_users[str(victim)])
                        print(dict_users)

                        defenses = ["rekey", "nf", "su"]
                        defense = random.choice(defenses)
                        if defense == "nf":
                            if random.random() < pd_nf:
                                print("perform Network Filtering")
                                UV = [i * 0.9 for i in UV]
                                since_rekey += 1
                                print("elapse:", since_rekey)
                                EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                print("EV:", EV)
                            else:
                                print("NO DEFENSE PERFORMED")

                        elif defense == "rekey":
                            if random.random() < pd_rekey:
                                print("perform rekeying")
                                #phish_recovered = True
                                node_compromised = [False, False, False, False, False]
                                victims.clear()
                                EV = [i * math.exp(-1 / 1) for i in EV_initial]
                                since_rekey = 0
                                print("elapse:", since_rekey)
                                print("EV:", EV)
                            else:
                                print("NO DEFENSE PERFORMED")

                        elif defense == "su":
                            if random.random() < pd_su:
                                SV = [i * 0.9 for i in SV]
                                since_rekey += 1
                                print("elapse:", since_rekey)
                                EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                print("EV:", EV)
                            else:
                                print("NO DEFENSE PERFORMED")

                    else:
                        rsu_asset[victim][0] += (rsu_asset[victim][0] * 0.3)
                        rsu_asset[victim][1] += (rsu_asset[victim][1] * 0.3)

                        rsu_participate[victim] = 'true'

                        # new_adding SD2 (sending model ccs to rsu)
                        if iter == 0:
                            for i in range(4):
                                if i == victim:
                                    List.append('true')
                                else:
                                    List.append('true')
                            print("leng of list after sd2 in iter0:", len(List))

                        if iter >= 1:
                            for i in range(len(node_compromised_NIDS) - 1):
                                if node_compromised_NIDS[i] == False:
                                    List.append('true')
                                elif node_compromised_NIDS[i] == True:
                                    List.append('false')
                            print("leng of list after sd2:", len(List))
                        # new_end SD2 (sending model ccs to rsu)


                        total_number_attacks += 1

                        print("failed data poisoning (model poisoning)")
                        print("this is the victim:", victim)
                        node_compromised[victim] = True
                        #phish_recovered = False
                        compromised = 1

                        #adding r
                        #all = np.array([0, 1, 2, 3])
                        #for i in all:
                        #    if i in np.sort(idxs_users):
                        #        List.append('true')
                        #    else:
                        #        List.append('false')
                        # if the attacker performs phishing
                        print(dict_users[str(victim)])
                        print(dict_users)

                        defenses = ["rekey", "nf", "su"]
                        defense = random.choice(defenses)
                        if defense == "nf":
                            if random.random() < pd_nf:
                                print("perform Network Filtering")
                                UV = [i * 0.9 for i in UV]
                                since_rekey += 1
                                print("elapse:", since_rekey)
                                EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                print("EV:", EV)
                            else:
                                print("NO DEFENSE PERFORMED")

                        elif defense == "rekey":
                            if random.random() < pd_rekey:
                                print("perform rekeying")
                                #phish_recovered = True
                                node_compromised = [False, False, False, False, False]
                                victims.clear()
                                EV = [i * math.exp(-1 / 1) for i in EV_initial]
                                since_rekey = 0
                                print("elapse:", since_rekey)
                                print("EV:", EV)
                            else:
                                print("NO DEFENSE PERFORMED")

                        elif defense == "su":
                            if random.random() < pd_su:
                                SV = [i * 0.9 for i in SV]
                                since_rekey += 1
                                print("elapse:", since_rekey)
                                EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
                                print("EV:", EV)
                            else:
                                print("NO DEFENSE PERFORMED")


        else:
            victim = None
            print("no attack happened")
            since_rekey += 1
            print("elapse:", since_rekey)
            EV = [i * math.exp(-1 / (1 + since_rekey)) for i in EV_initial]
            print("EV:",EV)

            compromised = 0

            # new_adding SD2 (sending model ccs to rsu)
            if iter == 0:
                for i in range(4):
                    if i == victim:
                        List.append('true')
                    else:
                        List.append('true')

                print("leng of list after sd2 in iter0:", len(List))

            if iter >= 1:
                for i in range(len(node_compromised_NIDS) - 1):
                    if node_compromised_NIDS[i] == False:
                        List.append('true')
                    elif node_compromised_NIDS[i] == True:
                        List.append('false')
                print("leng of list after sd2:", len(List))
            # new_end SD2 (sending model ccs to rsu)

            #adding r
            #all = np.array([0, 1, 2, 3])
            #for i in all:
            #    if i in np.sort(idxs_users):
            #        List.append('true')
            #    else:
            #        List.append('false')



        print("this is the EV:", EV)
        print("this is the EV:", SV)
        print("this is the EV:", UV)
        print("this is vul", vulnerability(EV, SV, UV))
        print("this is the rsu ac:", rsu_asset)
        print("this is the ccs ac:", ccs_asset)
        print(AC(rsu_asset[0][0],rsu_asset[0][1]), AC(rsu_asset[1][0],rsu_asset[1][1]), AC(rsu_asset[2][0],rsu_asset[2][1]), AC(rsu_asset[3][0],rsu_asset[3][1]))
        print(AC(ccs_asset[0][0], ccs_asset[0][1]))




        client_ccs_operate = []
        for i in rsu_participate:
            client_ccs_operate.append(i)

        client_ccs_operate.append(ccs_alive)




        #new_adding r (whether rsu was able to participate as a FL client)
        if iter == 0:
            for i in rsu_participate:
                List.append(i)
            print("leng of list after r in iter0:", len(List))

        if iter >= 1:
            for i in rsu_participate:
                List.append(i)
            print("leng of list after r:", len(List))

        # new_ending r (whether rsu was able to participate as a FL client)

        #List.append(ccs_alive)




        print("the ones that is alive:", client_ccs_operate)


        #rsu_service_success = []

        #new_adding S3: whether rsu had enough capacity to train
        for i in range(len(rsu_participate)):
            if rsu_participate[i] == 'false':
                List.append('false')
            elif rsu_participate[i] == 'true':
                if random.random() < AC(rsu_asset[i][0], rsu_asset[i][1]):
                    List.append('true')
                    number_service_success += 1
                    rsu_service_success.append(i)
                else:
                    List.append('false')
        total_number_service += 4
        print("leng of list after s3:", len(List))
        #new_ending S3: whether rsu had enough capacity to train



        if not rsu_service_success:
            for i in range(12):
                List.append('false')
            total_number_service += 1
            print("skipped")
            continue

        #new_adding SV3: whether it was able to train based on AC
        for i in range(4):
            if i in rsu_service_success:
                List.append("true")
            else:
                List.append("false")
        print("leng of list after sv3:", len(List))
        #new_ending SV3: whether it was able to train based on AC

        # new_adding sd3: whether rsu was able to send to ccs
        for i in range(4):
            if (i in rsu_service_success) and (attack == None):
                List.append('true')
            elif i in rsu_service_success and attack == 2 and victim == i and dos_success == 2:
                List.append('false')
            elif (i in rsu_service_success) and (attack != 2):
                List.append('true')
            elif i not in rsu_service_success:
                List.append('false')
            else:
                List.append('false')
        print("leng of list after sd3:", len(List))
        # new_ending sd3: whether rsu was able to send to ccs

        #adding ccs(a2): whether ccs operates
        if iter >= 1:
            List.append(ccs_alive)
            print("leng of list after a2 - ccs:", len(List))



        s4 = None
        #new_adding S4: does ccs have enough ac to aggregate models
        if ccs_alive == 'false':
            List.append('false')
            s4 = False
            List.append('false') # sv4
            List.append('false')  # sv5
            total_number_service += 3
            print("SKIPPED")
            continue
        elif ccs_alive == 'true':
            if random.random() < AC(ccs_asset[0][0], ccs_asset[0][1]):
                List.append('true')
                number_service_success += 1
                s4 = True
            else:
                List.append('false')
                s4 = False
                List.append('false') #sv4
                List.append('false')  # sv5
                total_number_service += 3
                print("SKIPPED")
                continue
        total_number_service += 1
        print("leng of list after s4:", len(List))
        #new_ending S4: does ccs have enough ac to aggregate models



        #adding s2 and svt2 and was the rsu able to train?
        #for j in range(2):
        #    all = np.array([0, 1, 2, 3])
        #    for i in all:
        #        if i in np.sort(idxs_users):
        #            List.append('true')
        #        else:
        #            List.append('false')

        #adding sdt2; was rsu able send to ccs; should only depend on attack, not AC
        #for j in range(1):
        #   all = np.array([0, 1, 2, 3])
        #    for i in all:
        #        if i in np.sort(idxs_users):
        #            List.append('true')
        #        else:
        #            List.append('false')



        #adding ccs; is ccs alive and active?
        #List.append('true')

        #print("idxxxxxxxxx:", np.sort(idxs_users))# np.sort(idxs_users)



        for i in idxs_users:
            if i not in rsu_service_success:
                rsu_store.append(i)
        #np.where(idxs_users == i)
        for i in rsu_store:
            idxs_users = np.delete(idxs_users, np.where(idxs_users == i))

        for i in rsu_store:
            if i not in data_length:
                print("if already not in the data length, pass")
            elif i in data_length:
                del data_length[i]

        print("idxxxxxxxxx:", np.sort(idxs_users))

        for idx in np.sort(idxs_users):#idxs_users:  #For every client picked; in this case, all clients are picked as fraction is 1
            #new line
            idx = str(idx)
            #end of new line

            # new code
            if int(idx) in fn:
                print("fp worked fine")
                print("in fp", idx)

            # new code

            #print("who is the victim:", victim)
            #print("who is the victim:", type(victim)) # it was int

            if ((int(idx) == victim and dp_success == 1)): #or int(idx) in fn):  #or int(idx) == victim_mp):#attack == 4)
                local = LocalUpdate_dp(args=args, dataset=dataset_train, idxs=dict_users[
                    idx])  # set variable "local" as the class "LocalUpdate". dict_users is a dictionary of images that each client holds
                # print("this one:",dict_users)
                w, loss = local.train_dp(
                    net=copy.deepcopy(net_glob).to(args.device))  # train each local client with global model

                prev_net_glob.load_state_dict(w)
                print("wwwwwwwwwww:", prev_net_glob)

                # testing
                prev_net_glob.eval()
                acc_train, loss_train_updated, liness, correct, whole_len = test_img_dp(prev_net_glob, test_train_cases_new, args)
                #train_accuracy.append(acc_train)
                print("this is the whole_len:", whole_len)
                print("train accuracy for dp:",acc_train)
                print("how many did you get it right", correct)

                print("whole_leng", whole_len)
                number_attack_success += (whole_len-int(correct))
                print("number_attack_success from dp:", number_attack_success)

                #acc_test, loss_test, lines = test_img(prev_net_glob, dataset_test, args)
                #test_accuracy.append(acc_test)


            elif (int(idx) in fn):
                if int(idx) == 0:
                    local = LocalUpdate_dp(args=args, dataset=dataset_train, idxs=dict_users[
                        idx])  # set variable "local" as the class "LocalUpdate". dict_users is a dictionary of images that each client holds
                    # print("this one:",dict_users)
                    w, loss = local.train_dp(
                        net=copy.deepcopy(net_glob).to(args.device))  # train each local client with global model

                    prev_net_glob.load_state_dict(w)
                    print("wwwwwwwwwww:", prev_net_glob)

                    # testing
                    prev_net_glob.eval()
                    acc_train, loss_train_updated, liness, correct, whole_len = test_img_dp(prev_net_glob,
                                                                                            test_train_cases_new_fn0, args)
                    # train_accuracy.append(acc_train)
                    print("this is the whole_len:", whole_len)
                    print("train accuracy for dp:", acc_train)
                    print("how many did you get it right", correct)

                    print("whole_leng", whole_len)
                    number_attack_success += (whole_len - int(correct))
                    print("number_attack_success from dp:", number_attack_success)

                    # acc_test, loss_test, lines = test_img(prev_net_glob, dataset_test, args)
                    # test_accuracy.append(acc_test)

                elif int(idx) == 1:
                    local = LocalUpdate_dp(args=args, dataset=dataset_train, idxs=dict_users[
                        idx])  # set variable "local" as the class "LocalUpdate". dict_users is a dictionary of images that each client holds
                    # print("this one:",dict_users)
                    w, loss = local.train_dp(
                        net=copy.deepcopy(net_glob).to(args.device))  # train each local client with global model

                    prev_net_glob.load_state_dict(w)
                    print("wwwwwwwwwww:", prev_net_glob)

                    # testing
                    prev_net_glob.eval()
                    acc_train, loss_train_updated, liness, correct, whole_len = test_img_dp(prev_net_glob,
                                                                                            test_train_cases_new_fn1, args)
                    # train_accuracy.append(acc_train)
                    print("this is the whole_len:", whole_len)
                    print("train accuracy for dp:", acc_train)
                    print("how many did you get it right", correct)

                    print("whole_leng", whole_len)
                    number_attack_success += (whole_len - int(correct))
                    print("number_attack_success from dp:", number_attack_success)

                    # acc_test, loss_test, lines = test_img(prev_net_glob, dataset_test, args)
                    # test_accuracy.append(acc_test)

                elif int(idx) == 2:
                    local = LocalUpdate_dp(args=args, dataset=dataset_train, idxs=dict_users[
                        idx])  # set variable "local" as the class "LocalUpdate". dict_users is a dictionary of images that each client holds
                    # print("this one:",dict_users)
                    w, loss = local.train_dp(
                        net=copy.deepcopy(net_glob).to(args.device))  # train each local client with global model

                    prev_net_glob.load_state_dict(w)
                    print("wwwwwwwwwww:", prev_net_glob)

                    # testing
                    prev_net_glob.eval()
                    acc_train, loss_train_updated, liness, correct, whole_len = test_img_dp(prev_net_glob,
                                                                                            test_train_cases_new_fn2, args)
                    # train_accuracy.append(acc_train)
                    print("this is the whole_len:", whole_len)
                    print("train accuracy for dp:", acc_train)
                    print("how many did you get it right", correct)

                    print("whole_leng", whole_len)
                    number_attack_success += (whole_len - int(correct))
                    print("number_attack_success from dp:", number_attack_success)

                    # acc_test, loss_test, lines = test_img(prev_net_glob, dataset_test, args)
                    # test_accuracy.append(acc_test)


                elif int(idx) == 3:
                    local = LocalUpdate_dp(args=args, dataset=dataset_train, idxs=dict_users[
                        idx])  # set variable "local" as the class "LocalUpdate". dict_users is a dictionary of images that each client holds
                    # print("this one:",dict_users)
                    w, loss = local.train_dp(
                        net=copy.deepcopy(net_glob).to(args.device))  # train each local client with global model

                    prev_net_glob.load_state_dict(w)
                    print("wwwwwwwwwww:", prev_net_glob)

                    # testing
                    prev_net_glob.eval()
                    acc_train, loss_train_updated, liness, correct, whole_len = test_img_dp(prev_net_glob,
                                                                                            test_train_cases_new_fn3, args)
                    # train_accuracy.append(acc_train)
                    print("this is the whole_len:", whole_len)
                    print("train accuracy for dp:", acc_train)
                    print("how many did you get it right", correct)

                    print("whole_leng", whole_len)
                    number_attack_success += (whole_len - int(correct))
                    print("number_attack_success from dp:", number_attack_success)

                    # acc_test, loss_test, lines = test_img(prev_net_glob, dataset_test, args)
                    # test_accuracy.append(acc_test)







                """"
                if ccs_dos_happend == 1:
                    local = LocalUpdate_dp(args=args, dataset=dataset_train, idxs=dict_users[idx])  # set variable "local" as the class "LocalUpdate". dict_users is a dictionary of images that each client holds
                # print("this one:",dict_users)ƒ
                    w, loss = local.train_dp(net=copy.deepcopy(prev_net_glob).to(args.device))
                    #ccs_dos_happend = 0
                """
                """
                else:
                    local = LocalUpdate_dp(args=args, dataset=dataset_train, idxs=dict_users[idx])  # set variable "local" as the class "LocalUpdate". dict_users is a dictionary of images that each client holds
                    # print("this one:",dict_users)
                    w, loss = local.train_dp(net=copy.deepcopy(net_glob).to(args.device))  # train each local client with global model
                """




                    #ccs_dos_happend = 0

            #if prev_net_glob == net_glob:
            #    print("it is same")
            #else:
            #    print("it is different")

            #newline
            ##if (int(idx) == victim and dos_success == 3): #dos_success == 3 or ):#attack == 3): #dp_success == 1):
                #training for jamming attack to a path from ccs to rsu
                ##local = LocalUpdate_dp(args=args, dataset=dataset_train, idxs=dict_users[idx])  # set variable "local" as the class "LocalUpdate". dict_users is a dictionary of images that each client holds
                # print("this one:",dict_users)


                ##w, loss = local.train_dp(net=copy.deepcopy(prev_net_glob).to(args.device))
                    # train each local client with global model
            #newline


            elif (int(idx) == victim and dos_success == 3):
                continue


            else:
                local = LocalUpdate(args=args, dataset=dataset_train, idxs=dict_users[
                    idx])  # set variable "local" as the class "LocalUpdate". dict_users is a dictionary of images that each client holds
                # print("this one:",dict_users)
                w, loss = local.train(
                    net=copy.deepcopy(net_glob).to(args.device))  # train each local client with global model

                # ccs_dos_happend = 0
            """
            else:
                if ccs_dos_happend == 1:
                    local = LocalUpdate(args=args, dataset=dataset_train, idxs=dict_users[idx])  # set variable "local" as the class "LocalUpdate". dict_users is a dictionary of images that each client holds
                        # print("this one:",dict_users)

                    w, loss = local.train(net=copy.deepcopy(prev_net_glob).to(args.device))
                    #ccs_dos_happend = 0
                else:
                    local = LocalUpdate(args=args, dataset=dataset_train, idxs=dict_users[idx]) #set variable "local" as the class "LocalUpdate". dict_users is a dictionary of images that each client holds
                    #print("this one:",dict_users)
                    w, loss = local.train(net=copy.deepcopy(net_glob).to(args.device))  # train each local client with global model

                    #ccs_dos_happend = 0
            """


            #print("thisthisthsitsststetewtw:", dataset_train[dict_users[str(victim)][1]])
            #print("thisthisthsitsststetewtw:", dataset_train[dict_users[str(victim)][2]])
            #print("thisthisthsitsststetewtw:", dataset_train[dict_users[str(victim)][3]])
            #print("thisthisthsitsststetewtw:", dataset_train[dict_users[str(victim)][4]])
            #print("thisthisthsitsststetewtw:", dataset_train[dict_users[str(victim)][5]])
            #print("thisthisthsitsststetewtw:", dataset_train[dict_users[str(victim)][7]])
            #print("thisthisthsitsststetewtw:", dataset_train[dict_users[str(victim)][8]])
            #print("thisthisthsitsststetewtw:", dataset_train[dict_users[str(victim)][9]])
            #print("thisthisthsitsststetewtw:", dataset_train[dict_users[str(victim)][10]])
            #print("thisthisthsitsststetewtw:", dataset_train[dict_users[str(victim)][11]])
            #print("thisthisthsitsststetewtw:", dataset_train[dict_users[str(victim)][12]])


            """
            if (dp_success == 1):
                local = LocalUpdate_dp(args=args, dataset=dataset_train, idxs=dict_users[
                    idx])  # set variable "local" as the class "LocalUpdate". dict_users is a dictionary of images that each client holds
                # print("this one:",dict_users)
                w, loss = local.train_dp(
                    net=copy.deepcopy(net_glob).to(args.device))  # train each local client with global model
            else:
                local = LocalUpdate(args=args, dataset=dataset_train, idxs=dict_users[
                    idx])  # set variable "local" as the class "LocalUpdate". dict_users is a dictionary of images that each client holds
                # print("this one:",dict_users)
                w, loss = local.train(
                    net=copy.deepcopy(net_glob).to(args.device))  # train each local client with global model
            """
                #print("this is wwwwwwwww:", w)
                #print("this is it:", w.keys())
                #for k in w.keys():
                    # print("first:",w_avg[k])
                #    w[k] = torch.mul(w[k], 2.0)
                #print("this is w[0]:", w)


            #w, loss = local.train(net=copy.deepcopy(net_glob).to(args.device))  #train each local client with global model
            if args.all_clients:
                w_locals[idx] = copy.deepcopy(w) #copying weights of every client to "w_locals"

            else:
                if ((int(idx) == victim and dp_success == 2)): #or int(idx) == victim_mp):# attack == 5)
                    print("change direction for local models")
                    for k in w.keys():
                        # print("first:",w_avg[k])
                        w[k] = torch.mul(w[k], -0.5)#2.0)  #-0.8 is a good option it was -1.0 it was -0.1
                    #for k in w.keys():
                        # print("first:",w_avg[k])
                     #   w[k] = torch.mul(w[k], 2)

                    w_locals.append(copy.deepcopy(w))
                    print("lenght of rsus that were able to send:", len(w_locals))



                elif (int(idx) == victim and dos_success == 2):#attack == 2):#dp_success == 2):
                    print("disrupt communication between rsu sender and ccs")
                    continue
                    #for k in w.keys():
                        # print("first:",w_avg[k])
                        #w[k] = torch.mul(w[k], -1.0)  #-0.8 is a good option
                    #for k in w.keys():
                        # print("first:",w_avg[k])
                     #   w[k] = torch.mul(w[k], 2)

                    #w_locals.append(copy.deepcopy(w))


                else:
                    w_locals.append(copy.deepcopy(w)) #append weights of every client to "w_locals"
                    print("lenght of rsus that were able to send:", len(w_locals))

                #newline

                #newline

            loss_locals.append(copy.deepcopy(loss)) #append local loss (local epoch that has batches) to "loss_locals"

            #print("w_local:", w_locals)

        #print("waht:", type(idxs_users))
        # update global weights
        #print('hello:', w_locals[0].keys())
        #print('hello:', len(w_locals[0]))
        #print("len of w_locals:", len(w_locals))
        #print(w_locals[0])
        #print("abababaaab:",w_locals[0][0])

        print("zzzzzzzzzz_wlocal:", len(w_locals))
        print("zzzzzzzzzz_data legnth:", len(data_length))


        #print("zzzzzzzzzz_wlocal:", w_locals)
        print("zzzzzzzzzz_data legnth:", data_length)

        victim_dp = None
        victim_mp = None


        if iter == 0:
            for i in range(len(node_compromised)):
                if node_compromised[i] == True: #for compromised nodes
                    if random.random() < 0.95: #TP
                        node_compromised_NIDS[i] = True #compromised as compromised = evicted
                        tp.append(i)
                    else: #FN
                        node_compromised_NIDS[i] = False #compromised as normal = alredy compromised (phished) so keep doing dp
                        fn.append(i)
                        #dp_twice = 1

                else: #for normal nodes
                    #random_num = random.random()
                    if random.random() < 0.99: #TN
                        node_compromised_NIDS[i] = False #normal as normal = good nodes that are not atttacked yet - should be targeted by attacker
                        tn.append(i)
                    else: #FP
                        node_compromised_NIDS[i] = True #normal as compromised = evicted
                        fp.append(i)

            for i in range(len(node_compromised)): # if seeing compromised as compromised, putting back in the network
                if (node_compromised[i] == True and node_compromised_NIDS[i] == True):
                    node_compromised[i] = False

            print("realoneone:", node_compromised)
            print("nidsoneone:",node_compromised_NIDS)

        """
        #NEW CODE
        if dos_success == 6 and ccs_dos_happend == 0:
        #    end = time.time()
        #    print("this is the applicaiton up time:", end - start)
        #    up_time.append(end-start)######this caused error
            ccs_dos_happend = 1
            continue

        if dos_success == 6 and ccs_dos_happend == 1:
            continue
        """





        #END OF NEW COD
        data_length = list(data_length.values())


        w_glob = FedAvg(w_locals, data_length) #w_locals is a list that contains all models of clients. By using Fedavg, aggregate all local models into one global model






        #print('what is w_glob:', w_glob)

        # adding s3 and svt3; was it able to aggregate?
        #List.append('true')
        #List.append('true')

        #newline #comment these lines later
        #if
        #rsu0_glob.load_state_dict(w_locals[0])
        #print("local 0 cleared")
        #rsu1_glob.load_state_dict(w_locals[1])
        #print("local 1 cleared")
        #rsu2_glob.load_state_dict(w_locals[2])
        #print("local 2 cleared")
        #rsu3_glob.load_state_dict(w_locals[3])
        #print("local 3 cleared")
        #newline

        print("length after fl", len(List))

        #generating prev global model
        prev_net_glob = copy.deepcopy(net_glob)


        # copy weight to net_glob
        net_glob.load_state_dict(w_glob) #copy new updated aggregated updated model to net_glob (updating new_glob)




        #if dos_success != 3:
        #    prev_net_glob.load_state_dict(w_glob)


        #if prev_net_glob == net_glob:
        #    print("they are the same")

        print("netglob:", net_glob)
        #print(loss)
        # print train loss
        loss_avg = sum(loss_locals) / len(loss_locals)  #"loss_avg" is sum of all losses in "loss_local" divided by its length.
        print('Round {:3d}, Average loss {:.3f}'.format(iter, loss_avg))
        loss_train.append(loss_avg)




    # plot train loss curve
    #plt.figure()
    #plt.plot(range(len(loss_train)), loss_train)
    #plt.ylabel('train_loss')
    #plt.savefig('./save/fed_{}_{}_{}_C{}_iid{}.png'.format(args.dataset, args.model, args.epochs, args.frac, args.iid))



        # testing
        net_glob.eval()
        acc_train, loss_train_updated,liness = test_img(net_glob, dataset_train, args)
        train_accuracy.append(acc_train)
        acc_test, loss_test, lines = test_img(net_glob, dataset_test, args)
        test_accuracy.append(acc_test)

        if (dos_success != 6 and ccs_dos_happend == 1):
            #start = time.time()
            ccs_dos_happend = 0






        #print("this is the uptime:", up_time)


        #if iter == 14:
            #whole_end = time.time()
            #print("this is the whole up time:", whole_end - whole_start)
            #whole_time = whole_end - whole_start

            #if len(up_time) == 0:
            #    up_time = whole_time
            #    print("this is the up time percentage:", ((up_time) / whole_time) * 100)
            #else:
            #    print("this is the applicaiton up time:", whole_end - start)
            #    up_time.append(whole_end - start)
            #    print("this is the final up time list:,", up_time)
            #    print("this is the up time percentage:", (sum(up_time) / whole_time)*100)




        #print(lines)
        #print(len(lines))
        #print(type(lines))
        #print(list(chain.from_iterable(chain.from_iterable(lines))))
        #print(len(list(chain.from_iterable(chain.from_iterable(lines)))))
        lines = list(chain.from_iterable(chain.from_iterable(lines)))

        #needed for mapping prediction later; uncomment later
        """
        # writing to a file
        with open('l.txt', 'w') as f:
            for line in lines:
                f.write(f"{line}\n")     
        """




        #print("label:",dataset_train[0][1])

        #print("label:", dataset_train[1][1])
        #print("label:", dataset_train[2][1])
        #print("label:", dataset_train[3][1])
        """
        #newline for map test #######
        #map_test, loss_map_test = test_img(net_glob, dataset_train, args)

        lines = ["oneway", "oneway", "oneway", "oneway", "oneway", "oneway", "noright", "noright",
                              "noright", "noparking", \
                              "noparking", "noparking", "noparking", "noparking", "noparking", "noparking", "noparking",
                              "noparking", "noentry", "noentry", "noentry", \
                              "noentry", "noentry", "noentry", "noentry", "noentry", "noparkingstop", "noparkingstop",
                              "noparkingstop", "noparkingstop", "noparkingstop", "noparkingstop", "parking", \
                              "parking", "yields", "yields", "yields", "yields", "yields", "yields", "yields",
                              "speedlimit", "speedlimit", "roadnarrowing", "noright", "roundabout", "roundabout", \
                              "roundabout", "roundabout", "roundabout", "roundabout", "roundabout", "roundabout",
                              "nocontrolledcrosswalk", "nocontrolledcrosswalk", "nocontrolledcrosswalk", \
                              "roadbump", "roadbump", "deadend", "deadend"]
        random.shuffle(lines)
        # writing to a file
        with open('l.txt', 'w') as f:
            for line in lines:
                f.write(f"{line}\n")

        #######
        """
        #print(len(dataset_train))
        #print(len(dataset_test))

        #new line
        #print(dataset_test[0][1])
        #print(dataset_test[1][1])
        #print(dataset_test[3][1])
        #print(dataset_test[4][1])







        print("Training accuracy: {:.2f}".format(acc_train))
        print("Testing accuracy: {:.2f}".format(acc_test))
        print(prev_acc_test)



        print("this is test for acc_test:", acc_test)
        print("this is the test for prev_acc_test:", prev_acc_test)




        if int(acc_test) <= int(prev_acc_test):
            print("TRUE")
        else:
            print("FALSE")

        if int(acc_test) <= int(prev_acc_test):
            count += 1
            print(count)
            if count == 50:
                break

        # new_adding SV4: does ccs produce an enhanced global model?
        #if s4 == False:
        #    List.append('false')
        if s4 == True and int(prev_acc_test) < int(acc_test):
            List.append("true")
            print("TRUE")
        elif s4 == True and int(prev_acc_test) >= int(acc_test):
            List.append("false")
            print("FALSE")
        print("leng of list after sv4:", len(List))
        # new_ending SV4: does ccs produce an enhanced global model?

        # new_adding SV5: does ccs produce a global model equal to or greater than 85?
        #if s4 == False:
        #    List.append('false')
        if s4 == True and int(acc_test) >= 85:
            List.append("true")
            print("TRUE")
        elif s4 == True and int(acc_test) < 85:
            List.append("false")
            print("FALSE")
        print("leng of list after sv5:", len(List))
        # new_ending SV5: does ccs produce a global model equal to or greater than 85?


        prev_acc_test = int(acc_test)





        #print(len(dict_users["0"]))
        #print(len(dict_users["1"]))
        #print(len(dict_users["2"]))
        #print(len(dict_users["3"]))



        #####new code

        #if acc_test >= 87:
        #    mission_acc_condition = 1

        #print(mission_acc_condition)
        ######end of new code




        #if we consider ending the mission earilier than 15 iteration if 87
        """
        # adding mission condition 1 and 2 and mission node
        
        if acc_test >= 87:
            for i in range((args.epochs-(iter+1))*23):
                List.append(None)
            List.append('true')
            List.append('true')
            List.append('true')

            file = open("file1.txt", "a")
            # Saving the array in a text file
            content = str(List) + '\n'
            file.write(content)
            file.close()

            sys.exit()
        else:
            continue
        
        """





    # adding mission condition 1 and 2 and mission node
    #if mission_acc_condition == 1: #acc_test >=87:
    #    List.append('true')
    #    List.append('true')
    #    List.append('true')
    #else:
    #    List.append('false')
    #    List.append('false')
    #    List.append('false')

    #print("length after fl", len(List))

    if total_number_attacks == 0:
        asr = 0.00
    else:
        asr = number_attack_success / total_number_attacks

    sa = number_service_success / total_number_service



    if sa < 0.87:
        List.append("false")
        print("SA: FALSE")
    else:
        List.append("true")
        print("SA: TRUE")


    if int(acc_test) < 85:
        List.append('false')
        print("PRED: FALSE")
    else:
        List.append('true')
        print("PRED: TRUE")

    if int(acc_test) >= 85 and sa >= 0.87:
        List.append('true')
        print("TRUE")
    else:
        List.append('false')
        print("FALSE")



    print("this is the test acc_test", acc_test)
    print("this is the test sa", sa)



    if int(acc_test) >= 85 and sa >= 0.87:
        outcome = 1
        print("OUTCOME: TRUE")

    else:
        outcome = 0
        print("OUTCOME: FALSE")




    print("length of List", len(List))


    #with open('file_4.txt', 'a') as file:
    #    file.write("%i\n" % outcome)
    #    file.close()



    print("length of List", len(List))


    ######t/f file
    file = open("file_arc_test.txt", "a") #it was file1.txt
    # Saving the array in a text file
    content = str(List) + '\n'
    file.write(content)
    file.close()
    ###reading it make it a nested list
    #with open('file1.txt') as f:
    #    a = f.read().splitlines()
    #for i in range(len(a)):
    #    a[i] = literal_eval(a[i])
        # b = []
        # for i in a:
        #    b.append(i)
        # print(b)
        #####end of t/f file





    #predictability file: MPE
    #with open('file_predictability_four.txt', 'a') as file:
    #    file.write("%i\n" % acc_test)
    #    file.close()

    # ASR file: MPE
    #with open('file_asr_four.txt', 'a') as file:
    #    file.write("%f\n" % asr)
    #    file.close()

    # Timely service availability file: MPE
    #with open('file_sa_four.txt', 'a') as file:
    #    file.write("%f\n" % sa)
    #    file.close()

    print("predictability:", int(acc_test))
    print("tna:", total_number_attacks)
    print("nas:", number_attack_success)
    print("attack success rate:", asr)
    print("total sa:", total_number_service)
    print("success sa:", number_service_success)
    print("timely service availability", sa)








    """
    plt.figure()
    plt.plot(range(len(train_accuracy)), train_accuracy, label="train accuracy")
    plt.plot(range(len(test_accuracy)), test_accuracy, label="test accuracy")
    plt.ylabel('accuracy')
    plt.legend()
    plt.savefig('./save/godplease_new256_fed_{}_{}_{}_C{}_iid{}.png'.format(args.dataset, args.model, args.epochs, args.frac, args.iid))
    """



    #args.epochs
    #if args.model == 'LeNet':
    #    print("true00")

    #if args.dataset == 'traffic':
    #    print("true0")
    #if args.iid:
    #    print("true")
    #print(len(dict_users))

    #print(len(dataset_train))
    #print(len(dict_users[0]))
    #print(len(dict_users[1]))
    #print(len(dict_users[2]))
    #print(len(dict_users[3]))
    #print(len(dict_users[4]))
    #print(len(dict_users[5]))
    #print(len(dict_users[6]))
    #print(len(dict_users[7]))
    #print(len(dict_users[8]))
    #print(len(dict_users[9]))
    #print(len(dataset_train))

    #print(args.num_users)
    #print(args.epochs)
    #print(args.local_bs)
    #print(len(w_locals))
    #print(args.frac)

    #print(FedAvg_New(w_locals))
    #w_avg = copy.deepcopy(w_locals[0])
    #print(w_avg.keys())
    #print(FedAvg_New(w_locals))







