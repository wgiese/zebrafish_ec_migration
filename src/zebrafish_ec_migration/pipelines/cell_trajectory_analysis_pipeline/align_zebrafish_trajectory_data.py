import sys
import numpy as np
import matplotlib
import os
matplotlib.use('Agg')
import pylab as plt
import scipy as sci
from scipy import io, stats, spatial
import pandas as pd
import math
import datetime
import seaborn as sns
import logging
from typing import Dict, List
sys.path.append("./src/isv_analysis/classes/")
import yaml
#import extract_data as extract

def align_cmso_trajectory_data(processed_key_file: pd.DataFrame, parameters: Dict, start_time, end_time):
    counter_statistics = 0
    counter_link_data = 0

    #aligned_trajectory_key_file = processed_key_file.copy()
    aligned_trajectory_key_file = pd.DataFrame() #processed_key_file.copy()
    fish_data_summary = pd.DataFrame()
    link_data_summary = pd.DataFrame()

    aligned_link_data = dict()
    aligned_object_data = dict()

    with open("./conf/base/catalog.yml") as file:
        catalog_dict = yaml.load(file, Loader=yaml.FullLoader)

    object_dir = catalog_dict['CMSO_aligned_object_data']['filepath']
    link_dir = catalog_dict['CMSO_aligned_link_data']['filepath']

    for fish_number in processed_key_file["fish_number"].unique():

        if (np.isnan(fish_number)):
            continue

        df_single_fish_all_groups = processed_key_file[processed_key_file['fish_number'] == fish_number]

        for analysis_group in df_single_fish_all_groups["analysis_group"].unique():

            df_single_fish = df_single_fish_all_groups[df_single_fish_all_groups["analysis_group"] == analysis_group]

            print("Aligning fish %s " % fish_number)

            movement_data = pd.DataFrame(data=[],
                                         columns=["x", "y", "z", "frame", "link_id", "object_id", "vessel_type"])

            for index, row in df_single_fish.iterrows():

                # print("Object data: %s" % row["object_data"])
                if not isinstance(row["object_data"], str):
                    continue

                object_data = pd.read_csv(row["object_data"])
                link_data = pd.read_csv(row["link_data"])
                movement_data_ = pd.merge(object_data, link_data, on='object_id')

                #movement_data_ = _align_tracks(movement_data_)

                vessel_type = row["vessel_type"]

                for link_id in movement_data_["link_id"].unique():
                    link_data_summary.at[counter_link_data, "unique_id"] = str(link_id) + "_fish_%s_%s" % (fish_number,
                                                                                                        vessel_type)

                    single_link_data = movement_data_[movement_data_["link_id"] == link_id]

                    link_data_summary.at[counter_link_data, "link_id"] = link_id
                    link_data_summary.at[counter_link_data, "fish_number"] = fish_number
                    link_data_summary.at[counter_link_data, "start_frame"] = single_link_data["frame"].min()
                    link_data_summary.at[counter_link_data, "end_frame"] = single_link_data["frame"].max()
                    link_data_summary.at[counter_link_data, "link_length"] = single_link_data["frame"].max() - \
                                                                          single_link_data["frame"].min()
                    link_data_summary.at[counter_link_data, "vessel_type"] = vessel_type
                    link_data_summary.at[counter_link_data, "analysis_group"] = analysis_group
                    counter_link_data += 1

                movement_data_["vessel_type"] = [vessel_type for x in movement_data_["x"]]

                if len(movement_data['x']) > 1:
                    movement_data = movement_data.append(movement_data_)
                else:
                    movement_data = movement_data_.copy()

            print("rotate fish data")
            movement_data = _rotate_fish(movement_data)

            for vessel_type in movement_data["vessel_type"].unique():

                movement_data_vessel = movement_data[movement_data["vessel_type"]==vessel_type]

                link_filename = "link_fish_%s_%s_%s.csv" % (fish_number, vessel_type, analysis_group)
                object_filename = "object_fish_%s_%s_%s.csv" % (fish_number, vessel_type, analysis_group)
                aligned_link_data[link_filename] = movement_data_vessel[["object_id", "link_id"]]
                aligned_object_data[object_filename] = movement_data_vessel[["object_id", "x", "y", "z", "frame"]]

                aligned_trajectory_key_file.at[counter_statistics, "fish_number"] = fish_number
                aligned_trajectory_key_file.at[counter_statistics, "analysis_group"] = analysis_group
                aligned_trajectory_key_file.at[counter_statistics, "vessel_type"] = vessel_type
                aligned_trajectory_key_file.at[counter_statistics, "object_data"] = link_dir + link_filename
                aligned_trajectory_key_file.at[counter_statistics, "link_data"] = object_dir + object_filename

                fish_data_summary.at[counter_statistics, 'fish_number'] = fish_number
                fish_data_summary.at[counter_statistics, '#tracks'] = 0
                fish_data_summary.at[counter_statistics, 'analysis_group'] = analysis_group
            # fish_data_summary.at[counter_statistics, 'start_track'] = movement_data
            #fish_data_summary.at[counter_statistics, 'dpf'] = key_row['dpf']

            # movement_data_summary.at[counter_statistics, 'filename'] = key_row['filename'].split("/")[-1]
            # movement_data_summary.at[counter_statistics, 'folder'] = "/".join(key_row['filename'].split("/")[0:-1])

                counter_statistics += 1


    # return key_aligned_objects, aligned_objects, fish_data_summary,track_data_summary
    return aligned_trajectory_key_file, fish_data_summary, link_data_summary, aligned_object_data, aligned_link_data

