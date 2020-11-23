import pandas as pd
import numpy as np
from typing import Dict, List


def process_key_file(parameters: Dict) -> pd.DataFrame:
    default_load_args = {"engine": "xlrd", "skiprows": 1}
    df_key = pd.read_excel(parameters["key_file"], **default_load_args)

    processed_key_file = _specify_analysis_groups(df_key)

    processed_key_file = processed_key_file[processed_key_file["filename"].str.contains(".csv")]

    # list columns that are needed

    processed_key_file = processed_key_file[
        ["filename", "fish number", "vessel_type", "dpf", "imaging orientation", "analysis_group"]]

    return processed_key_file


def _specify_analysis_groups(df_key):
    # TODO: remove some code chunks here since many columns are not needed anymore

    df_key = df_key.rename(columns={'File name': 'filename'})

    df_key = df_key[~df_key['filename'].isnull()]

    #df_key['imaging start [dpf]'] = df_key.loc[:, 'dpf']

    df_key = df_key[df_key["dpf"] == 1]

    df_key.rename(index=str, columns={'vessel type': 'vessel_type'}, inplace=True)

    df_key['vessel_type'] = ['aorta' if d_['Aorta'] else ('dlav' if d_['DLAV'] else (
        'aISV' if d_['aISV'] else ('vISV' if d_['vISV'] else ('either_ISV' if d_['ISV'] else 'none')))) for _, d_ in
                             df_key.iterrows()]  # vessel type

    df_key['filename'] = [fn_['filename'][fn_['filename'].find('Statistics on cell migration') - 1:] for _, fn_ in
                          df_key.iterrows()]

    processed_key_file = df_key.copy()

    for index, row in processed_key_file.iterrows():

        if pd.isna(row['WaspI [100uM]']) and pd.isna(row['WaspI [100uM].1']):
            processed_key_file.at[index, 'WaspI [100uM] (merged)'] = 0
        elif (not pd.isna(row['WaspI [100uM]'])):
            processed_key_file.at[index, 'WaspI [100uM] (merged)'] = row['WaspI [100uM]']
        else:
            processed_key_file.at[index, 'WaspI [100uM] (merged)'] = row['WaspI [100uM].1']

    control_false = ['WaspI [50uM]', 'WaspI [100uM] (merged)', 'WaspI [200uM]', 'WaspII [50uM]', 'WaspII [100uM]',
                     'WaspII [200uM]',
                     'tnnt2', 'Gata1', 'Rac1T17N', 'Cdc42G12V', 'Cdc42T17N', 'CK-666', 'CK689', 'Tricaine',
                     'Epinephrine', 'Glycerin', 'Wiskostatin', 'DMSO']

    wasp_100_false = ['WaspI [50uM]', 'WaspI [200uM]', 'WaspII [50uM]', 'WaspII [100uM]', 'WaspII [200uM]', 'tnnt2',
                      'Gata1',
                      'Rac1T17N', 'Cdc42G12V', 'Cdc42T17N', 'CK-666', 'CK689', 'Tricaine', 'Epinephrine', 'Glycerin',
                      'Wiskostatin', 'DMSO']

    df_control = processed_key_file[processed_key_file['Control'] == 1]

    for cond in control_false:
        df_control = df_control[df_control[cond] != 1]

    df_control["analysis_group"] = pd.Series(["control" for i in range(len(df_control))], index=df_control.index)

    df_wasp_100 = processed_key_file[processed_key_file['WaspI [100uM] (merged)'] == 1]

    for cond in wasp_100_false:
        df_wasp_100 = df_wasp_100[df_wasp_100[cond] != 1]

    df_wasp_100["analysis_group"] = pd.Series(['WaspI [100uM]' for i in range(len(df_wasp_100))],
                                              index=df_wasp_100.index)

    return pd.concat([df_control, df_wasp_100], ignore_index=True)
