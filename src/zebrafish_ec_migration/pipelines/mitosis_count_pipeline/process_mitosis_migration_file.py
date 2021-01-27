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
import extract_data as extract


def is_number(x):
    value = False
    if isinstance(x, int) or isinstance(x, float):
        if (not np.isnan(x)):
            value = True
    return value


def preprocess_mitosis_migration_file(preprocessed_key_file: pd.DataFrame, mitosis_migration_file: pd.DataFrame, parameters: Dict):
    
    processed_migration_file = pd.DataFrame()

    migration_statistics_file = pd.DataFrame()


    print(mitosis_migration_file.head())
    
    #mitosis_migration_file.columns = mitosis_migration_file.iloc[0]
    #mitosis_migration_file = mitosis_migration_file.drop(0)

    print(mitosis_migration_file.columns)
    counter = 0
    counter_stat = 0

    for idx,row in mitosis_migration_file.iterrows():
        if (np.isnan(row["Fish name"])):
                continue




#        print(row["Fish name"])
        processed_migration_file.at[counter, "fish_number"] = row["Fish name"]
        processed_migration_file.at[counter, "vessel_ID"] = "aorta"
        processed_migration_file.at[counter, "time"] = parameters["time_cell_count"]

        migration_statistics_file.at[counter_stat, "fish_number"] = row["Fish name"]
        migration_statistics_file.at[counter_stat, "vessel_ID"] = "aorta"
        migration_statistics_file.at[counter_stat, "processed"] = False
        migration_statistics_file.at[counter_stat, "time"] = parameters["time_cell_count"]


        if is_number(row["cell number Aorta"]) and is_number(row["mitosis Aorta"]):

            processed_migration_file.at[counter, "cell_number"] = int(row["cell number Aorta"])
            processed_migration_file.at[counter, "mitosis_events"] = row["mitosis Aorta"]
            migration_statistics_file.at[counter_stat, "processed"] = True
            counter += 1
        else:
            migration_statistics_file.at[counter_stat, "processed"] = False

        counter_stat += 1

        processed_migration_file.at[counter, "fish_number"] = row["Fish name"]
        processed_migration_file.at[counter, "vessel_ID"] = "dlav"
        processed_migration_file.at[counter, "time"] = parameters["time_cell_count"]

        migration_statistics_file.at[counter_stat, "fish_number"] = row["Fish name"]
        migration_statistics_file.at[counter_stat, "vessel_ID"] = "dlav"
        migration_statistics_file.at[counter_stat, "processed"] = False
        migration_statistics_file.at[counter_stat, "time"] = parameters["time_cell_count"]

        if is_number(row["cell number DLAV"]) and is_number(row["mitosis DLAV"]):

            processed_migration_file.at[counter, "cell_number"] = int(row["cell number DLAV"])
            processed_migration_file.at[counter, "mitosis_events"] = row["mitosis DLAV"]
            migration_statistics_file.at[counter_stat, "processed"] = True
            counter += 1
        else:
            migration_statistics_file.at[counter_stat, "processed"] = False

        counter_stat += 1

        cell_numbers = str(row["cell number aISV"]).split("+")
        cell_mitosis = str(row["mitosis aISV"]).split("+")

        migration_from_aorta = str(row["A->aISV"]).split("+")
        migration_to_aorta = str(row["aISV->A"]).split("+")

        migration_from_dlav = str(row["DLAV->aISV"]).split("+")
        migration_to_dlav = str(row["aISV->DLAV"]).split("+")

        if len(cell_numbers) == len(cell_mitosis):
            for isv_counter, (cell_number, mitosis_number) in enumerate(zip(cell_numbers,cell_mitosis)):
                processed_migration_file.at[counter, "fish_number"] = row["Fish name"]
                processed_migration_file.at[counter, "vessel_ID"] = "aISV_%s" % (isv_counter+1)
                processed_migration_file.at[counter, "time"] = parameters["time_cell_count"]

                processed_migration_file.at[counter, "cell_number"] = cell_number
                processed_migration_file.at[counter, "mitosis_events"] = mitosis_number

                if (len(migration_from_aorta) > isv_counter):
                    processed_migration_file.at[counter, "migration_from_aorta"] = migration_from_aorta[isv_counter]
                if (len(migration_to_aorta) > isv_counter):
                    processed_migration_file.at[counter, "migration_to_aorta"] = migration_to_aorta[isv_counter]

                if (len(migration_from_dlav) > isv_counter):
                    processed_migration_file.at[counter, "migration_from_dlav"] = migration_from_dlav[isv_counter]
                if (len(migration_to_dlav) > isv_counter):
                    processed_migration_file.at[counter, "migration_to_dlav"] = migration_to_dlav[isv_counter]

                counter += 1

        cell_numbers = str(row["cell number vISV"]).split("+")
        cell_mitosis = str(row["mitosis vISV"]).split("+")

        migration_to_dlav = str(row["vISV->DLAV"]).split("+")
        migration_from_dlav = str(row["DLAV->vISV"]).split("+")

        migration_from_pcv = str(row["PCV->vISV"]).split("+")
        migration_to_pcv = str(row["vISV->PCV"]).split("+")

        if len(cell_numbers) == len(cell_mitosis):
            for isv_counter, (cell_number, mitosis_number) in enumerate(zip(cell_numbers, cell_mitosis)):
                processed_migration_file.at[counter, "fish_number"] = row["Fish name"]
                processed_migration_file.at[counter, "vessel_ID"] = "vISV_%s" % (isv_counter+1)
                processed_migration_file.at[counter, "time"] = parameters["time_cell_count"]

                processed_migration_file.at[counter, "cell_number"] = cell_number
                processed_migration_file.at[counter, "mitosis_events"] = mitosis_number

                if (len(migration_from_dlav) > isv_counter):
                    processed_migration_file.at[counter, "migration_from_dlav"] = migration_from_dlav[isv_counter]
                if (len(migration_to_dlav) > isv_counter):
                    processed_migration_file.at[counter, "migration_to_dlav"] = migration_to_dlav[isv_counter]

                if (len(migration_from_pcv) > isv_counter):
                    processed_migration_file.at[counter, "migration_from_pcv"] = migration_from_pcv[isv_counter]
                if (len(migration_to_pcv) > isv_counter):
                    processed_migration_file.at[counter, "migration_to_pcv"] = migration_to_pcv[isv_counter]

                counter += 1


    return processed_migration_file, migration_statistics_file
