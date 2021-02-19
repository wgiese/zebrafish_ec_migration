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

def get_migration_distributions(preprocessed_key_file: pd.DataFrame, processed_mitosis_migration_file: pd.DataFrame,
                           parameters: Dict, dpf=1):

    statistics_df = pd.DataFrame()
    migration_dict = dict()
    distributions_dict = dict()

    analysis_groups = parameters["analysis_groups"]
    mitosis_events = np.arange(5)

    attribute_list = ["cell_number","mitosis_events","migration_to_dlav","migration_from_dlav"]
    for attribute in attribute_list:

        distributions_dict = dict()
        for analysis_group in analysis_groups:
            distributions_dict_group = dict()
            aISV_df_all, mitosis_events_aISV = _extract_mitosis_info(preprocessed_key_file, processed_mitosis_migration_file,
                                                             mitosis_events, "aISV", analysis_group, dpf)
            vISV_df_all, mitosis_events_vISV = _extract_mitosis_info(preprocessed_key_file, processed_mitosis_migration_file,
                                                             mitosis_events, "vISV", analysis_group , dpf)

            dist_aISV = np.array(aISV_df_all[attribute])
            dist_aISV = dist_aISV[~np.isnan(dist_aISV)]
            dist_vISV = np.array(vISV_df_all[attribute])
            dist_vISV = dist_vISV[~np.isnan(dist_vISV)]

            distributions_dict_group["aISV"] = list(dist_aISV)
            distributions_dict_group["vISV"] = list(dist_vISV)
            distributions_dict[analysis_group] = distributions_dict_group

        migration_dict[attribute] = distributions_dict

    attribute_list = ["migration_to_aorta", "migration_from_aorta"]
    for attribute in attribute_list:

        distributions_dict = dict()
        for analysis_group in analysis_groups:
            distributions_dict_group = dict()
            aISV_df_all, mitosis_events_aISV = _extract_mitosis_info(preprocessed_key_file,
                                                                     processed_mitosis_migration_file,
                                                                     mitosis_events, "aISV", analysis_group, dpf)


            dist_aISV = np.array(aISV_df_all[attribute])
            dist_aISV = dist_aISV[~np.isnan(dist_aISV)]

            distributions_dict_group["aISV"] = list(dist_aISV)
            distributions_dict[analysis_group] = distributions_dict_group

        migration_dict[attribute] = distributions_dict

    attribute_list = ["migration_to_pcv", "migration_from_pcv"]
    for attribute in attribute_list:

        distributions_dict = dict()
        for analysis_group in analysis_groups:
            distributions_dict_group = dict()
            vISV_df_all, mitosis_events_aISV = _extract_mitosis_info(preprocessed_key_file,
                                                                     processed_mitosis_migration_file,
                                                                     mitosis_events, "vISV", analysis_group, dpf)


            dist_vISV = np.array(vISV_df_all[attribute])
            dist_vISV = dist_vISV[~np.isnan(dist_vISV)]

            distributions_dict_group["vISV"] = list(dist_vISV)
            distributions_dict[analysis_group] = distributions_dict_group

        migration_dict[attribute] = distributions_dict

    return migration_dict