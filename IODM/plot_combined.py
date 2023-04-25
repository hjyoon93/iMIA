"""
Take the data in the results folder and plot it so we can stop using stupid
Excel.
"""

import glob
import os
import csv
from matplotlib import markers
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sympy import plot_implicit


def movingaverage(y, window_size):
    """
    Moving average function from:
    http://stackoverflow.com/questions/11352047/finding-moving-average-from-data-points-in-python
    """
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(y, window, 'same')


def readable_output(filename):
    readable = ''
    # Example:
    # learn_data-1000-1000-32-10000.csv
    f_parts = filename.split('-')

    if f_parts[0] == 'learn_data':
        readable += 'distance: '
    else:
        readable += 'loss: '

    readable += f_parts[1] + ', ' + f_parts[2] + ' | '
    readable += f_parts[3] + ' | '
    readable += f_parts[4].split('.')[0]

    return readable


def plot_file(filenames, type='Timeliness'):
    plt.clf() 
    for f in filenames:
         # Clear.
        with open(f, 'r') as csvfile:
            print(f)
            # print(f.split('\')
            plt.title(type)
            # setlabel=type
            if "random" in f:
                setlabel = "Random Strategy"
            elif "path" in f:
                setlabel = "Attacker Path"
            else:
                setlabel = "Hypergame EBM"
            reader = csv.reader(csvfile)
            # Turn our column into an array.
            y = []
            for row in reader:
                if len(row)==0:
                    continue
                # if type == 'loss':
                y.append(float(row[1]))
                # else:
                # y.append(float(row[1]))

            # Running tests will be empty.
            if len(y) == 0:
                return

            # print(readable_output(f))

            # Get the moving average so the graph isn't so crazy.
            # if type == 'loss' or type=='learn':
            window = 1
            # y_av = movingaverage(y, window)
            # else:
            #     y_av = y
                # window = 100

            # Use our moving average to get some metrics.
            # arr = np.array(y_av)
            # if type == 'loss':
            #     print("%f\t%f\n" % (arr.min(), arr.mean()))
            # else:
            #     print("%f\t%f\n" % (arr.max(), arr.mean()))

            # Plot it.
            # plt.clf()  # Clear.
            # plt.title(f)
            # The -50 removes an artificial drop at the end caused by the moving
            # average.
            if type == 'loss':
                plt.plot(y[:-350], label=setlabel)
                plt.ylabel('Smoothed Loss')
                # plt.ylim(0, 5000)
                # plt.xlim(0, 250000)
            elif type=="learn":
                plt.plot(y[100:-5], label=setlabel)
                plt.ylabel('Smoothed Distance between collisions')
                # plt.ylim(0, 4000)
            else:
                plt.plot([9,7,5,3,1], y[:], marker='o', label=setlabel)
                plt.ylabel(type)
    plt.xlabel('Mean Vulnerability')
    plt.legend()
    plt.savefig(type+".png", bbox_inches='tight')

