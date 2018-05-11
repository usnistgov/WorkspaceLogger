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
log.time_to_reach_target(target_label=args.target_label,
                         target_percentage=args.target_percentage)
