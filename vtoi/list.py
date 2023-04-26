from ast import literal_eval
import pandas as pd
import numpy
###reading it make it a nested list
with open('file1.txt') as f:
    a = f.read().splitlines()
    #for i in a:
        #print(i)
        #print(type(i))

#print(a)
for i in range(len(a)):

    a[i] = literal_eval(a[i])

#print(a)
#print(type(a[i]))

vals= []
for i in a:
    vals.append(i)


print(vals)
print(len(vals))

df = pd.DataFrame(vals, columns=['v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v13',\
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
                                 'sv6_mcc', 'sv7_mcc', 'outcome'])

# OR1, OR1_1, OR1_2, OR1_3, OR1_4, OR1_5, OR1_6, OR1_7
# OR2, OR2_1, OR2_2, OR2_3, OR2_4, OR2_5, OR2_6, OR2_7
# OR3, OR3_1, OR3_2, OR3_3, OR3_4, OR3_5, OR3_6, OR3_7
# OR4, OR4_1, OR4_2, OR4_3, OR4_4, OR4_5, OR4_6, OR4_7    #32

# OR5 to OR24   #20

# OR1_sv6, OR1_sv6_1, OR1_sv6_2 (3)
# to OR20_SV6 (X3)
# 60

# OR25, OR26, OR27, OR28, OR29

# OR30, OR 31

# OR32
# AND1 node
# 9
# 32+20+60+9+709 = 830


#subset = df.loc[df.col1 == 0] #subset for values equal to one in the col1
print(len(df))
print(df)


###########use this python script
#df.to_csv('file_name.csv', index=False,header=False)

tfile = open('test1.csv', 'a+')
tfile.write(df.to_csv(index=False, sep='\t')+"\n")
#
#tfile.write(df.to_string(index=False, sep='\t')+"\n")
#
#tfile.write(df.to_string(index=False, header=None)+"\n")
tfile.close()




"""
'v4', 'v5', 'v6', 'v7', 'v8', 'v9','v10', 'v11', 'v12', 'v13', 'v14', 'v15', 'v16', 'v17', 'v18', 'v19', \
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



'ccs0_1', 's2_ccs0_1', 'sv2_ccs0_1', 'sd2_ccs0_r0_1', 'sd2_ccs0_r1_1', 'sd2_ccs0_r2_1', 'sd2_ccs0_r3_1',
'r0_1', 'r1_1', 'r2_1', 'r3_1', 's3_r0_1', 's3_r1_1', 's3_r2_1', 's3_r3_1', 'sv3_r0_1', 'sv3_r1_1', 'sv3_r2_1', 'sv3_r3_1', \
'sd3_r0_css0_1', 'sd3_r1_ccs0_1', 'sd3_r2_ccs0_1', 'sd3_r3_ccs0_1', 's4_ccs0_1', 'sv4_ccs0_1', 'sv5_mcc_1',\






'sd2_ccs0_r0_2', 'sd2_ccs0_r1_2', 'sd2_ccs0_r2_2', 'sd2_ccs0_r3_2',

                                 'r0_2', 'r1_2', 'r2_2', 'r3_2',

                                 's3_r0_2', 's3_r1_2', 's3_r2_2', 's3_r3_2',


                                 'sv3_r0_2', 'sv3_r1_2', 'sv3_r2_2', 'sv3_r3_2',

                                 'sd3_r0_css0_2', 'sd3_r1_ccs0_2', 'sd3_r2_ccs0_2', 'sd3_r3_ccs0_2',

                                 'ccs0_2', 's4_ccs0_2', 'sv4_ccs0_2', 'sv5_mcc_2',\



'sd2_ccs0_r0_3', 'sd2_ccs0_r1_3', 'sd2_ccs0_r2_3', 'sd2_ccs0_r3_3', 'r0_3', 'r1_3', 'r2_3', 'r3_3', 's3_r0_3', 's3_r1_3', 's3_r2_3', 's3_r3_3', 'sv3_r0_3', 'sv3_r1_3', 'sv3_r2_3', 'sv3_r3_3', 'sd3_r0_css0_3', 'sd3_r1_ccs0_3', 'sd3_r2_ccs0_3', 'sd3_r3_ccs0_3', 'ccs0_3', 's4_ccs0_3', 'sv4_ccs0_3', 'sv5_mcc_3',\

'sd2_ccs0_r0_4', 'sd2_ccs0_r1_4', 'sd2_ccs0_r2_4', 'sd2_ccs0_r3_4', 'r0_4', 'r1_4', 'r2_4', 'r3_4', 's3_r0_4', 's3_r1_4', 's3_r2_4', 's3_r3_4', 'sv3_r0_4', 'sv3_r1_4', 'sv3_r2_4', 'sv3_r3_4', 'sd3_r0_css0_4', 'sd3_r1_ccs0_4', 'sd3_r2_ccs0_4', 'sd3_r3_ccs0_4', 'ccs0_4', 's4_ccs0_4', 'sv4_ccs0_4', 'sv5_mcc_4',\

'sd2_ccs0_r0_5', 'sd2_ccs0_r1_5', 'sd2_ccs0_r2_5', 'sd2_ccs0_r3_5', 'r0_5', 'r1_5', 'r2_5', 'r3_5', 's3_r0_5', 's3_r1_5', 's3_r2_5', 's3_r3_5', 'sv3_r0_5', 'sv3_r1_5', 'sv3_r2_5', 'sv3_r3_5', 'sd3_r0_css0_5', 'sd3_r1_ccs0_5', 'sd3_r2_ccs0_5', 'sd3_r3_ccs0_5', 'ccs0_5', 's4_ccs0_5', 'sv4_ccs0_5', 'sv5_mcc_5',\

'sd2_ccs0_r0_6', 'sd2_ccs0_r1_6', 'sd2_ccs0_r2_6', 'sd2_ccs0_r3_6', 'r0_6', 'r1_6', 'r2_6', 'r3_6', 's3_r0_6', 's3_r1_6', 's3_r2_6', 's3_r3_6', 'sv3_r0_6', 'sv3_r1_6', 'sv3_r2_6', 'sv3_r3_6', 'sd3_r0_css0_6', 'sd3_r1_ccs0_6', 'sd3_r2_ccs0_6', 'sd3_r3_ccs0_6', 'ccs0_6', 's4_ccs0_6', 'sv4_ccs0_6', 'sv5_mcc_6',\

'sd2_ccs0_r0_7', 'sd2_ccs0_r1_7', 'sd2_ccs0_r2_7', 'sd2_ccs0_r3_7', 'r0_7', 'r1_7', 'r2_7', 'r3_7', 's3_r0_7', 's3_r1_7', 's3_r2_7', 's3_r3_7', 'sv3_r0_7', 'sv3_r1_7', 'sv3_r2_7', 'sv3_r3_7', 'sd3_r0_css0_7', 'sd3_r1_ccs0_7', 'sd3_r2_ccs0_7', 'sd3_r3_ccs0_7', 'ccs0_7', 's4_ccs0_7', 'sv4_ccs0_7', 'sv5_mcc_7',\

'sd2_ccs0_r0_8', 'sd2_ccs0_r1_8ß', 'sd2_ccs0_r2_8', 'sd2_ccs0_r3_8', 'r0_8', 'r1_8', 'r2_8', 'r3_8', 's3_r0_8', 's3_r1_8', 's3_r2_8', 's3_r3_8', 'sv3_r0_8', 'sv3_r1_8', 'sv3_r2_8', 'sv3_r3_8', 'sd3_r0_css0_8', 'sd3_r1_ccs0_8', 'sd3_r2_ccs0_8', 'sd3_r3_ccs0_8', 'ccs0_8', 's4_ccs0_8', 'sv4_ccs0_8', 'sv5_mcc_8',\

'sd2_ccs0_r0_9', 'sd2_ccs0_r1_9', 'sd2_ccs0_r2_9', 'sd2_ccs0_r3_9', 'r0_9', 'r1_9', 'r2_9', 'r3_9', 's3_r0_9', 's3_r1_9', 's3_r2_9', 's3_r3_9', 'sv3_r0_9', 'sv3_r1_9', 'sv3_r2_9', 'sv3_r3_9', 'sd3_r0_css0_9', 'sd3_r1_ccs0_9', 'sd3_r2_ccs0_9', 'sd3_r3_ccs0_9', 'ccs0_9', 's4_ccs0_9', 'sv4_ccs0_9', 'sv5_mcc_9',\

'sd2_ccs0_r0_10', 'sd2_ccs0_r1_10', 'sd2_ccs0_r2_10', 'sd2_ccs0_r3_10', 'r0_10', 'r1_10', 'r2_10', 'r3_10', 's3_r0_10', 's3_r1_10', 's3_r2_10', 's3_r3_10', 'sv3_r0_10', 'sv3_r1_10', 'sv3_r2_10', 'sv3_r3_10', 'sd3_r0_css0_10', 'sd3_r1_ccs0_10', 'sd3_r2_ccs0_10', 'sd3_r3_ccs0_10', 'ccs0_10', 's4_ccs0_10', 'sv4_ccs0_10', 'sv5_mcc_10',\

'sd2_ccs0_r0_11', 'sd2_ccs0_r1_11', 'sd2_ccs0_r2_11', 'sd2_ccs0_r3_11', 'r0_11', 'r1_11', 'r2_11', 'r3_11', 's3_r0_11', 's3_r1_11', 's3_r2_11', 's3_r3_11', 'sv3_r0_11', 'sv3_r1_11', 'sv3_r2_11', 'sv3_r3_11', 'sd3_r0_css0_11', 'sd3_r1_ccs0_11', 'sd3_r2_ccs0_11', 'sd3_r3_ccs0_11', 'ccs0_11', 's4_ccs0_11', 'sv4_ccs0_11', 'sv5_mcc_11',\

'sd2_ccs0_r0_12', 'sd2_ccs0_r1_12', 'sd2_ccs0_r2_12', 'sd2_ccs0_r3_12', 'r0_12', 'r1_12', 'r2_12', 'r3_12', 's3_r0_12', 's3_r1_12', 's3_r2_12', 's3_r3_12', 'sv3_r0_12', 'sv3_r1_12', 'sv3_r2_12', 'sv3_r3_12', 'sd3_r0_css0_12', 'sd3_r1_ccs0_12', 'sd3_r2_ccs0_12', 'sd3_r3_ccs0_12', 'ccs0_12', 's4_ccs0_12', 'sv4_ccs0_12', 'sv5_mcc_12',\

'sd2_ccs0_r0_13', 'sd2_ccs0_r1_13', 'sd2_ccs0_r2_13', 'sd2_ccs0_r3_13', 'r0_13', 'r1_13', 'r2_13', 'r3_13', 's3_r0_13', 's3_r1_13', 's3_r2_13', 's3_r3_13', 'sv3_r0_13', 'sv3_r1_13', 'sv3_r2_13', 'sv3_r3_13', 'sd3_r0_css0_13', 'sd3_r1_ccs0_13', 'sd3_r2_ccs0_13', 'sd3_r3_ccs0_13', 'ccs0_13', 's4_ccs0_13', 'sv4_ccs0_13', 'sv5_mcc_13',\

'sd2_ccs0_r0_14', 'sd2_ccs0_r1_14', 'sd2_ccs0_r2_14', 'sd2_ccs0_r3_14', 'r0_14', 'r1_14', 'r2_14', 'r3_14', 's3_r0_14', 's3_r1_14', 's3_r2_14', 's3_r3_14', 'sv3_r0_14', 'sv3_r1_14', 'sv3_r2_14', 'sv3_r3_14', 'sd3_r0_css0_14', 'sd3_r1_ccs0_14', 'sd3_r2_ccs0_14', 'sd3_r3_ccs0_14', 'ccs0_14', 's4_ccs0_14', 'sv4_ccs0_14', 'sv5_mcc_14',\

'sd2_ccs0_r0_15', 'sd2_ccs0_r1_15', 'sd2_ccs0_r2_15', 'sd2_ccs0_r3_15', 'r0_15', 'r1_15', 'r2_15', 'r3_15', 's3_r0_15', 's3_r1_15', 's3_r2_15', 's3_r3_15', 'sv3_r0_15', 'sv3_r1_15', 'sv3_r2_15', 'sv3_r3_15', 'sd3_r0_css0_15', 'sd3_r1_ccs0_15', 'sd3_r2_ccs0_15', 'sd3_r3_ccs0_15', 'ccs0_15', 's4_ccs0_15', 'sv4_ccs0_15', 'sv5_mcc_15',\

'sd2_ccs0_r0_16', 'sd2_ccs0_r1_16', 'sd2_ccs0_r2_16', 'sd2_ccs0_r3_16', 'r0_16', 'r1_16', 'r2_16', 'r3_16', 's3_r0_16', 's3_r1_16', 's3_r2_16', 's3_r3_16', 'sv3_r0_16', 'sv3_r1_16', 'sv3_r2_16', 'sv3_r3_16', 'sd3_r0_css0_16', 'sd3_r1_ccs0_16', 'sd3_r2_ccs0_16', 'sd3_r3_ccs0_16', 'ccs0_16', 's4_ccs0_16', 'sv4_ccs0_16', 'sv5_mcc_16',\

'sd2_ccs0_r0_17', 'sd2_ccs0_r1_17', 'sd2_ccs0_r2_17', 'sd2_ccs0_r3_17', 'r0_17', 'r1_17', 'r2_17', 'r3_17', 's3_r0_17', 's3_r1_17', 's3_r2_17', 's3_r3_17', 'sv3_r0_17', 'sv3_r1_17', 'sv3_r2_17', 'sv3_r3_17', 'sd3_r0_css0_17', 'sd3_r1_ccs0_17', 'sd3_r2_ccs0_17', 'sd3_r3_ccs0_17', 'ccs0_17', 's4_ccs0_17', 'sv4_ccs0_17', 'sv5_mcc_17',\

'sd2_ccs0_r0_18', 'sd2_ccs0_r1_18', 'sd2_ccs0_r2_18', 'sd2_ccs0_r3_18', 'r0_18', 'r1_18', 'r2_18', 'r3_18', 's3_r0_18', 's3_r1_18', 's3_r2_18', 's3_r3_18', 'sv3_r0_18', 'sv3_r1_18', 'sv3_r2_18', 'sv3_r3_18', 'sd3_r0_css0_18', 'sd3_r1_ccs0_18', 'sd3_r2_ccs0_18', 'sd3_r3_ccs0_18', 'ccs0_18', 's4_ccs0_18', 'sv4_ccs0_18', 'sv5_mcc_18',\

'sd2_ccs0_r0_19', 'sd2_ccs0_r1_19', 'sd2_ccs0_r2_19', 'sd2_ccs0_r3_19', 'r0_19', 'r1_19', 'r2_19', 'r3_19', 's3_r0_19', 's3_r1_19', 's3_r2_19', 's3_r3_19', 'sv3_r0_19', 'sv3_r1_19', 'sv3_r2_19', 'sv3_r3_19', 'sd3_r0_css0_19', 'sd3_r1_ccs0_19', 'sd3_r2_ccs0_19', 'sd3_r3_ccs0_19', 'ccs0_19', 's4_ccs0_19', 'sv4_ccs0_19', 'sv5_mcc_19',\

'sd2_ccs0_r0_20', 'sd2_ccs0_r1_20', 'sd2_ccs0_r2_20', 'sd2_ccs0_r3_20', 'r0_20', 'r1_20', 'r2_20', 'r3_20', 's3_r0_20', 's3_r1_20', 's3_r2_20', 's3_r3_20', 'sv3_r0_20', 'sv3_r1_20', 'sv3_r2_20', 'sv3_r3_20', 'sd3_r0_css0_20', 'sd3_r1_ccs0_20', 'sd3_r2_ccs0_20', 'sd3_r3_ccs0_20', 'ccs0_20', 's4_ccs0_20', 'sv4_ccs0_20', 'sv5_mcc_20',\
                                 'sv6_mcc', 'sv7_mcc', 'outcome'])



"""
########################################################
#below is not needed
"""
import random
a = []
for i in range(453):
    if random.random() < 0.5:
        a.append('true')
    else:
        a.append('false')

print(a)
print(len(a))
"""





