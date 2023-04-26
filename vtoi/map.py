from tkinter import *
import tkinter
import tkintermapview
from PIL import Image, ImageTk


import random



root = Tk()
root.title('Traffic Sign service provision - Welcome to Traffic Sign map')
root.iconbitmap('c:/gui/uavanet-service-provision')
root.geometry("750x450") #900X700

my_label = LabelFrame(root)
my_label.pack(pady=20)

# Create a photoimage object of the image in the path
image1 = Image.open("1way.png").resize((20, 20))
oneway = ImageTk.PhotoImage(image1)

image2 = Image.open("yield.png").resize((20, 20))
yields = ImageTk.PhotoImage(image2)

image3 = Image.open("roadbump.png").resize((20, 20))
roadbump = ImageTk.PhotoImage(image3)

image4 = Image.open("noright.png").resize((20, 20))
noright = ImageTk.PhotoImage(image4)

image5 = Image.open("nocontrolledcrosswalk.png").resize((20, 20))
nocontrolledcrosswalk = ImageTk.PhotoImage(image5)

image6 = Image.open("noentry.png").resize((20, 20))
noentry = ImageTk.PhotoImage(image6)

image7 = Image.open("speedlimit.png").resize((20, 20))
speedlimit = ImageTk.PhotoImage(image7)

image8 = Image.open("roadnarrowing.png").resize((20, 20))
roadnarrowing = ImageTk.PhotoImage(image8)

image9 = Image.open("noparking.png").resize((20, 20))
noparking = ImageTk.PhotoImage(image9)

image10 = Image.open("noparkingstop.png").resize((20, 20))
noparkingstop = ImageTk.PhotoImage(image10)

image11 = Image.open("deadend.png").resize((20, 20))
deadend = ImageTk.PhotoImage(image11)

image12 = Image.open("parking.png").resize((20, 20))
parking = ImageTk.PhotoImage(image12)

image13 = Image.open("roundabout.png").resize((20, 20))
roundabout = ImageTk.PhotoImage(image13)


######

########

map_widget = tkintermapview.TkinterMapView(my_label, width=650, height=350, corner_radius=0) #800*600

map_widget.set_position(51.2249469, 4.4692042)#(51.22490466033755, 4.4692656115851115) #hoboken
map_widget.set_zoom(17.4)
#print(list_traffic_signs)

#button for quit######
button_quit = Button(root, text = "Exit Traffic Sign Provision App", command=root.quit)
button_quit.pack()
###########

####
#how to go from a list of string to a list of variables

#str = "pythonpool"
#locals()[str] = 5000
#print(pythonpool)
#varA = ImageTk.PhotoImage(image1)
#varB = ImageTk.PhotoImage(image1)
#varC = ImageTk.PhotoImage(image1)
#listStrings = ['varA','varB','varC']




#lines = ["hi","oneway", "oneway", "oneway", "oneway", "oneway", "oneway", "noright","noright","noright", "noparking"]



#writing to a file
#with open('l.txt', 'w') as f:
#    for line in lines:
#        f.write(f"{line}\n")

#reading from a file
#with open('l.txt') as f:
#    a = f.read().splitlines()
#    print(a)

