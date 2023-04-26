from simulation_new import *
import numpy as np
display = False

if __name__ == '__main__':
    start = time.time()
    simulation_time = 1
    # game_start()
    # run_sumulation_fixed_setting("IODM", False, False, simulation_time)
    # arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    arr = [9]*10
    t=0
    scheme = 'ebm'
    while t<1:
        try:  
            game_start(t, 0, False, True, web_data_upper_vul=7, Iot_upper_vul=arr[t%10], scheme=scheme)
            print("Project took", time.time() - start, "seconds.")
            t+=1
        except:
            pass
    # time.sleep(10)
    # try:
    #     os.system('say "your program has finished"')
    #     os._exit(0)
    # except:
    #     print("Your command not found: say")