"""
a = ['v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9','v10', 'v11', 'v12', 'v13', 'v14', 'v15', 'v16', 'v17', 'v18', 'v19', \
'v20', 'v21', 'v22', 'v23', 'v24', 'v25', 'v26', 'v27', 'v28', 'v29','v30', 'v31', 'v32', 'v33', 'v34', 'v35', 'v36', 'v37', 'v38', 'v39',\
'v40', 'v41', 'v42', 'v43', 'v44', 'v45', 'v46', 'v47', 'v48', 'v49','v50', 'v51', 'v52', 'v53', 'v54', 'v55',\
'sd10', 'sd11', 'sd12', 'sd13', 'sd14', 'sd15', 'sd16', 'sd17', 'sd18','sd19', 'sd110', 'sd111', 'sd112', 'sd113', 'sd114', 'sd115', 'sd116',\
'sd117','sd118', 'sd119', 'sd120', 'sd121', 'sd122', 'sd123', 'sd124', 'sd125', 'sd126', 'sd127', 'sd128', 'sd129', 'sd130', 'sd131', 'sd132', 'sd133','sd134', 'sd135', 'sd136',\
'sd137', 'sd138', 'sd139', 'sd140', 'sd141', 'sd142', 'sd143', 'sd144', 'sd145','sd146', 'sd147', 'sd 148', 'sd149', 'sd150', 'sd151', 'sd152', 'sd153', 'sd154', 'sd155',\
'r10', 'rs10', 'rsv10', 'rsd10', 'r11', 'rs11', 'rsv11', 'rsd11','r12', 'rs12', 'rsv12','rsd12', 'r13', 'rs13', 'rsv13', 'rsd13',"ccs1", "ccss1", "ccssv1",\
"ccs2sdr0", "ccs2sdr1", "ccs2sdr2", "ccs2sdr3", 'r20', 'rs20', 'rsv20', 'rsd20', 'r21', 'rs21', 'rsv21', 'rsd21','r22', 'rs22', 'rsv22','rsd22', 'r23', 'rs23', 'rsv23', 'rsd23',"ccs2", "ccss2", "ccssv2",\
"ccs3sdr0", "ccs3sdr1", "ccs3sdr2", "ccs3sdr3", 'r30', 'rs30', 'rsv30', 'rsd30', 'r31', 'rs31', 'rsv31', 'rsd31','r32', 'rs32', 'rsv32','rsd32', 'r33', 'rs33', 'rsv33', 'rsd33',"ccs3", "ccss3", "ccssv3",\
"ccs4sdr0", "ccs4sdr1", "ccs4sdr2", "ccs4sdr3", 'r40', 'rs40', 'rsv40', 'rsd40', 'r41', 'rs41', 'rsv41', 'rsd41','r42', 'rs42', 'rsv42','rsd42', 'r43', 'rs43', 'rsv43', 'rsd43',"ccs4", "ccss4", "ccssv4",\
"ccs5sdr0", "ccs5sdr1", "ccs5sdr2", "ccs5sdr3", 'r50', 'rs50', 'rsv50', 'rsd50', 'r51', 'rs51', 'rsv51', 'rsd51','r52', 'rs52', 'rsv52','rsd52', 'r53', 'rs53', 'rsv53', 'rsd53',"ccs5", "ccss5", "ccssv5",\
"ccs6sdr0", "ccs6sdr1", "ccs6sdr2", "ccs6sdr3", 'r60', 'rs60', 'rsv60', 'rsd60', 'r61', 'rs61', 'rsv61', 'rsd61','r62', 'rs62', 'rsv62','rsd62', 'r63', 'rs63', 'rsv63', 'rsd63',"ccs6", "ccss6", "ccssv6",\
"ccs7sdr0", "ccs7sdr1", "ccs7sdr2", "ccs7sdr3", 'r70', 'rs70', 'rsv70', 'rsd70', 'r71', 'rs71', 'rsv71', 'rsd71','r72', 'rs72', 'rsv72','rsd72', 'r73', 'rs73', 'rsv73', 'rsd73',"ccs7", "ccss7", "ccssv7",\
"ccs8sdr0", "ccs8sdr1", "ccs8sdr2", "ccs8sdr3", 'r80', 'rs80', 'rsv80', 'rsd80', 'r81', 'rs81', 'rsv81', 'rsd81','r82', 'rs82', 'rsv82','rsd82', 'r83', 'rs83', 'rsv83', 'rsd83',"ccs8", "ccss8", "ccssv8",\
"ccs9sdr0", "ccs9sdr1", "ccs9sdr2", "ccs9sdr3", 'r90', 'rs90', 'rsv90', 'rsd90', 'r91', 'rs91', 'rsv91', 'rsd91','r92', 'rs92', 'rsv92','rsd92', 'r93', 'rs93', 'rsv93', 'rsd93',"ccs9", "ccss9", "ccssv9",\
"ccs10sdr0", "ccs10sdr1", "ccs10sdr2", "ccs10sdr3", 'r100', 'rs100', 'rsv100', 'rsd100', 'r101', 'rs101', 'rsv101', 'rsd101','r102', 'rs102', 'rsv102','rsd102', 'r103', 'rs103', 'rsv103', 'rsd103',"ccs10", "ccss10", "ccssv10",\
"ccs11sdr0", "ccs11sdr1", "ccs11sdr2", "ccs11sdr3", 'r110', 'rs110', 'rsv110', 'rsd110', 'r111', 'rs111', 'rsv111', 'rsd111','r112', 'rs112', 'rsv112','rsd112', 'r113', 'rs113', 'rsv113', 'rsd113',"ccs11", "ccss11", "ccssv11",\
"ccs12sdr0", "ccs12sdr1", "ccs12sdr2", "ccs12sdr3", 'r120', 'rs120', 'rsv120', 'rsd120', 'r121', 'rs121', 'rsv121', 'rsd121','r122', 'rs122', 'rsv122','rsd122', 'r123', 'rs123', 'rsv123', 'rsd123',"ccs12", "ccss12", "ccssv12",\
"ccs13sdr0", "ccs13sdr1", "ccs13sdr2", "ccs13sdr3", 'r130', 'rs130', 'rsv130', 'rsd130', 'r131', 'rs131', 'rsv131', 'rsd131','r132', 'rs132', 'rsv132','rsd132', 'r133', 'rs133', 'rsv133', 'rsd133',"ccs13", "ccss13", "ccssv13",\
"ccs14sdr0", "ccs14sdr1", "ccs14sdr2", "ccs14sdr3", 'r140', 'rs140', 'rsv140', 'rsd140', 'r141', 'rs141', 'rsv141', 'rsd141','r142', 'rs142', 'rsv142','rsd142', 'r143', 'rs143', 'rsv143', 'rsd143',"ccs14", "ccss14", "ccssv14",\
"ccs15sdr0", "ccs15sdr1", "ccs15sdr2", "ccs15sdr3", 'r150', 'rs150', 'rsv150', 'rsd150', 'r151', 'rs151', 'rsv151', 'rsd151','r152', 'rs152', 'rsv152','rsd152', 'r153', 'rs153', 'rsv153', 'rsd153',"ccs15", "ccss15", "ccssv15"]

print(len(a))
"""

