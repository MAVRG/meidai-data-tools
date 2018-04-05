## 2017 Tsukuba Challenge Dataset Tools

This is a set of tools to be used alongside the [2017 Tsukuba Challenge Dataset](https://goo.gl/k2pGHE). This dataset contains 3D Lidar (HDL-32) dynamic object detection and tracking data. The objects are largely pedestrians, some cyclists and others, in particular robots.

The tracking data of 15 runs is given, raw data and convenient pickle files. A pickle file containing all available data is also available. In each pickle file, you will find raw tracking information, b-spline smoothed, and filtered tracks. Segmented pointclouds of the detected dynamic objects are also given. A sample pickle file is given, as well as the Tsukuba lidar map, is given in this package. Please follow the above link for the raw data and complete pickle files.

### Packages
##### dict_tools
The dictionary tools *dict_tools* package contains:
*   **loader.py** : simple functions to load the pickle files and maps.
*   **create_dict.py** : function showing how to create dictionaries from the raw data, as well as the filtering parameters used in our work.

##### vis_tools
Tools to visualize the data are distributed in *vis_tools*:
*   **plot_tracks.py** : simple function that plots the tracks in 2D as well as the map.
*   **plot_velocity.py** : plots tracks colored by velocity, with some parameters controlling colormap.
*   **plot_headings.py** : plots tracks by heading with cyclical colormap.
*   **plot_pointclouds.py** : plots segmented pointcloud sequentially.
*   **plot_pointcloud_seq.py** : plots segmented pointcloud sequentially also keeping around old pointclouds with increasing alpha to show some history.

Easy to use functions from command line or from your favorite IDE.