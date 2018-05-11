import argparse
import json
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--target_label", "-l", help="label of interest", type=str, default="Proj1")
parser.add_argument("--target_percentage", "-p", help="percent of time you would like to spend on target_label", type=float, default=0.1)
parser.add_argument("--status_file", "-s", help="status file name", type=str, default="stat.txt")
args = parser.parse_args()

import logger
log = logger.Logger()
available = log.time_to_reach_target(target_label=args.target_label,
                                     target_percentage=args.target_percentage)
print("Available time to spend on", args.target_label, "to reach target of",
      int(args.target_percentage*100), "%:\n", round(available/60., 1),
      "hours,", round(available/60/8, 1), "days, or",
      round(available/60/8/5, 1), "weeks")
