
import numpy as np

def DoS(G_real, G_att, G_def, monit_time):
    node_id_set = list(G_att.nodes())
    if random.random() <= G_real.nodes[random_id]["vulnerability"] * math.exp(-1/monit_time): 
        G_real.nodes[random_id]["compromised"] = True
        G_att.nodes[random_id]["compromised"] = True

def dataManipulation(G_real, G_att, G_def, monit_time):
    node_id_set = list(G_att.nodes())
    if random.random() >= G_real.nodes[random_id]["integrity"] * math.exp(-monit_time): 
        G_real.nodes[random_id]["integrity"] = G_real.nodes[random_id]["integrity"] - 0.1
        G_real.nodes[random_id]["compromised"] = True
        G_att.nodes[random_id]["compromised"] = True

def Phishing(G_real, G_att, G_def, monit_time):
    node_id_set = list(G_att.nodes())
    if random.random() >= G_real.nodes[random_id]["confidentiality"] * math.exp(-monit_time): 
        G_real.nodes[random_id]["confidentiality"] = G_real.nodes[random_id]["confidentiality"] - 0.2
        G_real.nodes[random_id]["compromised"] = True
        G_att.nodes[random_id]["compromised"] = True