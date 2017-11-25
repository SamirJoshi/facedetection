import os
import json
from roc_curve import draw_ROC
from cmc_curve import create_recog_rates, draw_cmc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.optimize import curve_fit

def get_distributions(base_dir):
    genuine_dist = []
    impost_dist = []

    people_dirs = os.listdir(base_dir)
    print ("num peeople:", len(people_dirs))
    num_people = len(people_dirs)

    for name in people_dirs:
        curr_path = base_dir + name
        if os.path.exists(curr_path) and curr_path != "recog_results/.DS_Store":
            with open(curr_path, "r") as json_data:
                person_dict = json.loads(json_data.read())
                for key in person_dict:
                    if key == name:
                        genuine_dist.append(person_dict[key] / float(4.0))
                    else:
                        impost_dist.append(person_dict[key] / float(4.0))

    print ("size gen:", len(genuine_dist))
    print ("size impost:", len(impost_dist))

    return [genuine_dist, impost_dist]

def draw_hist(genuine, impost):
    g_mean = np.mean(genuine)
    i_mean = np.mean(impost)
    g_std = np.std(genuine)
    i_std = np.std(impost)
    g_x = np.linspace(g_mean - 5 * g_std, g_mean + 5 * g_std, 100)
    i_x = np.linspace(i_mean - 5 * i_std, i_mean + 5 * i_std, 100)
    print ("g mean:", g_mean)
    print ("g std:", g_std)
    print ("i mean:", i_mean)
    print ("i std:", i_std)
    plt.plot(g_x, mlab.normpdf(g_x, g_mean, g_std), linewidth=2)
    plt.plot(i_x, mlab.normpdf(i_x, i_mean, i_std), linewidth=2)
    plt.title("Genuine and Imposter Distributions")
    plt.xlabel("Distance")
    axes = plt.gca()
    axes.set_xlim([0.0, 1.0])
    # axes.set_ylim([0.0, 100])
    plt.show()

    return 0

if __name__ == "__main__":
    base_dir = "recog_results/"
    [g, i] = get_distributions(base_dir)
    draw_hist(g, i)
    draw_ROC(g, i)
    r = create_recog_rates(base_dir)
