#!/usr/bin/env python
import sys, os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn
from tsukuba2017_jrm.dict_tools import loader


def plot_head(dataset, stride = 4):
    # Plot map
    fig = plt.figure()
    plt.scatter(map_data[:, 0], map_data[:, 1], s=0.02, c="k", alpha=0.5, marker='.')

    # Set colormap
    n_h = 629
    colors_h = seaborn.color_palette("hls", n_h)

    # Plot heading
    for key in dataset['filtered']:
        # Unpack the data
        x = dataset['filtered'][key][:, 1]  # x position
        y = dataset['filtered'][key][:, 2]  # y position
        h = dataset['filtered'][key][:, 3]  # heading, [-pi,pi] from x-axis ccw

        # stride controls incremental heading color of trajectory, stride = number time steps between color change
        for i in range(0, len(x), stride):
            # print(i)
            idx = np.asarray((h[i]+np.pi)*100, dtype=np.int) # Convert heading to cmap idx
            plt.plot(x[i:i+2+stride], y[i:i+2+stride], c=colors_h[idx])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        dir = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
        dataset_file = dir + "/sample_data/log_2017-11-06-11-11-40/log_2017-11-06-11-11-40.pk1"
        map_file = dir + "/sample_data/map.txt"
    else:
        dataset_file = sys.argv[1]
        map_file = sys.argv[2]

    # Load data
    dataset = loader.load_dict(dataset_file)
    map_data = loader.load_map(map_file)

    # Plot
    plot_head(dataset)

    plt.xlabel(r'Map $x$ coordinate (m)', size=14)
    plt.ylabel(r'Map $y$ coordinate (m)', size=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.show()
