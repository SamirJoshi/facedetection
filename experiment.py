#!/usr/bin/env python2
#
# Example to compare the faces in two images.
# Brandon Amos
# 2015/09/29
#
# Copyright 2015-2016 Carnegie Mellon University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time

start = time.time()

import argparse
import cv2
import itertools
import os
import re
import json

import numpy as np
np.set_printoptions(precision=2)

import openface

fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join(fileDir, '..', 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')

parser = argparse.ArgumentParser()

#parser.add_argument('imgs', type=str, nargs='+', help="Input images.")
parser.add_argument('gallery', type=str, nargs=1, help="Input images.")
parser.add_argument('save_loc', type=str, nargs=1, help="Score save dest.")

parser.add_argument('--dlibFacePredictor', type=str, help="Path to dlib's face predictor.",
                    default=os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat"))
parser.add_argument('--networkModel', type=str, help="Path to Torch network model.",
                    default=os.path.join(openfaceModelDir, 'nn4.small2.v1.t7'))
parser.add_argument('--imgDim', type=int,
                    help="Default image dimension.", default=96)
parser.add_argument('--verbose', action='store_true')

args = parser.parse_args()

if args.verbose:
    print("Argument parsing and loading libraries took {} seconds.".format(
        time.time() - start))

start = time.time()
align = openface.AlignDlib(args.dlibFacePredictor)
net = openface.TorchNeuralNet(args.networkModel, args.imgDim)
if args.verbose:
    print("Loading the dlib and OpenFace models took {} seconds.".format(
        time.time() - start))


def getRep(imgPath):
    if args.verbose:
        print("Processing {}.".format(imgPath))
    bgrImg = cv2.imread(imgPath)
    if bgrImg is None:
        raise Exception("Unable to load image: {}".format(imgPath))
    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

    if args.verbose:
        print("  + Original size: {}".format(rgbImg.shape))

    start = time.time()
    bb = align.getLargestFaceBoundingBox(rgbImg)
    if bb is None:
        raise Exception("Unable to find a face: {}".format(imgPath))
    if args.verbose:
        print("  + Face detection took {} seconds.".format(time.time() - start))

    start = time.time()
    alignedFace = align.align(args.imgDim, rgbImg, bb,
                              landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
    if alignedFace is None:
        raise Exception("Unable to align image: {}".format(imgPath))
    if args.verbose:
        print("  + Face alignment took {} seconds.".format(time.time() - start))

    start = time.time()
    rep = net.forward(alignedFace)
    if args.verbose:
        print("  + OpenFace forward pass took {} seconds.".format(time.time() - start))
        print("Representation:")
        print(rep)
        print("-----\n")
    return rep

def select_probes(gallery):
    probes = []

    for root, dirs, files in os.walk(gallery):
        for i in dirs:
            for root, path, files in os.walk(os.path.join(gallery, i)):
                for img in files:
                    probes.append(os.path.join(gallery,i, img))
                    break
                break
        break

    return probes

def test_on_gallery(probe, gallery):
    MAX_IMAGES = 5
    results = {}
    for gal, members, imgs in os.walk(gallery):
        for i in members:
            m = re.search('\d{5}', probe)
            if m.group(0) == i:
                continue
            else:
                results[i] = []
                print "Comparing probe %s with gallery member %s" % (m.group(0), i)
                for root, path, files in os.walk(os.path.join(gallery, i)):
                    #here is where we can limit the gallery size to only compare with 5 or 6 images
                    if len(files) > MAX_IMAGES:
                        count = MAX_IMAGES
                    else:
                        count = len(files)

                    for img in xrange(count):
                        d = getRep(probe) - getRep(os.path.join(gallery,i, files[img]))
                        d = np.dot(d, d) #squared l2 distance
                        #d = random.random()
                        results[i].append(d)
                        #print d

                    print "Best Score: ", min(results[i])
                    results[i] = min(results[i])
                    break
        break

    return results


gallery = args.gallery[0]
probes = select_probes(gallery)

print "Number of Probes: ", len(probes)

scores = {}
for p in probes:
    m = re.search('\d{5}', p)
    scores[m.group(0)] = test_on_gallery(p, gallery)
    print scores

save_dir = args.save_loc[0]
for person, results in scores.iteritems():
    print "Person: ", person
    print "Results: ", results, "\n\n"
    with open(save_dir + '/' + person,'w') as f:
        f.write(json.dumps(results))