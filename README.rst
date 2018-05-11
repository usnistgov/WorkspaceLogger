*************************
README
*************************

The WorkspaceLogger is a simple python script to log and analyze which workspaces ("viewports" in unity) you are using in Ubuntu 16.04 (see `<DISCLAIMER.rst>`_).
If you dedicate each workspace to a specific type of task, you may then analyze how much time is spent on these tasks.
You may also automate reminders and messages for taking breaks or projects that are collecting dust.
Note: healthy workstation guidelines suggest that you take two to three 30- to 60-second breaks each hour to allow your body to recover from periods of repetitive stress.
This notification feature, and the analysis, is made possible if you reserve one workspace which you make active just before you stop using the workstation.
The scripts are meant to be run every minute by crontab, and saved periodically for analysis.

Installation
##############

#. Enable workspaces: Appearance -> Behavior -> Enable workspaces

#. Install X Window manager

.. code-block:: bash

   sudo apt install wmctrl

#. Update the path to python in `<update.sh>`_.

#. `Update workspace labels`_. If you would like more than 4 (default), `Add more workspaces`_.

#. Create your custom logger.json (as shown in `<logger.json.example>`) and customize `Notifications`_.

#. Test that the python script runs by the command below. A timeseries.txt file should have been created with your current workspace.

.. code-block:: bash

    ./update.sh

#. Add to crontab as shown in `<crontab.example>`_.

.. code-block:: bash

   crontab -e

#. If all goes well, you should see timeseries.txt updating every minute. And the file summary.txt will populate at midnight everyday, with an email notification and attached plot.png histogram. You may also receive notifications if you are not taking breaks. Use the mail command to check for errors if the logger does not appear to be working.

Update workspace labels
########################

Using `<labels.txt.example>`_ as a template, create a file `labels.txt` and assign labels for your workspace for a given numerical code for the workspace.
Workspaces are numbered from left to right and top to bottom, starting with 0.
These labels are the ones that will show up with your analysis, and they can be changed at any time.

Add more workspaces
########################

You can add more workspaces to unity as follows:

.. code-block:: bash

    sudo apt install compizconfig-settings-manager
    ccsm

Navigate to General Options -> Desktop Size tab

Notifications
############################

This script uses the linux command line program "mutt" to send email notifications.

.. code-block::

   sudo apt install mutt

https://wiki.ubuntu.com/Mutt

To disable the notifications, change "disable_notify" from 0 to 1 in `<logger.json>`_.

To add your email address, update "email_address" in `<logger.json>`_.

To change the number of minutes until notification, update "minutes_per_break" in `<logger.json>`_.

To change the workspace label which corresponds to taking a break, update "break_label" in `<logger.json>`_.

To reset the break notification:

.. code-block:: bash

    python /path/to/WorkspaceLogger/reset_break.py

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
