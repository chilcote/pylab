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

def get_data(category, recursive=False):
    cmd = '/usr/sbin/system_profiler', category, '-xml'
    task = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = task.communicate()
    if not recursive:
        plist = plistlib.readPlistFromString(out)[0]['_items'][0]
    else:
        plist = plistlib.readPlistFromString(out)[0]['_items']
    return plist

def debug_get_data(category):
    cmd = '/usr/sbin/system_profiler', category, '-xml'
    task = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = task.communicate()
    plist = plistlib.readPlistFromString(out)[0]
    return plist

def print_data(dict):
    for k, v in dict.items():
        print '%s: %s' % (k,v)

def main():
    print '\nSTORAGE DATA\n-------------------'
    storage_data = get_data('SPStorageDataType')
    print_data(storage_data['com.apple.corestorage.lvg'])
    # pprint(storage_data)

    print '\nHARDWARE DATA\n-------------------'
    hardware_data = get_data('SPHardwareDataType')
    print_data(hardware_data)
    #pprint(hardware_data)
    
    print '\nUNIVERSAL ACCESS\n-------------------'
    universal_access = get_data('SPUniversalAccessDataType')
    print_data(universal_access)
    # pprint(universal_access)
    
    print '\nCONFIGURATION PROFILE\n-------------------'
    config_profile = get_data('SPConfigurationProfileDataType')
    print_data(config_profile['_items'][0])
    # pprint(config_profile)

    print '\nDEVELOPER TOOLS\n-------------------'
    dev_tools = get_data('SPDeveloperToolsDataType')
    print_data(dev_tools)
    # pprint(dev_tools)
    
    print '\nINSTALL HISTORY\n-------------------'
    install_history = get_data('SPInstallHistoryDataType', recursive=True)
    for item in install_history:
        print '%s: %s' % (item['_name'], item['install_date'])
    # pprint(install_history)


if __name__ == "__main__":
    main()