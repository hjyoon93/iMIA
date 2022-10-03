import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import json 

from graph_function import *
from attacker_function import *
from defender_function import *

def save_graph(G):
    all_nodes = list(G.nodes())
    nodes = [{'name': str(i), 'group': G.nodes[i]["type"], 'compromised': G.nodes[i]["compromised"], 'centrality': G.nodes[i]["centrality"], 'vulnerability': G.nodes[i]["vulnerability"]}
            for i in G.nodes()]
    links = [{'source': all_nodes.index(u[0]), 'target': all_nodes.index(u[1]), 'value':0, 'size':1}
            for u in G.edges()]
    with open('static/graph.json', 'w') as f:
        json.dump({'nodes': nodes, 'links': links}, f, indent=4,)

if __name__ == '__main__':
    G = create_graph()
    set_type(G)
    set_compromised(G)
    set_centrality(G)
    set_vulnerability(G)
    attacker_subgame = 0
    sub_game_number = 3
    # while steps > 0:

    save_graph(G)

    game_continue = True
    while (game_continue):
        system_lifetime += 1

        print("Game: " + str(system_lifetime))

        print("Stage: " + str(attacker_subgame + 1))
        

        def_subgame = def_predict_stage(defender_uncertainty_update()[0], attacker_subgame)
        
        if def_subgame == 3:
            def_chosen_strategy = random.randint(0,4)
            print("defender select full game")
        else:
            # defender select strategy
            def_chosen_strategy = defender_choose_strategy(def_subgame)
            print("defender strategy: "+str(def_chosen_strategy + 1))

        
        # defender behavior
        defender_behavior(def_chosen_strategy)
        
        # attacker select strategy
        att_chosen_strategy = attacker_choose_strategy(att_subgame)
        print("attacker strategy: " + str(att_chosen_strategy + 1))

        # attacker behavior
        action_result = attacker_behavior(att_chosen_strategy)
        
        
        # changing stage
        if action_result:
            if att_chosen_strategy == 0 and att_subgame == 1:
                print("remain in Stage D")
            elif att_subgame >= sub_game_number-1:
                print("stay in stage 3")
            else:
                print("move to next stage")
                attacker_subgame += 1
            # new game, new impact
            attack_impact_record = np.zeros(att_strategy_number)
            defend_impact_record = np.zeros(def_strategy_number)
        

        attacker_action_history[attacker_subgame, att_chosen_strategy] += 1
        update_strategy_probability()
        
        if is_system_fail():
            game_continue = False
    # print(G.edges())
    # print(G)
        # print(nx.cycle_basis(G.to_undirected()))
    # cmap = []

    # for node in G:
    #     if 'IoT' in node:
    #         cmap.append('green')
    #     elif 'Edge' in node:
    #         cmap.append('red')
    #     elif 'MEC' in node:
    #         cmap.append('skyblue')
    #     else:
    #         cmap.append('yellow')
    

    # nx.draw(G, node_color = cmap)
    # plt.tight_layout()
    # plt.show()
    # plt.savefig("Graph.png", format="PNG")