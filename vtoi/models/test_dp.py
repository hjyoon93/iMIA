#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @python: 3.6

import torch
from torch import nn
import torch.nn.functional as F
from torch.utils.data import DataLoader


def test_img_dp(net_g, datatest, args):
    net_g.eval()
    # testing
    test_loss = 0
    correct = 0
    data_loader = DataLoader(datatest, batch_size=args.bs)
    #y_pred = None
    newlist = []


    l = len(data_loader)
    print(l)
    for idx, (data, target) in enumerate(data_loader):
        if args.gpu != -1:
            data, target = data.cuda(), target.cuda()
        print("this is the idx:", idx)
        print("this is the data",data)
        print("this is the target", target)



        log_probs = net_g(data)
        # sum up batch loss
        test_loss += F.cross_entropy(log_probs, target, reduction='sum').item()
        # get the index of the max log-probability
        y_pred = log_probs.data.max(1, keepdim=True)[1]

        print("this is the y_pred:",y_pred)

        correct += y_pred.eq(target.data.view_as(y_pred)).long().cpu().sum()
        print("this is the correct:", correct)

        #if idx <= 60:
        newlist.append(y_pred.cpu().detach().numpy())
        #    break




    test_loss /= len(data_loader.dataset)


    accuracy = 100.00 * correct / len(data_loader.dataset)




    if args.verbose:
        print('\nTest set: Average loss: {:.4f} \nAccuracy: {}/{} ({:.2f}%)\n'.format(
            test_loss, correct, len(data_loader.dataset), accuracy))
    return accuracy, test_loss, newlist, correct, len(data_loader.dataset)

