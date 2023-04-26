# importing package
import matplotlib.pyplot as plt
import numpy as np

# create data


plt.ylabel(r'$ASR$', fontsize=14)
plt.xlabel(r'$v_{m}$', fontsize=14)
x = [0.2,0.4,0.6,0.8, 1.0]
y_20 = [0.1767, 0.3567, 0.4993, 0.6881, 0.7699]
y_40 = [0.1763, 0.3766, 0.5514, 0.6504, 0.7715]
y_60 = [0.1953, 0.3744, 0.5813, 0.6654, 0.7094]


plt.xticks(fontsize=14)
plt.yticks(fontsize=14)


# plot lines
plt.plot(x, y_20, color ='blue', marker= "^", linestyle='dashed', linewidth=3, markersize = 10)#label="Mission Duration = 20 FL rounds")
plt.plot(x, y_40, color ='red', marker= "o", linestyle='solid', linewidth=3, markersize = 10)#label="Mission Duration = 40 FL rounds")
plt.plot(x, y_60, color ='green',marker= "d", linestyle='-.', linewidth=3, markersize = 10)#label="Mission Duration = 60 FL rounds")
#plt.legend()
plt.show()
