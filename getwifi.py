#!/usr/bin/python

import time
import subprocess

ifconfig_data = subprocess.check_output(["ifconfig", "en2"])
contains_ip = [i for i in ifconfig_data.split() if i.startswith('192.')]
airport_off = '/usr/sbin/networksetup -setairportpower en2 off'
airport_on = '/usr/sbin/networksetup -setairportpower en2 on'

while contains_ip == []:
    print "No IP, turning Airport Off and On again"
    subprocess.call(airport_off.split())
    subprocess.call(airport_on.split())
    time.sleep(20)
    ifconfig_data = subprocess.check_output(["ifconfig", "en2"])
    contains_ip = [i for i in ifconfig_data.split() if i.startswith('192.')]
