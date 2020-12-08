# Copyright 2020 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

#
#   This code has been derived and modified from https://pypi.org/project/kedro/ by Wolfgang Giese and Andre de la Rosa
#


"""Construction of the master pipeline.
"""

from typing import Dict

from kedro.pipeline import Pipeline, node

from zebrafish_ec_migration.pipelines.FAIR_pipeline import pipeline as FAIR_pipeline

from zebrafish_ec_migration.nodes.plot_migration_data import (
    plot_migration_data,
)

from zebrafish_ec_migration.nodes.load_cmso_migration_data import (
    align_cmso_migration_data,
    plot_link_lengths,
    plot_link_lengths_hist,
)


from zebrafish_ec_migration.nodes.detect_mitosis_events import (
    extract_potential_mitosis_events,
)

from zebrafish_ec_migration.nodes.extract_cell_migration_features import (
    extract_migration_features,
)


def create_pipelines(**kwargs) -> Dict[str, Pipeline]:
    """Create the project's pipeline.

    Args:
        kwargs: Ignore any additional arguments added in the future.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.

    """

    preprocess_pipeline = FAIR_pipeline.create_pipeline()

    master_pipeline = Pipeline(
        [node(plot_migration_data,
              ["processed_key_file", "parameters", "params:start_time_dpf1", "params:end_time_dpf1"],
              "trajectory_plots", name="plot_trajectories"),
         node(align_cmso_migration_data,
              ["processed_key_file", "parameters", "params:start_time_dpf1", "params:end_time_dpf1"],
              ["fish_data_summary", "link_data_summary"],
              name = "align_cmso_migration_data"),
         node(plot_link_lengths_hist, "link_data_summary",  "link_data_hist_plot",
              name="plot_link_data_hist"),
         node(plot_link_lengths, "link_data_summary", "link_length_plot",
              name="plot_link_length"),
         node(extract_migration_features,
              ["processed_key_file", "parameters", "params:start_time_dpf1", "params:end_time_dpf1"],
              ["migration_features", "migration_data_statistics"], name="extract_migration_features_dpf1"),
         node(extract_potential_mitosis_events,
              ["processed_key_file", "parameters", "params:start_time_dpf1", "params:end_time_dpf1"], "mitosis_events",
              name="detect_mitosis_events"),
         ])

    # return {"__default__": preprocess_pipeline}
    return {"__default__": master_pipeline, "preprocess_pipeline": preprocess_pipeline}
