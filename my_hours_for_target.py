import argparse
import json
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--target_label", "-l", help="label of interest", type=str, default="Proj1")
parser.add_argument("--target_percentage", "-p", help="percent of time you would like to spend on target_label", type=float, default=0.1)
parser.add_argument("--status_file", "-s", help="status file name", type=str, default="stat.txt")
args = parser.parse_args()

try:
    stat = open(args.status_file, 'r')
    stat_data = json.load(stat)
except:
    raise

summary = pd.read_csv(stat_data["summary_file"])
grp = summary.groupby("label").sum()
if args.target_label not in grp["minutes"]:
    target_minutes = 0
else:
    target_minutes = grp["minutes"][args.target_label]
total_minutes = grp["minutes"].sum()
available = (args.target_percentage*total_minutes - target_minutes)/(1. - args.target_percentage)

print("Available time to spend on", args.target_label, "to reach target of", int(args.target_percentage*100), "%:\n", round(available/60., 1), "hours,", round(available/60/8, 1), "days, or", round(available/60/8/5, 1), "weeks")


