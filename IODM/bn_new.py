from ntpath import join
import numpy as np
import pandas as pd
from pgmpy.models import BayesianModel
from pgmpy.estimators import BayesianEstimator, MaximumLikelihoodEstimator, HillClimbSearch, BicScore
from pgmpy.factors.discrete.CPD import TabularCPD
import random
import bnlearn as bn

# def print_full(cpd):
#     backup = TabularCPD._truncate_strtable
#     TabularCPD._truncate_strtable = lambda self, x: x
#     print(cpd)
#     TabularCPD._truncate_strtable = backup
# generate data
# data = pd.DataFrame(np.random.randint(low=0, high=2, size=(5000, 4)), columns=['A', 'B', 'C', 'D'])
data = pd.read_csv("train_fin.csv")
# print(len(data))
# g = data.groupby('mission')
# data = pd.DataFrame(g.apply(lambda x: x.sample(g.size().min()).reset_index(drop=True)))
# data = data.reset_index(drop=True)
# g.apply(lambda x: x.sample(g.size().min()).reset_index(drop=True))
print(data[2:].head())
# data = pd.DataFrame(g)
# print(data.head())
print(data['mission_performance'].value_counts())
print(data['timeliness'].value_counts())
print(data['mission'].value_counts())
# for c in data.columns:
#     if 'AC' in c:
#         data = data.drop(columns=[c])
data.dropna()
# data=data.drop(columns=['AND'])
# print(data.columns)
# print(data["timeliness"].value_counts())
# print(data.columns)
edges = []

from pgmpy.estimators import ExhaustiveSearch

# hc = HillClimbSearch(data)
# best_model = hc.estimate(scoring_method=BicScore(data))
# print(best_model.edges())

# print("\nAll DAGs by score:")
# for score, dag in reversed(hc.all_scores()):
#     print(score, dag.edges())


# for i in range(20):
#     # edges.append(("IoT"+str(i+1)+"_AC", "IoT"+str(i+1)+"_Edge"))
#     # edges.append(("IoT"+str(i+1)+"_Edge", "mission"))
#     edges.append(("IoT"+str(i+1)+"_Edge", "mission"))

# for i in range(10):
#     # edges.append(("Edge"+str(i+1)+"_AC", "Edge"+str(i+1)+"_MEC"))
#     # edges.append(("Edge"+str(i+1)+"_MEC", "MEC"+str(round((i+1.1)/2))+"_obj"))
#     # edges.append(("Edge"+str(i+1)+"_MEC", "MEC"+str(round((i+1.1)/2))+"_obj"))
#     edges.append(("Edge"+str(i+1)+"_IoT", "mission"))
#     # edges.append(("Edge"+str(i+1)+"_MEC", "mission"))
#     # edges.append(("Edge"+str(i+1)+"_IoT", "mission_performance"))

# for i in range(5):
#     # edges.append(("MEC"+str(i+1)+"_AC", "MEC"+str(i+1)+"_obj"))
#     edges.append(("MEC"+str(i+1)+"_obj", "mission")) 
    # edges.append(("MEC"+str(i+1)+"_Edge", "Edge"+str(2*i+1)+"_IoT"))
    # edges.append(("MEC"+str(i+1)+"_Edge", "mission"))

# for i in range(20):
#     # edges.append(("IoT"+str(i+1)+"_AC", "IoT"+str(i+1)+"_Edge"))
#     edges.append(("IoT"+str(i+1)+"_Edge", "Edge"+str(round((i+1.1)/2))+"_MEC"))

# for i in range(10):
#     # edges.append(("Edge"+str(i+1)+"_AC", "Edge"+str(i+1)+"_MEC"))
#     edges.append(("Edge"+str(i+1)+"_MEC", "MEC"+str(round((i+1.1)/2))+"_obj"))
#     edges.append(("Edge"+str(i+1)+"_IoT", "mission"))
#     # edges.append(("Edge"+str(i+1)+"_IoT", "mission_performance"))

# for i in range(5):
#     # edges.append(("MEC"+str(i+1)+"_AC", "MEC"+str(i+1)+"_obj"))
#     edges.append(("MEC"+str(i+1)+"_obj", "MEC"+str(i+1)+"_Edge")) 
#     edges.append(("MEC"+str(i+1)+"_Edge", "Edge"+str(2*i+1)+"_IoT"))
#     edges.append(("MEC"+str(i+1)+"_Edge", "Edge"+str(2*i+2)+"_IoT"))

