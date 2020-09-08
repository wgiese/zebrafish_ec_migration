from kedro.pipeline import Pipeline, node

from zebrafish_ec_migration.nodes.process_key_file import (
    process_key_file,
)

from zebrafish_ec_migration.nodes.CMSO_transformation import (
    CMSO_movement_data,
)




def create_pipeline(**kwargs):

    return Pipeline(
        [
            node(process_key_file, "parameters", "imaris_key_file", name="process_key_file"),
            node(CMSO_movement_data,
                 ["imaris_key_file", "parameters", "params:start_time_dpf1", "params:end_time_dpf1"],
                 ["processed_key_file", "IMARIS_data", "CMSO_object_data", "CMSO_objects_statistics",
                  "CMSO_link_data", "CMSO_track_data", "CMSO_json_data"],
                 name="CMSO_transformation"),
        ]
    )
