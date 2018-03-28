#!/usr/bin/env python
import sys, os
import numpy as np
from six.moves import cPickle as pickle

# The pickle file holds a dictionary with 4 keys, each holding a dictionary with the trajectory ID as key
# 'raw_tracks' : raw trajectory data
# 'tracks' : b-spline smoothed trajectories
# 'filtered' : b-spline trajectories filtered for false positives with derived heading, velocity and rotational velocity
#   see paper or create_dict for filtering details.
# 'pointclouds': segmented pointclouds for each object
# - dataset['raw_tracks'].keys() (or any other of the above 4 keys) returns all track IDs as keys in that dictionary.
# - dataset['pointclouds'][track_ID] is also a dictionary. dataset['pointclous'][track_ID].keys() returns all the timestamps
#       where that dataset was observed, as keys to that dictionary.
# - map_data is a Nx3 matrix of points, centroids for the voxel grid map.
# - dataset['raw_tracks'][track_ID] : N x 7
#       [timestamp, position_x, position_y, position_z, orientation_w, variance_x, variance_y]
#       - approximating the 2D particle filter distrubution as a gaussian, we get the above variance
# - dataset['tracks'][trackID] : N x 3
#       [obstime, positionx, positiony]
# - dataset['filtered'] : N x 7
#       [timestamp. position_x, position_y, heading, velocity_x, velocity_y, rotation_w]
#       heading is from +x-axis, ccw [-pi, pi
# - dataset['pointclouds'][trackID][timestamp] : K x 3
#       [x, y, z]


# Loading functions
def load_dict(filename):
    with open(filename, 'rb') as f:
        data_dict = pickle.load(f)
    return data_dict


def load_map(filename):
    data = np.genfromtxt(filename, delimiter=',', dtype=np.double)
    return data


if __name__ == "__main__":
    # Load from file or from calling the script
    if len(sys.argv) < 3:
        dir = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
        dataset_file = dir + "/sample_data/log_2017-11-06-11-11-40/log_2017-11-06-11-11-40.pk1"
        map_file = dir + "/sample_data/map.txt"
    else:
        dataset_file = sys.argv[1]
        map_file = sys.argv[2]

    dataset = load_dict(dataset_file)
    map_data = load_map(map_file)

# Easiest way to load data from any of the dictionaries:

    for key in dataset['filtered']:
        # Unpack the data
        t = dataset['filtered'][key][:, 0] # timestamp
        x = dataset['filtered'][key][:, 1] # x position
        y = dataset['filtered'][key][:, 2] # y position
        h = dataset['filtered'][key][:, 3] # heading, [-pi,pi] from x-axis ccw
        v_x = dataset['filtered'][key][:, 4] # x-dir, [m/s]
        v_y = dataset['filtered'][key][:, 5] # y-dir, [m/s]
        rotw = dataset['filtered'][key][:, 6] # [rad/s]

        # Do stuff with the data
        print('Have fun!')