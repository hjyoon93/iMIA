# importing package
import matplotlib.pyplot as plt
import numpy as np

# create data


plt.ylabel("ASR", fontsize=14)
plt.xlabel(r'$P_{A}$', fontsize=14)
x = [0,0.2,0.4,0.6,0.8, 1.0]
y_20 = [0, 0.3947, 0.4325, 0.4270 ,0.4371, 0.4214]
y_40 = [0, 0.4562, 0.4581, 0.4290, 0.4143, 0.3647]
y_60 = [0, 0.5230, 0.4991, 0.3937, 0.3710, 0.3452]

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# plot lines
plt.plot(x, y_20, color ='blue', marker= "^", linestyle='dashed',linewidth=3, markersize = 10)# label="Mission Duration = 20 FL rounds")
plt.plot(x, y_40,color ='red', marker= "o", linestyle='solid', linewidth=3, markersize = 10)#label="Mission Duration = 40 FL rounds")
plt.plot(x, y_60,color ='green', marker= "d", linestyle='-.', linewidth=3, markersize = 10)#label="Mission Duration = 60 FL rounds")
#plt.legend()
plt.show()
