'''
This class is updated every minute to log a timeseries.
Occasionally, the script may also notify you to take a break.
And it also compiles and sends daily summaries.
'''

import json
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import viewport

def file_len(fname):
    '''
    Return the number of lines in file fname
    https://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
    '''
    return sum(1 for line in open(fname))

def parse_end_points(dataframe, break_label, column=1):
    '''
       Return the timeseries pandas dataframe with parsed endpoints.
       In practice, this allows you to ignore the beginning and end of the day.
       All timeseries from beginning and end which match the given "break_label"
       in the given column are removed.
    '''
    vals = dataframe[column].values
    index_begin = 0
    index = 0
    label = break_label
    while (index < len(vals)) and (label == break_label):
        label = vals[index]
        index_begin = index
        index += 1
    index = len(vals) - 1
    label = break_label
    while (index >= 0) and (label == break_label):
        label = vals[index]
        index_end = index
        index -= 1
    return dataframe[index_begin:index_end]

def autolabel(rects):
    '''
    Attach a text label above each bar displaying its height
    https://matplotlib.org/examples/api/barchart_demo.html
    '''
    for rect in rects:
        height = rect.get_height()
        plt.gca().text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

def plot_summary(summary_file="summary.txt"):
    summary = pd.read_csv(summary_file)
    grp = summary.groupby("label").sum()
    grp_perc = grp["minutes"]/grp["minutes"].sum()*100
    rects1 = plt.bar(grp_perc.index, grp_perc)
    plt.ylabel("percentage time", fontsize=16)
    autolabel(rects1)
    plt.show()

class Logger(object):
    def __init__(self, data_file="logger.json"):
        with open(data_file, 'r') as status:
            self._data = json.load(status)

    def write(self, data_file="logger.json"):
        with open(data_file, 'w') as status:
            json.dump(self._data, status, indent=4, separators=(',', ': '))

    def update_date(self):
        self._data['day'] = datetime.datetime.now().day
        self._data['month'] = datetime.datetime.now().month
        self._data['year'] = datetime.datetime.now().year

    def reset_break(self):
        self._data['minutes_since_break'] = 0
        self._data['break_notified'] = 0

    def update_minutes_since_break(self):
        if not 'minutes_since_break' in self._data:
          self.reset_break()
        self._data['minutes_since_break'] += 1

    def plot_timeseries(self, timeseries):
        '''Plot the timeseries and a histogram and save as plot.png
           Arguments:
             timeseries: pandas dataframe
        '''
        num_labels = len(self._data["workspace_labels"])
        plt.subplots(1, 2, figsize=(7, 3))
        plt.subplot(1, 2, 1)
        plt.scatter(timeseries.index, timeseries[0])
        plt.yticks(np.arange(0, num_labels, 1.0), self._data["workspace_labels"])
        plt.xlabel("minute")
        plt.subplot(1, 2, 2)
        plt.hist(timeseries[0], bins=np.arange(num_labels)-0.5, orientation='horizontal')
        plt.yticks(np.arange(0, num_labels, 1.0), self._data["workspace_labels"])
        plt.xlabel("minutes")
        plt.tight_layout()
        plt.savefig("plot.png", bbox_inches="tight")

    def print_summary(self, timeseries):
        '''summarize the timeseries and then start over'''
        try:
            if isinstance(timeseries, str):
                timeseries = pd.read_csv(timeseries, header=None)
                timeseries = parse_end_points(dataframe=timeseries,
                                              break_label=self._data["break_label"],
                                              column=1)
            with open(self._data['summary_file'], 'a') as smmry:
                if file_len(self._data['summary_file']) == 0:
                    print('month,day,year,label,minutes', file=smmry)
                count = timeseries.groupby(1).count()
                for index in range(len(count.index)):
                    label = count[0].index[index]
                    num = count[0][index]
                    print(str(self._data['month']) + "," +
                          str(self._data['day']) + "," +
                          str(self._data['year']) + "," +
                          str(label) + "," + str(num), file=smmry)
                open(self._data['timeseries_file'], 'w').close()
        except FileNotFoundError:
            i = 0 # do nothing
        except:
            raise

    def summarize(self):
        if file_len(self._data['timeseries_file']) <= 0:
            return
        timeseries = pd.read_csv(self._data['timeseries_file'], header=None)
        timeseries = parse_end_points(dataframe=timeseries,
                                      break_label=self._data["break_label"],
                                      column=1)
        if timeseries.empty:
            return
        self.plot_timeseries(timeseries)
        if self._data['disable_notify'] == 0:
            import my_email
            my_email.email(subject="WorkspaceLogger",
                           address=self._data['email_address'],
                           body='WorkspaceLogger',
                           attachment='plot.png')
        self.print_summary(timeseries=timeseries)

    def update_timeseries(self):
        dflabels = self._data["workspace_labels"]
        workspace = viewport.current()
        with open(self._data['timeseries_file'], 'a') as log:
            if file_len(self._data['timeseries_file']) > 5*24*60:
                return
            if workspace < len(dflabels):
                print(str(workspace) + "," + str(dflabels[workspace]), file=log)
            else:
                print(str(workspace) + ", unlabeled", file=log)
            if dflabels[workspace] == self._data['break_label']:
                self.reset_break()

    def update_break_notification(self):
        if (self._data['minutes_since_break'] >= self._data['minutes_per_break'] and
            self._data['disable_notify'] == 0 and
            self._data['break_notified'] == 0):
            import my_email
            my_email.email(subject="Take a break",
                           address=self._data['email_address'],
                           body='Take a >30 second break. Its been over ' +
                           str(self._data['minutes_per_break']) + ' minutes. --WorkspaceLogger')
            self._data['break_notified'] = 1

    def update_summary(self):
        if 'day' in self._data:
            if self._data['day'] != datetime.datetime.now().day:
                self.summarize()

    def update(self):
        self.update_minutes_since_break()
        self.update_summary()
        self.update_timeseries()
        self.update_break_notification()
        self.update_date()

    def time_to_reach_target(self, target_label="Proj1", target_percentage=0.1):
        summary = pd.read_csv(self._data["summary_file"])
        grp = summary.groupby("label").sum()
        if target_label not in grp["minutes"]:
            target_minutes = 0
        else:
            target_minutes = grp["minutes"][target_label]
        total_minutes = grp["minutes"].sum()
        available = (target_percentage*total_minutes - target_minutes)/(1. - target_percentage)
        return available


    def print_status(self):
        '''
        Print the status, used continuously by status.py.
        '''
        print(self._data['minutes_since_break'], "minutes since break.")
        print("\nDays to reach target percentages:")
        for target in self._data["target_percentage"]:
            label = target["label"]
            available = self.time_to_reach_target(
                target_label=label,
                target_percentage=target["percent"])
            print(label + ":", round(available/60/8, 1))
