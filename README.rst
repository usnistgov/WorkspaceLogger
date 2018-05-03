*************************
README
*************************

The WorkspaceLogger is a simple python and bash script to log and analyze which workspaces ("viewports" in unity) you are using in Ubuntu 16.04 (see `<DISCLAIMER.rst>_`).
If you dedicate each workspace to a specific type of task, you may then analyze how much time is spent on these tasks.
You may also automate reminders and messages for taking breaks or projects that are collecting dust.
Note: healthy workstation guidelines suggest that you two 2-3 30- to 60-second breaks each hour to allow your body to recover from periods of repetitive stress.
This notification feature, and the analysis, is made possible if you reserve one workspace which you make active just before you stop using the workstation.

Installation
##############

Enable workspaces: Displace -> Behavior -> Enable workspaces

.. code-block::

   sudo apt install wmctrl

The scripts are meant to be run every minute by crontab, and saved periodically for analysis.
To begin logging and saving, simply take a look at `<crontab.example>`_ and modify your crontab using "crontab -e" with the appropriate path to the bash scripts.

Update workspace labels
########################

Open labels.txt and assign labels for your workspace for a given numerical code for the workspace.
Workspaces are numbered from left to right and top to bottom, starting with 0.
These labels are the ones that will show up with your analysis, and they can be changed at any time.

Add more workspaces
########################

You can add more workspaces to unity as follows:

.. code-block:: bash

    sudo apt install compizconfig-settings-manager
    ccsm

Navigate to General Options -> Desktop Size tab

Notify and other options
############################

This script uses the linux command line program "mutt" to send email notifications.

.. code-block::

   sudo apt install mutt

https://wiki.ubuntu.com/Mutt

To disable the notifications, use `python update.py --disable_notify` in your crontab.

For more options, use `python update.py --help`.

External contribution
###########################################

The python code used for computing which workspace (viewport) is active was taken almost entirely from Jacob Vlijm's 4/6/17 answer on https://askubuntu.com/questions/900970/how-do-i-look-up-the-name-of-the-current-workspace

Contact
#######

Harold Wickes Hatch

https://www.nist.gov/people/harold-hatch

harold.hatch@nist.gov

.. include:: DISCLAIMER.rst

.. include:: LICENSE.rst
