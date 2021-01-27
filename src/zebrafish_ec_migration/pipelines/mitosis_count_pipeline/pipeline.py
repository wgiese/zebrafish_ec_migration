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
	    #convert file to csv
	    node(preprocess_mitosis_migration_file, "parameters", "imaris_key_file", name="process_key_file"),
	    #process file
	    node(process_mitosis_migration_file, "parameters", "imaris_key_file", name="process_key_file"),
        ]
    )
