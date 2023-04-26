"""
#prediction accuracy file
import math
from statistics import mean


acc = 81

with open('file_predictability.txt', 'a') as file:
    file.write("%i\n" % acc)
    file.close()




#after getting predictability file, run this code
pred = []
with open("file_predictability.txt") as file:
    for line in file:
        line = line.strip()
        pred.append(int(line))

print(mean(pred))


#after getting ASRfile, run this code
asr = []
with open("file_asr.txt") as file:
    for line in file:
        line = line.strip()
        asr.append(float(line))

print(mean(asr))


#after getting safile, run this code
sa = []
with open("file_sa.txt") as file:
    for line in file:
        line = line.strip()
        sa.append(float(line))

print(mean(asr))
"""


"""
import random

batches = [22, 18, 40, 19, 32,  1, 40, 19, 22, 32,  1, 19, 40,  1, 37, 53, 19, 32,
        19, 40, 32, 32, 32, 19, 22, 32, 41, 53, 22, 19, 22, 32, 22, 53, 40, 40, 41, 41, 22,  1, 22, 32, 54, 22, 22, 22, 40, 53, 32,  1,
        18, 19, 22, 41, 22, 54, 32, 22, 53, 40, 32, 19, 22, 40, 22,  1, 45,  1, 53, 45, 32, 40, 40, 41, 22, 22, 32, 41, 37, 54, 53, 53,
        22, 19, 41, 40, 32, 54, 30, 45, 37, 32,  1, 45, 54, 41, 19, 32, 18, 19, 22, 32, 30, 40, 32,  1, 53, 40, 40, 32, 32, 22, 45, 53,
        18, 19, 30, 40, 19, 18, 40, 53, 19, 22, 32, 19, 37, 53, 22, 54, 19, 32,  1, 30, 22, 41, 18, 32, 54, 53, 19, 54, 53, 41, 19, 40,
        53, 54, 22, 19, 45, 19, 41, 45, 40, 32, 32, 19, 32, 32, 32, 32, 54, 19, 53, 19, 19, 22, 41, 40, 53, 22, 40, 18, 32, 32, 22,  1,
        30, 54, 41, 19, 32, 30, 54, 40, 22, 19, 22, 53, 22, 32, 53, 32, 22, 40, 40, 18, 32, 32, 37, 40, 53,  1, 22, 32, 41, 37, 22, 41,
         1, 22, 18, 32, 19, 19]



#total = [124, 133, 135, 141, 144, 145, 148, 152, 156, 159, 161, 175, 177, 182, 187, 190, 191, 200, 202, 204, 206, 214, 215, 217, 219, 220, 223, 227, 229, 233, 240, 249, 251, 252, 253, 254, 687, 689, 692, 704, 708, 712, 713, 716, 721, 726, 731, 733, 740, 745, 748, 758, 760, 764, 768, 769, 773, 775, 776, 781, 789, 792, 794, 799, 801, 805, 813, 814, 820, 823, 825, 831, 838, 861, 875, 881, 884, 891, 892, 893, 896, 898, 900, 905, 906, 916, 918, 923, 924, 927, 930, 933, 942, 943, 955, 957, 958, 960, 962, 963, 974, 979, 980, 986, 987, 988, 989, 992, 1002, 1003, 1005, 1025, 1029, 1031, 1034, 1042, 1047, 1055, 1057, 1064, 1070, 1074, 1076, 1083, 1097, 1101, 1110, 1114, 1121, 1122, 1126, 1128, 1132, 1140, 1145, 1148, 1165, 1170, 1174, 1180, 1183, 1187, 1188, 1193, 1476, 1478, 1484, 1489, 1490, 1494, 1495, 1498, 1499, 1501, 1503, 1504, 1509, 1513, 1515, 1521, 1525, 1529, 1533, 1537, 1542, 1544, 1546, 1548, 1553, 1559, 1566, 1567, 1568, 1570, 1582, 1588, 1590, 1591, 1595, 1609, 1880, 1881, 1888, 1891, 1893, 1895, 1898, 1900, 1904, 1911, 1913, 1915, 1916, 1921, 1926, 1932, 1934, 1935, 1937, 1938, 1942, 1943, 1947, 1963, 1969, 1970, 1973, 1988, 1989, 1991, 1997, 2003, 2007, 2011, 2012, 2015]
total = [53, 40, 22, 22, 19, 22, 22, 32, 18, 19, 53, 1, 53, 54, 40, 41, 19, 19, 32, 22, 22, 40, 18, 54, 37, 41, 40, 22, 37, 53, 32, 40, 18, 19, 19, 45, 32, 41, 22, 32, 40, 32, 40, 30, 22, 41, 22, 53, 45, 18, 53, 18, 41, 19, 19, 54, 40, 32, 32, 45, 41, 53, 1, 18, 22, 54, 32, 30, 22, 32, 32, 53, 53, 40, 30, 32, 32, 40, 22, 22, 41, 19, 19, 53, 22, 32, 22, 19, 1, 22, 19, 40, 40, 1, 32, 32, 19, 40, 22, 22, 41, 22, 19, 45, 22, 32, 53, 19, 22, 19, 32, 1, 32, 32, 1, 54, 40, 1, 53, 18, 19, 32, 54, 22, 53, 32, 32, 40, 41, 53, 1, 32, 22, 22, 41, 22, 53, 54, 40, 22, 32, 37, 41, 37, 41, 41, 54, 40, 19, 54, 19, 18, 32, 19, 40, 32, 22, 32, 32, 53, 32, 54, 45, 32, 45, 32, 22, 41, 32, 19, 1, 53, 19, 1, 40, 37, 32, 22, 18, 32, 19, 40, 30, 22, 40, 22, 54, 19, 45, 30, 40, 32, 30, 1, 40, 53, 53, 54, 32, 1, 19, 1, 37, 41, 40, 19, 32, 22, 22, 32, 22, 19, 40, 19, 53, 19]



import numpy as np

mu, sigma = 0.85, 0.03# mean and standard deviation


car_ac = np.random.normal(mu, sigma, 56)
print(car_ac)


for i in car_ac:
        if random.random() < i:
                print('ture')
        else:
                print("false")


#car vulnerability: whether dos will work or not
mu1, sigma1 = 0.4, 0.01  # mean and standard deviation
car_vulnerability = np.random.normal(mu1, sigma1, 56)
print("car_vul:", car_vulnerability)
"""
import math

