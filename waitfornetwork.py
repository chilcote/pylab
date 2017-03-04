#!/usr/bin/python
#ref: nick.mcspadden in slack

import subprocess, sys

def wait_for_network():
    """Wait until network access is up."""
    # Wait up to 180 seconds for scutil dynamic store to register DNS
    cmd = [
        '/usr/sbin/scutil',
        '-w', 'State:/Network/Global/DNS',
        '-t', '180'
    ]
    task = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = task.communicate()
    if task.returncode != 0:
        print "Network did not come up after 3 minutes. Aborting"
        sys.exit(1)
    return True

print wait_for_network()
