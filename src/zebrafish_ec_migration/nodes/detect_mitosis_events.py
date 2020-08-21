import pandas as pd
from typing import Dict, List
import numpy as np


def extract_potential_mitosis_events(processed_key_file: pd.DataFrame, parameters: Dict, start_time, end_time):
    trajectory_plots = dict()
    # oriented_trajectory_plots = dict()

    # ex = extract.ExtractData(parameters["data_dir"], key_filename='Key.xlsx')
    # f = extract_features.ExtractFeatures()
    # geo = extract_geometry.ExtractGeometry()

    counter_statistics = 0

    track_data = dict()
    mitosis_events_df = pd.DataFrame()
    mitosis_counter = 0

    time_distance_weight = parameters["time_distance_weight"]

    for fish_number in processed_key_file["fish number"].unique():

        if (np.isnan(fish_number)):
            continue

        df_single_fish_all_groups = processed_key_file[processed_key_file['fish number'] == fish_number]

        for analysis_group in df_single_fish_all_groups["analysis_group"].unique():

            df_single_fish = df_single_fish_all_groups[df_single_fish_all_groups["analysis_group"] == analysis_group]

            #movement_data = pd.DataFrame(data=[], columns=["x", "y", "z", "link_id", "object_id", "vessel_type"])
            for index, row in df_single_fish.iterrows():

                # print("Object data: %s" % row["object_data"])
                if not isinstance(row["object_data"], str):
                    continue

                object_data = pd.read_csv(row["object_data"])
                link_data = pd.read_csv(row["link_data"])
                movement_data_ = pd.merge(object_data, link_data, on='object_id')

                for link_id1 in movement_data_["link_id"].unique():
                    movement_data_link_id1 = movement_data_[movement_data_["link_id"] == link_id1]
                    for link_id2 in movement_data_["link_id"].unique():
                        movement_data_link_id2 = movement_data_[movement_data_["link_id"] == link_id2]

                        min_time_id1 = np.array(movement_data_link_id1["frame"]).min()
                        min_time_id2 = np.array(movement_data_link_id2["frame"]).min()

                        if min_time_id1 < min_time_id2:
                            row_daughter = movement_data_link_id1[movement_data_link_id1["frame"] == min_time_id1].iloc[0]
                            link_daughter = link_id1
                            mother_df = movement_data_link_id2.copy() #[movement_data_link_id1[""] >= min_time_id1]
                            link_mother = link_id2
                        else:
                            row_daughter = movement_data_link_id2[movement_data_link_id2["frame"] == min_time_id2].iloc[0]
                            link_daughter = link_id2
                            mother_df = movement_data_link_id1.copy()
                            link_mother = link_id1


                        dist2_min = np.infty


                        for ind_moth, row_moth in mother_df.iterrows():
                            dist2_ = (row_moth['x'] - row_daughter['x'])**2
                            dist2_ += (row_moth['y'] - row_daughter['y']) ** 2
                            dist2_ += (row_moth['z'] - row_daughter['z']) ** 2
                            dist2_ += time_distance_weight * (row_moth['frame'] - row_daughter['frame']) ** 2
                            if dist2_ < dist2_min:
                                dist2_min = dist2_
                                mitosis_events_df.at[mitosis_counter, "fish_number"] = fish_number
                                mitosis_events_df.at[mitosis_counter, "vessel_type"] = row["vessel_type"]
                                mitosis_events_df.at[mitosis_counter, "link_mother"] = link_mother
                                mitosis_events_df.at[mitosis_counter, "link_daughter"] = link_daughter
                                mitosis_events_df.at[mitosis_counter, "x_mother"] = row_moth['x']
                                mitosis_events_df.at[mitosis_counter, "y_mother"] = row_moth['y']
                                mitosis_events_df.at[mitosis_counter, "z_mother"] = row_moth['z']
                                mitosis_events_df.at[mitosis_counter, "frame_mother"] = row_moth['frame']

                                mitosis_events_df.at[mitosis_counter, "x_daughter"] = row_daughter['x']
                                mitosis_events_df.at[mitosis_counter, "y_daughter"] = row_daughter['y']
                                mitosis_events_df.at[mitosis_counter, "z_daughter"] = row_daughter['z']
                                mitosis_events_df.at[mitosis_counter, "frame_daughter"] = row_daughter['frame']

                                mitosis_events_df.at[mitosis_counter, "dist2"] = dist2_
                                
                        mitosis_counter += 1

        print(mitosis_events_df.head())


    return mitosis_events_df #track_data