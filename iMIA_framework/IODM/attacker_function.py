
import numpy as np

def DoS(G_real, G_att, G_def, monit_time):
    node_id_set = list(G_att.nodes())
    if random.random() <= G_real.nodes[random_id]["vulnerability"]: 
        G_real.nodes[random_id]["compromised"] = True
        G_att.nodes[random_id]["compromised"] = True

def dataManipulation(G_real, G_att, G_def, monit_time):
    node_id_set = list(G_att.nodes())
    if random.random() <= G_real.nodes[random_id]["vulnerability"]: 
        G_real.nodes[random_id]["compromised"] = True
        G_att.nodes[random_id]["compromised"] = True

def Phishing(G_real, G_att, G_def, monit_time):
    node_id_set = list(G_att.nodes())
    if random.random() <= G_real.nodes[random_id]["vulnerability"]:
        G_real.nodes[random_id]["compromised"] = True
        G_att.nodes[random_id]["compromised"] = True