def plot_file2(filenames, type='loss'):
    plt.clf() 
    entropy = [0] * 3
    dissonance = [0] * 3
    vacuity = [0] * 3
    epsilon = [0] * 3
    for f in filenames:
         # Clear.
        with open(f, 'r') as csvfile:
            print(f)
            # print(f.split('\')
            plt.title(f.split('\\')[2].split('-')[0])
            reader = csv.reader(csvfile)
            # Turn our column into an array.
            y = []
            r = ""
            for row in reader:
                if len(row) != 0:
                    r = row
                continue
            # if len(row)==0:
            #     continue
            # if type == 'dirt':
            if 'gamma0entropy' in f:
                # print("lol")entropy, vacuity, dissonance, epsilon
                entropy[0] = float(r[1])
            elif 'gamma0.5entropy' in f:
                entropy[1] = float(r[1])
            elif 'gamma1entropy' in f:
                entropy[2] = float(r[1])
            elif 'gamma0dissonance' in f:
                dissonance[0] = float(r[1])
            elif 'gamma0.5dissonance' in f:
                dissonance[1] = float(r[1])
            elif 'gamma1dissonance' in f:
                dissonance[2] = float(r[1])
            elif 'gamma0eps' in f:
                epsilon[0] = float(r[1])
            elif 'gamma0.5eps' in f:
                epsilon[1] = float(r[1])
            elif 'gamma1eps' in f:
                epsilon[2] = float(r[1])
            elif 'gamma0.5' in f:
                vacuity[1] = float(r[1])
            elif 'gamma0' in f:
                vacuity[0] = float(r[1])
            elif 'gamma1' in f:
                vacuity[2] = float(r[1])
            # else:
            #     if 'entropy' in f:
            #         entropy.append(float(reader[-1][1]))
            #     elif 'dissonance' in f:
            #         dissonance.append(float(reader[-1][1]))
            #     elif 'eps' in f:
            #         epsilon.append(float(reader[-1][1]))
            #     else:
            #         vacuity.append(float(reader[-1][1]))

            # Running tests will be empty.
            # if len(y) == 0:
            #     return


            # print(readable_output(f))

            # Get the moving average so the graph isn't so crazy.
            # if type=='learn':
            #     window = 350
            #     y_av = movingaverage(y, window)
            # else:
            #     y_av = y
            #     # window = 100
            # if "entropy" in f:
            #     entropy.append(y_av[-1])
            # # Use our moving average to get some metrics.
            # arr = np.array(y_av)
            # if type == 'loss':
            #     print("%f\t%f\n" % (arr.min(), arr.mean()))
            # else:
            #     print("%f\t%f\n" % (arr.max(), arr.mean()))

            # Plot it.
            # plt.clf()  # Clear.
            # plt.title(f)
            # The -50 removes an artificial drop at the end caused by the moving
            # average.
            # if type == 'loss':
            #     plt.plot(y_av[:-350], label=setlabel)
            #     plt.ylabel('Smoothed Loss')
            #     # plt.ylim(0, 5000)
            #     # plt.xlim(0, 250000)
            # elif type=="learn":
            #     plt.plot(y_av[100:-5], label=setlabel)
            #     plt.ylabel('Smoothed Distance between collisions')
            #     # plt.ylim(0, 4000)
    print(entropy, vacuity, dissonance, epsilon)   
    plt.plot([0, 0.5, 1], entropy, label="Entropy as Epsilon")
    plt.plot([0, 0.5, 1], dissonance, label="Dissonance as Epsilon")
    plt.plot([0, 0.5, 1], vacuity, label="Vacuity as Epsilon")
    plt.plot([0, 0.5, 1], epsilon, label="Linear Decreasing Espilon")
    plt.xlabel("Gamma")
    plt.ylabel(type)
    plt.legend()
    plt.savefig('sensitivity_'+ type + '.png', bbox_inches='tight')


