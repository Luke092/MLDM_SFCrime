from utilities import *
from featureEngineering import *

import numpy as np
from matplotlib import pyplot as plt
import random

ds_train, intest_train = dsFromCSV("./Dataset/train.csv")
ds, _ = processSDR(ds_train,intest_train)
ds, _, _ = processDate(ds,intest_train)
category = getDictCategories(ds, 39)
category = {y:x for x,y in category.iteritems()}

r = lambda: random.randint(0,255)

colors = category.copy()
for k in colors.keys():
    c = ('#%02X%02X%02X' % (r(),r(),r()))
    if c not in colors.values() + ["#000000"]:
        colors[k] = c
        colors[k] = c

seasons = {'summer':{}, 'winter':{}, 'spring':{}, 'autumn':{}}
hour = {'morning':{}, 'afternoon':{}, 'evening':{}, 'night':{}}

total = len(ds)

for cat in category.keys():
    category[cat] = 0

for row in ds_train:
    cat = row['Category']
    category[cat] += 1
    if cat not in seasons[row['Season']]:
        seasons[row['Season']][cat] = 1
    else:
        seasons[row['Season']][cat] += 1
    if cat not in hour[row['DailyRange']]:
        hour[row['DailyRange']][cat] = 1
    else:
        hour[row['DailyRange']][cat] += 1

cat = category.keys()
rate = category.values()

n = np.arange(len(cat))

plt.figure(1)
barlist = plt.barh(n,rate)
k = 0
for bar in barlist:
    bar.set_color(colors.values()[k])
    k += 1
plt.title("Crime frequency")
plt.yticks(n,cat)

# category = sorted(category.items(), key=lambda(k,v):(v,k))
# category.reverse()
# cat = category.keys()[0:4]
# rate = category.values()[0:4]
#
# n = np.arange(len(cat))
#
# plt.figure(2)
# plt.barh(n,rate)
# plt.title("5 most frequent crime")
# plt.yticks(n,cat)

i = 1
for s in seasons:
    plt.figure(3)

    plt.subplot(2,2,i)
    plt.title(s)
    n = np.arange(len(seasons[s].keys()))
    barlist = plt.barh(n,seasons[s].values())
    k = 0
    for bar in barlist:
        bar.set_color(colors.values()[k])
        k += 1
    # plt.yticks(n,seasons[s].keys())

    i +=1

i = 1
for h in hour:
    plt.figure(4)

    plt.subplot(2,2,i)
    plt.title(h)
    n = np.arange(len(hour[h].keys()))
    barlist = plt.barh(n,hour[h].values())
    k = 0
    for bar in barlist:
        bar.set_color(colors.values()[k])
        k += 1
    # plt.yticks(n,seasons[s].keys())

    i +=1

plt.show()
