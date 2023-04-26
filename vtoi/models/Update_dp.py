#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import torch
from torch import nn, autograd
from torch.utils.data import DataLoader, Dataset

import random



class DatasetSplit(Dataset):
    def __init__(self, dataset, idxs):
        self.dataset = dataset
        self.idxs = list(idxs)

    def __len__(self):
        return len(self.idxs)

    def __getitem__(self, item):
        image, label = self.dataset[self.idxs[item]]
        return image, label



class LocalUpdate_dp(object):
    def __init__(self, args, dataset=None, idxs=None):
        self.args = args
        self.loss_func = nn.CrossEntropyLoss()
        self.selected_clients = []
        self.ldr_train = DataLoader(DatasetSplit(dataset, idxs), batch_size=self.args.local_bs, shuffle=True)





    def train_dp(self, net):

        net.train()
        # train and update
        optimizer = torch.optim.SGD(net.parameters(), lr=self.args.lr, momentum=self.args.momentum)
        epoch_loss = []


        ####new lines

        #label_list = [1, 19, 22, 16, 32, 37, 40, 53, 54] # 18, 30, 41, 45,
        #a = random.choice(label_list)
        #label_list.remove(a)
        #b = random.choice(label_list)
        #label_list.remove(b)
        #c = random.choice(label_list)
        #label_list.remove(c)
        #d = random.choice(label_list)
        #label_list.remove(d)
        """
        e = random.choice(label_list)
        label_list.remove(e)
        f = random.choice(label_list)
        label_list.remove(f)
        g = random.choice(label_list)
        label_list.remove(g)
        h = random.choice(label_list)
        label_list.remove(h)
        i = random.choice(label_list)
        label_list.remove(i)
        j = random.choice(label_list)
        label_list.remove(j)
        k = random.choice(label_list)
        label_list.remove(k)
        l = random.choice(label_list)
        label_list.remove(l)
        m = random.choice(label_list)
        label_list.remove(m)
        """
        ####


        for iter in range(self.args.local_ep):

            #print(iter)
            batch_loss = []
            for batch_idx, (images, labels) in enumerate(self.ldr_train):

                #print("images:", images)

                #print('images:', images)
                #print("images len:", len(images))
                #print("labels:", labels)
                #print("lable len:", len(labels))
                #for i in labels:
                #    print(i)

                label_list = [1, 19, 22, 16, 32, 37, 40, 53, 54,  18, 30, 41, 45]
                a = random.choice(label_list)
                label_list.remove(a)
                b = random.choice(label_list)
                label_list.remove(b)
                c = random.choice(label_list)
                label_list.remove(c)
                d = random.choice(label_list)
                label_list.remove(d)



                ####label filping attack (untargeted: want those labels to be misclassifed as any label other than the true label)
                print("batch number", batch_idx)
                print("before change",labels)
                print("a:", a)
                print("b:", b)
                print("c:", c)
                print("d:", d)
                for i in range(len(labels)):
                    if labels[i] == 45:
                        labels[i] = a
                    elif labels[i] == 30:
                        labels[i] = b
                    elif labels[i] == 18:
                        labels[i] = c
                    elif labels[i] == 41:
                        labels[i] = d



                print("after change",labels)


                #print(batch_idx)
                images, labels = images.to(self.args.device), labels.to(self.args.device)
                net.zero_grad()
                log_probs = net(images)
                loss = self.loss_func(log_probs, labels)
                loss.backward()
                optimizer.step()

                if self.args.verbose and batch_idx % 10 == 0:
                    print('Update Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                        iter, batch_idx * len(images), len(self.ldr_train.dataset),
                               100. * batch_idx / len(self.ldr_train), loss.item()))
                batch_loss.append(loss.item())
                #print(batch_idx)


            #print("length of batch loss:",(batch_loss))
            epoch_loss.append(sum(batch_loss)/len(batch_loss))


            #print(epoch_loss)
        return net.state_dict(), sum(epoch_loss) / len(epoch_loss)