rsu_asset = [[0.1, 0.1], [0.15, 0.1], [0.1, 0.2], [0.1, 0.15]]



ccs_asset = [[0.1, 0.05]]


def AC(cpu_load, memory_load):
        a = (0.5 * cpu_load) + (0.5 * memory_load)
        AC = min((1 * (math.exp(-a), 1)))
        return AC

for i in range(20):
        rsu_asset[0][0] = rsu_asset[0][0]*1.1

        rsu_asset[0][1] = rsu_asset[0][1] * 1.1
        print(rsu_asset[0])
        print(AC(rsu_asset[0][0], rsu_asset[0][1]))




import numpy as np

a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
index = [2, 3, 6]

new_a = np.delete(a, index)

print(new_a) #Prints `[1, 2, 5, 6, 8, 9]`


a = ['v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9','v10', 'v11', 'v12', 'v13', 'v14', 'v15', 'v16', 'v17', 'v18', 'v19', \
'v20', 'v21', 'v22', 'v23', 'v24', 'v25', 'v26', 'v27', 'v28', 'v29','v30', 'v31', 'v32', 'v33', 'v34', 'v35', 'v36', 'v37', 'v38', 'v39',\
'v40', 'v41', 'v42', 'v43', 'v44', 'v45', 'v46', 'v47', 'v48', 'v49','v50', 'v51', 'v52', 'v53', 'v54', 'v55',\

's1_0', 's1_1', 's1_2', 's1_3','s1_4', 's1_5', 's1_6', 's1_7', 's1_8', 's1_9', 's1_10', 's1_11', 's1_12', 's1_13', 's1_14', 's1_15', 's1_16',\
's1_17', 's1_18', 's1_19', 's1_20','s1_21', 's1_22', 's1_23', 's1_24', 's1_25', 's1_26', 's1_27', 's1_28', 's1_29', 's1_30', 's1_31', 's1_32', 's1_33',\
's1_34', 's1_35', 's1_36', 's1_37','s1_38', 's1_39', 's1_40', 's1_41', 's1_42', 's1_43', 's1_44', 's1_45', 's1_46', 's1_47', 's1_48', 's1_49', 's1_50',\
's1_51', 's1_52', 's1_53', 's1_54', 's1_55',\


'sv1_0', 'sv1_1', 'sv1_2', 'sv1_3','sv1_4', 'sv1_5', 'sv1_6', 'sv1_7', 'sv1_8', 'sv1_9', 'sv1_10', 'sv1_11', 'sv1_12', 'sv1_13', 'sv1_14', 'sv1_15', 'sv1_16',\
'sv1_17', 'sv1_18', 'sv1_19', 'sv1_20', 'sv1_21', 'sv1_22', 'sv1_23', 'sv1_24', 'sv1_25', 'sv1_26', 'sv1_27', 'sv1_28', 'sv1_29', 'sv1_30', 'sv1_31', 'sv1_32', 'sv1_33',\
'sv1_34', 'sv1_35', 'sv1_36', 'sv1_37', 'sv1_38', 'sv1_39', 'sv1_40', 'sv1_41', 'sv1_42', 'sv1_43', 'sv1_44', 'sv1_45', 'sv1_46', 'sv1_47', 'sv1_48', 'sv1_49', 'sv1_50',\
'sv1_51', 'sv1_52', 'sv1_53', 'sv1_54', 'sv1_55',\


'sd1_0', 'sd1_1', 'sd1_2', 'sd1_3', 'sd1_4', 'sd1_5', 'sd1_6', 'sd1_7', 'sd1_8', 'sd1_9', 'sd1_10', 'sd1_11', 'sd1_12', 'sd1_13', 'sd1_14', 'sd1_15', 'sd1_16',\
'sd1_17', 'sd1_18', 'sd1_19', 'sd1_20', 'sd1_21', 'sd1_22', 'sd1_23', 'sd1_24', 'sd1_25', 'sd1_26', 'sd1_27', 'sd1_28', 'sd1_29', 'sd1_30', 'sd1_31', 'sd1_32', 'sd1_33',\
'sd1_34', 'sd1_35', 'sd1_36', 'sd1_37', 'sd1_38', 'sd1_39', 'sd1_40', 'sd1_41', 'sd1_42', 'sd1_43', 'sd1_44', 'sd1_45', 'sd1_46', 'sd1_47', 'sd1_48', 'sd1_49', 'sd1_50',\
'sd1_51', 'sd1_52', 'sd1_53', 'sd1_54', 'sd1_55',\



'ccs0_1', 's2_ccs0_1', 'sv2_ccs0_1', 'sd2_ccs0_r0_1', 'sd2_ccs0_r1_1', 'sd2_ccs0_r2_1', 'sd2_ccs0_r3_1', 'r0_1', 'r1_1', 'r2_1', 'r3_1', 's3_r0_1', 's3_r1_1', 's3_r2_1', 's3_r3_1', 'sv3_r0_1', 'sv3_r1_1', 'sv3_r2_1', 'sv3_r3_1', \
'sd3_r0_css0_1', 'sd3_r1_ccs0_1', 'sd3_r2_ccs0_1', 'sd3_r3_ccs0_1', 's4_ccs0_1', 'sv4_ccs0_1',\




'sd2_ccs0_r0_2', 'sd2_ccs0_r1_2', 'sd2_ccs0_r2_2', 'sd2_ccs0_r3_2', 'r0_2', 'r1_2', 'r2_2', 'r3_2', 's3_r0_2', 's3_r1_2', 's3_r2_2', 's3_r3_2', 'sv3_r0_2', 'sv3_r1_2', 'sv3_r2_2', 'sv3_r3_2', 'sd3_r0_css0_2', 'sd3_r1_ccs0_2', 'sd3_r2_ccs0_2', 'sd3_r3_ccs0_2', 'ccs0_2', 's4_ccs0_2', 'sv4_ccs0_2',\

'sd2_ccs0_r0_3', 'sd2_ccs0_r1_3', 'sd2_ccs0_r2_3', 'sd2_ccs0_r3_3', 'r0_3', 'r1_3', 'r2_3', 'r3_3', 's3_r0_3', 's3_r1_3', 's3_r2_3', 's3_r3_3', 'sv3_r0_3', 'sv3_r1_3', 'sv3_r2_3', 'sv3_r3_3', 'sd3_r0_css0_3', 'sd3_r1_ccs0_3', 'sd3_r2_ccs0_3', 'sd3_r3_ccs0_3', 'ccs0_3', 's4_ccs0_3', 'sv4_ccs0_3',\

'sd2_ccs0_r0_4', 'sd2_ccs0_r1_4', 'sd2_ccs0_r2_4', 'sd2_ccs0_r3_4', 'r0_4', 'r1_4', 'r2_4', 'r3_4', 's3_r0_4', 's3_r1_4', 's3_r2_4', 's3_r3_4', 'sv3_r0_4', 'sv3_r1_4', 'sv3_r2_4', 'sv3_r3_4', 'sd3_r0_css0_4', 'sd3_r1_ccs0_4', 'sd3_r2_ccs0_4', 'sd3_r3_ccs0_4', 'ccs0_4', 's4_ccs0_4', 'sv4_ccs0_4',\

'sd2_ccs0_r0_5', 'sd2_ccs0_r1_5', 'sd2_ccs0_r2_5', 'sd2_ccs0_r3_5', 'r0_5', 'r1_5', 'r2_5', 'r3_5', 's3_r0_5', 's3_r1_5', 's3_r2_5', 's3_r3_5', 'sv3_r0_5', 'sv3_r1_5', 'sv3_r2_5', 'sv3_r3_5', 'sd3_r0_css0_5', 'sd3_r1_ccs0_5', 'sd3_r2_ccs0_5', 'sd3_r3_ccs0_5', 'ccs0_5', 's4_ccs0_5', 'sv4_ccs0_5',\

'sd2_ccs0_r0_6', 'sd2_ccs0_r1_6', 'sd2_ccs0_r2_6', 'sd2_ccs0_r3_6', 'r0_6', 'r1_6', 'r2_6', 'r3_6', 's3_r0_6', 's3_r1_6', 's3_r2_6', 's3_r3_6', 'sv3_r0_6', 'sv3_r1_6', 'sv3_r2_6', 'sv3_r3_6', 'sd3_r0_css0_6', 'sd3_r1_ccs0_6', 'sd3_r2_ccs0_6', 'sd3_r3_ccs0_6', 'ccs0_6', 's4_ccs0_6', 'sv4_ccs0_6',\

'sd2_ccs0_r0_7', 'sd2_ccs0_r1_7', 'sd2_ccs0_r2_7', 'sd2_ccs0_r3_7', 'r0_7', 'r1_7', 'r2_7', 'r3_7', 's3_r0_7', 's3_r1_7', 's3_r2_7', 's3_r3_7', 'sv3_r0_7', 'sv3_r1_7', 'sv3_r2_7', 'sv3_r3_7', 'sd3_r0_css0_7', 'sd3_r1_ccs0_7', 'sd3_r2_ccs0_7', 'sd3_r3_ccs0_7', 'ccs0_7', 's4_ccs0_7', 'sv4_ccs0_7',\

'sd2_ccs0_r0_8', 'sd2_ccs0_r1_8', 'sd2_ccs0_r2_8', 'sd2_ccs0_r3_8', 'r0_8', 'r1_8', 'r2_8', 'r3_8', 's3_r0_8', 's3_r1_8', 's3_r2_8', 's3_r3_8', 'sv3_r0_8', 'sv3_r1_8', 'sv3_r2_8', 'sv3_r3_8', 'sd3_r0_css0_8', 'sd3_r1_ccs0_8', 'sd3_r2_ccs0_8', 'sd3_r3_ccs0_8', 'ccs0_8', 's4_ccs0_8', 'sv4_ccs0_8',\

'sd2_ccs0_r0_9', 'sd2_ccs0_r1_9', 'sd2_ccs0_r2_9', 'sd2_ccs0_r3_9', 'r0_9', 'r1_9', 'r2_9', 'r3_9', 's3_r0_9', 's3_r1_9', 's3_r2_9', 's3_r3_9', 'sv3_r0_9', 'sv3_r1_9', 'sv3_r2_9', 'sv3_r3_9', 'sd3_r0_css0_9', 'sd3_r1_ccs0_9', 'sd3_r2_ccs0_9', 'sd3_r3_ccs0_9', 'ccs0_9', 's4_ccs0_9', 'sv4_ccs0_9',\

'sd2_ccs0_r0_10', 'sd2_ccs0_r1_10', 'sd2_ccs0_r2_10', 'sd2_ccs0_r3_10', 'r0_10', 'r1_10', 'r2_10', 'r3_10', 's3_r0_10', 's3_r1_10', 's3_r2_10', 's3_r3_10', 'sv3_r0_10', 'sv3_r1_10', 'sv3_r2_10', 'sv3_r3_10', 'sd3_r0_css0_10', 'sd3_r1_ccs0_10', 'sd3_r2_ccs0_10', 'sd3_r3_ccs0_10', 'ccs0_10', 's4_ccs0_10', 'sv4_ccs0_10',\

'sd2_ccs0_r0_11', 'sd2_ccs0_r1_11', 'sd2_ccs0_r2_11', 'sd2_ccs0_r3_11', 'r0_11', 'r1_11', 'r2_11', 'r3_11', 's3_r0_11', 's3_r1_11', 's3_r2_11', 's3_r3_11', 'sv3_r0_11', 'sv3_r1_11', 'sv3_r2_11', 'sv3_r3_11', 'sd3_r0_css0_11', 'sd3_r1_ccs0_11', 'sd3_r2_ccs0_11', 'sd3_r3_ccs0_11', 'ccs0_11', 's4_ccs0_11', 'sv4_ccs0_11',\

'sd2_ccs0_r0_12', 'sd2_ccs0_r1_12', 'sd2_ccs0_r2_12', 'sd2_ccs0_r3_12', 'r0_12', 'r1_12', 'r2_12', 'r3_12', 's3_r0_12', 's3_r1_12', 's3_r2_12', 's3_r3_12', 'sv3_r0_12', 'sv3_r1_12', 'sv3_r2_12', 'sv3_r3_12', 'sd3_r0_css0_12', 'sd3_r1_ccs0_12', 'sd3_r2_ccs0_12', 'sd3_r3_ccs0_12', 'ccs0_12', 's4_ccs0_12', 'sv4_ccs0_12',\

'sd2_ccs0_r0_13', 'sd2_ccs0_r1_13', 'sd2_ccs0_r2_13', 'sd2_ccs0_r3_13', 'r0_13', 'r1_13', 'r2_13', 'r3_13', 's3_r0_13', 's3_r1_13', 's3_r2_13', 's3_r3_13', 'sv3_r0_13', 'sv3_r1_13', 'sv3_r2_13', 'sv3_r3_13', 'sd3_r0_css0_13', 'sd3_r1_ccs0_13', 'sd3_r2_ccs0_13', 'sd3_r3_ccs0_13', 'ccs0_13', 's4_ccs0_13', 'sv4_ccs0_13',\

'sd2_ccs0_r0_14', 'sd2_ccs0_r1_14', 'sd2_ccs0_r2_14', 'sd2_ccs0_r3_14', 'r0_14', 'r1_14', 'r2_14', 'r3_14', 's3_r0_14', 's3_r1_14', 's3_r2_14', 's3_r3_14', 'sv3_r0_14', 'sv3_r1_14', 'sv3_r2_14', 'sv3_r3_14', 'sd3_r0_css0_14', 'sd3_r1_ccs0_14', 'sd3_r2_ccs0_14', 'sd3_r3_ccs0_14', 'ccs0_14', 's4_ccs0_14', 'sv4_ccs0_14',\

'sd2_ccs0_r0_15', 'sd2_ccs0_r1_15', 'sd2_ccs0_r2_15', 'sd2_ccs0_r3_15', 'r0_15', 'r1_15', 'r2_15', 'r3_15', 's3_r0_15', 's3_r1_15', 's3_r2_15', 's3_r3_15', 'sv3_r0_15', 'sv3_r1_15', 'sv3_r2_15', 'sv3_r3_15', 'sd3_r0_css0_15', 'sd3_r1_ccs0_15', 'sd3_r2_ccs0_15', 'sd3_r3_ccs0_15', 'ccs0_15', 's4_ccs0_15', 'sv4_ccs0_15',\
                                 'mc_sa', 'mc_acc', 'outcome']

