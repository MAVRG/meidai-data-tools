#!/usr/bin/env python
import sys, os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn
from tsukuba2017_jrm.dict_tools import loader


def plot_vel(dataset, max_vel = 4, min_vel = 0):
    # Plot map
    fig = plt.figure()
    plt.scatter(map_data[:, 0], map_data[:, 1], s=0.02, c="k", alpha=0.5, marker='.')

    # Set colormap
    n_v = int((max_vel-min_vel)*100+1)
    colors_v = seaborn.color_palette("viridis", n_v)

    # Plot velocity
    for key in dataset['filtered']:
        # Unpack the data
        x = dataset['filtered'][key][:, 1]  # x position
        y = dataset['filtered'][key][:, 2]  # y position
        v = dataset['filtered'][key][:, 4:6] # x-dir, [m/s]
        avg_v = np.mean(np.linalg.norm(v, axis=1))
        if avg_v > max_vel:
            avg_v = 4
        cmap_idx = np.asarray((avg_v - min_vel) * 100, dtype=np.int) # Convert velocity to cmap idx
        plt.plot(x, y, c=colors_v[cmap_idx])

    # Plot colormap
    cmap_map = cm.ScalarMappable(cmap=cm.viridis)
    cmap_map.set_array([min_vel, max_vel])
    cbar = plt.colorbar(cmap_map)
    # cbar = plt.colorbar(m, ticks=[min_vel, 1, 2, 3, max_vel]) # Modifiable ticks
    # cbar.ax.set_yticklabels(['0.2', '1', '2', '3', '$\geq$4'])  # Vertically oriented colorbar
    cbar.set_label(r'Average Speed (m/s)', rotation=270)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        dir = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
        dataset_file = dir + "/sample_data/log_2017-11-03-10-30-10.pk1"
        map_file = dir + "/sample_data/map.txt"
    else:
        dataset_file = sys.argv[1]
        map_file = sys.argv[2]

    min_velocity = 0.2 # Controls minimum of the color palette. Optional, can just be 0.
    max_velocity = 4 # The controls the cap on the maximum velocity for the color palette. We do this because otherwise
        # unusually large velocities make it impossible to see everything else.

    # Load data
    dataset = loader.load_dict(dataset_file)
    map_data = loader.load_map(map_file)

    # Plot
    plot_vel(dataset, max_velocity, min_velocity)

    plt.xlabel(r'Map $x$ coordinate (m)', size=14)
    plt.ylabel(r'Map $y$ coordinate (m)', size=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.show()

