import pandas as pd
from typing import Dict, List
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


def align_cmso_migration_data(processed_key_file: pd.DataFrame, parameters: Dict, start_time, end_time):
    counter_statistics = 0
    counter_link_data = 0

    key_aligned_objects = pd.DataFrame()
    fish_data_summary = pd.DataFrame()
    link_data_summary = pd.DataFrame()

    aligned_objects = dict()

    for fish_number in processed_key_file["fish number"].unique():

        if (np.isnan(fish_number)):
            continue

        df_single_fish_all_groups = processed_key_file[processed_key_file['fish number'] == fish_number]

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

                vessel_type = row["vessel_type"]

                for link_id in movement_data_["link_id"].unique():
                    link_data_summary.at[counter_link_data, "unique_id"] = str(link_id) + "_fish_%s_%s" % (fish_number,
                                                                                                        vessel_type)
                    link_data_summary.at[counter_link_data, "link_id"] = link_id
                    link_data_summary.at[counter_link_data, "fish_number"] = fish_number
                    link_data_summary.at[counter_link_data, "start_frame"] = movement_data_["frame"].min()
                    link_data_summary.at[counter_link_data, "end_frame"] = movement_data_["frame"].max()
                    link_data_summary.at[counter_link_data, "link_length"] = movement_data_["frame"].max() - \
                                                                          movement_data_["frame"].min()
                    link_data_summary.at[counter_link_data, "vessel_type"] = vessel_type
                    counter_link_data += 1

                movement_data_["vessel_type"] = [vessel_type for x in movement_data_["x"]]

                if len(movement_data['x']) > 1:
                    movement_data = movement_data.append(movement_data_)
                else:
                    movement_data = movement_data_.copy()

            counter_statistics += 1

            fish_data_summary.at[counter_statistics, 'fish_number'] = fish_number
            fish_data_summary.at[counter_statistics, '#tracks'] = 0
            fish_data_summary.at[counter_statistics, 'analysis_group'] = analysis_group
            # fish_data_summary.at[counter_statistics, 'start_track'] = movement_data
            #fish_data_summary.at[counter_statistics, 'dpf'] = key_row['dpf']

            # movement_data_summary.at[counter_statistics, 'filename'] = key_row['filename'].split("/")[-1]
            # movement_data_summary.at[counter_statistics, 'folder'] = "/".join(key_row['filename'].split("/")[0:-1])

    # return key_aligned_objects, aligned_objects, fish_data_summary,track_data_summary
    return fish_data_summary, link_data_summary

def plot_link_lengths(link_data_summary: pd.DataFrame):

    plots = dict()

    for vessel_type in link_data_summary["vessel_type"].unique():

        fig, ax = plt.subplots(figsize=(5, 5))

        link_data_summary_sub = link_data_summary[link_data_summary["vessel_type"] == vessel_type]
        sns.histplot(x = "link_length", data = link_data_summary_sub,  binwidth=15, ax=ax)

        ax.set_xlim(0,150.0)
        ax.set_ylim(0,500.0)

        plots["link_length_%s.pdf" % vessel_type] = fig
        plots["link_length_%s.png" % vessel_type] = fig

    return plots