#import pandas as pd

#vals = [['false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true'],['false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true'],['false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true'],['false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true']]
"""
#df = pd.DataFrame(vals, columns=['v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9','v10', 'v11', 'v12', 'v13', 'v14', 'v15', 'v16', 'v17', 'v18', 'v19', \
'v20', 'v21', 'v22', 'v23', 'v24', 'v25', 'v26', 'v27', 'v28', 'v29','v30', 'v31', 'v32', 'v33', 'v34', 'v35', 'v36', 'v37', 'v38', 'v39',\
'v40', 'v41', 'v42', 'v43', 'v44', 'v45', 'v46', 'v47', 'v48', 'v49','v50', 'v51', 'v52', 'v53', 'v54', 'v55',\
'sd10', 'sd11', 'sd12', 'sd13', 'sd14', 'sd15', 'sd16', 'sd17', 'sd18','sd19', 'sd110', 'sd111', 'sd112', 'sd113', 'sd114', 'sd115', 'sd116',\
'sd117','sd118', 'sd119', 'sd120', 'sd121', 'sd122', 'sd123', 'sd124', 'sd125', 'sd126', 'sd127', 'sd128', 'sd129', 'sd130', 'sd131', 'sd132', 'sd133','sd134', 'sd135', 'sd136',\
'sd137', 'sd138', 'sd139', 'sd140', 'sd141', 'sd142', 'sd143', 'sd144', 'sd145','sd146', 'sd147', 'sd 148', 'sd149', 'sd150', 'sd151', 'sd152', 'sd153', 'sd154', 'sd155',\
'r10', 'rs10', 'rsv10', 'rsd10', 'r11', 'rs11', 'rsv11', 'rsd11','r12', 'rs12', 'rsv12','rsd12', 'r13', 'rs13', 'rsv13', 'rsd13',"ccs1", "ccss1", "ccssv1",\
"ccs2sdr0", "ccs2sdr1", "ccs2sdr2", "ccs2sdr3", 'r20', 'rs20', 'rsv20', 'rsd20', 'r21', 'rs21', 'rsv21', 'rsd21','r22', 'rs22', 'rsv22','rsd22', 'r23', 'rs23', 'rsv23', 'rsd23',"ccs2", "ccss2", "ccssv2",\
"ccs3sdr0", "ccs3sdr1", "ccs3sdr2", "ccs3sdr3", 'r30', 'rs30', 'rsv30', 'rsd30', 'r31', 'rs31', 'rsv31', 'rsd31','r32', 'rs32', 'rsv32','rsd32', 'r33', 'rs33', 'rsv33', 'rsd33',"ccs3", "ccss3", "ccssv3",\
"ccs4sdr0", "ccs4sdr1", "ccs4sdr2", "ccs4sdr3", 'r40', 'rs40', 'rsv40', 'rsd40', 'r41', 'rs41', 'rsv41', 'rsd41','r42', 'rs42', 'rsv42','rsd42', 'r43', 'rs43', 'rsv43', 'rsd43',"ccs4", "ccss4", "ccssv4",\
"ccs5sdr0", "ccs5sdr1", "ccs5sdr2", "ccs5sdr3", 'r50', 'rs50', 'rsv50', 'rsd50', 'r51', 'rs51', 'rsv51', 'rsd51','r52', 'rs52', 'rsv52','rsd52', 'r53', 'rs53', 'rsv53', 'rsd53',"ccs5", "ccss5", "ccssv5",\
"ccs6sdr0", "ccs6sdr1", "ccs6sdr2", "ccs6sdr3", 'r60', 'rs60', 'rsv60', 'rsd60', 'r61', 'rs61', 'rsv61', 'rsd61','r62', 'rs62', 'rsv62','rsd62', 'r63', 'rs63', 'rsv63', 'rsd63',"ccs6", "ccss6", "ccssv6",\
"ccs7sdr0", "ccs7sdr1", "ccs7sdr2", "ccs7sdr3", 'r70', 'rs70', 'rsv70', 'rsd70', 'r71', 'rs71', 'rsv71', 'rsd71','r72', 'rs72', 'rsv72','rsd72', 'r73', 'rs73', 'rsv73', 'rsd73',"ccs7", "ccss7", "ccssv7",\
"ccs8sdr0", "ccs8sdr1", "ccs8sdr2", "ccs8sdr3", 'r80', 'rs80', 'rsv80', 'rsd80', 'r81', 'rs81', 'rsv81', 'rsd81','r82', 'rs82', 'rsv82','rsd82', 'r83', 'rs83', 'rsv83', 'rsd83',"ccs8", "ccss8", "ccssv8",\
"ccs9sdr0", "ccs9sdr1", "ccs9sdr2", "ccs9sdr3", 'r90', 'rs90', 'rsv90', 'rsd90', 'r91', 'rs91', 'rsv91', 'rsd91','r92', 'rs92', 'rsv92','rsd92', 'r93', 'rs93', 'rsv93', 'rsd93',"ccs9", "ccss9", "ccssv9",\
"ccs10sdr0", "ccs10sdr1", "ccs10sdr2", "ccs10sdr3", 'r100', 'rs100', 'rsv100', 'rsd100', 'r101', 'rs101', 'rsv101', 'rsd101','r102', 'rs102', 'rsv102','rsd102', 'r103', 'rs103', 'rsv103', 'rsd103',"ccs10", "ccss10", "ccssv10",\
"ccs11sdr0", "ccs11sdr1", "ccs11sdr2", "ccs11sdr3", 'r110', 'rs110', 'rsv110', 'rsd110', 'r111', 'rs111', 'rsv111', 'rsd111','r112', 'rs112', 'rsv112','rsd112', 'r113', 'rs113', 'rsv113', 'rsd113',"ccs11", "ccss11", "ccssv11",\
"ccs12sdr0", "ccs12sdr1", "ccs12sdr2", "ccs12sdr3", 'r120', 'rs120', 'rsv120', 'rsd120', 'r121', 'rs121', 'rsv121', 'rsd121','r122', 'rs122', 'rsv122','rsd122', 'r123', 'rs123', 'rsv123', 'rsd123',"ccs12", "ccss12", "ccssv12",\
"ccs13sdr0", "ccs13sdr1", "ccs13sdr2", "ccs13sdr3", 'r130', 'rs130', 'rsv130', 'rsd130', 'r131', 'rs131', 'rsv131', 'rsd131','r132', 'rs132', 'rsv132','rsd132', 'r133', 'rs133', 'rsv133', 'rsd133',"ccs13", "ccss13", "ccssv13",\
"ccs14sdr0", "ccs14sdr1", "ccs14sdr2", "ccs14sdr3", 'r140', 'rs140', 'rsv140', 'rsd140', 'r141', 'rs141', 'rsv141', 'rsd141','r142', 'rs142', 'rsv142','rsd142', 'r143', 'rs143', 'rsv143', 'rsd143',"ccs14", "ccss14", "ccssv14",\
"ccs15sdr0", "ccs15sdr1", "ccs15sdr2", "ccs15sdr3", 'r150', 'rs150', 'rsv150', 'rsd150', 'r151', 'rs151', 'rsv151', 'rsd151','r152', 'rs152', 'rsv152','rsd152', 'r153', 'rs153', 'rsv153', 'rsd153',"ccs15", "ccss15", "ccssv15"])
"""
#subset = df.loc[df.col1 == 0] #subset for values equal to one in the col1
#print(len(df))
#print(df)

