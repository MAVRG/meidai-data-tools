#!/usr/bin/env python
import sys, os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn
from tsukuba2017_jrm.dict_tools import loader


def plot_pointcloud(dataset, stride = 4):

    # Plot heading
    for track_id in dataset['pointclouds']:
        for timestamp in dataset['pointclouds'][track_id]:
            pointcloud = dataset['pointclouds'][track_id][timestamp]
                plt.scatter(xs, ys, zs, c=c, marker=m)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        dir = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
        dataset_file = dir + "/sample_data/log_2017-11-06-11-11-40/log_2017-11-06-11-11-40.pk1"
    else:
        dataset_file = sys.argv[1]

    # Load data
    dataset = loader.load_dict(dataset_file)

    # Plot
    plot_pointcloud(dataset)

    plt.axis('off')
