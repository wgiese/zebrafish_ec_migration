# Copyright 2020, Wolfgang Giese, Andre de la Rosa
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# See the License for the specific language governing permissions and
# limitations under the License.


import pandas as pd
import numpy as np
from typing import Dict, List
import yaml
import os

def _read_IMARIS_cell_migration_data(filename):
    '''

    '''

    if (not os.path.isfile(filename)):
        return pd.DataFrame()

    print("Open file: %s" % filename)

    sep = _count_delimiters(open(filename, "r", encoding="ISO-8859-1").read())

    num_lines = sum(1 for line in open(filename, encoding="ISO-8859-1"))

    if num_lines < 10:
        return pd.DataFrame()

    f = open(filename, "r", encoding="ISO-8859-1")
    skip_row = 0

    for line in f.readlines():
        row = line.split(sep)
        if len(row) > 0:
            if row[0] == "Variable":
                break
            if row[0] == "Position X":
                break
        skip_row += 1

    f.close()

    if skip_row > 10:
        return pd.DataFrame()

    df_stat = pd.read_csv(filename, skiprows=skip_row, sep=sep, encoding="ISO-8859-1")



    return df_stat


def _count_delimiters(s):
    valid_seps = [' ', '|', ',', ';', '\t']
    cnt = {' ': 0, '|': 0, ',': 0, ';': 0, '\t': 0}
    for c in s:
        if c in valid_seps: cnt[c] = cnt[c] + 1

    tup = [(value, key) for key, value in cnt.items()]

    if (cnt[';'] > 0):
        print("File contains semicolons, check if opened correctly! %s")
        print(cnt)

    return max(tup)[1]


