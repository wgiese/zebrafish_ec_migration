from kedro.pipeline import Pipeline, node

from zebrafish_ec_migration.pipelines.mitosis_count_pipeline.process_mitosis_migration_file import (
    process_mitosis_migration_file,
)

from zebrafish_ec_migration.pipelines.mitosis_count_pipeline.get_discrete_distributions import (
    get_migration_distributions,
)


def create_pipeline(**kwargs):

    return Pipeline(
        [
	    #convert file to csv
	    node(process_mitosis_migration_file, ["imaris_key_file", "preprocessed_mitosis_migration_file", "parameters"] ,
             ["processed_migration_file", "migration_statistics_file"], name="process_key_file"),
        node(get_migration_distributions,
                 ["imaris_key_file", "processed_migration_file", "parameters"],
                 "migration_distributions", name="get_migration_distributions"),
        ]
    )
