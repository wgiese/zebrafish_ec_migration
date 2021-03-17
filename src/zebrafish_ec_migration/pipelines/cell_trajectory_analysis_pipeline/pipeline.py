from kedro.pipeline import Pipeline, node

from zebrafish_ec_migration.pipelines.cell_trajectory_analysis_pipeline.align_zebrafish_trajectory_data import (
    align_cmso_trajectory_data,
)

from zebrafish_ec_migration.pipelines.cell_trajectory_analysis_pipeline.evaluate_data_abundance import (
    plot_link_lengths,
    plot_link_lengths_hist,
)

from zebrafish_ec_migration.pipelines.cell_trajectory_analysis_pipeline.plot_trajectory_data import (
    plot_trajectory_data,
)

from zebrafish_ec_migration.pipelines.cell_trajectory_analysis_pipeline.compute_trajectory_features import (
    compute_trajectory_features,
)


def create_pipeline(**kwargs):

    return Pipeline(
        [
            node(align_cmso_trajectory_data,
                 ["processed_key_file", "parameters", "params:start_time_dpf1", "params:end_time_dpf1"],
                 ["aligned_trajectory_key_file", "fish_data_summary", "link_data_summary", "CMSO_aligned_object_data", "CMSO_aligned_link_data"],
                 name="align_cmso_migration_data"),
            node(plot_link_lengths_hist, "link_data_summary", "link_data_hist_plot",
                 name="plot_link_data_hist"),
            node(plot_link_lengths, ["fish_data_summary", "link_data_summary"], "link_length_plot",
                 name="plot_link_length"),
            node(plot_trajectory_data,
                 ["aligned_trajectory_key_file", "parameters", "params:start_time_dpf1", "params:end_time_dpf1"],
                 "aligned_trajectory_plots", name="plot_aligned_trajectories"),
            node(compute_trajectory_features, ["aligned_trajectory_key_file", "parameters",
                 "params:start_time_dpf1", "params:end_time_dpf1"], "trajectory_features",
                 name="compute_trajectory_features")
        ])
