import pandas as pd
from typing import Dict, List
import numpy as np
import pylab as plt

def plot_migration_data(processed_key_file: pd.DataFrame, parameters: Dict, start_time, end_time):

    trajectory_plots = dict()



    #oriented_trajectory_plots = dict()

    #ex = extract.ExtractData(parameters["data_dir"], key_filename='Key.xlsx')
    #f = extract_features.ExtractFeatures()
    #geo = extract_geometry.ExtractGeometry()

    counter_statistics = 0

    for fish_number in processed_key_file["fish number"].unique():

        if (np.isnan(fish_number)):
            continue

        df_single_fish_all_groups = processed_key_file[processed_key_file['fish number'] == fish_number]

        for analysis_group in df_single_fish_all_groups["analysis_group"].unique():

            df_single_fish = df_single_fish_all_groups[df_single_fish_all_groups["analysis_group"] == analysis_group]

            movement_data = pd.DataFrame(data=[], columns = ["x","y","z","link_id","object_id", "vessel_type"])
            for index,row in df_single_fish.iterrows():

                #print("Object data: %s" % row["object_data"])
                if not isinstance(row["object_data"], str):
                     continue

                object_data = pd.read_csv( row["object_data"])
                link_data = pd.read_csv( row["link_data"])
                movement_data_ = pd.merge(object_data, link_data, on='object_id')

                #vessel_type_ = row["vessel_type"]

                #if vessel_type_ == "isv":
                #    vessel_type = row["isv_type"]
                #else:
                #    vessel_type = vessel_type_

                vessel_type = row["vessel_type"]

                movement_data_["vessel_type"] = [vessel_type for x in movement_data_["x"]]

                if len(movement_data['x']) > 1:
                    movement_data = movement_data.append(movement_data_)
                else:
                    movement_data = movement_data_.copy()




            #print("=================================================")
            #print("fish number: %s" % int(fish_number))
            #print("=================================================")

            #movement_data, key_row = ex.get_movement_data(fish_number, df_key, parameters["data_dir"], start_time,
            #                                              end_time, analysis_group)

            #print(parameters["data_dir"])

            #if (np.isnan(key_row['dpf'])):
                # print("Error !!!!!!!!!!!!!!!")
            #    print("Fish %s does not have a dpf entry!!!!!!!!!!!!!!!" % fish_number)
            #    continue

            #print("=========================================")
            #print("movement_data (head)")
            #print("=========================================")
            #print(movement_data.head())

            #cwd = os.getcwd()
            #print("cwd: %s" % cwd)

            #'''
            #rotate fish
            #'''
            if (len(movement_data['x']) < 3):
                continue

            trajectory_plots["trajectories_fish_%s.pdf" % fish_number] = _plot_trajectory(movement_data,parameters)
            trajectory_plots["trajectories_fish_%s.png" % fish_number] = _plot_trajectory(movement_data,parameters)

            #movement_data = geo.rotate_fish(movement_data, rotate_XY=True, rotate_XZ=True)

            #oriented_trajectory_plots["oriented_trajectories_fish_ % s.pdf" % fish_number] = geo.plot_trajectories2(movement_data,parameters)
            #oriented_trajectory_plots["oriented_trajectories_fish_ % s.png" % fish_number] = geo.plot_trajectories2(movement_data,parameters)


    return trajectory_plots#, oriented_trajectory_plots

def _plot_trajectory(movement_data, parameters):

    x_min = movement_data['x'].min()
    y_min = movement_data['y'].min()
    z_min = movement_data['z'].min()

    x_max = movement_data['x'].max()
    y_max = movement_data['y'].max()
    z_max = movement_data['z'].max()

    max_ext = max(x_max - x_min, y_max - y_min, z_max - z_min)

    plt.rcParams.update({'font.size': 16})
    fig, axarr = plt.subplots(1, 3, figsize=(18, 6))

    legend_aorta = True
    legend_aISV = True
    legend_either = True
    legend_vISV = True
    legend_dlav = True

    vessel_type_colors = parameters["vessel_type_colors"]

    for vessel_type in movement_data['vessel_type'].unique():
        vessel_df = movement_data[movement_data['vessel_type'] == vessel_type]
        for link_id in vessel_df["link_id"].unique():
            temp = vessel_df[vessel_df["link_id"] == link_id]

            mean_x_link_id = temp["x"].mean()
            mean_y_link_id = temp["y"].mean()
            mean_z_link_id = temp["z"].mean()

            if (len(temp) < 2):
                continue

            x_pos = np.array(temp["x"])
            x_pos = x_pos - x_min - 0.5 * (x_max - x_min) + 0.5 * max_ext
            y_pos = np.array(temp["y"])
            y_pos = y_pos - y_min - 0.5 * (y_max - y_min) + 0.5 * max_ext
            z_pos = np.array(temp["z"])
            z_pos = z_pos - z_min - 0.5 * (z_max - z_min) + 0.5 * max_ext

            mean_x_link_id = mean_x_link_id - x_min - 0.5 * (x_max - x_min) + 0.5 * max_ext
            mean_y_link_id = mean_y_link_id - y_min - 0.5 * (y_max - y_min) + 0.5 * max_ext
            mean_z_link_id = mean_z_link_id - z_min - 0.5 * (z_max - z_min) + 0.5 * max_ext
            color = vessel_type_colors[vessel_type]

            axarr[0].plot(x_pos, y_pos, color)
            axarr[0].text(mean_x_link_id, mean_y_link_id, link_id, fontsize=7)
            axarr[0].set_title("x-y-projection with link IDs")
            #axarr[0].text(100, 100, "link_id: %s" % link_id, fontsize=3)
            axarr[0].set_xlabel("x")
            axarr[0].set_ylabel("y")
            axarr[0].set_xlim(0, max_ext)
            axarr[0].set_ylim(0, max_ext)



            if legend_dlav and (vessel_type == 'dlav'):
                axarr[1].plot(x_pos, z_pos, color, label=vessel_type)
                legend_dlav = False
            if legend_aorta and (vessel_type == 'aorta'):
                axarr[1].plot(x_pos, z_pos, color, label=vessel_type)
                legend_aorta = False
            if legend_aISV and (vessel_type == 'aISV'):
                axarr[1].plot(x_pos, z_pos, color, label=vessel_type)
                legend_aISV = False
            if legend_either and (vessel_type == 'either'):
                axarr[1].plot(x_pos, z_pos, color, label=vessel_type)
                legend_either = False
            if legend_vISV and (vessel_type == 'vISV'):
                axarr[1].plot(x_pos, z_pos, color, label=vessel_type)
                legend_vISV = False
            else:
                axarr[1].plot(x_pos, z_pos, color)

            axarr[1].set_xlabel("x")
            axarr[1].set_ylabel("z")
            axarr[1].set_xlim(0, max_ext)
            axarr[1].set_ylim(0, max_ext)
            axarr[1].set_title("x-z-projection")

            axarr[2].plot(y_pos, z_pos, color)
            axarr[2].set_xlabel("y")
            axarr[2].set_ylabel("z")
            axarr[2].set_xlim(0, max_ext)
            axarr[2].set_ylim(0, max_ext)
            axarr[2].set_title("y-z-projection")

    axarr[1].legend()

    plt.tight_layout()

    return fig
