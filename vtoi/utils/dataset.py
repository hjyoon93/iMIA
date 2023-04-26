import random

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



'ccs0_1', 's2_ccs0_1', 'sv2_ccs0_1', 'sd2_ccs0_r0_1', 'sd2_ccs0_r1_1', 'sd2_ccs0_r2_1', 'sd2_ccs0_r3_1',
'r0_1', 'r1_1', 'r2_1', 'r3_1', 's3_r0_1', 's3_r1_1', 's3_r2_1', 's3_r3_1', 'sv3_r0_1', 'sv3_r1_1', 'sv3_r2_1', 'sv3_r3_1', \
'sd3_r0_css0_1', 'sd3_r1_ccs0_1', 'sd3_r2_ccs0_1', 'sd3_r3_ccs0_1', 's4_ccs0_1', 'sv4_ccs0_1', 'sv5_mcc_1',\

'sd2_ccs0_r0_2', 'sd2_ccs0_r1_2', 'sd2_ccs0_r2_2', 'sd2_ccs0_r3_2',

                                 'r0_2', 'r1_2', 'r2_2', 'r3_2',

                                 's3_r0_2', 's3_r1_2', 's3_r2_2', 's3_r3_2',


                                 'sv3_r0_2', 'sv3_r1_2', 'sv3_r2_2', 'sv3_r3_2',

                                 'sd3_r0_css0_2', 'sd3_r1_ccs0_2', 'sd3_r2_ccs0_2', 'sd3_r3_ccs0_2',

                                 'ccs0_2', 's4_ccs0_2', 'sv4_ccs0_2', 'sv5_mcc_2',\




'sv6_mcc', 'sv7_mcc', 'outcome']

List = []

for i in range(277):
    if random.random() < 0.5:
        List.append('true')
    else:
        List.append('false')



print(len(List))


file = open("file_dataset.txt", "a") #it was file1.txt
# Saving the array in a text file
content = str(List) + '\n'
file.write(content)
file.close()


bbbb = ['true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'true', 'true', 'false', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'false', 'true', 'true', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'false', 'false', 'false', 'true', 'false', 'true', 'true', 'false', 'true', 'true', 'false', 'true', 'false', 'true', 'true', 'false', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'false', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true', 'true']
ab = bbbb[:277]
print(ab)
print(len(ab))