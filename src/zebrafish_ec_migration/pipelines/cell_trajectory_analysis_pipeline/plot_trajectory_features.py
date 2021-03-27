import pandas as pd
import pylab as plt
import seaborn as sns
import numpy as np
from typing import Dict
from scipy import stats


def plot_velocities(trajectory_features: pd.DataFrame, parameters: Dict, start_time, end_time):

    velocity_plots = dict()

    vessel_colors = parameters['vessel_type_colors']
    feature = "vd_velocity_micron_per_h"
    #feature = "step_size_y"

    paper_rc = {'lines.linewidth': 1, 'lines.markersize': 4}
    sns.set_context("paper", rc=paper_rc)

    for analysis_group in trajectory_features["analysis_group"].unique():
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.set_xlim(parameters["start_plot_dpf1"], parameters["end_plot_dpf1"])
        ax.set_ylim(-5, 7)

        for vessel_type in ['aISV','vISV']:
            plot_df = trajectory_features[trajectory_features["analysis_group"] == analysis_group]
            plot_df = plot_df[plot_df['vessel_type'] == vessel_type]
            plot_df = plot_df.sort_values(by="frame").dropna()
            plot_df = plot_df[plot_df['time_in_hpf'] >= parameters["start_plot_dpf1"]]
            plot_df = plot_df[plot_df['time_in_hpf'] <= parameters["end_plot_dpf1"]]
            #sns.lineplot(x='time_in_hpf', y=feature, data=plot_df, ax=ax, ci=95, style="vessel_type", markers=True, color=vessel_colors[vessel_type])
            sns.lineplot(x='time_in_hpf', y=feature, data=plot_df, ax=ax, ci=95, color=vessel_colors[vessel_type])
            #sns.pointplot(x='time_in_hpf', y=feature, data=plot_df, ax=ax, color=vessel_colors[vessel_type])

        ax.set_xlabel("time post fertilization [h]")
        ax.set_ylabel("velocity [$\mathrm{\mu}$m/h]")

        ax.set_xticks(np.arange(parameters["start_plot_dpf1"], parameters["end_plot_dpf1"], 4))
        #ax.set_xticks(np.arange(0,len(plot_df['time_in_hpf'].unique()),12))

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        ax.axhline(0.0, color="black")
        velocity_plots["velocity_%s.png" % analysis_group] = fig
        velocity_plots["velocity_%s.pdf" % analysis_group] = fig

    return velocity_plots

def plot_velocities_hourly(trajectory_features: pd.DataFrame, parameters: Dict, start_time, end_time):

    velocity_plots = dict()

    vessel_colors = parameters['vessel_type_colors']
    feature = "vd_velocity_micron_per_h"
    #feature = "step_size_y"
    time_values = np.arange(26,47,1)

    for analysis_group in trajectory_features["analysis_group"].unique():
        fig, ax = plt.subplots(figsize=(20, 10))

        ax.set_xlim(parameters["start_plot_dpf1"], parameters["end_plot_dpf1"])
        ax.set_ylim(-5, 7)

        for vessel_type in ['aISV','vISV']:
            plot_df = trajectory_features[trajectory_features["analysis_group"] == analysis_group]
            plot_df = plot_df[plot_df['vessel_type'] == vessel_type]
            plot_df = plot_df.sort_values(by="frame").dropna()

            plot_df = plot_df[plot_df['time_in_hpf'].isin(time_values)]

            sns.lineplot(x='time_in_hpf', y=feature, data=plot_df, ax=ax, ci=95, color=vessel_colors[vessel_type])
            #sns.pointplot(x='time_in_hpf', y=feature, data=plot_df, ax=ax, color=vessel_colors[vessel_type])

        ax.set_xlabel("time post fertilization [h]")
        ax.set_ylabel("velocity [$\mathrm{\mu}$m/h]")

        ax.set_xticks(np.arange(parameters["start_plot_dpf1"], parameters["end_plot_dpf1"], 4))

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        ax.axhline(0.0, color="black")
        velocity_plots["hourly_velocity_%s.png" % analysis_group] = fig

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

            sns.pointplot(x='dev_phase', y=feature, data=plot_df, ax=ax,
                          color=vessel_colors[vessel_type], linestyles = "dashed", capsize = 0.05, scale = 1.5, ci=95)

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
        velocity_plots["biphasic_velocity_%s.pdf" % analysis_group] = fig

    return velocity_plots


