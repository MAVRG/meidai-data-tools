import numpy as np
from six.moves import cPickle as pickle

# Combine data in all these directories into one dictionary
directories = ["~/Documents/workspaces/meidai-data-tools/tsukuba2017-jrm/sample_data/log_2017-11-06-11-11-40/",
               "~/Documents/workspaces/meidai-data-tools/tsukuba2017-jrm/sample_data/log_2017-11-06-11-11-40/"
               # You can add several directories, a list of strings separated by a comma as above
    ]

# Pickle file output name
save_fn = "~/Documents/workspaces/meidai-data-tools/tsukuba2017-jrm/sample_data/log_2017-11-06-11-11-40.pk1"

# Dictionary initialization
dataset = {}
dataset['raw_tracks'] = {}      # This holds raw track information
dataset['tracks'] = {}          # This holds b-spline smoothed information
dataset['pointclouds'] = {}     # This holds point cloud
dataset['filtered'] = {}        # This holds filtered tracks
dataset_no = 0                  # Dataset counter to make sure no track ID overlap


def load_file(fn, skipheader=1):
    data = np.genfromtxt(fn, delimiter=',', dtype=np.double, skip_header=skipheader)
    return data


def add_to_dict(dictionary, key, data):
    if key in dictionary:
        dictionary[key] = np.vstack([dictionary[key], data])
    else:
        dictionary[key] = data
    return dictionary


for cd in directories:
    dataset_no += 0.1
    raw_tracks = load_file(cd + '/trajectories.txt')
    smooth_tracks = load_file(cd + '/smoothedtrajectories.txt')
    pointclouds = cd + '/pointcloudobservations.txt'

    # Add raw data to dictionary
    for row in raw_tracks:
        key = row[0] + dataset_no
        data = row[1:]
        data = data.reshape((1,data.shape[0]))
        dataset['raw_tracks'] = add_to_dict(dataset['raw_tracks'], key, data)

    # Add smooth data to dictionary
    for row in smooth_tracks:
        key = row[0] + dataset_no
        data = row[1:]
        data = data.reshape((1, data.shape[0]))
        dataset['tracks'] = add_to_dict(dataset['tracks'], key, data)

    # Add pointclouds to the dictionary
    f = open(pointclouds, "r")
    next(f)
    for line in f:
        line = line.replace('{','[')
        line = line.replace('}',']')
        pointcloud_data = eval(line)
        key = pointcloud_data[0] + dataset_no
        timestamp = pointcloud_data[1]
        pointcloud = np.asarray(eval(pointcloud_data[2]),dtype=np.float32)
        if key not in dataset['pointclouds']:
            dataset['pointclouds'][key] = {}
        dataset['pointclouds'][key][timestamp] = pointcloud

    for key in dataset['tracks']:
        # Unpack data
        data = dataset['tracks'][key]
        time = data[:, 0].reshape(-1, 1)
        num_obs = len(time)
        position = data[:, 1:3]

        # Calculate trajectory time length
        length = np.amax(time) - np.amin(time)

        # Calculate trajectory length
        start = position[0, :]
        end = position[-1, :]
        bird_distance = np.linalg.norm(start - end)
        path_distance = 0  # Will be computed in next loop

        # Calculate heading, velocity and rotational velocity
        heading = np.ndarray(shape=(num_obs - 1, 1), dtype=np.double)
        velocity = np.ndarray(shape=(num_obs - 1, 2), dtype=np.double)
        rotw = np.ndarray(shape=(num_obs - 2, 1), dtype=np.double)

        for i in range(len(velocity)):
            dt = time[i + 1] - time[i]
            dist = position[i + 1, :] - position[i, :]
            path_distance += np.linalg.norm(dist)
            heading[i, 0] = np.arctan2((position[i + 1, 1] - position[i, 1]), (position[i + 1, 0] - position[i, 0]))
            velocity[i, :] = (dist) / dt
            if i > 0:
                dh = heading[i, 0] - heading[i - 1, 0]
                dh = np.arctan2(np.sin(dh), np.cos(dh))
                rotw[i - 1, :] = dh / dt
        avg_velocity = np.mean(np.linalg.norm(velocity[1:, :], axis=1))
        avg_rotw = np.mean(np.abs(rotw))

        # Filters
        # Statistic Filters
        if avg_velocity > 6:
            continue
        if avg_velocity < 0.2:
            continue
        if avg_rotw > 3:
            continue
        if path_distance < 4:
            continue
        if path_distance > 100:
            continue
        if bird_distance < 2:
            continue
        if bird_distance > 100:
            continue
        if length < 2:
            continue
        if length > 60:
            continue

        # Area filters
        if np.mean(position[:,1]) > 50 and np.mean(position[:,1]) < 60 and np.mean(position[:,0]) > -35 and np.mean(position[:,0]) < 15:
            continue
        if np.mean(position[:, 1]) > -40 and np.mean(position[:, 1]) < -5 and np.mean(position[:, 0]) > -10 and np.mean(position[:, 0]) < 70:
            continue
        if np.mean(position[:, 1]) > 30 and np.mean(position[:, 1]) < 45 and np.mean(position[:, 0]) > -50 and np.mean(position[:, 0]) < -20:
            continue
        if np.mean(position[:, 1]) > -5 and np.mean(position[:, 1]) < 45 and np.mean(position[:, 0]) > -30 and np.mean(position[:, 0]) < 10:
            continue
        if np.mean(position[:, 1]) > 49.5 and np.mean(position[:, 1]) < 65 and np.mean(position[:, 0]) > -40 and np.mean(position[:, 0]) < 10:
            continue
        if np.mean(position[:, 1]) > 40 and np.mean(position[:, 1]) < 70 and np.mean(position[:, 0]) > -60 and np.mean(position[:, 0]) < 20 and avg_velocity > 3.5:
            continue

        # Save in dict
        filtered_data = np.ndarray(shape=(num_obs - 2, 7))
        filtered_data = np.concatenate([time[2:], position[2:, :], heading[1:], velocity[1:, :], rotw], axis=1)
        dataset['filtered'][key] = filtered_data

    # Save dictionary to file
with open(save_fn, 'wb') as f:
    print("Saving filtered dataset to {}".format(save_fn))
    pickle.dump(dataset, f)

