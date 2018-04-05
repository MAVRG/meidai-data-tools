#!/usr/bin/env python
import sys, os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import OrderedDict
from tsukuba2017_jrm.dict_tools import loader



def plot_pointcloud_seq(dataset, stride = 4):

    # Plot pointcloud sequence

    # for track_id in dataset['pointclouds']: # Show all point clouds
    for track_id in dataset['filtered']: # Show only unfiltered pointclouds
        num_t = 0
        c = np.random.rand(3, 1)
        ordered_pc = OrderedDict(sorted(dataset['pointclouds'][track_id].items(), key=lambda t: t[0]))
        for timestamp in ordered_pc: # Show all pointclouds
            pointcloud = ordered_pc[timestamp]
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(pointcloud[:,0], pointcloud[:,1], pointcloud[:,2], c=c, marker='o', depthshade=False)
            print(num_t)
            num_t += 1
            if num_t > 4:
                ax.scatter(pppprev_pointcloud[:, 0], pppprev_pointcloud[:, 1], pppprev_pointcloud[:, 2], c=c,
                           edgecolors=c, marker='o', alpha=0.1, depthshade=False)
            if num_t > 3:
                ax.scatter(ppprev_pointcloud[:, 0], ppprev_pointcloud[:, 1], ppprev_pointcloud[:, 2], c=c,
                           edgecolors=c, marker='o', alpha=0.2, depthshade=False)
                pppprev_pointcloud = ppprev_pointcloud
            if num_t > 2:
                ax.scatter(pprev_pointcloud[:, 0], pprev_pointcloud[:, 1], pprev_pointcloud[:, 2], c=c,
                           edgecolors=c, marker='o', alpha=0.4, depthshade=False)
                ppprev_pointcloud = pprev_pointcloud
            if num_t > 1:
                ax.scatter(prev_pointcloud[:, 0], prev_pointcloud[:, 1], prev_pointcloud[:, 2], c=c,
                           edgecolors=c, marker='o', alpha=0.7, depthshade=False)
                pprev_pointcloud = prev_pointcloud
            if num_t > 0:
                prev_pointcloud = pointcloud

            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        dir = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
        dataset_file = dir + "/sample_data/log_2017-11-03-10-30-10.pk1"
    else:
        dataset_file = sys.argv[1]

    # Load data
    dataset = loader.load_dict(dataset_file)

    # Plot
    plot_pointcloud_seq(dataset)
