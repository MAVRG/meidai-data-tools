#!/usr/bin/env python
import sys, os
from tsukuba2017_jrm.dict_tools import loader
import matplotlib.pyplot as plt


def plot_tracks(dataset):
    # Plot map
    fig = plt.figure()
    plt.scatter(map_data[:, 0], map_data[:, 1], s=0.02, c="k", alpha=0.5, marker='.')

    # Unpack and plot
    for key in dataset['filtered']:
        # Unpack the data
        x = dataset['filtered'][key][:, 1]  # x position
        y = dataset['filtered'][key][:, 2]  # y position
        plt.plot(x, y, '-b')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        dir = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
        dataset_file = dir + "/sample_data/log_2017-11-04-11-38-47.pk1"
        map_file = dir + "/sample_data/map.txt"
    else:
        dataset_file = sys.argv[1]
        map_file = sys.argv[2]

    # Load data
    dataset = loader.load_dict(dataset_file)
    map_data = loader.load_map(map_file)

    # Plot
    plot_tracks(dataset)

    plt.xlabel(r'Map $x$ coordinate (m)', size=14)
    plt.ylabel(r'Map $y$ coordinate (m)', size=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.show()