def update():
    with open('l.txt') as f:
        a = f.read().splitlines()
        a = a[:60]
        #print(a)

    for i in range(len(a)):
        if a[i] == '53':
            a[i] = "oneway"
        if a[i] == '30':
            a[i] = "noright"
        if a[i] == '40':
            a[i] = "noparking"
        if a[i] == '22':
            a[i] = "noentry"
        if a[i] == '41':
            a[i] = "noparkingstop"
        if a[i] == '45':
            a[i] = "parking"
        if a[i] == '19':
            a[i] = "yields"
        if a[i] == '32':
            a[i] = "speedlimit"
        if a[i] == '16':
            a[i] = "roadnarrowing"
        if a[i] == '37':
            a[i] = "roundabout"
        if a[i] == '18':
            a[i] = "nocontrolledcrosswalk"
        if a[i] == '1':
            a[i] = "roadbump"
        if a[i] == '54':
            a[i] = "deadend"

    #print(a)
    """
    a = ["oneway", "oneway", "oneway", "oneway", "oneway", "oneway", "noright", "noright", "noright", "noparking", \
         "noparking", "noparking", "noparking", "noparking", "noparking", "noparking", "noparking", "noparking",
         "noentry", "noentry", "noentry", \
         "noentry", "noentry", "noentry", "noentry", "noentry", "noparkingstop", "noparkingstop", "noparkingstop",
         "noparkingstop", "noparkingstop", "noparkingstop", "parking", \
         "parking", "yields", "yields", "yields", "yields", "yields", "yields", "yields", "speedlimit", "speedlimit",
         "roadnarrowing", "noright", "roundabout", "roundabout", \
         "roundabout", "roundabout", "roundabout", "roundabout", "roundabout", "roundabout", "nocontrolledcrosswalk",
         "nocontrolledcrosswalk", "nocontrolledcrosswalk", \
         "roadbump", "roadbump", "deadend", "deadend"]
    """
        #print(a)
    #random.shuffle(a)
    #print(list.list_traffic_signs)
    listVar = [globals()[k] for k in a]
    #print(listVar)

    for i in range(len(a)):
        if i == 0:
            marker_1 = map_widget.set_marker(51.2258853, 4.4676198, icon= listVar[0]) #oneway
        if i == 1:
            marker_2 = map_widget.set_marker(51.2258768, 4.4691008, icon=listVar[1]) #oneway
        if i == 2:
            marker_3 = map_widget.set_marker(51.2258674, 4.4706527, icon=listVar[2]) #oneway
        if i == 3:
            marker_4 = map_widget.set_marker(51.2258976, 4.4711409, icon=listVar[3]) #oneway
        if i == 4:
            marker_5 = map_widget.set_marker(51.2241365, 4.4662121, icon=listVar[4]) #oneway
        if i == 5:
            marker_6 = map_widget.set_marker(51.2248275, 4.4713782, icon=listVar[5]) #oneway
        if i == 6:
            marker_7 = map_widget.set_marker(51.2257697, 4.4662758, icon=listVar[6]) #no right turn
        if i == 7:
            marker_8 = map_widget.set_marker(51.2249224, 4.4722049, icon=listVar[7]) #no right turn
        if i == 8:
            marker_9 = map_widget.set_marker(51.2258871, 4.4681419, icon=listVar[8]) #no right turn
        if i == 9:
            marker_10 = map_widget.set_marker(51.2239085, 4.4725873, icon=listVar[9]) #no parking
        if i == 10:
            marker_11 = map_widget.set_marker(51.2239891, 4.4717665, icon=listVar[10]) #no parking
        if i == 11:
            marker_12 = map_widget.set_marker(51.2258515, 4.4704112, icon=listVar[11]) #no parking

        if i == 12:
            marker_13 = map_widget.set_marker(51.2249635, 4.4694239, icon=listVar[12])  # no parking

        if i == 13:
            marker_14 = map_widget.set_marker(51.2249450, 4.4702044, icon=listVar[13])  # no parking

        if i == 14:
            marker_15 = map_widget.set_marker(51.2249450, 4.4713577, icon=listVar[14])  # no parking

        if i == 15:
            marker_16 = map_widget.set_marker(51.2258284, 4.4726538, icon=listVar[15])  # no parking

        if i == 16:
            marker_17 = map_widget.set_marker(51.2257966, 4.4720476, icon=listVar[16])  # no parking

        if i == 17:
            marker_18 = map_widget.set_marker(51.2257966, 4.4720476, icon=listVar[17])  # no parking

        if i == 18:
            marker_19 = map_widget.set_marker(51.2249500, 4.4702768, icon=listVar[18])  # no entry

        if i == 19:
            marker_20 = map_widget.set_marker(51.2258419, 4.4663474, icon=listVar[19])  # no entry

        if i == 20:
            marker_21 = map_widget.set_marker(51.2258032, 4.4678870, icon=listVar[20])  # no entry

        if i == 21:
            marker_22 = map_widget.set_marker(51.2259693, 4.4677848, icon=listVar[21])  # no entry

        if i == 22:
            marker_23 = map_widget.set_marker(51.2240446, 4.4689786, icon=listVar[22])  # no entry

        if i == 23:
            marker_24 = map_widget.set_marker(51.2238734, 4.4706872, icon=listVar[23])  # no entry

        if i == 24:
            marker_25 = map_widget.set_marker(51.2260623, 4.4706419, icon=listVar[24])  # no entry

        if i == 25:
            marker_26 = map_widget.set_marker(51.2260824, 4.4704273, icon=listVar[25])  # no entry

        if i == 26:
            marker_27 = map_widget.set_marker(51.2258807, 4.4681957, icon=listVar[26])  # no stopping and parking

        if i == 27:
            marker_28 = map_widget.set_marker(51.2250277, 4.4669790, icon=listVar[27])  # no stopping and parking

        if i == 28:
            marker_29 = map_widget.set_marker(51.2250210, 4.4671560, icon=listVar[28])  # no stopping and parking

        if i == 29:
            marker_30 = map_widget.set_marker(51.2241182, 4.4667052, icon=listVar[29])  # no stopping and parking


        if i == 30:
            marker_31 = map_widget.set_marker(51.2238189, 4.4689843, icon=listVar[30])  # no stopping and parking

        if i == 31:
            marker_32 = map_widget.set_marker(51.2239844, 4.4714247, icon=listVar[31])  # no stopping and parking

        if i == 32:
            marker_33 = map_widget.set_marker(51.2240779, 4.4681229, icon=listVar[32])  # parking

        if i == 33:
            marker_34 = map_widget.set_marker(51.2257414, 4.4722240, icon=listVar[33])  # parking

        if i == 34:
            marker_35 = map_widget.set_marker(51.2257771, 4.4690680, icon=listVar[34])  #yield

        if i == 35:
            marker_36 = map_widget.set_marker(51.2256524, 4.4693759, icon=listVar[35])  #yield

        if i == 36:
            marker_37 = map_widget.set_marker(51.2240530, 4.4688673, icon=listVar[36])  #yield

        if i == 37:
            marker_38 = map_widget.set_marker(51.2240222, 4.4695091, icon=listVar[37])  #yield

        if i == 38:
            marker_39 = map_widget.set_marker(51.2238249, 4.4692927, icon=listVar[38])  #yield

        if i == 39:
            marker_40 = map_widget.set_marker(51.2257637, 4.4727207, icon=listVar[39])  # yield

        if i == 40:
            marker_41 = map_widget.set_marker(51.2259725, 4.4726732, icon=listVar[40])  # yield

        if i == 41:
            marker_42 = map_widget.set_marker(51.2258836, 4.4690406, icon=listVar[41])  # speedlimit

        if i == 42:
            marker_43 = map_widget.set_marker(51.2248184, 4.4722251, icon=listVar[42])  # speedlimit


        if i == 43:
            marker_44 = map_widget.set_marker(51.2257217, 4.4662645, icon=listVar[43])  # road narrowing

        if i == 44:
            marker_45 = map_widget.set_marker(51.2256894, 4.4662986, icon=listVar[44])  # no right turn

        if i == 45:
            marker_46 = map_widget.set_marker(51.2258144, 4.4691972, icon=listVar[45])  # roundabout

        if i == 46:
            marker_47 = map_widget.set_marker(51.2257666, 4.4693008, icon=listVar[46])  # roundabout

        if i == 47:
            marker_48 = map_widget.set_marker(51.2258338, 4.4693437, icon=listVar[47])  # roundabout

        if i == 48:
            marker_49 = map_widget.set_marker(51.2258702, 4.4692696, icon=listVar[48])  # roundabout

        if i == 49:
            marker_50 = map_widget.set_marker(51.2240042, 4.4692597, icon=listVar[49])  # roundabout

        if i == 50:
            marker_51 = map_widget.set_marker(51.2239539, 4.4691980, icon=listVar[50])  # roundabout

        if i == 51:
            marker_52 = map_widget.set_marker(51.2239925, 4.4690988, icon=listVar[51])  # roundabout

        if i == 52:
            marker_53 = map_widget.set_marker(51.2240429, 4.4691766, icon=listVar[52])  # roundabout

        if i == 53:
            marker_54 = map_widget.set_marker(51.2247822, 4.4692823, icon=listVar[53])  # nocontrolcw

        if i == 54:
            marker_55 = map_widget.set_marker(51.2239087, 4.4661801, icon=listVar[54])  # nocontrolcw

        if i == 55:
            marker_56 = map_widget.set_marker(51.2258337, 4.4709226, icon=listVar[55])  # nocontrolcw

        if i == 56:
            marker_57 = map_widget.set_marker(51.2257598, 4.4699577, icon=listVar[56])  # road bump

        if i == 57:
            marker_58 = map_widget.set_marker(51.2239905, 4.4711451, icon=listVar[57])  # road bump

        if i == 58:
            marker_59 = map_widget.set_marker(51.2257152, 4.4661899, icon=listVar[58])  # road bump


        if i == 59:
            marker_60 = map_widget.set_marker(51.2257039, 4.4722217, icon=listVar[59])  # road bump



    #marker_1 = map_widget.set_marker(40.738990481465, -74.03913641685668, icon=test1)
    #marker_2 = map_widget.set_marker(40.7386084, -74.0382459, icon=test2)

    #marker_3 = map_widget.set_marker(40.7382670, -74.0404024, icon=test3)
    #marker_4 = map_widget.set_marker(40.7391937, -74.0410308, icon=test4)

    #marker_5 = map_widget.set_marker(40.7395514, -74.0399364, icon=test5)
    #marker_6 = map_widget.set_marker(40.7372752, -74.0406982, icon=test6)

    #marker_7 = map_widget.set_marker(40.7390962, -74.0403227, icon=test7)

    #my_label['text'] = random.randint(0, 1000)

    #my_label.marker_1['icon'] = stop


    root.after(10000, update)  # run itself again after 1000 ms



    map_widget.pack(fill="both", expand=True)


######################################
update()
root.mainloop()


