import sys
import numpy as np
import matplotlib
import os
matplotlib.use('Agg')
import pylab as plt
import scipy as sci
from scipy import io, stats, spatial
import pandas as pd
import math
import datetime
import seaborn as sns
import logging
from typing import Dict, List
import yaml


def plot_link_lengths_hist(link_data_summary: pd.DataFrame):

    plots = dict()

    for analysis_group in link_data_summary["analysis_group"].unique():

        link_data_summary_ = link_data_summary[link_data_summary["analysis_group"] == analysis_group]


        for vessel_type in link_data_summary_["vessel_type"].unique():


            link_data_summary_sub = link_data_summary_[link_data_summary_["vessel_type"] == vessel_type]

            fig, ax = plt.subplots(figsize=(5, 5))



            sns.histplot(x = "link_length", data = link_data_summary_sub, ax=ax, binwidth=6, binrange=[0,144])#,  binwidth=15, ax=ax)

            ax.set_xlim(0,144.0)
            ax.set_ylim(0,100.0)
            ax.set_xlabel("track length in hours")
            ax.set_ylabel("counts")

            ax.set_xticks(np.arange(0,144,12))
            ax.set_xticklabels(np.arange(0,24,2))

            ax.axvline(x=6, color="r", linestyle="dashed")

            plots["link_length_hist_%s_%s.pdf" % (vessel_type, analysis_group)] = fig
            plots["link_length_hist_%s_%s.png" % (vessel_type, analysis_group)] = fig

        link_data_summary_sub = link_data_summary_[(link_data_summary_["vessel_type"] == "aISV") | (link_data_summary_["vessel_type"] == "vISV")]

        fig, ax = plt.subplots(figsize=(5, 5))

        sns.histplot(x="link_length", data=link_data_summary_sub, ax=ax, binwidth=6,
                     binrange=[0, 144])  # ,  binwidth=15, ax=ax)

        ax.set_xlim(0, 144.0)
        ax.set_ylim(0, 200.0)
        ax.set_xlabel("track length in hours")
        ax.set_ylabel("counts")

        ax.set_xticks(np.arange(0, 144, 12))
        ax.set_xticklabels(np.arange(0, 24, 2))

        ax.axvline(x=6, color="r", linestyle="dashed")

        plots["link_length_hist_%s_%s.pdf" % ("ISV", analysis_group)] = fig
        plots["link_length_hist_%s_%s.png" % ("ISV", analysis_group)] = fig

    return plots

def plot_link_lengths(fish_data_summary: pd.DataFrame, link_data_summary: pd.DataFrame):

    plots = dict()

    for analysis_group in link_data_summary["analysis_group"].unique():

        link_data_summary_ = link_data_summary[link_data_summary["analysis_group"] == analysis_group]

        # all vessel types separately

        for vessel_type in link_data_summary_["vessel_type"].unique():
            link_data_summary_sub = link_data_summary_[link_data_summary_["vessel_type"] == vessel_type]

            fig, ax = plt.subplots(figsize=(10, 10))

            height = 2.0
            #color = 'goldenrod'
            #color = 'gainsboro'
            color = 'burlywood'
            tick_positions = []
            tick_labels = []
            for fish_number in link_data_summary_sub["fish_number"].unique():

                link_data_plot = link_data_summary_sub[link_data_summary_sub["fish_number"]==fish_number]
                link_data_plot = link_data_plot.sort_values(by=['start_frame'])

                print("plot track length of fish %s" % fish_number)

                for unique_id in  link_data_plot["unique_id"].unique():

                    single_link = link_data_plot[link_data_plot["unique_id"] == unique_id]

                    ax.plot([single_link["start_frame"].iloc[0], single_link["end_frame"].iloc[0]], [height,height], color = color, marker = 'x', ms = 1, mec = 'k', mfc = 'k')
                    height += 10.0

                #if color == "r":
                #    color = "b"
                #else:
                #    color = "r"

                height += 50.0
                #ax.axhline(height, color ='k', linestyle = 'dashed')
                linewidth = 5.0
                tick_positions.append(height)
                ax.plot([link_data_plot["start_frame"].min()+linewidth/2.0 - 2.0, link_data_plot["end_frame"].max()-linewidth/2.0 +2.0],[height,height], color='k', linewidth=linewidth)
                height += 100.0
                tick_labels.append(int(fish_number))
            #ax.set(ylabel=None,yticklabels=[] )

            ax.set_ylabel("fish ID")
            ax.set_yticks(tick_positions)
            ax.set_yticklabels(tick_labels)

            ax.set_xlim(0,144.0)
            ax.set_xlabel("time in hpf")

            ax.set_xticks(np.arange(0, 144, 12))
            ax.set_xticklabels(np.arange(24, 48, 2))

            plots["link_length_%s_%s.pdf" % (vessel_type, analysis_group)] = fig
            plots["link_length_%s_%s.png" % (vessel_type, analysis_group)] = fig


        link_data_summary_sub = link_data_summary_[(link_data_summary_["vessel_type"] == "aISV") | (link_data_summary_["vessel_type"] == "vISV")]

        fig, ax = plt.subplots(figsize=(10, 10))
        height = 2.0
        #color = 'goldenrod'
        tick_positions = []
        tick_labels = []
        for fish_number in link_data_summary_sub["fish_number"].unique():

            link_data_plot = link_data_summary_sub[link_data_summary_sub["fish_number"]==fish_number]
            link_data_plot = link_data_plot.sort_values(by=['start_frame'])

            print("plot track length of fish %s" % fish_number)

            for unique_id in  link_data_plot["unique_id"].unique():

                single_link = link_data_plot[link_data_plot["unique_id"] == unique_id]
                ax.plot([single_link["start_frame"].iloc[0], single_link["end_frame"].iloc[0]],[height,height], color = color, marker = 'x', ms = 1, mec = 'k', mfc = 'k' )
                height += 10.0

            height += 50.0
            linewidth = 5.0
            tick_positions.append(height)
            ax.plot([link_data_plot["start_frame"].min()+linewidth/2.0 - 2.0, link_data_plot["end_frame"].max()-linewidth/2.0 +2.0],[height,height], color='k', linewidth=linewidth)
            height += 100.0
            tick_labels.append(int(fish_number))

        ax.set_ylabel("fish ID")
        ax.set_yticks(tick_positions)
        ax.set_yticklabels(tick_labels)

        ax.set_xlim(0,144.0)
        ax.set_xlabel("time in hpf")

        ax.set_xticks(np.arange(0, 144, 12))
        ax.set_xticklabels(np.arange(24, 48, 2))

        plots["link_length_%s_%s.pdf" % ("ISV", analysis_group)] = fig
        plots["link_length_%s_%s.png" % ("ISV", analysis_group)] = fig

    return plots

