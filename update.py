"""
This script is called every minute to update the timeseries.
Occasionally, the script may also notify you to take a break.
And it also compiles and sends daily summaries.
"""

import argparse
import json
import datetime
import pandas as pd
import viewport

parser = argparse.ArgumentParser()
parser.add_argument("--timeseries_file", "-l", help="log file name", type=str,
                    default="timeseries.csv")
parser.add_argument("--summary_file", "-u", help="summary file name", type=str,
                    default="summary.txt")
parser.add_argument("--status_file", "-s", help="status file name", type=str, default="stat.txt")
parser.add_argument("--labels_file", "-w", help="WORKSPACE labels file name", type=str,
                    default="labels.txt")
parser.add_argument("--minutes_per_break", "-m",
                    help="notify if this many minutes pass without break", type=int, default=30)
parser.add_argument("--break_label", "-b", help="label for break", type=str, default="Out")
parser.add_argument("--disable_notify", "-d", help="disable notifications", action='store_true',
                    default=False)
parser.add_argument("--email_address", "-e", help="email address for notifications", type=str,
                    default="user@host.com")
args = parser.parse_args()

# read the day and break info from the stat file
try:
    stat = open(args.status_file, 'r')
    stat_data = json.load(stat)
except FileNotFoundError:
    stat_data = {}
    stat_data['day'] = datetime.datetime.now().day
    stat_data['month'] = datetime.datetime.now().month
    stat_data['year'] = datetime.datetime.now().year
    stat_data['minutes_since_break'] = 0
    stat_data['break_notified'] = 0
except:
    raise
stat_data['minutes_since_break'] += 1

def summary(timeseries, summary_file):
    """summarize the timeseries and then start over"""
    try:
        if isinstance(timeseries, str):
            timeseries = pd.read_csv(timeseries, header=None)
            timeseries = my_parse.endpoints(dataframe=timeseries, break_label=args.break_label,
                                            column=1)
        with open(summary_file, 'a') as smmry:
            count = timeseries.groupby(1).count()
            for index in range(len(count.index)):
                label = count[0].index[index]
                num = count[0][index]
                print(str(stat_data['month']) + "," +
                      str(stat_data['day']) + "," +
                      str(stat_data['year']) + "," +
                      str(label) + "," + str(num), file=smmry)
        open(args.timeseries_file, 'w').close()
    except FileNotFoundError:
        i = 0 # do nothing
    except:
        raise

# check if the day has changed
if stat_data['day'] != datetime.datetime.now().day:
    timeseries = pd.read_csv(args.timeseries_file, header=None)
    import my_parse
    timeseries = my_parse.endpoints(dataframe=timeseries, break_label=args.break_label, column=1)
    if timeseries:
        import my_plot
        my_plot.plot_timeseries(timeseries=timeseries,
                                labels_file=args.labels_file)
        if not args.disable_notify:
            import my_email
            my_email.email(subject="WorkspaceLogger",
                           address=args.email_address,
                           body='WorkspaceLogger',
                           attachment='plot.png')
        summary(timeseries=timeseries,
                summary_file=args.summary_file)

# read labels and append line to time series
DFLABELS = pd.read_csv(args.labels_file)
WORKSPACE = viewport.current()
with open(args.timeseries_file, 'a') as log:
    if WORKSPACE < len(DFLABELS):
        print(str(WORKSPACE) + "," + str(DFLABELS["label"][WORKSPACE]), file=log)
    else:
        print(str(WORKSPACE) + ", unlabeled", file=log)
    if DFLABELS["label"][WORKSPACE] == args.break_label:
        stat_data['minutes_since_break'] = 0

# notify by email if user should take a break
if stat_data['minutes_since_break'] >= args.minutes_per_break and not args.disable_notify:
    if stat_data['break_notified'] == 0:
        import my_email
        my_email.email(subject="Take a break",
                       address=args.email_address,
                       body='Take a >30 second break. Its been over ' +
                       str(args.minutes_per_break) + ' minutes. --WorkspaceLogger')
        stat_data['break_notified'] = 1
    else:
        stat_data['break_notified'] = 0

# print a new stat file
stat_data['day'] = datetime.datetime.now().day
stat_data['month'] = datetime.datetime.now().month
stat_data['year'] = datetime.datetime.now().year
with open(args.status_file, 'w') as stat:
    json.dump(stat_data, stat)
