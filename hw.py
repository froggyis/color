import cv2
import matplotlib.pyplot as plt
import numpy as np
import csv
from itertools import chain
import os
from os import walk
from os import listdir
from os.path import isfile, isdir, join
mean_b = 0
mean_g=0
mean_r=0
total_b =0
total_g=0
total_r=0
var_b=0
var_g=0
var_r=0

mypath = "./pictures"
files = listdir(mypath)
try:
    os.mkdir("./output")
except OSError as e:
    print("Directory exists")

for f in files:
    #fullpath = join(mypath, f)
    for i in range(1,3+1):
        source = cv2.imread("./pictures/s" + str(i)+".png")
        target = cv2.imread("./pictures/f" + str(i)+".png")

    img = cv2.imread("./pictures/" + f)
    (b,g,r)=cv2.split(img)
    color = ('b','g','r')


    b = cv2.calcHist([img],[0],None,[256],[0, 256])
    g = cv2.calcHist([img],[1],None,[256],[0, 256])
    r = cv2.calcHist([img],[2],None,[256],[0, 256])

    bb, gg, rr = cv2.split(img)
    BB = list(chain(*bb))
    GG = list(chain(*gg))
    RR = list(chain(*rr))

    for i, col in enumerate(color):
      histr = cv2.calcHist([img],[i],None,[256],[0, 256])
      plt.plot(histr, color = col)
      plt.xlim([0, 256])

    delisted_b = np.array([i[0] for i in b])
    delisted_g = np.array([i[0] for i in g])
    delisted_r = np.array([i[0] for i in r])
    index = np.arange(0,256,1)
    rows = zip(index,delisted_b,delisted_g,delisted_r)

    for i in np.arange(0,256,1):
        mean_b = mean_b +delisted_b[i]*i
        total_b = total_b +delisted_b[i]
        mean_g = mean_g + delisted_g[i] * i
        total_g = total_g + delisted_g[i]
        mean_r = mean_r + delisted_r[i] * i
        total_r = total_r + delisted_r[i]

    for i in np.arange(0,256,1):
        var_b=var_b+( i-(mean_b/total_b) )**2 *delisted_b[i]
        var_g=var_g+( i-(mean_g/total_g) )**2 *delisted_b[i]
        var_r=var_r+( i-(mean_r / total_r))**2 *delisted_b[i]

    with open('./output/'+f+'.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["index","B","G","R"])

        for row in rows:
            writer.writerow(row)
        writer.writerow(["Mean",mean_b/total_b , mean_g/total_g , mean_r/total_r])
        writer.writerow(["STD",np.sqrt(var_b/total_b),np.sqrt(var_g/total_g),np.sqrt(var_r/total_r)])
#plt.show()