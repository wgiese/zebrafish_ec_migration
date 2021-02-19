from kedro.pipeline import Pipeline, node

from zebrafish_ec_migration.pipelines.mitosis_count_pipeline.process_mitosis_migration_file import (
    process_mitosis_migration_file,
)

def create_pipeline(**kwargs):

    return Pipeline(
        [
	    #convert file to csv
	    node(process_mitosis_migration_file, ["imaris_key_file", "preprocessed_mitosis_migration_file", "parameters"] ,
             ["processed_migration_file", "migration_statistics_file"], name="process_key_file"),
	    #process file
	    #node(process_mitosis_migration_file, "parameters", "imaris_key_file", name="process_key_file"),
        ]
    )