#df.to_csv('file_name.csv', index=False,header=False)

#tfile = open('test.txt', 'a+')

#tfile.write(df.to_string(index=False)+"\n")

#tfile.close()

"""
from ast import literal_eval
import numpy

# Creating an array
#List = []
#for i in range(500):
#    List.append('true')


List = ['false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true','false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true']
#Array = numpy.array(List)

# Displaying the array
#print('Array:\n', List)
#print(type(List))
file = open("file1.txt", "a")

# Saving the array in a text file
content = str(List) +'\n'
#print(str(List))
#print(type(str(List)))

file.write(content)

file.close()

"""



"""

import pandas as pd

vals = [['false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true'],['false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true'],['false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true'],['false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true']]

df = pd.DataFrame(vals, columns=['v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9','v10', 'v11', 'v12', 'v13', 'v14', 'v15', 'v16', 'v17', 'v18', 'v19', \
'v20', 'v21', 'v22', 'v23', 'v24', 'v25', 'v26', 'v27', 'v28', 'v29','v30', 'v31', 'v32', 'v33', 'v34', 'v35', 'v36', 'v37', 'v38', 'v39',\
'v40', 'v41', 'v42', 'v43', 'v44', 'v45', 'v46', 'v47', 'v48', 'v49','v50', 'v51', 'v52', 'v53', 'v54', 'v55',\ 

s1_0, s1_1, s1_2, s1_3,s1_4, s1_5, s1_6, s1_7, s1_8, s1_9, s1_10, s1_11, s1_12, s1_13, s1_14, s1_15, s1_16,\
s1_17, s1_18, s1_19, s1_20,s1_21, s1_22, s1_23, s1_24, s1_25, s1_26, s1_27, s1_28, s1_29, s1_30, s1_31, s1_32, s1_33,\
s1_34, s1_35, s1_36, s1_37,s1_38, s1_39, s1_40, s1_41, s1_42, s1_43, s1_44, s1_45, s1_46, s1_47, s1_48, s1_49, s1_50,\
s1_51, s1_52, s1_53, s1_54, s1_55,\

svt1_0, svt1_1, svt1_2, svt1_3,svt1_4, svt1_5, svt1_6, svt1_7, svt1_8, svt1_9, svt1_10, svt1_11, svt1_12, svt1_13, svt1_14, svt1_15, svt1_16,\
svt1_17, svt1_18, svt1_19, svt1_20, svt1_21, svt1_22, svt1_23, svt1_24, svt1_25, svt1_26, svt1_27, svt1_28, svt1_29, svt1_30, svt1_31, svt1_32, svt1_33,\
svt1_34, svt1_35, svt1_36, svt1_37,svt1_38, svt1_39, svt1_40, svt1_41, svt1_42, svt1_43, svt1_44, svt1_45, svt1_46, svt1_47, svt1_48, svt1_49, svt1_50,\
svt1_51, svt1_52, svt1_53, svt1_54, svt1_55,\


sdt1_0, sdt1_1, sdt1_2, sdt1_3, sdt1_4, sdt1_5, sdt1_6, sdt1_7, sdt1_8, sdt1_9, sdt1_10, sdt1_11, sdt1_12, sdt1_13, sdt1_14, sdt1_15, sdt1_16,\
sdt1_17, sdt1_18, sdt1_19, sdt1_20, sdt1_21, sdt1_22, sdt1_23, sdt1_24, sdt1_25, sdt1_26, sdt1_27, sdt1_28, sdt1_29, sdt1_30, sdt1_31, sdt1_32, sdt1_33,\
sdt1_34, sdt1_35, sdt1_36, sdt1_37, sdt1_38, sdt1_39, sdt1_40, sdt1_41, sdt1_42, sdt1_43, sdt1_44, sdt1_45, sdt1_46, sdt1_47, sdt1_48, sdt1_49, sdt1_50,\
sdt1_51, sdt1_52, sdt1_53, sdt1_54, sdt1_55,\












r0_1, r1_1, r2_1, r3_1,\            #done

s2_r0_1, s2_r1_1, s2_r2_1, s2_r3_1,\    #done

svt2_r0_1, svt2_r1_1, svt2_r2_1, svt2_r3_1,\    #done

sdt2_r0_css0_1, sdt2_r1_ccs0_1, sdt2_r2_ccs0_1, sdt2_r3_ccs0_1,\ #done

ccs0_1,\ #done

s3_ccs0_1,\ #done

svt3_ccs0_1,\ #done

sdt3_ccs0_r0_2, sdt3_ccs0_r1_2, sdt3_ccs0_r2_2, sdt3_ccs0_r3_2, #done










r0_2, r1_2, r2_2, r3_2, s2_r0_2, s2_r1_2, s2_r2_2, s2_r3_2, svt2_r0_2, svt2_r1_2, svt2_r2_2, svt2_r3_2, sdt2_r0_css0_2, sdt2_r1_ccs0_2, sdt2_r2_ccs0_2, sdt2_r3_ccs0_2, ccs0_2, s3_ccs0_2, svt3_ccs0_2,\ 
sdt3_ccs0_r0_3, sdt3_ccs0_r1_3, sdt3_ccs0_r2_3, sdt3_ccs0_r3_3, 

r0_3, r1_3, r2_3, r3_3, s2_r0_3, s2_r1_3, s2_r2_3, s2_r3_3, svt2_r0_3, svt2_r1_3, svt2_r2_3, svt2_r3_3, sdt2_r0_css0_3, sdt2_r1_ccs0_3, sdt2_r2_ccs0_3, sdt2_r3_ccs0_3, ccs0_3, s3_ccs0_3, svt3_ccs0_3,\
sdt3_ccs0_r0_4, sdt3_ccs0_r1_4, sdt3_ccs0_r2_4, sdt3_ccs0_r3_4, 

r0_4, r1_4, r2_4, r3_4, s2_r0_4, s2_r1_4, s2_r2_4, s2_r3_4, svt2_r0_4, svt2_r1_4, svt2_r2_4, svt2_r3_4, sdt2_r0_css0_4, sdt2_r1_ccs0_4, sdt2_r2_ccs0_4, sdt2_r3_ccs0_4, ccs0_4, s3_ccs0_4, svt3_ccs0_4,\
sdt3_ccs0_r0_5, sdt3_ccs0_r1_5, sdt3_ccs0_r2_5, sdt3_ccs0_r3_5, 

r0_5, r1_5, r2_5, r3_5, s2_r0_5, s2_r1_5, s2_r2_5, s2_r3_5, svt2_r0_5, svt2_r1_5, svt2_r2_5, svt2_r3_5, sdt2_r0_css0_5, sdt2_r1_ccs0_5, sdt2_r2_ccs0_5, sdt2_r3_ccs0_5, ccs0_5, s3_ccs0_5, svt3_ccs0_5,\
sdt3_ccs0_r0_6, sdt3_ccs0_r1_6, sdt3_ccs0_r2_6, sdt3_ccs0_r3_6, 

r0_6, r1_6, r2_6, r3_6, s2_r0_6, s2_r1_6, s2_r2_6, s2_r3_6, svt2_r0_6, svt2_r1_6, svt2_r2_6, svt2_r3_6, sdt2_r0_css0_6, sdt2_r1_ccs0_6, sdt2_r2_ccs0_6, sdt2_r3_ccs0_6, ccs0_6, s3_ccs0_6, svt3_ccs0_6,\
sdt3_ccs0_r0_7, sdt3_ccs0_r1_7, sdt3_ccs0_r2_7, sdt3_ccs0_r3_7, 

r0_7, r1_7, r2_7, r3_7, s2_r0_7, s2_r1_7, s2_r2_7, s2_r3_7, svt2_r0_7, svt2_r1_7, svt2_r2_7, svt2_r3_7, sdt2_r0_css0_7, sdt2_r1_ccs0_7, sdt2_r2_ccs0_7, sdt2_r3_ccs0_7, ccs0_7, s3_ccs0_7, svt3_ccs0_7,\
sdt3_ccs0_r0_8, sdt3_ccs0_r1_8, sdt3_ccs0_r2_8, sdt3_ccs0_r3_8, 

r0_8, r1_8, r2_8, r3_8, s2_r0_8, s2_r1_8, s2_r2_8, s2_r3_8, svt2_r0_8, svt2_r1_8, svt2_r2_8, svt2_r3_8, sdt2_r0_css0_8, sdt2_r1_ccs0_8, sdt2_r2_ccs0_8, sdt2_r3_ccs0_8, ccs0_8, s3_ccs0_8, svt3_ccs0_8,\
sdt3_ccs0_r0_9, sdt3_ccs0_r1_9, sdt3_ccs0_r2_9, sdt3_ccs0_r3_9, 

r0_9, r1_9, r2_9, r3_9, s2_r0_9, s2_r1_9, s2_r2_9, s2_r3_9, svt2_r0_9, svt2_r1_9, svt2_r2_9, svt2_r3_9, sdt2_r0_css0_9, sdt2_r1_ccs0_9, sdt2_r2_ccs0_9, sdt2_r3_ccs0_9, ccs0_9, s3_ccs0_9, svt3_ccs0_9,\
sdt3_ccs0_r0_10, sdt3_ccs0_r1_10, sdt3_ccs0_r2_10, sdt3_ccs0_r3_10, 

r0_10, r1_10, r2_10, r3_10, s2_r0_10, s2_r1_10, s2_r2_10, s2_r3_10, svt2_r0_10, svt2_r1_10, svt2_r2_10, svt2_r3_10, sdt2_r0_css0_10, sdt2_r1_ccs0_10, sdt2_r2_ccs0_10, sdt2_r3_ccs0_10, ccs0_10, s3_ccs0_10, svt3_ccs0_10,\
sdt3_ccs0_r0_11, sdt3_ccs0_r1_11, sdt3_ccs0_r2_11, sdt3_ccs0_r3_11, 

r0_11, r1_11, r2_11, r3_11, s2_r0_11, s2_r1_11, s2_r2_11, s2_r3_11, svt2_r0_11, svt2_r1_11, svt2_r2_11, svt2_r3_11, sdt2_r0_css0_11, sdt2_r1_ccs0_11, sdt2_r2_ccs0_11, sdt2_r3_ccs0_11, ccs0_11, s3_ccs0_11, svt3_ccs0_11,\
sdt3_ccs0_r0_12, sdt3_ccs0_r1_12, sdt3_ccs0_r2_12, sdt3_ccs0_r3_12, 

r0_12, r1_12, r2_12, r3_12, s2_r0_12, s2_r1_12, s2_r2_12, s2_r3_12, svt2_r0_12, svt2_r1_12, svt2_r2_12, svt2_r3_12, sdt2_r0_css0_12, sdt2_r1_ccs0_12, sdt2_r2_ccs0_12, sdt2_r3_ccs0_12, ccs0_12, s3_ccs0_12, svt3_ccs0_12,\
sdt3_ccs0_r0_13, sdt3_ccs0_r1_13, sdt3_ccs0_r2_13, sdt3_ccs0_r3_13, 

r0_13, r1_13, r2_13, r3_13, s2_r0_13, s2_r1_13, s2_r2_13, s2_r3_13, svt2_r0_13, svt2_r1_13, svt2_r2_13, svt2_r3_13, sdt2_r0_css0_13, sdt2_r1_ccs0_13, sdt2_r2_ccs0_13, sdt2_r3_ccs0_13, ccs0_13, s3_ccs0_13, svt3_ccs0_13,\
sdt3_ccs0_r0_14, sdt3_ccs0_r1_14, sdt3_ccs0_r2_14, sdt3_ccs0_r3_14, 

r0_14, r1_14, r2_14, r3_14, s2_r0_14, s2_r1_14, s2_r2_14, s2_r3_14, svt2_r0_14, svt2_r1_14, svt2_r2_14, svt2_r3_14, sdt2_r0_css0_14, sdt2_r1_ccs0_14, sdt2_r2_ccs0_14, sdt2_r3_ccs0_14, ccs0_14, s3_ccs0_14, svt3_ccs0_14,\
sdt3_ccs0_r0_15, sdt3_ccs0_r1_15, sdt3_ccs0_r2_15, sdt3_ccs0_r3_15, 

r0_15, r1_15, r2_15, r3_15, s2_r0_15, s2_r1_15, s2_r2_15, s2_r3_15, svt2_r0_15, svt2_r1_15, svt2_r2_15, svt2_r3_15, sdt2_r0_css0_15, sdt2_r1_ccs0_15, sdt2_r2_ccs0_15, sdt2_r3_ccs0_15, ccs0_15, s3_ccs0_15, svt3_ccs0_15,\

])

#subset = df.loc[df.col1 == 0] #subset for values equal to one in the col1
print(len(df))
print(df)

#df.to_csv('file_name.csv', index=False,header=False)

tfile = open('test.txt', 'a+')

tfile.write(df.to_string(index=False, header=False)+"\n")
tfile.close()
"""