def plot_file3(filenames, type='loss'):
    plt.clf() 
    entropy = [0] * 3
    dissonance = [0] * 3
    vacuity = [0] * 3
    epsilon = [0] * 3
    for f in filenames:
         # Clear.
        with open(f, 'r') as csvfile:
            print(f)
            # print(f.split('\')
            plt.title("Distance Travelled vs Gamma")
            reader = csv.reader(csvfile)
            # Turn our column into an array.
            y = []
            r = 0
            for row in reader:
                if len(row) != 0:
                    if float(row[1])>r:
                        r = float(row[1])
                continue
            # if len(row)==0:
            #     continue
            # if type == 'dirt':
            if 'gamma0entropy' in f:
                # print("lol")entropy, vacuity, dissonance, epsilon
                entropy[0] = float(r)
            elif 'gamma0.5entropy' in f:
                entropy[1] = float(r)
            elif 'gamma1entropy' in f:
                entropy[2] = float(r)
            elif 'gamma0dissonance' in f:
                dissonance[0] = float(r)
            elif 'gamma0.5dissonance' in f:
                dissonance[1] = float(r)
            elif 'gamma1dissonance' in f:
                dissonance[2] = float(r)
            elif 'gamma0eps' in f:
                epsilon[0] = float(r)
            elif 'gamma0.5eps' in f:
                epsilon[1] = float(r)
            elif 'gamma1eps' in f:
                epsilon[2] = float(r)
            elif 'gamma0.5' in f:
                vacuity[1] = float(r)
            elif 'gamma0' in f:
                vacuity[0] = float(r)
            elif 'gamma1' in f:
                vacuity[2] = float(r)
            # else:
            #     if 'entropy' in f:
            #         entropy.append(float(reader[-1][1]))
            #     elif 'dissonance' in f:
            #         dissonance.append(float(reader[-1][1]))
            #     elif 'eps' in f:
            #         epsilon.append(float(reader[-1][1]))
            #     else:
            #         vacuity.append(float(reader[-1][1]))

            # Running tests will be empty.
            # if len(y) == 0:
            #     return


            # print(readable_output(f))

            # Get the moving average so the graph isn't so crazy.
            # if type=='learn':
            #     window = 350
            #     y_av = movingaverage(y, window)
            # else:
            #     y_av = y
            #     # window = 100
            # if "entropy" in f:
            #     entropy.append(y_av[-1])
            # # Use our moving average to get some metrics.
            # arr = np.array(y_av)
            # if type == 'loss':
            #     print("%f\t%f\n" % (arr.min(), arr.mean()))
            # else:
            #     print("%f\t%f\n" % (arr.max(), arr.mean()))

            # Plot it.
            # plt.clf()  # Clear.
            # plt.title(f)
            # The -50 removes an artificial drop at the end caused by the moving
            # average.
            # if type == 'loss':
            #     plt.plot(y_av[:-350], label=setlabel)
            #     plt.ylabel('Smoothed Loss')
            #     # plt.ylim(0, 5000)
            #     # plt.xlim(0, 250000)
            # elif type=="learn":
            #     plt.plot(y_av[100:-5], label=setlabel)
            #     plt.ylabel('Smoothed Distance between collisions')
            #     # plt.ylim(0, 4000)
    print(entropy, vacuity, dissonance, epsilon)   
    plt.plot([0, 0.5, 1], entropy, label="Entropy as Epsilon")
    plt.plot([0, 0.5, 1], dissonance, label="Dissonance as Epsilon")
    plt.plot([0, 0.5, 1], vacuity, label="Vacuity as Epsilon")
    plt.plot([0, 0.5, 1], epsilon, label="Linear Decreasing Espilon")
    plt.xlabel("Gamma")
    plt.ylabel(type)
    plt.legend()
    plt.savefig('sensitivity_'+ type + '.png', bbox_inches='tight')

