"""
Module to send email
"""

import subprocess

def email(subject, address, body="", attachment=""):
    """Send email using the linux command line utility mutt"""
    email_command = 'echo \"' + body + '\" | mutt '
    if attachment != "":
        email_command += '-a \"' + attachment + '\" '
    email_command += '-s \"' + subject + '\" -- \"' + address + '\"'
    subprocess.getoutput(email_command)