def CMSO_movement_data(imaris_key_file: pd.DataFrame, parameters: Dict, start_time, end_time) -> pd.DataFrame:


    processed_key_file = imaris_key_file.copy()


    imaris_data = dict()

    unified_imaris = dict()

    object_data = dict()

    link_data = dict()

    tracking_data = dict()

    json_meta = dict()

    #json_meta["test.json"] = {"cmso_space_unit": "micron", "cmso_time_unit": "frame"}

    object_data_statistics = pd.DataFrame()
    counter = 1

    with open("./conf/base/catalog.yml") as file:
        catalog_dict = yaml.load(file, Loader=yaml.FullLoader)

    cmso_object_dir = catalog_dict['CMSO_object_data']['filepath']
    cmso_link_dir = catalog_dict['CMSO_link_data']['filepath']
    cmso_track_dir = catalog_dict['CMSO_track_data']['filepath']

    for fish_number in imaris_key_file["fish_number"].unique():

        if (np.isnan(fish_number)):
            continue

        df_single_fish_all_groups = imaris_key_file[imaris_key_file['fish_number'] == fish_number]

        for analysis_group in df_single_fish_all_groups["analysis_group"].unique():

            df_single_fish = df_single_fish_all_groups[df_single_fish_all_groups["analysis_group"] == analysis_group]

            print("=================================================")
            print("fish number: %s" % int(fish_number))
            print("=================================================")

            print(df_single_fish)

            object_filename = 'objects_fish_%s_%s.csv' % (int(fish_number), analysis_group)
            #object_data[filename] = objects_d am not sharing that piece about Kate to be disparaging about herf

            object_data_statistics.at[counter, "filename"] = object_filename

            for index, row in df_single_fish.iterrows():

                filename = parameters["data_dir"] + row["filename"]

                #print("FILENAME: %s" % filename)

                imaris_df = _read_IMARIS_cell_migration_data(filename)

                object_data_statistics.at[counter,"imaris_df.size"] = imaris_df.size
                if imaris_df.size <= 1:
                   print("ERROR: Imaris df too small")
                   print(imaris_df.head())
                else:
                    imaris_data['tracks_fish_%s_%s_%s.csv' % (
                    analysis_group, int(fish_number), row["vessel_type"])] = imaris_df
                    unified_df = _unify_tidy_wide_IMARIS_formats(imaris_df)
                    print(unified_df.head())
                    if unified_df.size <= 1:
                        print("ERROR: Unified df too small")
                        print(unified_df.head())
                    else:
                        object_data_statistics.at[counter, "unified_df.size"] = unified_df.size

                        imaris_data['tracks_fish_%s_%s_%s.csv' % (
                            analysis_group, int(fish_number), row["vessel_type"])] = imaris_df
                        unified_imaris['tracks_fish_%s_%s_%s.csv' % (
                        analysis_group, int(fish_number), row["vessel_type"])] = unified_df
                        object_filename = 'objects_fish_%s_%s_%s.csv' % (
                            analysis_group, int(fish_number), row["vessel_type"])
                        object_data[object_filename] = unified_df[["object_id", "x", "y", "z", "frame"]]
                        link_filename = 'link_fish_%s_%s_%s.csv' % (analysis_group, int(fish_number), row["vessel_type"])
                        link_df = unified_df[["object_id", "track_id"]]
                        link_df = link_df.rename(columns={"track_id": "link_id"})
                        link_data[link_filename] = link_df

                        json_filename = "meta_fish_%s_%s_%s.json" % (analysis_group, int(fish_number), row["vessel_type"])

                        json_meta[json_filename] = {"cmso_space_unit": "micron",
                                                               "cmso_time_unit": "frame",
                                                               "name": "cmso_tracks_zebrafish_%s" % analysis_group,
                                                               "resources": [
                                                                   {
                                                                       "name" : "objects_table_fish_%s_%s_%s" % (
                                                                        analysis_group, int(fish_number), row["vessel_type"]),
                                                                       "path": "../CMSO_object_data/%s" % object_filename,
                                                                       "schema": {
                                                                           "fields": [
                                                                               {
                                                                                   "constraints": {
                                                                                       "unique": True
                                                                                   },
                                                                                   "description": "",
                                                                                   "format": "default",
                                                                                   "name": "object_id",
                                                                                   "title": "",
                                                                                   "type": "integer"
                                                                               },
                                                                               {
                                                                                   "description": "",
                                                                                   "format": "default",
                                                                                   "name": "frame",
                                                                                   "title": "",
                                                                                   "type": "integer"
                                                                               },
                                                                               {
                                                                                   "description": "",
                                                                                   "format": "default",
                                                                                   "name": "x",
                                                                                   "title": "",
                                                                                   "type": "number"
                                                                               },
                                                                               {
                                                                                   "description": "",
                                                                                   "format": "default",
                                                                                   "name": "y",
                                                                                   "title": "",
                                                                                   "type": "number"
                                                                               },
                                                                               {
                                                                                   "description": "",
                                                                                   "format": "default",
                                                                                   "name": "z",
                                                                                   "title": "",
                                                                                   "type": "number"
                                                                               },
                                                                           ],
                                                                           "primaryKey": "cmso_object_id"
                                                                       }
                                                                   },
                                                                   {
                                                                       "name": "objects_table_fish_%s_%s_%s" % (
                                                                           analysis_group, int(fish_number),
                                                                           row["vessel_type"]),
                                                                       "path": "../CMSO_link_data/%s" % link_filename,
                                                                       "schema": {
                                                                           "fields": [
                                                                               {
                                                                                   "description": "",
                                                                                   "format": "default",
                                                                                   "name": "link_id",
                                                                                   "title": "",
                                                                                   "type": "integer"
                                                                               },
                                                                               {
                                                                                   "description": "",
                                                                                   "format": "default",
                                                                                   "name": "object_id",
                                                                                   "title": "",
                                                                                   "type": "integer"
                                                                               }
                                                                           ],
                                                                           "foreignKeys": [
                                                                               {
                                                                                   "fields": "cmso_object_id",
                                                                                   "reference": {
                                                                                       "datapackage": "",
                                                                                       "fields": "object_id",
                                                                                       "resource": "cmso_objects_table"
                                                                                   }
                                                                               }
                                                                           ]
                                                                       }
                                                                   }
                                                               ]

                                                               }

                        track_counter = 0

                        track_df = pd.DataFrame()
                        for TrackID in unified_df["track_id"].unique():
                            track_df.at[track_counter, "link_id"] = TrackID
                            track_df.at[track_counter, "track_id"] = TrackID
                            track_counter += 1                # _read_IMARIS_cell_migration_data()
                        track_filename = 'tracks_fish_%s_%s_%s.csv' % (analysis_group, int(fish_number), row["vessel_type"])
                        tracking_data[track_filename] = track_df

                        processed_key_file.at[index,"link_data"] = cmso_link_dir + link_filename
                        processed_key_file.at[index, "track_data"] = cmso_track_dir + track_filename
                        processed_key_file.at[index, "object_data"] = cmso_object_dir + object_filename
        counter += 1

    processed_key_file = processed_key_file[processed_key_file["object_data"] != np.nan]

    processed_key_file = processed_key_file.drop('filename', 1)

    return processed_key_file, imaris_data, object_data, object_data_statistics, link_data, tracking_data, json_meta

    # print("The following parameters are used: ")
    # print(parameters)

    # time_points = np.arange(start_time,end_time,parameters["time_resolution"])

    ##feature_dir = "./data/02_intermediate/" + "/feature_files_%s_%s_%s/" % (start_time,end_time,parameters["dt"])
    # movement_data_dir = "./data/03_intermediate/" + "/movement_data_%s_%s/" % (start_time,end_time)
    ##trajectory_dir = "./data/02_intermediate/" + "/plot_trajectories_%s_%s_%s/" % (start_time,end_time,parameters["dt"])

    # try:
    ## Create target Directory
    # os.mkdir(feature_dir)
    # print("Directory " , feature_dir ,  " Created ")
    # except FileExistsError:
    # print("Directory " , feature_dir ,  " already exists")

    # try:
    ## Create target Directory
    # os.mkdir(movement_data_dir)
    # print("Directory " , movement_data_dir ,  " Created ")
    # except FileExistsError:
    # print("Directory " , movement_data_dir ,  " already exists")

    # try:
    ## Create target Directory
    # os.mkdir(trajectory_dir)
    # print("Directory " , trajectory_dir ,  " Created ")
    # except FileExistsError:
    # print("Directory " , trajectory_dir ,  " already exists")

    # features_df = pd.DataFrame()

    ##file_statistics_df = pd.DataFrame(data=[], index=[], columns=['#tracks','mean_track_length','max_step'])
    # file_statistics_df = pd.DataFrame()

    # df_key = preprocessed_key_file.copy()

    # ex = extract.ExtractData(parameters["data_dir"], key_filename = 'Key.xlsx')
    # f = extract_features.ExtractFeatures()
    # geo = extract_geometry.ExtractGeometry()

    # counter_statistics = 0

    # for fish_number in df_key["fish number"].unique():

    # if (np.isnan(fish_number)):
    # continue

    # df_single_fish_all_groups = df_key[df_key['fish number'] == fish_number]

    # for analysis_group in  df_single_fish_all_groups["analysis_group"].unique():

    # df_single_fish = df_single_fish_all_groups[df_single_fish_all_groups["analysis_group"] == analysis_group]

    # print("=================================================")
    # print("fish number: %s" % int(fish_number))
    # print("=================================================")

    # movement_data, key_row = ex.get_movement_data(fish_number, df_key, parameters["data_dir"], start_time, end_time, analysis_group)

