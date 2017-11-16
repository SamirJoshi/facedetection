# generate an ROC curve
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def calculateRateTuples(thresh, auth, impost):
    return sum(i <= thresh for i in auth)/float(len(auth)), sum(i <= thresh for i in impost)/float(len(impost))

def draw_ROC(auth, impost):
    matching_rates = [calculateRateTuples(x/100.0, auth, impost) for x in range(100)]

    for x in range(100):
        print "Threshhold: " + (" " if x % 10 == 0 else "") + str(x/100.0) + ", True Match: " + str(matching_rates[x][0]) + ", False Match Rate: " + str(matching_rates[x][1])

    np_matching_rates = np.array(matching_rates)
    x = np_matching_rates[:, 1]
    y = np_matching_rates[:, 0]

    plt.scatter(x , y, color='r', s=50)
    plt.plot(x , y, color='b', linewidth=2)
    plt.title("ROC Curve")
    plt.xlabel("False Match Rate")
    plt.ylabel("Verification Rate")

    axes = plt.gca()
    axes.set_xlim([-0.01, 1.0])
    axes.set_ylim([0.0, 1.01])

    plt.show()


if __name__ == "__main__":
    genuine = [.1, .11, .1, .09, .1]
    imposter = [.51, .5, .51, .49, .5, .5, .52, .5, .51, .5, .49, .51, .49, .5, .5, .49, .48, .5, .51, .49]
    draw_ROC(genuine, imposter)
