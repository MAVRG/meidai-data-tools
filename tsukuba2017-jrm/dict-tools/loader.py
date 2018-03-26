import sys
import numpy as np
from six.moves import cPickle as pickle

# Load from file or from calling the script
if len(sys.argv) < 3:
    dataset_file = "~/Documents/workspaces/meidai-data-tools/tsukuba2017-jrm/sample_data/log_2017-11-06-11-11-40/log_2017-11-06-11-11-40.pk1"
    map = "~/Documents/workspaces/meidai-data-tools/tsukuba2017-jrm/sample_data/map.txt"
else:
    dataset_file = sys.argv[1]
    map_file = sys.argv[2]

# Loading functions
def load_dict(filename):
    with open(filename, 'rb') as f:
        data_dict = pickle.load(f)
    return data_dict

def load_map(filename):
    data = np.genfromtxt(filename, delimiter=',', dtype=np.double)
    return data

dataset = load_dict(dataset_file)
map_data = load_map(map_file)

# The pickle file holds a dictionary with 4 keys, each holding a dictionary with the trajectory ID as key
# 'raw_tracks' : raw trajectory data
# 'tracks' : b-spline smoothed trajectories
# 'filtered' : b-spline trajectories filtered for false positives with derived heading, velocity and rotational velocity
#   see paper or create_dict for filtering details.
# 'pointclouds': segmented pointclouds for each object
# - dataset['raw_tracks'].keys() (or any other of the above 4 keys) returns all track IDs as keys in that dictionary.
# - dataset['pointclous'][track_ID] is also a dictionary. dataset['pointclous'][track_ID].keys() returns all the timestamps
#       where that dataset was observed, as keys to that dictionary.
# - map_data is a Nx3 matrix of points, centroids for the voxel grid map.
#