print(len(a))


aa = ['v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9','v10', 'v11', 'v12', 'v13', 'v14', 'v15', 'v16', 'v17', 'v18', 'v19', \
'v20', 'v21', 'v22', 'v23', 'v24', 'v25', 'v26', 'v27', 'v28', 'v29','v30', 'v31', 'v32', 'v33', 'v34', 'v35', 'v36', 'v37', 'v38', 'v39',\
'v40', 'v41', 'v42', 'v43', 'v44', 'v45', 'v46', 'v47', 'v48', 'v49','v50', 'v51', 'v52', 'v53', 'v54', 'v55',\

's1_0', 's1_1', 's1_2', 's1_3','s1_4', 's1_5', 's1_6', 's1_7', 's1_8', 's1_9', 's1_10', 's1_11', 's1_12', 's1_13', 's1_14', 's1_15', 's1_16',\
's1_17', 's1_18', 's1_19', 's1_20','s1_21', 's1_22', 's1_23', 's1_24', 's1_25', 's1_26', 's1_27', 's1_28', 's1_29', 's1_30', 's1_31', 's1_32', 's1_33',\
's1_34', 's1_35', 's1_36', 's1_37','s1_38', 's1_39', 's1_40', 's1_41', 's1_42', 's1_43', 's1_44', 's1_45', 's1_46', 's1_47', 's1_48', 's1_49', 's1_50',\
's1_51', 's1_52', 's1_53', 's1_54', 's1_55',\


'sv1_0', 'sv1_1', 'sv1_2', 'sv1_3','sv1_4', 'sv1_5', 'sv1_6', 'sv1_7', 'sv1_8', 'sv1_9', 'sv1_10', 'sv1_11', 'sv1_12', 'sv1_13', 'sv1_14', 'sv1_15', 'sv1_16',\
'sv1_17', 'sv1_18', 'sv1_19', 'sv1_20', 'sv1_21', 'sv1_22', 'sv1_23', 'sv1_24', 'sv1_25', 'sv1_26', 'sv1_27', 'sv1_28', 'sv1_29', 'sv1_30', 'sv1_31', 'sv1_32', 'sv1_33',\
'sv1_34', 'sv1_35', 'sv1_36', 'sv1_37', 'sv1_38', 'sv1_39', 'sv1_40', 'sv1_41', 'sv1_42', 'sv1_43', 'sv1_44', 'sv1_45', 'sv1_46', 'sv1_47', 'sv1_48', 'sv1_49', 'sv1_50',\
'sv1_51', 'sv1_52', 'sv1_53', 'sv1_54', 'sv1_55',\


'sd1_0', 'sd1_1', 'sd1_2', 'sd1_3', 'sd1_4', 'sd1_5', 'sd1_6', 'sd1_7', 'sd1_8', 'sd1_9', 'sd1_10', 'sd1_11', 'sd1_12', 'sd1_13', 'sd1_14', 'sd1_15', 'sd1_16',\
'sd1_17', 'sd1_18', 'sd1_19', 'sd1_20', 'sd1_21', 'sd1_22', 'sd1_23', 'sd1_24', 'sd1_25', 'sd1_26', 'sd1_27', 'sd1_28', 'sd1_29', 'sd1_30', 'sd1_31', 'sd1_32', 'sd1_33',\
'sd1_34', 'sd1_35', 'sd1_36', 'sd1_37', 'sd1_38', 'sd1_39', 'sd1_40', 'sd1_41', 'sd1_42', 'sd1_43', 'sd1_44', 'sd1_45', 'sd1_46', 'sd1_47', 'sd1_48', 'sd1_49', 'sd1_50',\
'sd1_51', 'sd1_52', 'sd1_53', 'sd1_54', 'sd1_55']



