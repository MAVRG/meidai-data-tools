#!/usr/bin/env python
import sys, os
import numpy as np
from six.moves import cPickle as pickle
import matplotlib.pyplot as plt

if len(sys.argv) < 3:
    dir = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
    dataset_file = dir + "/sample_data/log_2017-11-06-11-11-40/log_2017-11-06-11-11-40.pk1"
    map_file = dir + "/sample_data/map.txt"
else:
    dataset_file = sys.argv[1]
    map_file = sys.argv[2]

def load_dict(filename):
    with open(filename, 'rb') as f:
        data_dict = pickle.load(f)
    return data_dict


def load_map(filename):
    data = np.genfromtxt(filename, delimiter=',', dtype=np.double)
    return data