from kedro.pipeline import Pipeline, node

from zebrafish_ec_migration.pipelines.cell_trajectory_analysis_pipeline.nodes import (
    align_cmso_migration_data,
    plot_link_lengths,
    plot_link_lengths_hist,
)



def create_pipeline(**kwargs):

    return Pipeline(
        [
            node(align_cmso_migration_data,
                 ["processed_key_file", "parameters", "params:start_time_dpf1", "params:end_time_dpf1"],
                 ["fish_data_summary", "link_data_summary", "CMSO_aligned_object_data", "CMSO_aligned_link_data"],
                 name="align_cmso_migration_data"),
            node(plot_link_lengths_hist, "link_data_summary", "link_data_hist_plot",
                 name="plot_link_data_hist"),
            node(plot_link_lengths, ["fish_data_summary", "link_data_summary"], "link_length_plot",
                 name="plot_link_length"),
        ])