print(len(aa))



ccs_asset = [[0.5, 0.5]]

def AC(cpu_load, memory_load):
        a = (0.5 * cpu_load) + (0.5 * memory_load)
        AC = min((1 * (math.exp(-a), 1)))
        return AC


            # print(AC(rsu_asset[0][0], rsu_asset[0][1]))
print("ac:",AC(ccs_asset[0][0], ccs_asset[0][1]))
"""
import random

ab= []
for i in range(100):
        if random.random() < AC(ccs_asset[0][0], ccs_asset[0][1]):
                ab.append(1)

        else:
                ab.append(0)
count = 0
for i in ab:
        if i == 0:
                count+=1

print(count)



a = np.array([11,14,2,1,45])

b = [0,1]

aa = np.delete(a,b)
print(aa)


for i in range(100):

        rsu0_ev = min(np.random.normal(0.5,0.05),1)

        print(rsu0_ev)
"""

"""
import torch


tensor1 = torch.tensor(90)

print(tensor1)
print(type(tensor1))

print(type(int(tensor1)))

if tensor1 >= 80:
        print('yes')
else:
        print('no')


for i in range(100):
        rsu0_ev = min(np.random.normal(0.04, 0.05), 1)
        print(rsu0_ev)

"""
for i in range(100):
        rsu0_cpu = min(np.random.normal(0.07, 0.05), 1)

        print(rsu0_cpu)