a = ['true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true']

#print(len(a))



bb= ['v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9','v10', 'v11', 'v12', 'v13', 'v14', 'v15', 'v16', 'v17', 'v18', 'v19', \
'v20', 'v21', 'v22', 'v23', 'v24', 'v25', 'v26', 'v27', 'v28', 'v29','v30', 'v31', 'v32', 'v33', 'v34', 'v35', 'v36', 'v37', 'v38', 'v39',\
'v40', 'v41', 'v42', 'v43', 'v44', 'v45', 'v46', 'v47', 'v48', 'v49','v50', 'v51', 'v52', 'v53', 'v54', 'v55',\
'sd10', 'sd11', 'sd12', 'sd13', 'sd14', 'sd15', 'sd16', 'sd17', 'sd18','sd19', 'sd110', 'sd111', 'sd112', 'sd113', 'sd114', 'sd115', 'sd116',\
'sd117','sd118', 'sd119', 'sd120', 'sd121', 'sd122', 'sd123', 'sd124', 'sd125', 'sd126', 'sd127', 'sd128', 'sd129', 'sd130', 'sd131', 'sd132', 'sd133','sd134', 'sd135', 'sd136',\
'sd137', 'sd138', 'sd139', 'sd140', 'sd141', 'sd142', 'sd143', 'sd144', 'sd145','sd146', 'sd147', 'sd 148', 'sd149', 'sd150', 'sd151', 'sd152', 'sd153', 'sd154', 'sd155',\
'r10', 'rs10', 'rsv10', 'rsd10', 'r11', 'rs11', 'rsv11', 'rsd11','r12', 'rs12', 'rsv12','rsd12', 'r13', 'rs13', 'rsv13', 'rsd13',"ccs1", "ccss1", "ccssv1",\
"ccs2sdr0", "ccs2sdr1", "ccs2sdr2", "ccs2sdr3", 'r20', 'rs20', 'rsv20', 'rsd20', 'r21', 'rs21', 'rsv21', 'rsd21','r22', 'rs22', 'rsv22','rsd22', 'r23', 'rs23', 'rsv23', 'rsd23',"ccs2", "ccss2", "ccssv2",\
"ccs3sdr0", "ccs3sdr1", "ccs3sdr2", "ccs3sdr3", 'r30', 'rs30', 'rsv30', 'rsd30', 'r31', 'rs31', 'rsv31', 'rsd31','r32', 'rs32', 'rsv32','rsd32', 'r33', 'rs33', 'rsv33', 'rsd33',"ccs3", "ccss3", "ccssv3",\
"ccs4sdr0", "ccs4sdr1", "ccs4sdr2", "ccs4sdr3", 'r40', 'rs40', 'rsv40', 'rsd40', 'r41', 'rs41', 'rsv41', 'rsd41','r42', 'rs42', 'rsv42','rsd42', 'r43', 'rs43', 'rsv43', 'rsd43',"ccs4", "ccss4", "ccssv4",\
"ccs5sdr0", "ccs5sdr1", "ccs5sdr2", "ccs5sdr3", 'r50', 'rs50', 'rsv50', 'rsd50', 'r51', 'rs51', 'rsv51', 'rsd51','r52', 'rs52', 'rsv52','rsd52', 'r53', 'rs53', 'rsv53', 'rsd53',"ccs5", "ccss5", "ccssv5",\
"ccs6sdr0", "ccs6sdr1", "ccs6sdr2", "ccs6sdr3", 'r60', 'rs60', 'rsv60', 'rsd60', 'r61', 'rs61', 'rsv61', 'rsd61','r62', 'rs62', 'rsv62','rsd62', 'r63', 'rs63', 'rsv63', 'rsd63',"ccs6", "ccss6", "ccssv6",\
"ccs7sdr0", "ccs7sdr1", "ccs7sdr2", "ccs7sdr3", 'r70', 'rs70', 'rsv70', 'rsd70', 'r71', 'rs71', 'rsv71', 'rsd71','r72', 'rs72', 'rsv72','rsd72', 'r73', 'rs73', 'rsv73', 'rsd73',"ccs7", "ccss7", "ccssv7",\
"ccs8sdr0", "ccs8sdr1", "ccs8sdr2", "ccs8sdr3", 'r80', 'rs80', 'rsv80', 'rsd80', 'r81', 'rs81', 'rsv81', 'rsd81','r82', 'rs82', 'rsv82','rsd82', 'r83', 'rs83', 'rsv83', 'rsd83',"ccs8", "ccss8", "ccssv8",\
"ccs9sdr0", "ccs9sdr1", "ccs9sdr2", "ccs9sdr3", 'r90', 'rs90', 'rsv90', 'rsd90', 'r91', 'rs91', 'rsv91', 'rsd91','r92', 'rs92', 'rsv92','rsd92', 'r93', 'rs93', 'rsv93', 'rsd93',"ccs9", "ccss9", "ccssv9",\
"ccs10sdr0", "ccs10sdr1", "ccs10sdr2", "ccs10sdr3", 'r100', 'rs100', 'rsv100', 'rsd100', 'r101', 'rs101', 'rsv101', 'rsd101','r102', 'rs102', 'rsv102','rsd102', 'r103', 'rs103', 'rsv103', 'rsd103',"ccs10", "ccss10", "ccssv10",\
"ccs11sdr0", "ccs11sdr1", "ccs11sdr2", "ccs11sdr3", 'r110', 'rs110', 'rsv110', 'rsd110', 'r111', 'rs111', 'rsv111', 'rsd111','r112', 'rs112', 'rsv112','rsd112', 'r113', 'rs113', 'rsv113', 'rsd113',"ccs11", "ccss11", "ccssv11",\
"ccs12sdr0", "ccs12sdr1", "ccs12sdr2", "ccs12sdr3", 'r120', 'rs120', 'rsv120', 'rsd120', 'r121', 'rs121', 'rsv121', 'rsd121','r122', 'rs122', 'rsv122','rsd122', 'r123', 'rs123', 'rsv123', 'rsd123',"ccs12", "ccss12", "ccssv12",\
"ccs13sdr0", "ccs13sdr1", "ccs13sdr2", "ccs13sdr3", 'r130', 'rs130', 'rsv130', 'rsd130', 'r131', 'rs131', 'rsv131', 'rsd131','r132', 'rs132', 'rsv132','rsd132', 'r133', 'rs133', 'rsv133', 'rsd133',"ccs13", "ccss13", "ccssv13",\
"ccs14sdr0", "ccs14sdr1", "ccs14sdr2", "ccs14sdr3", 'r140', 'rs140', 'rsv140', 'rsd140', 'r141', 'rs141', 'rsv141', 'rsd141','r142', 'rs142', 'rsv142','rsd142', 'r143', 'rs143', 'rsv143', 'rsd143',"ccs14", "ccss14", "ccssv14",\
"ccs15sdr0", "ccs15sdr1", "ccs15sdr2", "ccs15sdr3", 'r150', 'rs150', 'rsv150', 'rsd150', 'r151', 'rs151', 'rsv151', 'rsd151','r152', 'rs152', 'rsv152','rsd152', 'r153', 'rs153', 'rsv153', 'rsd153',"ccs15", "ccss15", "ccssv15"]
#print("a",len(bb))











