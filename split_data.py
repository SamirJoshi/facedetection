#split converted_face_data into training and testing lists
import os
from random import *
import pickle


def get_test_names(pickle_fname):
    if os.path.isfile(pickle_fname):
        print ("Pickled file found returning")
        return pickle.load(open(pickle_fname, "rb"))

    data_dir = "converted_face_data/"

    people_dirs = os.listdir(data_dir)
    print ("number of people:", len(people_dirs))
    print ("people:", people_dirs)
    test_pics = []

    for i in range(0, len(people_dirs)):
        curr_path = data_dir + people_dirs[i] + "/"
        if os.path.isdir(curr_path):
            person_pics = os.listdir(curr_path)
            num_pics = len(person_pics)
            rand_file = person_pics[randint(0, num_pics - 1)]
            test_pics.append(curr_path + rand_file)


    test_set = set(test_pics)
    print ("Test set:", test_set)
    pickle.dump(test_set, open(pickle_fname, "wb"))


get_test_names("testset_names.p")


