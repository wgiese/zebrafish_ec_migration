import pandas as pd
from typing import Dict, List
import numpy as np
import pylab as plt

def compute_trajectory_features(aligned_trajector_key_file: pd.DataFrame, parameters: Dict, start_time, end_time):

    features_df = pd.DataFrame()
    data_statistics_df = pd.DataFrame()
    counter = 0
    frame_interval = 12.0
    time_interval = frame_interval*10.0/60.0

    for fish_number in aligned_trajector_key_file["fish_number"].unique():

        if (np.isnan(fish_number)):
            continue

        df_single_fish_all_groups = aligned_trajector_key_file[aligned_trajector_key_file['fish_number'] == fish_number]

        for analysis_group in df_single_fish_all_groups["analysis_group"].unique():

            df_single_fish = df_single_fish_all_groups[df_single_fish_all_groups["analysis_group"] == analysis_group]

            movement_data = pd.DataFrame(data=[],
                                         columns=["x", "y", "z", "frame", "link_id", "object_id", "vessel_type"])
            for index, row in df_single_fish.iterrows():

                object_data = pd.read_csv(row["object_data"])
                link_data = pd.read_csv(row["link_data"])
                movement_data = pd.merge(object_data, link_data, on='object_id')

                for link_id in movement_data["link_id"].unique():
                    movement_data_ = movement_data[movement_data["link_id"]==link_id]
                    dist = movement_data_.diff(frame_interval).fillna(np.nan)
                    dist_step = movement_data_.diff(1).fillna(np.nan)

                    movement_data_['step_size'] = np.sqrt(dist.x**2 + dist.y**2)
                    movement_data_['step_size_x'] = dist_step.x
                    movement_data_['step_size_y'] = dist_step.y
                    movement_data_['velocity_micron_per_h'] = np.sqrt(dist.x**2 + dist.y**2)/time_interval
                    movement_data_['vd_velocity_micron_per_h'] = -dist.y/time_interval
                    #movement_data_['step_size_y'] = dist.y
                    movement_data_['fish_number'] = fish_number
                    movement_data_['vessel_type'] = row['vessel_type']
                    movement_data_['analysis_group'] = analysis_group
                    movement_data_['time_in_hpf'] = 24.0 + 10.0 * movement_data_['frame']/60.0
                    movement_data_['time_in_min'] = 10 * movement_data_['frame']

                    if len(features_df.columns) > 1:
                        features_df = movement_data_.append(features_df)
                    else:
                        features_df = movement_data_.copy()

    return features_df#, data_statistics_df