"""
#this one is it
df = pd.DataFrame(vals, columns=['v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9','v10', 'v11', 'v12', 'v13', 'v14', 'v15', 'v16', 'v17', 'v18', 'v19', \
'v20', 'v21', 'v22', 'v23', 'v24', 'v25', 'v26', 'v27', 'v28', 'v29','v30', 'v31', 'v32', 'v33', 'v34', 'v35', 'v36', 'v37', 'v38', 'v39',\
'v40', 'v41', 'v42', 'v43', 'v44', 'v45', 'v46', 'v47', 'v48', 'v49','v50', 'v51', 'v52', 'v53', 'v54', 'v55',\

's1_0', 's1_1', 's1_2', 's1_3','s1_4', 's1_5', 's1_6', 's1_7', 's1_8', 's1_9', 's1_10', 's1_11', 's1_12', 's1_13', 's1_14', 's1_15', 's1_16',\
's1_17', 's1_18', 's1_19', 's1_20','s1_21', 's1_22', 's1_23', 's1_24', 's1_25', 's1_26', 's1_27', 's1_28', 's1_29', 's1_30', 's1_31', 's1_32', 's1_33',\
's1_34', 's1_35', 's1_36', 's1_37','s1_38', 's1_39', 's1_40', 's1_41', 's1_42', 's1_43', 's1_44', 's1_45', 's1_46', 's1_47', 's1_48', 's1_49', 's1_50',\
's1_51', 's1_52', 's1_53', 's1_54', 's1_55',\

'svt1_0', 'svt1_1', 'svt1_2', 'svt1_3','svt1_4', 'svt1_5', 'svt1_6', 'svt1_7', 'svt1_8', 'svt1_9', 'svt1_10', 'svt1_11', 'svt1_12', 'svt1_13', 'svt1_14', 'svt1_15', 'svt1_16',\
'svt1_17', 'svt1_18', 'svt1_19', 'svt1_20', 'svt1_21', 'svt1_22', 'svt1_23', 'svt1_24', 'svt1_25', 'svt1_26', 'svt1_27', 'svt1_28', 'svt1_29', 'svt1_30', 'svt1_31', 'svt1_32', 'svt1_33',\
'svt1_34', 'svt1_35', 'svt1_36', 'svt1_37', 'svt1_38', 'svt1_39', 'svt1_40', 'svt1_41', 'svt1_42', 'svt1_43', 'svt1_44', 'svt1_45', 'svt1_46', 'svt1_47', 'svt1_48', 'svt1_49', 'svt1_50',\
'svt1_51', 'svt1_52', 'svt1_53', 'svt1_54', 'svt1_55',\


'sdt1_0', 'sdt1_1', 'sdt1_2', 'sdt1_3', 'sdt1_4', 'sdt1_5', 'sdt1_6', 'sdt1_7', 'sdt1_8', 'sdt1_9', 'sdt1_10', 'sdt1_11', 'sdt1_12', 'sdt1_13', 'sdt1_14', 'sdt1_15', 'sdt1_16',\
'sdt1_17', 'sdt1_18', 'sdt1_19', 'sdt1_20', 'sdt1_21', 'sdt1_22', 'sdt1_23', 'sdt1_24', 'sdt1_25', 'sdt1_26', 'sdt1_27', 'sdt1_28', 'sdt1_29', 'sdt1_30', 'sdt1_31', 'sdt1_32', 'sdt1_33',\
'sdt1_34', 'sdt1_35', 'sdt1_36', 'sdt1_37', 'sdt1_38', 'sdt1_39', 'sdt1_40', 'sdt1_41', 'sdt1_42', 'sdt1_43', 'sdt1_44', 'sdt1_45', 'sdt1_46', 'sdt1_47', 'sdt1_48', 'sdt1_49', 'sdt1_50',\
'sdt1_51', 'sdt1_52', 'sdt1_53', 'sdt1_54', 'sdt1_55',\
'r0_1', 'r1_1', 'r2_1', 'r3_1',\
's2_r0_1', 's2_r1_1', 's2_r2_1', 's2_r3_1',\
'svt2_r0_1', 'svt2_r1_1', 'svt2_r2_1', 'svt2_r3_1',\
'sdt2_r0_css0_1', 'sdt2_r1_ccs0_1', 'sdt2_r2_ccs0_1', 'sdt2_r3_ccs0_1',\
'ccs0_1',\
's3_ccs0_1',\
'svt3_ccs0_1',\
'sdt3_ccs0_r0_2', 'sdt3_ccs0_r1_2', 'sdt3_ccs0_r2_2', 'sdt3_ccs0_r3_2',\
'r0_2', 'r1_2', 'r2_2', 'r3_2', 's2_r0_2', 's2_r1_2', 's2_r2_2', 's2_r3_2', 'svt2_r0_2', 'svt2_r1_2', 'svt2_r2_2', 'svt2_r3_2', 'sdt2_r0_css0_2', 'sdt2_r1_ccs0_2', 'sdt2_r2_ccs0_2', 'sdt2_r3_ccs0_2', 'ccs0_2', 's3_ccs0_2', 'svt3_ccs0_2',\
'sdt3_ccs0_r0_3', 'sdt3_ccs0_r1_3', 'sdt3_ccs0_r2_3', 'sdt3_ccs0_r3_3',\
'r0_3', 'r1_3', 'r2_3', 'r3_3', 's2_r0_3', 's2_r1_3', 's2_r2_3', 's2_r3_3', 'svt2_r0_3', 'svt2_r1_3', 'svt2_r2_3', 'svt2_r3_3', 'sdt2_r0_css0_3', 'sdt2_r1_ccs0_3', 'sdt2_r2_ccs0_3', 'sdt2_r3_ccs0_3', 'ccs0_3', 's3_ccs0_3', 'svt3_ccs0_3',\
'sdt3_ccs0_r0_4', 'sdt3_ccs0_r1_4', 'sdt3_ccs0_r2_4', 'sdt3_ccs0_r3_4',\

'r0_4', 'r1_4', 'r2_4', 'r3_4', 's2_r0_4', 's2_r1_4', 's2_r2_4', 's2_r3_4', 'svt2_r0_4', 'svt2_r1_4', 'svt2_r2_4', 'svt2_r3_4', 'sdt2_r0_css0_4', 'sdt2_r1_ccs0_4', 'sdt2_r2_ccs0_4', 'sdt2_r3_ccs0_4', 'ccs0_4', 's3_ccs0_4', 'svt3_ccs0_4',\
'sdt3_ccs0_r0_5', 'sdt3_ccs0_r1_5', 'sdt3_ccs0_r2_5', 'sdt3_ccs0_r3_5',

'r0_5', 'r1_5', 'r2_5', 'r3_5', 's2_r0_5', 's2_r1_5', 's2_r2_5', 's2_r3_5', 'svt2_r0_5', 'svt2_r1_5', 'svt2_r2_5', 'svt2_r3_5', 'sdt2_r0_css0_5', 'sdt2_r1_ccs0_5', 'sdt2_r2_ccs0_5', 'sdt2_r3_ccs0_5', 'ccs0_5', 's3_ccs0_5', 'svt3_ccs0_5',\
'sdt3_ccs0_r0_6', 'sdt3_ccs0_r1_6', 'sdt3_ccs0_r2_6', 'sdt3_ccs0_r3_6',

'r0_6', 'r1_6', 'r2_6', 'r3_6', 's2_r0_6', 's2_r1_6', 's2_r2_6', 's2_r3_6', 'svt2_r0_6', 'svt2_r1_6', 'svt2_r2_6', 'svt2_r3_6', 'sdt2_r0_css0_6', 'sdt2_r1_ccs0_6', 'sdt2_r2_ccs0_6', 'sdt2_r3_ccs0_6', 'ccs0_6', 's3_ccs0_6', 'svt3_ccs0_6',\
'sdt3_ccs0_r0_7', 'sdt3_ccs0_r1_7', 'sdt3_ccs0_r2_7', 'sdt3_ccs0_r3_7',

'r0_7', 'r1_7', 'r2_7', 'r3_7', 's2_r0_7', 's2_r1_7', 's2_r2_7', 's2_r3_7', 'svt2_r0_7', 'svt2_r1_7', 'svt2_r2_7', 'svt2_r3_7', 'sdt2_r0_css0_7', 'sdt2_r1_ccs0_7', 'sdt2_r2_ccs0_7', 'sdt2_r3_ccs0_7', 'ccs0_7', 's3_ccs0_7', 'svt3_ccs0_7',\
'sdt3_ccs0_r0_8', 'sdt3_ccs0_r1_8', 'sdt3_ccs0_r2_8', 'sdt3_ccs0_r3_8',

'r0_8', 'r1_8', 'r2_8', 'r3_8', 's2_r0_8', 's2_r1_8', 's2_r2_8', 's2_r3_8', 'svt2_r0_8', 'svt2_r1_8', 'svt2_r2_8', 'svt2_r3_8', 'sdt2_r0_css0_8', 'sdt2_r1_ccs0_8', 'sdt2_r2_ccs0_8', 'sdt2_r3_ccs0_8', 'ccs0_8', 's3_ccs0_8', 'svt3_ccs0_8',\
'sdt3_ccs0_r0_9', 'sdt3_ccs0_r1_9', 'sdt3_ccs0_r2_9', 'sdt3_ccs0_r3_9',

'r0_9', 'r1_9', 'r2_9', 'r3_9', 's2_r0_9', 's2_r1_9', 's2_r2_9', 's2_r3_9', 'svt2_r0_9', 'svt2_r1_9', 'svt2_r2_9', 'svt2_r3_9', 'sdt2_r0_css0_9', 'sdt2_r1_ccs0_9', 'sdt2_r2_ccs0_9', 'sdt2_r3_ccs0_9', 'ccs0_9', 's3_ccs0_9', 'svt3_ccs0_9',\
'sdt3_ccs0_r0_10', 'sdt3_ccs0_r1_10', 'sdt3_ccs0_r2_10', 'sdt3_ccs0_r3_10',

'r0_10', 'r1_10', 'r2_10', 'r3_10', 's2_r0_10', 's2_r1_10', 's2_r2_10', 's2_r3_10', 'svt2_r0_10', 'svt2_r1_10', 'svt2_r2_10', 'svt2_r3_10', 'sdt2_r0_css0_10', 'sdt2_r1_ccs0_10', 'sdt2_r2_ccs0_10', 'sdt2_r3_ccs0_10', 'ccs0_10', 's3_ccs0_10', 'svt3_ccs0_10',\
'sdt3_ccs0_r0_11', 'sdt3_ccs0_r1_11', 'sdt3_ccs0_r2_11', 'sdt3_ccs0_r3_11',

'r0_11', 'r1_11', 'r2_11', 'r3_11', 's2_r0_11', 's2_r1_11', 's2_r2_11', 's2_r3_11', 'svt2_r0_11', 'svt2_r1_11', 'svt2_r2_11', 'svt2_r3_11', 'sdt2_r0_css0_11', 'sdt2_r1_ccs0_11', 'sdt2_r2_ccs0_11', 'sdt2_r3_ccs0_11', 'ccs0_11', 's3_ccs0_11', 'svt3_ccs0_11',\
'sdt3_ccs0_r0_12', 'sdt3_ccs0_r1_12', 'sdt3_ccs0_r2_12', 'sdt3_ccs0_r3_12',

'r0_12', 'r1_12', 'r2_12', 'r3_12', 's2_r0_12', 's2_r1_12', 's2_r2_12', 's2_r3_12', 'svt2_r0_12', 'svt2_r1_12', 'svt2_r2_12', 'svt2_r3_12', 'sdt2_r0_css0_12', 'sdt2_r1_ccs0_12', 'sdt2_r2_ccs0_12', 'sdt2_r3_ccs0_12', 'ccs0_12', 's3_ccs0_12', 'svt3_ccs0_12',\
'sdt3_ccs0_r0_13', 'sdt3_ccs0_r1_13', 'sdt3_ccs0_r2_13', 'sdt3_ccs0_r3_13',

'r0_13', 'r1_13', 'r2_13', 'r3_13', 's2_r0_13', 's2_r1_13', 's2_r2_13', 's2_r3_13', 'svt2_r0_13', 'svt2_r1_13', 'svt2_r2_13', 'svt2_r3_13', 'sdt2_r0_css0_13', 'sdt2_r1_ccs0_13', 'sdt2_r2_ccs0_13', 'sdt2_r3_ccs0_13', 'ccs0_13', 's3_ccs0_13', 'svt3_ccs0_13',\
'sdt3_ccs0_r0_14', 'sdt3_ccs0_r1_14', 'sdt3_ccs0_r2_14', 'sdt3_ccs0_r3_14',

'r0_14', 'r1_14', 'r2_14', 'r3_14', 's2_r0_14', 's2_r1_14', 's2_r2_14', 's2_r3_14', 'svt2_r0_14', 'svt2_r1_14', 'svt2_r2_14', 'svt2_r3_14', 'sdt2_r0_css0_14', 'sdt2_r1_ccs0_14', 'sdt2_r2_ccs0_14', 'sdt2_r3_ccs0_14', 'ccs0_14', 's3_ccs0_14', 'svt3_ccs0_14',\
'sdt3_ccs0_r0_15', 'sdt3_ccs0_r1_15', 'sdt3_ccs0_r2_15', 'sdt3_ccs0_r3_15',

'r0_15', 'r1_15', 'r2_15', 'r3_15', 's2_r0_15', 's2_r1_15', 's2_r2_15', 's2_r3_15', 'svt2_r0_15', 'svt2_r1_15', 'svt2_r2_15', 'svt2_r3_15', 'sdt2_r0_css0_15', 'sdt2_r1_ccs0_15', 'sdt2_r2_ccs0_15', 'sdt2_r3_ccs0_15', 'ccs0_15', 's3_ccs0_15', 'svt3_ccs0_15'])


"""

