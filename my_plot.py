"""
Module to plot
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_timeseries(timeseries, labels_file):
    """Plot the timeseries and a histogram and save as plot.png
       Arguments:
         timeseries: pandas dataframe
         labels_file: file which contains all workspace labels
    """
    dflabels = pd.read_csv(labels_file)
    num_labels = len(dflabels)

    plt.subplots(1, 2, figsize=(7, 3))

    plt.subplot(1, 2, 1)
    plt.scatter(timeseries.index, timeseries[0])
    plt.yticks(np.arange(0, num_labels, 1.0), dflabels["label"])
    plt.xlabel("minute")

    plt.subplot(1, 2, 2)
    plt.hist(timeseries[0], bins=np.arange(num_labels)-0.5, orientation='horizontal')
    plt.yticks(np.arange(0, num_labels, 1.0), dflabels["label"])
    plt.xlabel("minutes")

    plt.tight_layout()
    plt.savefig("plot.png", bbox_inches="tight")

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    https://matplotlib.org/examples/api/barchart_demo.html
		"""
    for rect in rects:
        height = rect.get_height()
        plt.gca().text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

def summary(summary_file="summary.txt"):
		summary = pd.read_csv(summary_file)
		grp = summary.groupby("label").sum()
		grp_perc = grp["minutes"]/grp["minutes"].sum()*100
		rects1 = plt.bar(grp_perc.index, grp_perc)
		plt.ylabel("percentage time", fontsize=16)
		autolabel(rects1)
		plt.show()
