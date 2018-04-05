#!/usr/bin/env python
import sys, os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tsukuba2017_jrm.dict_tools import loader
from collections import OrderedDict


def plot_pointcloud(dataset, stride = 4):

    # Plot pointclouds
    # for track_id in dataset['pointclouds']: # Show all point clouds
    for track_id in dataset['filtered']: # Show only unfiltered pointclouds
        c = np.random.rand(3, 1)
        ordered_pc = OrderedDict(sorted(dataset['pointclouds'][track_id].items(), key=lambda t: t[0]))
        for timestamp in ordered_pc: # Show all pointclouds
            pointcloud = ordered_pc[timestamp]
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(pointcloud[:,0], pointcloud[:,1], pointcloud[:,2], c=c, edgecolors=c, marker='o', depthshade=False)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            # ax.axis('square')
            plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        dir = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
        dataset_file = dir + "/sample_data/log_2017-11-04-11-38-47.pk1"

    else:
        dataset_file = sys.argv[1]

    # Load data
    dataset = loader.load_dict(dataset_file)

    # Plot
    plot_pointcloud(dataset)