def _align_tracks(df_stat, turn_x=False, turn_y=False):

    df_stat_rot = pd.DataFrame()

    for link_id in df_stat["link_id"].unique():
        link = df_stat[df_stat["link_id"] == link_id]

        #print(link)

        link_x = np.array(link["x"])
        link_y = np.array(link["y"])
        link_z = np.array(link["z"])
        frames = np.array(link["frame"].astype(float))

        link_ids = [str(link_id) for i in range(len(frames))]

        if turn_x:
            link_x = -link_x

        if turn_y:
            link_y = -link_y

        temp = pd.DataFrame({'x': link_x, 'y': link_y, 'z': link_z, 'frame': frames, 'link_id': link_ids},
                            index=range(len(frames)))

        if (len(df_stat_rot) > 1):
            df_stat_rot = df_stat_rot.append(temp, ignore_index=True)
        else:
            df_stat_rot = temp.copy()

    return df_stat_rot


def _rotate_fish(movement_data, rotate_xy=True, rotate_xz=True, rotate_yz=False):

    movement_data_rot = movement_data.copy()

    alpha_rot = 0.0

    if (rotate_xz):
        aorta_data = movement_data_rot[movement_data_rot['vessel_type'] == 'aorta']
        if ("x" in aorta_data.columns) and ("z" in aorta_data.columns):
            if (len(aorta_data) > 3):
                linear_aorta_fit = np.polyfit(x=np.array(aorta_data['x'], dtype=np.float32),
                                              y=np.array(aorta_data['z'], dtype=np.float32), deg=1)

                # calculate rotational angle and matrix
                alpha_rot = -np.arctan(linear_aorta_fit[0])
                alpha_rot = float(alpha_rot)
            else:
                print("not enough data for Aorta to rotate")
        else:
            print("not data for Aorta available")

        movement_data_rot['x'] = np.cos(alpha_rot) * movement_data_rot['x'] - np.sin(alpha_rot) * movement_data_rot['z']
        movement_data_rot['z'] = np.sin(alpha_rot) * movement_data_rot['x'] + np.cos(alpha_rot) * movement_data_rot['z']
        #for index, row in movement_data_rot.iterrows():
        #    x = float(row['x'])
        #    z = float(row['z'])
            #movement_data_rot.at[index, 'x'] = np.cos(alpha_rot) * x - np.sin(alpha_rot) * z
            #movement_data_rot.at[index, 'z'] = np.sin(alpha_rot) * x + np.cos(alpha_rot) * z

    if (rotate_xy):

        aorta_data = movement_data_rot[movement_data_rot['vessel_type'] == 'aorta']
        if ("x" in aorta_data.columns) and ("y" in aorta_data.columns):
            if (len(aorta_data) > 3):
                linear_aorta_fit = np.polyfit(x=np.array(aorta_data['x'], dtype=np.float32),
                                              y=np.array(aorta_data['y'], dtype=np.float32), deg=1)

                # calculate rotational angle and matrix
                alpha_rot = -np.arctan(linear_aorta_fit[0])
                alpha_rot = float(alpha_rot)
            else:
                print("not enough data for Aorta to rotate")
        else:
            print("not data for Aorta available")

        movement_data_rot['x'] = np.cos(alpha_rot) * movement_data_rot['x'] - np.sin(alpha_rot) * movement_data_rot['y']
        movement_data_rot['y'] = np.sin(alpha_rot) * movement_data_rot['x'] + np.cos(alpha_rot) * movement_data_rot['y']
        #for index, row in movement_data_rot.iterrows():
        #    x = float(row['x'])
        #    y = float(row['y'])

            #movement_data_rot.at[index, 'x'] = np.cos(alpha_rot) * x - np.sin(alpha_rot) * yyy
            #movement_data_rot.at[index, 'y'] = np.sin(alpha_rot) * x + np.cos(alpha_rot) * y

    aorta_data = movement_data_rot[movement_data_rot['vessel_type'] == 'aorta']

    x_min = movement_data['x'].min()
    y_min = movement_data['y'].min()
    z_min = movement_data['z'].min()

    y_mean_aorta = aorta_data['y'].mean()

    # print("aorta mean:")
    # print(y_mean_aorta)1
    # print("aorta data:")
    # print(aorta_data['Y'])


    movement_data_rot['x'] = movement_data_rot['x'] - x_min
    movement_data_rot['y'] = movement_data_rot['y'] - y_mean_aorta
    movement_data_rot['z'] = movement_data_rot['z'] - z_min
    for index, row in movement_data_rot.iterrows():
        x = float(row['x'])
        y = float(row['y'])
        z = float(row['z'])

        #movement_data_rot.at[index, 'x'] = x - x_min
        ## movement_data_rot.at[index,'y'] = y - y_min
        #movement_data_rot.at[index, 'y'] = y - y_mean_aorta
        #movement_data_rot.at[index, 'z'] = z - z_min

    return movement_data_rot