aaaa= ['v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9','v10', 'v11', 'v12', 'v13', 'v14', 'v15', 'v16', 'v17', 'v18', 'v19', \
'v20', 'v21', 'v22', 'v23', 'v24', 'v25', 'v26', 'v27', 'v28', 'v29','v30', 'v31', 'v32', 'v33', 'v34', 'v35', 'v36', 'v37', 'v38', 'v39',\
'v40', 'v41', 'v42', 'v43', 'v44', 'v45', 'v46', 'v47', 'v48', 'v49','v50', 'v51', 'v52', 'v53', 'v54', 'v55',\

's1_0', 's1_1', 's1_2', 's1_3','s1_4', 's1_5', 's1_6', 's1_7', 's1_8', 's1_9', 's1_10', 's1_11', 's1_12', 's1_13', 's1_14', 's1_15', 's1_16',\
's1_17', 's1_18', 's1_19', 's1_20','s1_21', 's1_22', 's1_23', 's1_24', 's1_25', 's1_26', 's1_27', 's1_28', 's1_29', 's1_30', 's1_31', 's1_32', 's1_33',\
's1_34', 's1_35', 's1_36', 's1_37','s1_38', 's1_39', 's1_40', 's1_41', 's1_42', 's1_43', 's1_44', 's1_45', 's1_46', 's1_47', 's1_48', 's1_49', 's1_50',\
's1_51', 's1_52', 's1_53', 's1_54', 's1_55',\

'svt1_0', 'svt1_1', 'svt1_2', 'svt1_3','svt1_4', 'svt1_5', 'svt1_6', 'svt1_7', 'svt1_8', 'svt1_9', 'svt1_10', 'svt1_11', 'svt1_12', 'svt1_13', 'svt1_14', 'svt1_15', 'svt1_16',\
'svt1_17', 'svt1_18', 'svt1_19', 'svt1_20', 'svt1_21', 'svt1_22', 'svt1_23', 'svt1_24', 'svt1_25', 'svt1_26', 'svt1_27', 'svt1_28', 'svt1_29', 'svt1_30', 'svt1_31', 'svt1_32', 'svt1_33',\
'svt1_34', 'svt1_35', 'svt1_36', 'svt1_37', 'svt1_38', 'svt1_39', 'svt1_40', 'svt1_41', 'svt1_42', 'svt1_43', 'svt1_44', 'svt1_45', 'svt1_46', 'svt1_47', 'svt1_48', 'svt1_49', 'svt1_50',\
'svt1_51', 'svt1_52', 'svt1_53', 'svt1_54', 'svt1_55',\


'sdt1_0', 'sdt1_1', 'sdt1_2', 'sdt1_3', 'sdt1_4', 'sdt1_5', 'sdt1_6', 'sdt1_7', 'sdt1_8', 'sdt1_9', 'sdt1_10', 'sdt1_11', 'sdt1_12', 'sdt1_13', 'sdt1_14', 'sdt1_15', 'sdt1_16',\
'sdt1_17', 'sdt1_18', 'sdt1_19', 'sdt1_20', 'sdt1_21', 'sdt1_22', 'sdt1_23', 'sdt1_24', 'sdt1_25', 'sdt1_26', 'sdt1_27', 'sdt1_28', 'sdt1_29', 'sdt1_30', 'sdt1_31', 'sdt1_32', 'sdt1_33',\
'sdt1_34', 'sdt1_35', 'sdt1_36', 'sdt1_37', 'sdt1_38', 'sdt1_39', 'sdt1_40', 'sdt1_41', 'sdt1_42', 'sdt1_43', 'sdt1_44', 'sdt1_45', 'sdt1_46', 'sdt1_47', 'sdt1_48', 'sdt1_49', 'sdt1_50',\
'sdt1_51', 'sdt1_52', 'sdt1_53', 'sdt1_54', 'sdt1_55',\


'r0_1', 'r1_1', 'r2_1', 'r3_1', 's2_r0_1', 's2_r1_1', 's2_r2_1', 's2_r3_1', 'svt2_r0_1', 'svt2_r1_1', 'svt2_r2_1', 'svt2_r3_1', 'sdt2_r0_css0_1', 'sdt2_r1_ccs0_1', 'sdt2_r2_ccs0_1', 'sdt2_r3_ccs0_1', 'ccs0_1','s3_ccs0_1','svt3_ccs0_1',\


'sdt3_ccs0_r0_2', 'sdt3_ccs0_r1_2', 'sdt3_ccs0_r2_2', 'sdt3_ccs0_r3_2', 'r0_2', 'r1_2', 'r2_2', 'r3_2', 's2_r0_2', 's2_r1_2', 's2_r2_2', 's2_r3_2', 'svt2_r0_2', 'svt2_r1_2', 'svt2_r2_2', 'svt2_r3_2', 'sdt2_r0_css0_2', 'sdt2_r1_ccs0_2', 'sdt2_r2_ccs0_2', 'sdt2_r3_ccs0_2', 'ccs0_2', 's3_ccs0_2', 'svt3_ccs0_2',\

'sdt3_ccs0_r0_3', 'sdt3_ccs0_r1_3', 'sdt3_ccs0_r2_3', 'sdt3_ccs0_r3_3', 'r0_3', 'r1_3', 'r2_3', 'r3_3', 's2_r0_3', 's2_r1_3', 's2_r2_3', 's2_r3_3', 'svt2_r0_3', 'svt2_r1_3', 'svt2_r2_3', 'svt2_r3_3', 'sdt2_r0_css0_3', 'sdt2_r1_ccs0_3', 'sdt2_r2_ccs0_3', 'sdt2_r3_ccs0_3', 'ccs0_3', 's3_ccs0_3', 'svt3_ccs0_3',\


'sdt3_ccs0_r0_4', 'sdt3_ccs0_r1_4', 'sdt3_ccs0_r2_4', 'sdt3_ccs0_r3_4','r0_4', 'r1_4', 'r2_4', 'r3_4', 's2_r0_4', 's2_r1_4', 's2_r2_4', 's2_r3_4', 'svt2_r0_4', 'svt2_r1_4', 'svt2_r2_4', 'svt2_r3_4', 'sdt2_r0_css0_4', 'sdt2_r1_ccs0_4', 'sdt2_r2_ccs0_4', 'sdt2_r3_ccs0_4', 'ccs0_4', 's3_ccs0_4', 'svt3_ccs0_4',\


'sdt3_ccs0_r0_5', 'sdt3_ccs0_r1_5', 'sdt3_ccs0_r2_5', 'sdt3_ccs0_r3_5', 'r0_5', 'r1_5', 'r2_5', 'r3_5', 's2_r0_5', 's2_r1_5', 's2_r2_5', 's2_r3_5', 'svt2_r0_5', 'svt2_r1_5', 'svt2_r2_5', 'svt2_r3_5', 'sdt2_r0_css0_5', 'sdt2_r1_ccs0_5', 'sdt2_r2_ccs0_5', 'sdt2_r3_ccs0_5', 'ccs0_5', 's3_ccs0_5', 'svt3_ccs0_5',\


'sdt3_ccs0_r0_6', 'sdt3_ccs0_r1_6', 'sdt3_ccs0_r2_6', 'sdt3_ccs0_r3_6', 'r0_6', 'r1_6', 'r2_6', 'r3_6', 's2_r0_6', 's2_r1_6', 's2_r2_6', 's2_r3_6', 'svt2_r0_6', 'svt2_r1_6', 'svt2_r2_6', 'svt2_r3_6', 'sdt2_r0_css0_6', 'sdt2_r1_ccs0_6', 'sdt2_r2_ccs0_6', 'sdt2_r3_ccs0_6', 'ccs0_6', 's3_ccs0_6', 'svt3_ccs0_6',\


'sdt3_ccs0_r0_7', 'sdt3_ccs0_r1_7', 'sdt3_ccs0_r2_7', 'sdt3_ccs0_r3_7', 'r0_7', 'r1_7', 'r2_7', 'r3_7', 's2_r0_7', 's2_r1_7', 's2_r2_7', 's2_r3_7', 'svt2_r0_7', 'svt2_r1_7', 'svt2_r2_7', 'svt2_r3_7', 'sdt2_r0_css0_7', 'sdt2_r1_ccs0_7', 'sdt2_r2_ccs0_7', 'sdt2_r3_ccs0_7', 'ccs0_7', 's3_ccs0_7', 'svt3_ccs0_7',\


'sdt3_ccs0_r0_8', 'sdt3_ccs0_r1_8', 'sdt3_ccs0_r2_8', 'sdt3_ccs0_r3_8', 'r0_8', 'r1_8', 'r2_8', 'r3_8', 's2_r0_8', 's2_r1_8', 's2_r2_8', 's2_r3_8', 'svt2_r0_8', 'svt2_r1_8', 'svt2_r2_8', 'svt2_r3_8', 'sdt2_r0_css0_8', 'sdt2_r1_ccs0_8', 'sdt2_r2_ccs0_8', 'sdt2_r3_ccs0_8', 'ccs0_8', 's3_ccs0_8', 'svt3_ccs0_8',\


'sdt3_ccs0_r0_9', 'sdt3_ccs0_r1_9', 'sdt3_ccs0_r2_9', 'sdt3_ccs0_r3_9', 'r0_9', 'r1_9', 'r2_9', 'r3_9', 's2_r0_9', 's2_r1_9', 's2_r2_9', 's2_r3_9', 'svt2_r0_9', 'svt2_r1_9', 'svt2_r2_9', 'svt2_r3_9', 'sdt2_r0_css0_9', 'sdt2_r1_ccs0_9', 'sdt2_r2_ccs0_9', 'sdt2_r3_ccs0_9', 'ccs0_9', 's3_ccs0_9', 'svt3_ccs0_9',\


'sdt3_ccs0_r0_10', 'sdt3_ccs0_r1_10', 'sdt3_ccs0_r2_10', 'sdt3_ccs0_r3_10', 'r0_10', 'r1_10', 'r2_10', 'r3_10', 's2_r0_10', 's2_r1_10', 's2_r2_10', 's2_r3_10', 'svt2_r0_10', 'svt2_r1_10', 'svt2_r2_10', 'svt2_r3_10', 'sdt2_r0_css0_10', 'sdt2_r1_ccs0_10', 'sdt2_r2_ccs0_10', 'sdt2_r3_ccs0_10', 'ccs0_10', 's3_ccs0_10', 'svt3_ccs0_10',\


'sdt3_ccs0_r0_11', 'sdt3_ccs0_r1_11', 'sdt3_ccs0_r2_11', 'sdt3_ccs0_r3_11', 'r0_11', 'r1_11', 'r2_11', 'r3_11', 's2_r0_11', 's2_r1_11', 's2_r2_11', 's2_r3_11', 'svt2_r0_11', 'svt2_r1_11', 'svt2_r2_11', 'svt2_r3_11', 'sdt2_r0_css0_11', 'sdt2_r1_ccs0_11', 'sdt2_r2_ccs0_11', 'sdt2_r3_ccs0_11', 'ccs0_11', 's3_ccs0_11', 'svt3_ccs0_11',\


'sdt3_ccs0_r0_12', 'sdt3_ccs0_r1_12', 'sdt3_ccs0_r2_12', 'sdt3_ccs0_r3_12','r0_12', 'r1_12', 'r2_12', 'r3_12', 's2_r0_12', 's2_r1_12', 's2_r2_12', 's2_r3_12', 'svt2_r0_12', 'svt2_r1_12', 'svt2_r2_12', 'svt2_r3_12', 'sdt2_r0_css0_12', 'sdt2_r1_ccs0_12', 'sdt2_r2_ccs0_12', 'sdt2_r3_ccs0_12', 'ccs0_12', 's3_ccs0_12', 'svt3_ccs0_12',\


'sdt3_ccs0_r0_13', 'sdt3_ccs0_r1_13', 'sdt3_ccs0_r2_13', 'sdt3_ccs0_r3_13', 'r0_13', 'r1_13', 'r2_13', 'r3_13', 's2_r0_13', 's2_r1_13', 's2_r2_13', 's2_r3_13', 'svt2_r0_13', 'svt2_r1_13', 'svt2_r2_13', 'svt2_r3_13', 'sdt2_r0_css0_13', 'sdt2_r1_ccs0_13', 'sdt2_r2_ccs0_13', 'sdt2_r3_ccs0_13', 'ccs0_13', 's3_ccs0_13', 'svt3_ccs0_13',\


'sdt3_ccs0_r0_14', 'sdt3_ccs0_r1_14', 'sdt3_ccs0_r2_14', 'sdt3_ccs0_r3_14', 'r0_14', 'r1_14', 'r2_14', 'r3_14', 's2_r0_14', 's2_r1_14', 's2_r2_14', 's2_r3_14', 'svt2_r0_14', 'svt2_r1_14', 'svt2_r2_14', 'svt2_r3_14', 'sdt2_r0_css0_14', 'sdt2_r1_ccs0_14', 'sdt2_r2_ccs0_14', 'sdt2_r3_ccs0_14', 'ccs0_14', 's3_ccs0_14', 'svt3_ccs0_14',\


'sdt3_ccs0_r0_15', 'sdt3_ccs0_r1_15', 'sdt3_ccs0_r2_15', 'sdt3_ccs0_r3_15', 'r0_15', 'r1_15', 'r2_15', 'r3_15', 's2_r0_15', 's2_r1_15', 's2_r2_15', 's2_r3_15', 'svt2_r0_15', 'svt2_r1_15', 'svt2_r2_15', 'svt2_r3_15', 'sdt2_r0_css0_15', 'sdt2_r1_ccs0_15', 'sdt2_r2_ccs0_15', 'sdt2_r3_ccs0_15', 'ccs0_15', 's3_ccs0_15', 'svt3_ccs0_15']


#print("length:", len(aaaa))