# importing package
import matplotlib.pyplot as plt
import numpy as np

# create data


plt.ylabel(r'$P_{ACC}$', fontsize=14)
plt.xlabel(r'$v_{m}$', fontsize=14)
x = [0.2,0.4,0.6,0.8,1.0]

y_20 = [81.59, 76.82, 71.84, 56.5, 45.0]

y_40 = [81.19, 70.51, 61.74, 48.53, 33.51]

y_60 = [79.48, 66.93, 55.87, 32.69, 22.07]


plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# plot lines
plt.plot(x, y_20, marker= "^", color='blue', linestyle='dashed', linewidth=3, markersize = 10)# label="Mission Duration = 20 FL rounds")
plt.plot(x, y_40, marker= "o", color='red', linestyle='solid',linewidth=3, markersize = 10)# label="Mission Duration = 40 FL rounds")
plt.plot(x, y_60, marker= "d", color='green', linestyle='-.',linewidth=3, markersize = 10) #label="Mission Duration = 60 FL rounds")
#plt.legend()
plt.show()

