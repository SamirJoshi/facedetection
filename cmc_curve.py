# generate a CMC curve

import os
import json
import operator
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def draw_cmc(recog_rates):
    n = len(recog_rates)
    x = np.linspace(1, n, n)


    plt.plot(x, recog_rates, linewidth=2)
    plt.title("CMC Curve")
    plt.xlabel("Rank")
    plt.ylabel("Percent")
    axes = plt.gca()
    axes.set_xlim([1.0, n])
    axes.set_ylim([0.0, 1.0])
    plt.show()

    return 0

def create_recog_rates(base_dir):
    people_dirs = os.listdir(base_dir)
    print ("num peeople:", len(people_dirs))
    n = len(people_dirs)
    recog_rates = np.zeros(n)

    for name in people_dirs:
        curr_path = base_dir + name
        if os.path.exists(curr_path):
            print ("curr path:", curr_path)
            with open(curr_path) as json_data:
                person_dict = json.load(json_data)
                s_pd = sorted(person_dict.items(), key=operator.itemgetter(1))
                print ("SPD:", s_pd)
                index = len(s_pd) - 1
                for i in range(0, len(s_pd)):
                    # print ("spdi:", s_pd[i][0])
                    if s_pd[i][0] == name[:-5]:
                        index = i
                        break
                for i in range(index, len(s_pd)):
                    recog_rates[i] += 1

                # sort all keys by value
                # find index in that list of keys
                # increment for all recog_rates 0 < i < index
    print ("recog rates:", recog_rates)
    recog_rates = recog_rates / n
    draw_cmc(recog_rates)
    return recog_rates
