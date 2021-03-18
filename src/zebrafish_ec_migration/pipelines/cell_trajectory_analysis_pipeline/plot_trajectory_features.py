import pandas as pd
import pylab as plt
import seaborn as sns
import numpy as np
from typing import Dict


def plot_velocities(trajectory_features: pd.DataFrame, parameters: Dict, start_time, end_time):

    velocity_plots = dict()

    #plt.rcParams.update({'font.size': 16})

    #for analysis_group in trajectory_features["analysis_group"].unique():
    #    trajectory_features_group = trajectory_features[trajectory_features["analysis_group"] == analysis_group]
    #    for vessel_type in ['aISV','vISV']:

    #        trajectory_features_vessel = trajectory_features_group[trajectory_features_group["vessel_type"] == vessel_type]
    #        trajectory_features_vessel = trajectory_features_vessel.sort_values(by="frame").dropna()
    #        print(trajectory_features_vessel)

    #        fig, ax = plt.subplots(figsize=(18, 6))
    #        sns.lineplot( x="frame", y="step_size_y", data=trajectory_features_vessel, ax=ax)

    #        velocity_plots["velocity_%s_%s.png" % (vessel_type, analysis_group)] = fig

    vessel_colors = parameters['vessel_type_colors']
    feature = "vd_velocity_micron_per_h"
    #feature = "step_size_y"

    for analysis_group in trajectory_features["analysis_group"].unique():
        fig, ax = plt.subplots(figsize=(15, 10))

        ax.set_xlim(parameters["start_plot_dpf1"], parameters["end_plot_dpf1"])
        ax.set_ylim(-5, 7)

        for vessel_type in ['aISV','vISV']:
            plot_df = trajectory_features[trajectory_features["analysis_group"] == analysis_group]
            plot_df = plot_df[plot_df['vessel_type'] == vessel_type]
            plot_df = plot_df.sort_values(by="frame").dropna()
            sns.lineplot(x='time_in_hpf', y=feature, data=plot_df, ax=ax, ci=95, color=vessel_colors[vessel_type])
            #sns.pointplot(x='time_in_hpf', y=feature, data=plot_df, ax=ax, color=vessel_colors[vessel_type])

        ax.set_xlabel("time post fertilization [h]")
        ax.set_ylabel("velocity [$\mathrm{\mu}$m/h]")

        ax.set_xticks(np.arange(parameters["start_plot_dpf1"], parameters["end_plot_dpf1"], 4))

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        ax.axhline(0.0, color="black")
        velocity_plots["velocity_%s.png" % analysis_group] = fig

    return velocity_plots


def plot_biphasic_velocities(trajectory_features: pd.DataFrame, parameters: Dict, start_time, end_time):

    velocity_plots = dict()

    plt.rcParams.update({'font.size': 16})

    dev_phases = parameters["dev_phases"]
    vessel_colors = parameters['vessel_type_colors']
    feature = "vd_velocity_micron_per_h"

    for analysis_group in trajectory_features["analysis_group"].unique():
        trajectory_features_group = trajectory_features[trajectory_features["analysis_group"] == analysis_group]

        trajectory_features_phases_ = []
        for dev_phase in dev_phases:
            time_interval = dev_phases[dev_phase]
            trajectory_features_phase = trajectory_features_group[trajectory_features_group["time_in_hpf"] >= time_interval[0]]
            trajectory_features_phase = trajectory_features_phase[trajectory_features_phase["time_in_hpf"] <= time_interval[1]]
            trajectory_features_phase["dev_phase"] = dev_phase
            trajectory_features_phases_.append(trajectory_features_phase)

        trajectory_features_phases = pd.concat(trajectory_features_phases_)
        fig, ax = plt.subplots(figsize=(15, 10))
        for vessel_type in ['aISV','vISV']:
            plot_df = trajectory_features_phases[trajectory_features_phases['vessel_type'] == vessel_type]
            plot_df = plot_df.sort_values(by="frame").dropna()
            sns.pointplot(x='dev_phase', y=feature, data=plot_df, ax=ax, color=vessel_colors[vessel_type], ci=95)

        ax.set_ylim(-1.0, 6.0)
        ax.set_xlabel("developmental phases")
        ax.set_ylabel("velocity [$\mathrm{\mu}$m/h]")

        #for vessel_type in ['aISV', 'vISV']:

        # #   trajectory_features_vessel = trajectory_features_group[trajectory_features_group["vessel_type"] == vessel_type]
        # #   trajectory_features_vessel = trajectory_features_vessel.sort_values(by="frame").dropna()
        # #   trajectory_features_vessel_phase1 = trajectory_features_vessel[trajectory_features_vessel["frame"] < 48]
        # #   trajectory_features_vessel_phase2 = trajectory_features_vessel[trajectory_features_vessel["frame"] > 48]
        # #   trajectory_features_vessel_phase1["phase"] = "26h-30h"
        # #   trajectory_features_vessel_phase2["phase"] = "30h-48h"
        # #   trajectory_features_vessel_biphasic = pd.concat([trajectory_features_vessel_phase1, trajectory_features_vessel_phase2], ignore_index=True)
        # #   print(trajectory_features_vessel)

        #    fig, ax = plt.subplots(figsize=(18, 6))
            #sns.swarmplot(x = "phase", y="step_size_y", data=trajectory_features_vessel_biphasic, ax=ax)
        #    sns.violinplot(x="phase", y="vd_velocity_micron_per_h", data=trajectory_features_vessel_biphasic, ax=ax, showfliers = False)
            #hue = "smoker"

        velocity_plots["biphasic_velocity_%s.png" % analysis_group] = fig


    return velocity_plots