aaaa= ['v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v13',\
                                 'v14', 'v15', 'v16', 'v17', 'v18', 'v19',\
                                 'v20', 'v21', 'v22', 'v23', 'v24', 'v25', 'v26', 'v27', 'v28', 'v29', 'v30', 'v31',\
                                 'v32', 'v33', 'v34', 'v35', 'v36', 'v37', 'v38', 'v39', \
                                 'v40', 'v41', 'v42', 'v43', 'v44', 'v45', 'v46', 'v47', 'v48', 'v49', 'v50', 'v51',\
                                 'v52', 'v53', 'v54', 'v55', \

                                 's1_0', 's1_1', 's1_2', 's1_3', 's1_4', 's1_5', 's1_6', 's1_7', 's1_8', 's1_9',\
                                 's1_10', 's1_11', 's1_12', 's1_13', 's1_14', 's1_15', 's1_16', \
                                 's1_17', 's1_18', 's1_19', 's1_20', 's1_21', 's1_22', 's1_23', 's1_24', 's1_25',\
                                 's1_26', 's1_27', 's1_28', 's1_29', 's1_30', 's1_31', 's1_32', 's1_33', \
                                 's1_34', 's1_35', 's1_36', 's1_37', 's1_38', 's1_39', 's1_40', 's1_41', 's1_42',\
                                 's1_43', 's1_44', 's1_45', 's1_46', 's1_47', 's1_48', 's1_49', 's1_50', \
                                 's1_51', 's1_52', 's1_53', 's1_54', 's1_55', \

                                 'sv1_0', 'sv1_1', 'sv1_2', 'sv1_3', 'sv1_4', 'sv1_5', 'sv1_6', 'sv1_7', 'sv1_8',
                                 'sv1_9', 'sv1_10', 'sv1_11', 'sv1_12', 'sv1_13', 'sv1_14', 'sv1_15', 'sv1_16', \
                                 'sv1_17', 'sv1_18', 'sv1_19', 'sv1_20', 'sv1_21', 'sv1_22', 'sv1_23', 'sv1_24',
                                 'sv1_25', 'sv1_26', 'sv1_27', 'sv1_28', 'sv1_29', 'sv1_30', 'sv1_31', 'sv1_32',
                                 'sv1_33', \
                                 'sv1_34', 'sv1_35', 'sv1_36', 'sv1_37', 'sv1_38', 'sv1_39', 'sv1_40', 'sv1_41',
                                 'sv1_42', 'sv1_43', 'sv1_44', 'sv1_45', 'sv1_46', 'sv1_47', 'sv1_48', 'sv1_49',
                                 'sv1_50', \
                                 'sv1_51', 'sv1_52', 'sv1_53', 'sv1_54', 'sv1_55', \

                                 'sd1_0', 'sd1_1', 'sd1_2', 'sd1_3', 'sd1_4', 'sd1_5', 'sd1_6', 'sd1_7', 'sd1_8',
                                 'sd1_9', 'sd1_10', 'sd1_11', 'sd1_12', 'sd1_13', 'sd1_14', 'sd1_15', 'sd1_16', \
                                 'sd1_17', 'sd1_18', 'sd1_19', 'sd1_20', 'sd1_21', 'sd1_22', 'sd1_23', 'sd1_24',
                                 'sd1_25', 'sd1_26', 'sd1_27', 'sd1_28', 'sd1_29', 'sd1_30', 'sd1_31', 'sd1_32',
                                 'sd1_33', \
                                 'sd1_34', 'sd1_35', 'sd1_36', 'sd1_37', 'sd1_38', 'sd1_39', 'sd1_40', 'sd1_41',
                                 'sd1_42', 'sd1_43', 'sd1_44', 'sd1_45', 'sd1_46', 'sd1_47', 'sd1_48', 'sd1_49',
                                 'sd1_50', \
                                 'sd1_51', 'sd1_52', 'sd1_53', 'sd1_54', 'sd1_55', \

                                 'ccs0_1', 's2_ccs0_1', 'sv2_ccs0_1', 'sd2_ccs0_r0_1', 'sd2_ccs0_r1_1', 'sd2_ccs0_r2_1',
                                 'sd2_ccs0_r3_1', 'r0_1', 'r1_1', 'r2_1', 'r3_1', 's3_r0_1', 's3_r1_1', 's3_r2_1',
                                 's3_r3_1', 'sv3_r0_1', 'sv3_r1_1', 'sv3_r2_1', 'sv3_r3_1', \
                                 'sd3_r0_css0_1', 'sd3_r1_ccs0_1', 'sd3_r2_ccs0_1', 'sd3_r3_ccs0_1', 's4_ccs0_1',
                                 'sv4_ccs0_1', 'sv5_mcc_1', \

                                 'sd2_ccs0_r0_2', 'sd2_ccs0_r1_2', 'sd2_ccs0_r2_2', 'sd2_ccs0_r3_2',

                                 'r0_2', 'r1_2', 'r2_2', 'r3_2',

                                 's3_r0_2', 's3_r1_2', 's3_r2_2', 's3_r3_2',

                                 'sv3_r0_2', 'sv3_r1_2', 'sv3_r2_2', 'sv3_r3_2',

                                 'sd3_r0_css0_2', 'sd3_r1_ccs0_2', 'sd3_r2_ccs0_2', 'sd3_r3_ccs0_2',

                                 'ccs0_2', 's4_ccs0_2', 'sv4_ccs0_2', 'sv5_mcc_2', \

                                 'sd2_ccs0_r0_3', 'sd2_ccs0_r1_3', 'sd2_ccs0_r2_3', 'sd2_ccs0_r3_3', 'r0_3', 'r1_3',
                                 'r2_3', 'r3_3', 's3_r0_3', 's3_r1_3', 's3_r2_3', 's3_r3_3', 'sv3_r0_3', 'sv3_r1_3',
                                 'sv3_r2_3', 'sv3_r3_3', 'sd3_r0_css0_3', 'sd3_r1_ccs0_3', 'sd3_r2_ccs0_3',
                                 'sd3_r3_ccs0_3', 'ccs0_3', 's4_ccs0_3', 'sv4_ccs0_3', 'sv5_mcc_3', \

                                 'sd2_ccs0_r0_4', 'sd2_ccs0_r1_4', 'sd2_ccs0_r2_4', 'sd2_ccs0_r3_4', 'r0_4', 'r1_4',
                                 'r2_4', 'r3_4', 's3_r0_4', 's3_r1_4', 's3_r2_4', 's3_r3_4', 'sv3_r0_4', 'sv3_r1_4',
                                 'sv3_r2_4', 'sv3_r3_4', 'sd3_r0_css0_4', 'sd3_r1_ccs0_4', 'sd3_r2_ccs0_4',
                                 'sd3_r3_ccs0_4', 'ccs0_4', 's4_ccs0_4', 'sv4_ccs0_4', 'sv5_mcc_4', \

                                 'sd2_ccs0_r0_5', 'sd2_ccs0_r1_5', 'sd2_ccs0_r2_5', 'sd2_ccs0_r3_5', 'r0_5', 'r1_5',
                                 'r2_5', 'r3_5', 's3_r0_5', 's3_r1_5', 's3_r2_5', 's3_r3_5', 'sv3_r0_5', 'sv3_r1_5',
                                 'sv3_r2_5', 'sv3_r3_5', 'sd3_r0_css0_5', 'sd3_r1_ccs0_5', 'sd3_r2_ccs0_5',
                                 'sd3_r3_ccs0_5', 'ccs0_5', 's4_ccs0_5', 'sv4_ccs0_5', 'sv5_mcc_5', \

                                 'sd2_ccs0_r0_6', 'sd2_ccs0_r1_6', 'sd2_ccs0_r2_6', 'sd2_ccs0_r3_6', 'r0_6', 'r1_6',
                                 'r2_6', 'r3_6', 's3_r0_6', 's3_r1_6', 's3_r2_6', 's3_r3_6', 'sv3_r0_6', 'sv3_r1_6',
                                 'sv3_r2_6', 'sv3_r3_6', 'sd3_r0_css0_6', 'sd3_r1_ccs0_6', 'sd3_r2_ccs0_6',
                                 'sd3_r3_ccs0_6', 'ccs0_6', 's4_ccs0_6', 'sv4_ccs0_6', 'sv5_mcc_6', \

                                 'sd2_ccs0_r0_7', 'sd2_ccs0_r1_7', 'sd2_ccs0_r2_7', 'sd2_ccs0_r3_7', 'r0_7', 'r1_7',
                                 'r2_7', 'r3_7', 's3_r0_7', 's3_r1_7', 's3_r2_7', 's3_r3_7', 'sv3_r0_7', 'sv3_r1_7',
                                 'sv3_r2_7', 'sv3_r3_7', 'sd3_r0_css0_7', 'sd3_r1_ccs0_7', 'sd3_r2_ccs0_7',
                                 'sd3_r3_ccs0_7', 'ccs0_7', 's4_ccs0_7', 'sv4_ccs0_7', 'sv5_mcc_7', \

                                 'sd2_ccs0_r0_8', 'sd2_ccs0_r1_8', 'sd2_ccs0_r2_8', 'sd2_ccs0_r3_8', 'r0_8', 'r1_8',
                                 'r2_8', 'r3_8', 's3_r0_8', 's3_r1_8', 's3_r2_8', 's3_r3_8', 'sv3_r0_8', 'sv3_r1_8',
                                 'sv3_r2_8', 'sv3_r3_8', 'sd3_r0_css0_8', 'sd3_r1_ccs0_8', 'sd3_r2_ccs0_8',
                                 'sd3_r3_ccs0_8', 'ccs0_8', 's4_ccs0_8', 'sv4_ccs0_8', 'sv5_mcc_8', \

                                 'sd2_ccs0_r0_9', 'sd2_ccs0_r1_9', 'sd2_ccs0_r2_9', 'sd2_ccs0_r3_9', 'r0_9', 'r1_9',
                                 'r2_9', 'r3_9', 's3_r0_9', 's3_r1_9', 's3_r2_9', 's3_r3_9', 'sv3_r0_9', 'sv3_r1_9',
                                 'sv3_r2_9', 'sv3_r3_9', 'sd3_r0_css0_9', 'sd3_r1_ccs0_9', 'sd3_r2_ccs0_9',
                                 'sd3_r3_ccs0_9', 'ccs0_9', 's4_ccs0_9', 'sv4_ccs0_9', 'sv5_mcc_9', \

                                 'sd2_ccs0_r0_10', 'sd2_ccs0_r1_10', 'sd2_ccs0_r2_10', 'sd2_ccs0_r3_10', 'r0_10',
                                 'r1_10', 'r2_10', 'r3_10', 's3_r0_10', 's3_r1_10', 's3_r2_10', 's3_r3_10', 'sv3_r0_10',
                                 'sv3_r1_10', 'sv3_r2_10', 'sv3_r3_10', 'sd3_r0_css0_10', 'sd3_r1_ccs0_10',
                                 'sd3_r2_ccs0_10', 'sd3_r3_ccs0_10', 'ccs0_10', 's4_ccs0_10', 'sv4_ccs0_10',
                                 'sv5_mcc_10', \

                                 'sd2_ccs0_r0_11', 'sd2_ccs0_r1_11', 'sd2_ccs0_r2_11', 'sd2_ccs0_r3_11', 'r0_11',
                                 'r1_11', 'r2_11', 'r3_11', 's3_r0_11', 's3_r1_11', 's3_r2_11', 's3_r3_11', 'sv3_r0_11',
                                 'sv3_r1_11', 'sv3_r2_11', 'sv3_r3_11', 'sd3_r0_css0_11', 'sd3_r1_ccs0_11',
                                 'sd3_r2_ccs0_11', 'sd3_r3_ccs0_11', 'ccs0_11', 's4_ccs0_11', 'sv4_ccs0_11',
                                 'sv5_mcc_11', \

                                 'sd2_ccs0_r0_12', 'sd2_ccs0_r1_12', 'sd2_ccs0_r2_12', 'sd2_ccs0_r3_12', 'r0_12',
                                 'r1_12', 'r2_12', 'r3_12', 's3_r0_12', 's3_r1_12', 's3_r2_12', 's3_r3_12', 'sv3_r0_12',
                                 'sv3_r1_12', 'sv3_r2_12', 'sv3_r3_12', 'sd3_r0_css0_12', 'sd3_r1_ccs0_12',
                                 'sd3_r2_ccs0_12', 'sd3_r3_ccs0_12', 'ccs0_12', 's4_ccs0_12', 'sv4_ccs0_12',
                                 'sv5_mcc_12', \

                                 'sd2_ccs0_r0_13', 'sd2_ccs0_r1_13', 'sd2_ccs0_r2_13', 'sd2_ccs0_r3_13', 'r0_13',
                                 'r1_13', 'r2_13', 'r3_13', 's3_r0_13', 's3_r1_13', 's3_r2_13', 's3_r3_13', 'sv3_r0_13',
                                 'sv3_r1_13', 'sv3_r2_13', 'sv3_r3_13', 'sd3_r0_css0_13', 'sd3_r1_ccs0_13',
                                 'sd3_r2_ccs0_13', 'sd3_r3_ccs0_13', 'ccs0_13', 's4_ccs0_13', 'sv4_ccs0_13',
                                 'sv5_mcc_13', \

                                 'sd2_ccs0_r0_14', 'sd2_ccs0_r1_14', 'sd2_ccs0_r2_14', 'sd2_ccs0_r3_14', 'r0_14',
                                 'r1_14', 'r2_14', 'r3_14', 's3_r0_14', 's3_r1_14', 's3_r2_14', 's3_r3_14', 'sv3_r0_14',
                                 'sv3_r1_14', 'sv3_r2_14', 'sv3_r3_14', 'sd3_r0_css0_14', 'sd3_r1_ccs0_14',
                                 'sd3_r2_ccs0_14', 'sd3_r3_ccs0_14', 'ccs0_14', 's4_ccs0_14', 'sv4_ccs0_14',
                                 'sv5_mcc_14', \

                                 'sd2_ccs0_r0_15', 'sd2_ccs0_r1_15', 'sd2_ccs0_r2_15', 'sd2_ccs0_r3_15', 'r0_15',
                                 'r1_15', 'r2_15', 'r3_15', 's3_r0_15', 's3_r1_15', 's3_r2_15', 's3_r3_15', 'sv3_r0_15',
                                 'sv3_r1_15', 'sv3_r2_15', 'sv3_r3_15', 'sd3_r0_css0_15', 'sd3_r1_ccs0_15',
                                 'sd3_r2_ccs0_15', 'sd3_r3_ccs0_15', 'ccs0_15', 's4_ccs0_15', 'sv4_ccs0_15',
                                 'sv5_mcc_15', \

                                 'sd2_ccs0_r0_16', 'sd2_ccs0_r1_16', 'sd2_ccs0_r2_16', 'sd2_ccs0_r3_16', 'r0_16',
                                 'r1_16', 'r2_16', 'r3_16', 's3_r0_16', 's3_r1_16', 's3_r2_16', 's3_r3_16', 'sv3_r0_16',
                                 'sv3_r1_16', 'sv3_r2_16', 'sv3_r3_16', 'sd3_r0_css0_16', 'sd3_r1_ccs0_16',
                                 'sd3_r2_ccs0_16', 'sd3_r3_ccs0_16', 'ccs0_16', 's4_ccs0_16', 'sv4_ccs0_16',
                                 'sv5_mcc_16', \

                                 'sd2_ccs0_r0_17', 'sd2_ccs0_r1_17', 'sd2_ccs0_r2_17', 'sd2_ccs0_r3_17', 'r0_17',
                                 'r1_17', 'r2_17', 'r3_17', 's3_r0_17', 's3_r1_17', 's3_r2_17', 's3_r3_17', 'sv3_r0_17',
                                 'sv3_r1_17', 'sv3_r2_17', 'sv3_r3_17', 'sd3_r0_css0_17', 'sd3_r1_ccs0_17',
                                 'sd3_r2_ccs0_17', 'sd3_r3_ccs0_17', 'ccs0_17', 's4_ccs0_17', 'sv4_ccs0_17',
                                 'sv5_mcc_17', \

                                 'sd2_ccs0_r0_18', 'sd2_ccs0_r1_18', 'sd2_ccs0_r2_18', 'sd2_ccs0_r3_18', 'r0_18',
                                 'r1_18', 'r2_18', 'r3_18', 's3_r0_18', 's3_r1_18', 's3_r2_18', 's3_r3_18', 'sv3_r0_18',
                                 'sv3_r1_18', 'sv3_r2_18', 'sv3_r3_18', 'sd3_r0_css0_18', 'sd3_r1_ccs0_18',
                                 'sd3_r2_ccs0_18', 'sd3_r3_ccs0_18', 'ccs0_18', 's4_ccs0_18', 'sv4_ccs0_18',
                                 'sv5_mcc_18', \

                                 'sd2_ccs0_r0_19', 'sd2_ccs0_r1_19', 'sd2_ccs0_r2_19', 'sd2_ccs0_r3_19', 'r0_19',
                                 'r1_19', 'r2_19', 'r3_19', 's3_r0_19', 's3_r1_19', 's3_r2_19', 's3_r3_19', 'sv3_r0_19',
                                 'sv3_r1_19', 'sv3_r2_19', 'sv3_r3_19', 'sd3_r0_css0_19', 'sd3_r1_ccs0_19',
                                 'sd3_r2_ccs0_19', 'sd3_r3_ccs0_19', 'ccs0_19', 's4_ccs0_19', 'sv4_ccs0_19',
                                 'sv5_mcc_19', \

                                 'sd2_ccs0_r0_20', 'sd2_ccs0_r1_20', 'sd2_ccs0_r2_20', 'sd2_ccs0_r3_20', 'r0_20',
                                 'r1_20', 'r2_20', 'r3_20', 's3_r0_20', 's3_r1_20', 's3_r2_20', 's3_r3_20', 'sv3_r0_20',
                                 'sv3_r1_20', 'sv3_r2_20', 'sv3_r3_20', 'sd3_r0_css0_20', 'sd3_r1_ccs0_20',
                                 'sd3_r2_ccs0_20', 'sd3_r3_ccs0_20', 'ccs0_20', 's4_ccs0_20', 'sv4_ccs0_20',
                                 'sv5_mcc_20', \
                                 'sv6_mcc', 'sv7_mcc', 'outcome']

print(len(aaaa))