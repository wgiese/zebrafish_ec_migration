from kedro.pipeline import Pipeline, node

from zebrafish_ec_migration.pipelines.FAIR_pipeline.process_key_file import (
    process_key_file,
    preprocess_mitosis_migration_file,
)

from zebrafish_ec_migration.pipelines.FAIR_pipeline.CMSO_transformation import (
    CMSO_movement_data,
)

from zebrafish_ec_migration.pipelines.FAIR_pipeline.plot_trajectory_data import (
    plot_trajectory_data,
)


def create_pipeline(**kwargs):

    return Pipeline(
        [
            node(process_key_file, "parameters", "imaris_key_file", name="process_key_file"),
            node(preprocess_mitosis_migration_file, "parameters", "preprocessed_mitosis_migration_file", name="preprocess_mitosis_migration_file"),
            node(CMSO_movement_data,
                 ["imaris_key_file", "parameters", "params:start_time_dpf1", "params:end_time_dpf1"],
                 ["processed_key_file", "IMARIS_data", "unprocessed_key_file", "CMSO_object_data", "CMSO_objects_statistics",
                  "CMSO_link_data", "CMSO_track_data", "CMSO_json_data"],
                 name="CMSO_transformation"),
            node(plot_trajectory_data,
                 ["processed_key_file", "parameters", "params:start_time_dpf1", "params:end_time_dpf1"],
                 "trajectory_plots", name="plot_trajectories"),
        ]
    )