def _unify_tidy_wide_IMARIS_formats(imaris_df):

    unified_df = pd.DataFrame()

    for trackID in imaris_df["TrackID"].unique():
        track = imaris_df[imaris_df["TrackID"] == trackID]

        if "Variable" in track.columns:
            track_x = np.array(track[track["Variable"] == "Position X"]["Value"])
            track_y = np.array(track[track["Variable"] == "Position Y"]["Value"])
            track_z = np.array(track[track["Variable"] == "Position Z"]["Value"])
            time = np.array(track[track["Variable"] == "Position X"]["Time"].astype(float))
            object_id = np.array(track[track["Variable"] == "Position X"]["ID"])
        else:
            track_x = np.array(track["Position X"])
            track_y = np.array(track["Position Y"])
            track_z = np.array(track["Position Z"])
            time = np.array(track["Time"].astype(float))
            object_id = np.array(track["ID"])

        if (len(track_x) < 3):
            continue

        if isinstance(track_x[0], str):
            for i in range(len(track_x)):
                track_x[i] = float(track_x[i].replace(",", "."))
                track_y[i] = float(track_y[i].replace(",", "."))
                track_z[i] = float(track_z[i].replace(",", "."))

        trackIDs = [str(int(trackID)) for i in range(len(time))]


        temp = pd.DataFrame({'x': track_x, 'y': track_y, 'z': track_z, 'frame': time,
                             'track_id': trackIDs, "object_id": object_id},
                            index=range(len(time)))

        if (len(unified_df) > 1):
            unified_df = unified_df.append(temp, ignore_index=True)
        else:
            unified_df = temp.copy()

    return unified_df


def _align_tracks(self, df_stat, turn_x=False, turn_y=False):

    df_stat_rot = pd.DataFrame()

    for trackID in df_stat["TrackID"].unique():
        track = df_stat[df_stat["TrackID"] == trackID]

        if "Variable" in track.columns:
            track_x = np.array(track[track["Variable"] == "Position X"]["Value"])
            track_y = np.array(track[track["Variable"] == "Position Y"]["Value"])
            track_z = np.array(track[track["Variable"] == "Position Z"]["Value"])
            time = np.array(track[track["Variable"] == "Position X"]["Time"].astype(float))
        else:
            track_x = np.array(track["Position X"])
            track_y = np.array(track["Position Y"])
            track_z = np.array(track["Position Z"])
            time = np.array(track["Time"].astype(float))

        if (len(track_x) < 3):
            continue

        if isinstance(track_x[0], str):
            for i in range(len(track_x)):
                track_x[i] = float(track_x[i].replace(",", "."))
                track_y[i] = float(track_y[i].replace(",", "."))
                track_z[i] = float(track_z[i].replace(",", "."))

        trackIDs = [str(trackID) for i in range(len(time))]

        if turn_x:
            track_x = -track_x
        # else:
        # df_stat_rot.at[index,'X'] = float(x)

        if turn_y:
            track_y = -track_y
        # else:
        # df_stat_rot.at[index,'y'] = float(y)

        temp = pd.DataFrame({'X': track_x, 'Y': track_y, 'Z': track_z, 'Time': time, 'TrackID': trackIDs},
                            index=range(len(time)))
        # temp = pd.concat([track_x, track_y, track_z, time, trackIDs, axis=1, keys=['X','Y','Z','Time','TrackID'])

        if (len(df_stat_rot) > 1):
            df_stat_rot = df_stat_rot.append(temp, ignore_index=True)
        else:
            df_stat_rot = temp.copy()

    return df_stat_rot