for i in range(20):
    # edges.append(("IoT"+str(i+1)+"_AC", "IoT"+str(i+1)+"_service"))
    edges.append(("IoT"+str(i+1)+"_service", "IoT"+str(i+1)+"_Edge"))  
    edges.append(("IoT"+str(i+1)+"_service", "IoT_Edge_OR"))  
    edges.append(("IoT"+str(i+1)+"_Edge", "OR_Edge"+str(round((i+1.1)/2))))
    # edges.append(("IoT"+str(i+1)+"_Edge", "Edge"+str(round((i+1.1)/2))+"_MEC"))

for i in range(10):
    # edges.append(("Edge"+str(i+1)+"_AC", "Edge"+str(i+1)+"_service"))
    edges.append(("OR_Edge"+str(i+1), "Edge"+str(i+1)+"_MEC"))
    # edges.append(("OR_Edge"+str(i+1), "IoT_Edge_OR"))
    # edges.append(("OR_Edge"+str(i+1), "timeliness"))
    edges.append(("Edge"+str(i+1)+"_service", "Edge_iot_OR"))
    edges.append(("Edge"+str(i+1)+"_service", "Edge"+str(i+1)+"_MEC"))
    edges.append(("Edge"+str(i+1)+"_service", "Edge"+str(i+1)+"_IoT"))
    edges.append(("Edge"+str(i+1)+"_MEC", "OR_MEC"+str(round((i+1.1)/2))))
    # edges.append(("Edge"+str(i+1)+"_IoT", "timeliness"))
    edges.append(("Edge"+str(i+1)+"_IoT", "Edge_iot_OR"))
    # edges.append(("Edge"+str(i+1)+"_IoT", "mission_performance"))

for i in range(5):
    # edges.append(("MEC"+str(i+1)+"_AC", "MEC"+str(i+1)+"_service"))
    edges.append(("MEC"+str(i+1)+"_service", "Edge_MEC_OR"))
    edges.append(("MEC"+str(i+1)+"_service", "MEC"+str(i+1)+"_obj"))
    edges.append(("MEC"+str(i+1)+"_service", "MEC"+str(i+1)+"_Edge"))
    edges.append(("OR_MEC"+str(i+1), "MEC"+str(i+1)+"_obj"))
    edges.append(("OR_MEC"+str(i+1), "MEC"+str(i+1)+"_Edge"))
    # edges.append(("OR_MEC"+str(i+1), "timeliness"))
    # edges.append(("OR_MEC"+str(i+1), "Edge_MEC_OR"))




    # edges.append(("MEC"+str(i+1)+"_service", "MEC"+str(i+1)+"_Edge"+str(2*i+1)))
    edges.append(("MEC"+str(i+1)+"_obj", "Obj_OR")) 

    edges.append(("MEC"+str(i+1)+"_Edge", "Edge"+str(2*i+1)+"_IoT"))
    edges.append(("MEC"+str(i+1)+"_Edge", "Edge"+str(2*i+2)+"_IoT"))

# edges.append(("Obj_OR","AND"))
# edges.append(("Edge_iot_OR","AND"))

edges.append(("Obj_OR","mission_performance"))
edges.append(("Edge_iot_OR","timeliness"))
edges.append(("IoT_Edge_OR","timeliness"))
edges.append(("Edge_MEC_OR","timeliness"))
edges.append(("timeliness", "mission"))
edges.append(("mission_performance", "mission"))
# edges.append(("AND","mission"))
# print(edges)
# print(edges)/
model = BayesianModel(edges)
                                            #  ])

# print(edges)
# model = None
model.fit(data, estimator=BayesianEstimator) # default equivalent_sample_size=5

# model = bn.structure_learning.fit(data)
# # Compute edge strength with the chi_square test statistic
# model = bn.independence_test(model, data)
# G = bn.plot(model)
# for cpd in model.get_cpds():
#     print(cpd)

from pgmpy.inference import VariableElimination

