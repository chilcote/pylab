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
        # print type(d)
        # print type(d['_items'])
        # print type(d['_items'][0])
        # print type(d['_items'][0]['_items'])
        # print type(d['_items'][0]['_items'][0])
        # print type(d['_items'][0]['_items'][0]['_items'])
        # print type(d['_items'][0]['_items'][0]['_items'][0])
        # for k, v in d['_items'][0]['_items'][0]['_items'][0].items():
        #     print '%s: %s' % (k, v)
        # return d['_items'][0]
        return d['_items'][0]['_items'][0]
        # return d['_items'][0]['_items'][0]['_items'][0]
        # return {}

    def get_install_history(self):
        d = self.get_data('SPInstallHistoryDataType')['_items']
        d1 = {}
        for item in d:
            d1[item['_name']] = item['install_date']
        return d1

    def get_diagnostic_data(self):
        d = self.get_data('SPDiagnosticsDataType')['_items']
        return d[0]

    def get_firewall_settings(self):
        d = self.get_data('SPFirewallDataType')['_items']
        return d[0]

    def get_display_data(self):
        d = self.get_data('SPDisplaysDataType')['_items']
        return d[0]

    def get_network_location(self):
        d = self.get_data('SPNetworkLocationDataType')['_items']
        return d[0]['spnetworklocation_services'][0]

    def get_managed_client_data(self):
        d = self.get_data('SPManagedClientDataType')['_items']
        return d[0]['_items'][0]

    def get_memory_data(self):
        d = self.get_data('SPMemoryDataType')['_items']
        l = []
        for item in d[0]['_items']:
            l.append(item)
        return l

    def get_network_data(self):
        d = self.get_data('SPNetworkDataType')['_items']
        l = []
        for item in d:
            l.append(item)
        return l

    def get_power_data(self):
        d = self.get_data('SPPowerDataType')['_items']
        l = []
        for item in d:
            l.append(item)
        return l

    def get_pref_data(self):
        d = self.get_data('SPPrefPaneDataType')['_items']
        l = []
        for item in d:
            l.append(item)
        return l

    def get_printer_data(self):
        d = self.get_data('SPPrintersDataType')['_items']
        l = []
        for item in d:
            l.append(item)
        return l

    def get_sata_data(self):
        d = self.get_data('SPSerialATADataType')['_items']
        return d[0]['_items'][0]

    def get_software_data(self):
        d = self.get_data('SPSoftwareDataType')['_items']
        return d[0]

    def get_network_volume_data(self):
        d = self.get_data('SPNetworkVolumeDataType')['_items']
        l = []
        for item in d:
            l.append(item)
        return l

    def get_airport_data(self):
        d = self.get_data('SPAirPortDataType')['_items']
        print d[0]['spairport_software_information']
        return d[0]['spairport_airport_interfaces']

    def get_airport_software_data(self):
        d = self.get_data('SPAirPortDataType')['_items']
        return d[0]['spairport_software_information']

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
    diagnostic_data = sysprofiler.get_diagnostic_data()
    print_data('DIAGNOSTIC DATA', diagnostic_data)
    firewall_settings = sysprofiler.get_firewall_settings()
    print_data('FIREWALL SETTINGS', firewall_settings)
    display_data = sysprofiler.get_display_data()
    print_data('DISPLAY DATA', display_data)
    network_location = sysprofiler.get_network_location()
    print_data('NETWORK LOCATIONS', network_location)
    managed_client_data = sysprofiler.get_managed_client_data()
    print_data('MANAGED CLIENT DATA', managed_client_data)
    memory_data = sysprofiler.get_memory_data()
    for item in memory_data:
        print_data('MEMORY DATA', item)
    network_data = sysprofiler.get_network_data()
    for item in network_data:
        print_data('NETWORK DATA', item)
    power_data = sysprofiler.get_power_data()
    for item in power_data:
        print_data('POWER DATA', item)
    pref_data = sysprofiler.get_pref_data()
    for item in pref_data:
        print_data('PREFERENCE PANE DATA', item)
    printer_data = sysprofiler.get_printer_data()
    for item in printer_data:
        print_data('PRINTER DATA', item)
    sata_data = sysprofiler.get_sata_data()
    print_data('SATA DATA', sata_data)
    software_data = sysprofiler.get_software_data()
    print_data('SOFTWARE DATA', software_data)
    network_volume_data = sysprofiler.get_network_volume_data()
    for item in network_volume_data:
        print_data('NETWORK VOLUME DATA', item)
    airport_data = sysprofiler.get_airport_data()
    for item in airport_data:
        print_data('AIRPORT DATA', item)
    airport_software_data = sysprofiler.get_airport_software_data()
    print_data('AIRPORT SOFTWARE DATA', airport_software_data)



if __name__ == "__main__":
    main()