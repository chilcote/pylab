#!/usr/bin/env python

'''
This script collects data from system_profiler
'''

##############################################################################
# Copyright 2014 Joseph Chilcote
# 
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not
#  use this file except in compliance with the License. You may obtain a copy
#  of the License at  
# 
#       http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
##############################################################################

import os, sys, subprocess
import plistlib
from pprint import pprint

class SystemProfiler(object):
    '''This object returns dictionaries of data from system_profiler'''

    def __init__(self):
        pass

    def get_data(self, category):
        cmd = '/usr/sbin/system_profiler', category, '-xml'
        task = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = task.communicate()
        plist = plistlib.readPlistFromString(out)[0]
        return plist

    def get_storage_data(self):
        d = self.get_data('SPStorageDataType')['_items']
        if 'com.apple.corestorage.lvg' in d:
            return d['_items']['com.apple.corestorage.lvg'][0]
        return d[0]

    def get_hardware_data(self):
        d = self.get_data('SPHardwareDataType')['_items']
        return d[0]

    def get_universal_access_data(self):
        d = self.get_data('SPUniversalAccessDataType')['_items']
        return d[0]

    def get_dev_tools(self):
        d = self.get_data('SPDeveloperToolsDataType')['_items']
        return d[0]

    def get_config_profile(self):
        d = self.get_data('SPConfigurationProfileDataType')
        return d

    def get_install_history(self):
        d = self.get_data('SPInstallHistoryDataType')['_items']
        d1 = {}
        for item in d:
            d1[item['_name']] = item['install_date']
        return d1

def print_data(title, dct):
    print '\n%s\n-------------------' % title
    for k, v in dct.items():
        print '%s: %s' % (k,v)

def main():
    sysprofiler = SystemProfiler()

    storage_data = sysprofiler.get_storage_data()
    print_data('STORAGE DATA', storage_data)
    hardware_data = sysprofiler.get_hardware_data()
    print_data('HARDWARE DATA', hardware_data)
    universal_access = sysprofiler.get_universal_access_data()
    print_data('UNIVERSAL ACCESS', universal_access)
    dev_tools = sysprofiler.get_dev_tools()
    print_data('DEVELOPER TOOLS', dev_tools)
    config_profile = sysprofiler.get_config_profile()
    print_data('CONFIGURATION PROFILE', config_profile)
    install_history = sysprofiler.get_install_history()
    print_data('INSTALL HISTORY', install_history)

if __name__ == "__main__":
    main()