def plot_biphasic_velocities_with_stat_test(trajectory_features: pd.DataFrame, parameters: Dict, start_time, end_time):
    velocity_plots = dict()

    stat_tests = pd.DataFrame()
    stat_ind = 0
    stat_test = "Welch’s t-test"

    plt.rcParams.update({'font.size': 16})

    dev_phases = parameters["dev_phases"]
    dev_phases_list = list(dev_phases.keys())
    vessel_colors = parameters['vessel_type_colors']
    feature = "vd_velocity_micron_per_h"

    for analysis_group in trajectory_features["analysis_group"].unique():
        trajectory_features_group = trajectory_features[trajectory_features["analysis_group"] == analysis_group]

        trajectory_features_phases_ = []
        for dev_phase in dev_phases:
            time_interval = dev_phases[dev_phase]
            trajectory_features_phase = trajectory_features_group[
                trajectory_features_group["time_in_hpf"] >= time_interval[0]]
            trajectory_features_phase = trajectory_features_phase[
                trajectory_features_phase["time_in_hpf"] <= time_interval[1]]
            trajectory_features_phase["dev_phase"] = dev_phase
            trajectory_features_phases_.append(trajectory_features_phase)

        trajectory_features_phases = pd.concat(trajectory_features_phases_)
        fig, ax = plt.subplots(figsize=(15, 10))



        for vessel_type_A in ['aISV', 'vISV']:
            plot_df = trajectory_features_phases[trajectory_features_phases['vessel_type'] == vessel_type_A]
            plot_df = plot_df.sort_values(by="frame").dropna()

            sns.pointplot(x='dev_phase', y=feature, data=plot_df, ax=ax,
                          color=vessel_colors[vessel_type_A], linestyles="dashed", capsize=0.05, scale=1.5, ci=95)



            #for dev_phase_A in plot_df['dev_phase'].unique():
            for i in range(len(dev_phases_list)):
                dev_phase_A = dev_phases_list[i]
                sample_A = plot_df[plot_df['dev_phase'] == dev_phase_A]

                vessel_type_B = vessel_type_A

                #for dev_phase_B in plot_df['dev_phase'].unique():
                for j in range(i+1,len(dev_phases_list)):
                    dev_phase_B = dev_phases_list[j]

                    sample_B = plot_df[plot_df['dev_phase'] == dev_phase_B]

                    stat_tests.at[stat_ind, "analysis_group"] = analysis_group
                    stat_tests.at[stat_ind, "vessel_type_A"] = vessel_type_A
                    stat_tests.at[stat_ind, "vessel_type_B"] = vessel_type_B
                    stat_tests.at[stat_ind, "dev_phase_A"] = dev_phase_A
                    stat_tests.at[stat_ind, "dev_phase_B"] = dev_phase_B

                    result = stats.ttest_ind(sample_A[feature], sample_B[feature], equal_var = False)

                    stat_tests.at[stat_ind, "t-statistic"] = result[0]
                    stat_tests.at[stat_ind, "p-value"] = result[1]

                    stat_ind += 1

                if vessel_type_A == "aISV":
                    vessel_type_B = "vISV"
                    sample_B = trajectory_features_phases[trajectory_features_phases['vessel_type'] == vessel_type_B]
                    sample_B = sample_B.sort_values(by="frame").dropna()
                    sample_B = sample_B[sample_B['dev_phase'] == dev_phase_A]

                    stat_tests.at[stat_ind, "analysis_group"] = analysis_group
                    stat_tests.at[stat_ind, "vessel_type_A"] = vessel_type_A
                    stat_tests.at[stat_ind, "vessel_type_B"] = vessel_type_B
                    stat_tests.at[stat_ind, "dev_phase_A"] = dev_phase_A
                    stat_tests.at[stat_ind, "dev_phase_B"] = dev_phase_A

                    result = stats.ttest_ind(sample_A[feature], sample_B[feature], equal_var = False)

                    stat_tests.at[stat_ind, "t-statistic"] = result[0]
                    stat_tests.at[stat_ind, "p-value"] = result[1]

                    stat_ind += 1

        #def label_diff(i, j, text, X, Y):
        #    x = (X[i] + X[j]) / 2
        #    y = 1.1 * max(Y[i], Y[j])
        #    dx = abs(X[i] - X[j])

        #   props = {'connectionstyle': 'bar', 'arrowstyle': '-', \
        #             'shrinkA': 20, 'shrinkB': 20, 'linewidth': 2}
        #    ax.annotate(text, xy=(X[i], y + 7), zorder=10)
        #    ax.annotate('', xy=(X[i], y), xytext=(X[j], y), arrowprops=props)

        #ind = np.arange(4)
        #label_diff(0, 2, "***", ind, [3.0, 3.0, 3.0, 3.0])

        ## comparison vISV dev_phase_1 against dev_phase_3

        conds = trajectory_features_phases[trajectory_features_phases['vessel_type'] == "vISV"]
        conds = conds.sort_values(by="frame").dropna()
        cond_A = conds[conds['dev_phase'] == dev_phases_list[0]]
        cond_B = conds[conds['dev_phase'] == dev_phases_list[2]]
        result = stats.ttest_ind(cond_A[feature], cond_B[feature], equal_var=False)

        y = max(cond_A[feature].mean(),cond_B[feature].mean()) +0.5
        #ax.annotate("***", xy=(1, y + 2.0), zorder=10)
        #ax.annotate('', xy=(0, y), xytext=(2, y), arrowprops=props)
        significance = "ns"
        if result[1] < 0.05:
            significance = "*"
        if result[1] < 0.005:
            significance = "**"
        if result[1] < 0.0005:
            significance = "***"

        x1, x2, h = 0, 2, 0.2
        ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1.5, c='k')
        ax.text((x1 + x2) * .5, y + h, significance, ha='center', va='bottom', color='k')

        ## comparison aISV dev_phase_1 against dev_phase_3

        conds = trajectory_features_phases[trajectory_features_phases['vessel_type'] == "aISV"]
        conds = conds.sort_values(by="frame").dropna()
        cond_A = conds[conds['dev_phase'] == dev_phases_list[0]]
        cond_B = conds[conds['dev_phase'] == dev_phases_list[2]]
        result = stats.ttest_ind(cond_A[feature], cond_B[feature], equal_var=False)

        y = min(cond_A[feature].mean(), cond_B[feature].mean()) - 0.5
        # ax.annotate("***", xy=(1, y + 2.0), zorder=10)
        # ax.annotate('', xy=(0, y), xytext=(2, y), arrowprops=props)
        significance = "ns"
        if result[1] < 0.05:
            significance = "*"
        if result[1] < 0.005:
            significance = "**"
        if result[1] < 0.0005:
            significance = "***"

        x1, x2, h = 0, 2, 0.2
        ax.plot([x1, x1, x2, x2], [y, y - h, y - h, y], lw=1.5, c='k')
        ax.text((x1 + x2) * .5, y - h, significance, ha='center', va='bottom', color='k')
        # comparison of remodelling phase

        conds = trajectory_features_phases[trajectory_features_phases['dev_phase'] == dev_phases_list[2]]
        conds = conds.sort_values(by="frame").dropna()
        cond_A = conds[conds['vessel_type'] == "aISV"]
        cond_B = conds[conds['vessel_type'] == "vISV"]
        result = stats.ttest_ind(cond_A[feature], cond_B[feature], equal_var=False)

        y1 = cond_A[feature].mean()
        y2 = cond_B[feature].mean()
        # ax.annotate("***", xy=(1, y + 2.0), zorder=10)
        # ax.annotate('', xy=(0, y), xytext=(2, y), arrowprops=props)
        significance = "ns"
        if result[1] < 0.05:
            significance = "*"
        if result[1] < 0.005:
            significance = "**"
        if result[1] < 0.0005:
            significance = "***"

        x, h = 2.1, 0.1
        ax.plot([x , x + h , x + h, x], [y1, y1, y2, y2], lw=1.5, c='k')
        ax.text(x+2*h, (y1 + y2) * 0.5, significance, ha='center', va='bottom', color='k')

        ax.set_ylim(-1.5, 6.5)
        ax.set_xlabel("developmental phases")
        ax.set_ylabel("velocity [$\mathrm{\mu}$m/h]")



        # for vessel_type in ['aISV', 'vISV']:

        # #   trajectory_features_vessel = trajectory_features_group[trajectory_features_group["vessel_type"] == vessel_type]
        # #   trajectory_features_vessel = trajectory_features_vessel.sort_values(by="frame").dropna()
        # #   trajectory_features_vessel_phase1 = trajectory_features_vessel[trajectory_features_vessel["frame"] < 48]
        # #   trajectory_features_vessel_phase2 = trajectory_features_vessel[trajectory_features_vessel["frame"] > 48]
        # #   trajectory_features_vessel_phase1["phase"] = "26h-30h"
        # #   trajectory_features_vessel_phase2["phase"] = "30h-48h"
        # #   trajectory_features_vessel_biphasic = pd.concat([trajectory_features_vessel_phase1, trajectory_features_vessel_phase2], ignore_index=True)
        # #   print(trajectory_features_vessel)

        #    fig, ax = plt.subplots(figsize=(18, 6))
        # sns.swarmplot(x = "phase", y="step_size_y", data=trajectory_features_vessel_biphasic, ax=ax)
        #    sns.violinplot(x="phase", y="vd_velocity_micron_per_h", data=trajectory_features_vessel_biphasic, ax=ax, showfliers = False)
        # hue = "smoker"

        velocity_plots["biphasic_velocity_%s_with_stat_test.png" % analysis_group] = fig
        velocity_plots["biphasic_velocity_%s_with_stat_test.pdf" % analysis_group] = fig

        stat_tests["stat_test"] = stat_test

    return velocity_plots, stat_tests


