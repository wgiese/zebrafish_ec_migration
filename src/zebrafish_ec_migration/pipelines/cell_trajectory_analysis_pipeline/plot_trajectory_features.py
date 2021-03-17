import pandas as pd
import pylab as plt
import seaborn as sns
from typing import Dict


def plot_velocities(trajectory_features: pd.DataFrame, parameters: Dict, start_time, end_time):

    velocity_plots = dict()

    plt.rcParams.update({'font.size': 16})

    for analysis_group in trajectory_features["analysis_group"].unique():
        trajectory_features_group = trajectory_features[trajectory_features["analysis_group"] == analysis_group]
        for vessel_type in ['aISV','vISV']:

            trajectory_features_vessel = trajectory_features_group[trajectory_features_group["vessel_type"] == vessel_type].dropna()

            fig, ax = plt.subplots(figsize=(18, 6))
            sns.lineplot( x="frame", y="step_size_y", data=trajectory_features_vessel, ax=ax)

            velocity_plots["velocity_%s_%s.png" % (vessel_type, analysis_group)] = fig


    return velocity_plots