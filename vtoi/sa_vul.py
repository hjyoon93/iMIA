# importing package
import matplotlib.pyplot as plt
import numpy as np

# create data


plt.ylabel("SA", fontsize=14)
plt.xlabel(r'$v_{m}$', fontsize=14)
x = [0.2,0.4,0.6,0.8,1.0]
y_20 = [0.8668, 0.8548, 0.8312, 0.8217, 0.7995]
y_40 = [0.8586, 0.8296, 0.8121, 0.7851, 0.7835]
y_60 = [0.8217, 0.7980, 0.7723, 0.7579, 0.7423]


plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# plot lines
plt.plot(x, y_20, color ='blue', marker= "^", linestyle='dashed', linewidth=3, markersize = 10)#,  linewidth=3)#, label="MD = 20 FL rounds")
plt.plot(x, y_40, color ='red',marker= "o", linestyle='solid', linewidth=3, markersize = 10)#, linewidth=3)#, label="MD = 40 FL rounds")
plt.plot(x, y_60, color ='green',marker= "d", linestyle='-.', linewidth=3, markersize = 10)#, linewidth=3)#, label="MD = 60 FL rounds")
#plt.legend()
plt.show()

#legendFig = plt.figure("Legend plot")

#legendFig.legend([a,b,c], ["MD = 20 FL rounds", "MD = 40 FL rounds", "MD = 60 FL rounds"], loc='center', mode='expand', ncol=3)
#legendFig.savefig('legend.png')
