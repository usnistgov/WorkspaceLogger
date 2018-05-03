#!/usr/bin/env python3

"""
Module to get the current viewport in Ubuntu 16.04 unity
from https://askubuntu.com/questions/900970/how-do-i-look-up-the-name-of-the-current-workspace
"""

import subprocess

def get_res():
    """Return resolution"""
    xr = subprocess.check_output(["xrandr"]).decode("utf-8").split()
    pos = xr.index("current")
    return [int(xr[pos+1]), int(xr[pos+3].replace(",", ""))]

def current():
    """Return current viewport"""
    # get the resolution (viewport size)
    res = get_res()
    # read wmctrl -d
    vp_data = subprocess.check_output(
        ["wmctrl", "-d"]
        ).decode("utf-8").split()
    # get the size of the spanning workspace (all viewports)
    dt = [int(n) for n in vp_data[3].split("x")]
    # calculate the number of columns
    cols = int(dt[0]/res[0])
    # calculate the number of rows
    rows = int(dt[1]/res[1])
    # get the current position in the spanning workspace
    curr_vpdata = [int(n) for n in vp_data[5].split(",")]
    # current column (readable format)
    curr_col = int(curr_vpdata[0]/res[0])
    # current row (readable format)
    curr_row = int(curr_vpdata[1]/res[1])
    # calculate the current viewport
    return curr_col+curr_row*cols
