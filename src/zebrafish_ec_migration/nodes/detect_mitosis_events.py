



def amend_potential_mitosis_events(processed_key_file: pd.DataFrame, parameters: Dict, start_time, end_time):
    trajectory_plots = dict()
    # oriented_trajectory_plots = dict()

    # ex = extract.ExtractData(parameters["data_dir"], key_filename='Key.xlsx')
    # f = extract_features.ExtractFeatures()
    # geo = extract_geometry.ExtractGeometry()

    counter_statistics = 0

    track_data = dict()
    mitosis_events_df = pd.DataFrame()

    for fish_number in processed_key_file["fish number"].unique():

        if (np.isnan(fish_number)):
            continue

        df_single_fish_all_groups = processed_key_file[processed_key_file['fish number'] == fish_number]



        for analysis_group in df_single_fish_all_groups["analysis_group"].unique():

            df_single_fish = df_single_fish_all_groups[df_single_fish_all_groups["analysis_group"] == analysis_group]

            movement_data = pd.DataFrame(data=[], columns=["x", "y", "z", "link_id", "object_id", "vessel_type"])
            for index, row in df_single_fish.iterrows():

                # print("Object data: %s" % row["object_data"])
                if not isinstance(row["object_data"], str):
                    continue

                object_data = pd.read_csv(row["object_data"])
                link_data = pd.read_csv(row["link_data"])
                movement_data_ = pd.merge(object_data, link_data, on='object_id')



    return track_data