infer = VariableElimination(model)
vars = list(model.nodes())
# print(data)
data = pd.read_csv("test_fin.csv")
# g = data.groupby('mission')
# data = pd.DataFrame(g.apply(lambda x: x.sample(g.size().min()).reset_index(drop=True)))
# data = data.reset_index(drop=True)
# g.apply(lambda x: x.sample(g.size().min()).reset_index(drop=True))
# data = g
# for c in data.columns:
#     if 'AC' in c:
#         data = data.drop(columns=[c])
data.dropna()
# data = data.drop(columns = ["mission_performance", "timeliness"])
# data = data.drop(columns = ["OR_Edge1", "OR_Edge2", "OR_Edge3", "OR_Edge4", "OR_Edge5", "OR_Edge6", "OR_Edge7", "OR_Edge8", "OR_Edge9", "OR_Edge10", "OR_MEC1", "OR_MEC2", "OR_MEC3", "OR_MEC4", "OR_MEC5", "Obj_OR", "Edge_iot_OR", "mission_performance", "timeliness", "Edge_MEC_OR", "IoT_Edge_OR"])
#  = data['mission']
data = data.drop(columns=['Obj_OR'])
# print(data)
# vars = data.columns
# vars.remove("mission")
# q = infer.map_query(variables=[vars], evidence={'mission': 0})
# print(q)

# vars.remove("timeliness")
# vars.remove("mission_performance")
count = 0
correct = 0
zeros = 0
ones = 0
t=0
remove_list = ["OR_Edge1", "OR_Edge2", "OR_Edge3", "OR_Edge4", "OR_Edge5", "OR_Edge6", "OR_Edge7", "OR_Edge8", "OR_Edge9", "OR_Edge10", "OR_MEC1", "OR_MEC2", "OR_MEC3", "OR_MEC4", "OR_MEC5", "Edge_iot_OR", "mission_performance", "timeliness","Edge_MEC_OR", "IoT_Edge_OR"]
while t<1:
    print(str(t) + "*"*100)
    for index, row in data.iterrows():
        print(index, correct)
        evidence = dict()
        f = 1
        if np.isnan(row[-1]):
            continue
        for i, c in enumerate(data.columns[:-1]):
            if c in remove_list:
                continue
            if i>len(row):
                break
            if np.isnan(row[i]):
                f = 0
                break
            evidence[c] = row[i]
            # print(evidence)/
        
        if f==1:
            # q = infer.map_query(variables=['mission'], evidence=evidence, show_progress=False)
            # try:
            q = infer.query(variables=['mission'], evidence=evidence, joint=False, show_progress=False)
            # q3 = infer.query(variables=['mission_performance'], evidence=evidence, joint=False, show_progress=False)
            # print(q['mission'])
            
            # q = bn.inference.fit(model, variables=['Rain'], evidence={'Cloudy':1})
            # print(q.df)
            # except:
                # continue
            # print(q['mission'], row[-1])
            # if row[-1] == 0:
            if row[-1]==0:
                if random.random() < q['mission'].values[0]:
                # if row[-1]==0:
                    correct+=1
                    zeros+=1
                # else:
                    # print(row.to_dict())
                    # for r in remove_list:
                    #     print(r, row[r], end = " ")
                    # print(q['mission'].values, row[-1])
                    # for r in remove_list:
                    #     print(r, np.argmax(infer.query(variables=[r], evidence=evidence, joint=False, show_progress=False)[r].values), end = ' ')
                    
            else:
                if random.random() < q['mission'].values[1]:
                    # print(row[-1], q['mission'].values[1], q2['timeliness'], q3['mission_performance'])
                    correct+=1
                    ones+=1
                # else:
                #     # print(row.to_dict())
                #     for r in remove_list:
                #         print(row[r])
                    # print(q['mission'].values, row[-1])
                #     for r in remove_list:
                #         print(r, np.argmax(infer.query(variables=[r], evidence=evidence, joint=False, show_progress=False)[r].values), end = ' ')

                    # print(row.to_dict(), q['mission'], q2['timeliness'], q3['mission_performance'])
                    # ones+=1
            # if q['mission'] == row[-1]:
            #     correct +=1
            # elif row[-1] == 1:
            #     if random.random() < q['mission'].values[1]:
            #         correct+=1
            # print()
            # print()
            count+=1
    t+=1

print(data['mission'].value_counts())
print("Accuracy", correct/count)



print(zeros, ones)
    # print((q['mission'].values[0], q['mission'].values[1]))
    
        # for v in vars:
#     if "AC" in v:
#         vars.remove(v)
# print(vars)
# for v in vars:
#     q = infer.query(variables=[v], evidence={"mission_performance": 0})
#     print(q)
# q = infer.map_query(variables=["A", "B", "C"], evidence={"D": 0})
# print(q)
