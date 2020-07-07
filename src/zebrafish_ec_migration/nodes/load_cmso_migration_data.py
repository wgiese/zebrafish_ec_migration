import pandas as pd

def align_cmso_migration_data(processed_key_file: pd.DataFrame, parameters: Dict, start_time, end_time):

    counter_statistics = 0

    key_aligned_objects = pd.DataFrame()
    movement_data_summary = pd.DataFrame()

    aligned_objects = dict()

    for fish_number in processed_key_file["fish number"].unique():

        if (np.isnan(fish_number)):
            continue

        df_single_fish_all_groups = df_key[df_key['fish number'] == fish_number]

        for analysis_group in df_single_fish_all_groups["analysis_group"].unique():

            df_single_fish = df_single_fish_all_groups[df_single_fish_all_groups["analysis_group"] == analysis_group]

            if ((start_time >= key_row['dpf'] * 24.0) and (end_time <= key_row['dpf'] * 24.0 + 24.0)):
                counter_statistics += 1

                movement_data_summary.at[counter_statistics, 'fish_number'] = fish_number
                movement_data_summary.at[counter_statistics, '#tracks'] = 0
                movement_data_summary.at[counter_statistics, 'analysis_group'] = analysis_group
                movement_data_summary.at[counter_statistics, 'dpf'] = key_row['dpf']

                #movement_data_summary.at[counter_statistics, 'filename'] = key_row['filename'].split("/")[-1]
                #movement_data_summary.at[counter_statistics, 'folder'] = "/".join(key_row['filename'].split("/")[0:-1])



    return key_aligned_objects, aligned_objects, movement_data_summary