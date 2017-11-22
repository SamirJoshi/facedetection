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

    for name in people_dirs:
        curr_path = base_dir + name
        if os.path.exists(curr_path):
            print ("curr path:", curr_path)
            with open(curr_path) as json_data:
                person_dict = json.load(json_data)
                for key in person_dict:
                    print ("name: ", name, ", key: ", key)
                    if key == name[:-5]:
                        genuine_dist.append(person_dict[key])
                    else:
                        impost_dist.append(person_dict[key])

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
    print ("g x:", g_x)
    plt.plot(g_x, mlab.normpdf(g_x, g_mean, g_std), linewidth=2)
    plt.plot(i_x, mlab.normpdf(i_x, i_mean, i_std), linewidth=2)
    plt.title("Genuine and Imposter Distributions")
    plt.xlabel("Distance")
    axes = plt.gca()
    axes.set_xlim([0.0, 1.0])
    axes.set_ylim([0.0, 100])
    plt.show()

    return 0

if __name__ == "__main__":
    # dummy data for testing plotters
    genuine = [.1, .11, .1, .09, .1]
    imposter = [.51, .5, .51, .49, .5, .5, .52, .5, .51, .5, .49, .51, .49, .5, .5, .49, .48, .5, .51, .49]
    # end dummy data for testing plotters
    base_dir = "recog_results/"
    [g, i] = get_distributions(base_dir)
    draw_hist(genuine, imposter)
    draw_ROC(genuine, imposter)
    r = create_recog_rates(base_dir)


    # TO-DO
    # [] divide all the scores by 4