def box_plot_file(filenames, type='Timeliness'):
    plt.clf() 
    i = 0
    colors = ['red', 'green', 'darkorchid']
    for t in ['random', 'ebm', 'path']:
        combined = []
        for f in filenames:
            if t in f:
            # Clear.
            # print(f)
                data = pd.read_csv(f)
                df = data
                # df = data.T.reset_index(drop=True)  # transpose dataframe
                # print(len(data))
                combined.append(data[10:])
        combined = pd.concat(combined)
        combined.columns = ['Timestep', type]
        # print(len(combined))
        print(combined.head())
        # combined.boxplot(column=['Timeliness'], by=['Timestep'])

        group_combined = combined.groupby('Timestep')

        meantimely=group_combined.mean().rename(columns={type: "meantimely"})
        timely_25per=group_combined.quantile(q=.25).rename(columns={type: "timely_25per"})
        timely_75per=group_combined.quantile(q=.75).rename(columns={type: "timely_75per"})
        maxtimely=group_combined.max().rename(columns={type: "maxtimely"})
        mintimely=group_combined.min().rename(columns={type: "mintimely"})
        timely_5per=group_combined.quantile(q=.05).rename(columns={type: "timely_5per"})
        timely_95per=group_combined.quantile(q=.95).rename(columns={type: "timely_95per"})
        #naming shortcuts
        data_frames = [meantimely, timely_25per, timely_75per, maxtimely,mintimely, 
                timely_5per, timely_95per]
    # Merge them all at once
        merged_df = pd.concat(data_frames, join='outer', axis=1)[:150]
        # df = merged_df
        # df = df.reindex(df.index.union(pd.np.linspace(df.index.min(),df.index.max(), df.index.shape[0]*1))).reset_index(drop=True)  # insert 10 "empty" points between existing ones
        # data = df.interpolate('pchip', order=2)
        # merged_df = df
        x=merged_df.index
        y=merged_df.meantimely
        y_low=merged_df.timely_25per
        y_high=merged_df.timely_75per
        y1_low=merged_df.timely_5per
        y1_high=merged_df.timely_95per
        #make lots of line plots:
        plt.plot(x, y, color=colors[i],marker='o',label=str(t)+' mean') 
        # plt.plot(x, y_low, color='darkorchid', linestyle='-.', label=str(t)+' 25th %') 
        # plt.plot(x, y_high, color='darkorchid', linestyle='-.', label=str(t)+' 75th %') 
        plt.plot(x, y1_low, color=colors[i], linestyle='-', label=str(t)+' 5th %') 
        plt.plot(x, y1_high, color=colors[i], linestyle='-', label=str(t)+' 95th %') 
        plt.legend()
        #fill between the upper and lower bands
        # plt.fill_between(x, y_low, y_high, alpha = .1,color = 'darkorchid')
        plt.fill_between(x, y1_low, y1_high, alpha = .1,color = colors[i])
        #add background grid for visual appeal
        plt.grid(alpha = .2, which='both')
        i +=1
    # plt.yscale("log")
    plt.xlabel('Timestep')
    plt.ylabel(type)
    plt.show()

    # plt.title("")
    # plt.xlabel("Timestep")
    # plt.ylabel("Timeliness")
    # # plt.yscale("log")
    # plt.show()


        # with open(f, 'r') as csvfile:
        #     # print(f)
        #     # print(f.split('\')
        #     plt.title(type)
        #     # setlabel=type
        #     if "random" in f:
        #         setlabel = "Random Strategy"
        #     elif "path" in f:
        #         setlabel = "Attacker Path"
        #     else:
        #         setlabel = "Hypergame EBM"
        #     reader = csv.reader(csvfile)
        #     # Turn our column into an array.
        #     y = []
        #     for row in reader:
        #         if len(row)==0:
        #             continue
        #         # if type == 'loss':
        #         y.append(float(row[1]))
        #         # else:
        #         # y.append(float(row[1]))

        #     # Running tests will be empty.
        #     if len(y) == 0:
        #         return

        #     # print(readable_output(f))

        #     # Get the moving average so the graph isn't so crazy.
        #     # if type == 'loss' or type=='learn':
        #     window = 5
        #     y_av = movingaverage(y, window)
        #     # else:
        #     #     y_av = y
        #         # window = 100

        #     # Use our moving average to get some metrics.
        #     arr = np.array(y_av)
        #     if type == 'loss':
        #         print("%f\t%f\n" % (arr.min(), arr.mean()))
        #     else:
        #         print("%f\t%f\n" % (arr.max(), arr.mean()))

        #     # Plot it.
        #     # plt.clf()  # Clear.
        #     # plt.title(f)
        #     # The -50 removes an artificial drop at the end caused by the moving
        #     # average.
        #     if type == 'loss':
        #         plt.plot(y_av[:-350], label=setlabel)
        #         plt.ylabel('Smoothed Loss')
        #         # plt.ylim(0, 5000)
        #         # plt.xlim(0, 250000)
        #     elif type=="learn":
        #         plt.plot(y_av[100:-5], label=setlabel)
        #         plt.ylabel('Smoothed Distance between collisions')
        #         # plt.ylim(0, 4000)
        #     else:
        #         plt.plot(y_av[10:-5], label=setlabel)
        #         plt.ylabel(type)
    # plt.xlabel('Timestep')
    # plt.legend()
    # plt.savefig(type+".png", bbox_inches='tight')

if __name__ == "__main__":
    # Get our loss result files.
    # os.chdir("results")
    # f = glob.glob("./iou/*.csv")
    f = glob.glob("./timeliness_lol/*.csv")
    # f = glob.glob("./*_miou_final.csv")
    # f = glob.glob("./iou/*1.csv")
    # print(f)
    # plot_file(f, 'mean Intersecion Over Union (mIoU)')
    # plot_file(f, 'Timeliness')
    # box_plot_file(f, 'mean Intersecion Over Union (mIoU)')
    box_plot_file(f, 'Timeliness')
    # plot_file(f, 'meanIoU')
    # f = glob.glob("./*/loss*.csv")
    # plot_file(f, 'loss')
    
    # f = glob.glob("./*/vacuity*.csv")
    # print(f)
    # plot_file(f, 'vacuity')
    
    # f = glob.glob("./*/dissonance*.csv")
    # plot_file(f, 'dissonance')
    
    # f = glob.glob("./*/entropy*.csv")
    # plot_file(f, 'entropy')

    # f = glob.glob("epsilon*.csv")
    # plot_file(f, 'epsilon')

    # f = glob.glob("./*/dirt*.csv")
    # plot_file2(f, 'dirt collected')
    
