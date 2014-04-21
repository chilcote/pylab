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
        '''This method is called by all the get methods to gather
        category specific system_profiler data'''
        cmd = '/usr/sbin/system_profiler', category, '-xml'
        task = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = task.communicate()
        plist = plistlib.readPlistFromString(out)[0]
        return plist

    def get_SPStorageDataType(self):
        '''Returns a dict containing storage device data'''
        d = self.get_data('SPStorageDataType')['_items']
        if 'com.apple.corestorage.lvg' in d:
            return d['_items']['com.apple.corestorage.lvg'][0]
        return d[0]

    def get_SPHardwareDataType(self):
        '''Returns a dict containing hardware data'''        
        d = self.get_data('SPHardwareDataType')['_items']
        return d[0]

    def get_SPUniversalAccessDataType(self):
        '''Returns a dict containing universal access data'''                
        d = self.get_data('SPUniversalAccessDataType')['_items']
        return d[0]

    def get_SPDeveloperToolsDataType(self):
        '''Returns a dict containing dev tools data'''                        
        d = self.get_data('SPDeveloperToolsDataType')['_items']
        return d[0]

    def get_SPConfigurationProfileDataType(self):
        '''Returns a dict containing configuration profile data'''          
        d = self.get_data('SPConfigurationProfileDataType')
        print type(d)
        if d['_items']:
            return d['_items'][0]['_items'][0]
        return {}

    def get_SPInstallHistoryDataType(self):
        '''Returns a dict containing install history data'''
        d = self.get_data('SPInstallHistoryDataType')['_items']
        d1 = {}
        for item in d:
            d1[item['_name']] = item['install_date']
        return d1

    def get_SPDiagnosticsDataType(self):
        '''Returns a dict containing diagnostic data'''
        d = self.get_data('SPDiagnosticsDataType')['_items']
        return d[0]

    def get_SPFirewallDataType(self):
        '''Returns a dict containing firewall data'''
        d = self.get_data('SPFirewallDataType')['_items']
        return d[0]

    def get_SPDisplaysDataType(self):
        '''Returns a dict containing display data'''
        d = self.get_data('SPDisplaysDataType')['_items']
        return d[0]

    def get_SPNetworkLocationDataType(self):
        '''Returns a dict containing network location data'''
        d = self.get_data('SPNetworkLocationDataType')['_items']
        return d[0]['spnetworklocation_services'][0]

    def SPManagedClientDataType(self):
        '''Returns a dict containing managed client data'''        
        d = self.get_data('SPManagedClientDataType')['_items']
        if d:
            return d[0]['_items'][0]
        return {}

    def get_SPMemoryDataType(self):
        '''Returns a list of dicts containing memory module data'''        
        d = self.get_data('SPMemoryDataType')['_items']
        l = []
        for item in d[0]['_items']:
            l.append(item)
        return l

    def get_SPNetworkDataType(self):
        '''Returns a list of dicts containing network interface data'''                
        d = self.get_data('SPNetworkDataType')['_items']
        l = []
        for item in d:
            l.append(item)
        return l

    def get_SPPowerDataType(self):
        '''Returns a dict containing power data'''        
        d = self.get_data('SPPowerDataType')['_items']
        d1 = {}
        for item in d:
            d1.update(item)
        return d1

    def get_SPPrefPaneDataType(self):
        '''Returns a list of dicts containing pref pane data'''                        
        d = self.get_data('SPPrefPaneDataType')['_items']
        l = []
        for item in d:
            l.append(item)
        return l

    def get_SPPrintersDataType(self):
        '''Returns a list of dicts containing printer data'''                                
        d = self.get_data('SPPrintersDataType')['_items']
        l = []
        for item in d:
            l.append(item)
        return l

    def get_SPSerialATADataType(self):
        '''Returns a dict containing sata data'''                                
        d = self.get_data('SPSerialATADataType')['_items']
        return d[0]['_items'][0]

    def get_SPSoftwareDataType(self):
        '''Returns a dict containing system software data'''
        d = self.get_data('SPSoftwareDataType')['_items']
        return d[0]

    def get_SPNetworkVolumeDataType(self):
        '''Returns a list of dicts network volume data'''
        d = self.get_data('SPNetworkVolumeDataType')['_items']
        l = []
        for item in d:
            l.append(item)
        return l

    def get_SPAirPortDataType(self):
        '''Returns a dict containing airport data''' 
        d = self.get_data('SPAirPortDataType')['_items']
        d1 = {}
        for item in d[0]['spairport_airport_interfaces']:
            d1.update(item)
        d1.update(d[0]['spairport_software_information'])
        return d1

def print_data(title, dct):
    print '\n%s\n-------------------' % title
    for k, v in dct.items():
        print '%s: %s' % (k,v)

def main():
    sysprofiler = SystemProfiler()

    storage_data = sysprofiler.get_SPStorageDataType()
    print_data('STORAGE DATA', storage_data)
    hardware_data = sysprofiler.get_SPHardwareDataType()
    print_data('HARDWARE DATA', hardware_data)
    universal_access = sysprofiler.get_SPUniversalAccessDataType()
    print_data('UNIVERSAL ACCESS', universal_access)
    dev_tools = sysprofiler.get_SPDeveloperToolsDataType()
    print_data('DEVELOPER TOOLS', dev_tools)
    config_profile = sysprofiler.get_SPConfigurationProfileDataType()
    print_data('CONFIGURATION PROFILE', config_profile)
    install_history = sysprofiler.get_SPInstallHistoryDataType()
    print_data('INSTALL HISTORY', install_history)
    diagnostic_data = sysprofiler.get_SPDiagnosticsDataType()
    print_data('DIAGNOSTIC DATA', diagnostic_data)
    firewall_settings = sysprofiler.get_SPFirewallDataType()
    print_data('FIREWALL SETTINGS', firewall_settings)
    display_data = sysprofiler.get_SPDisplaysDataType()
    print_data('DISPLAY DATA', display_data)
    network_location = sysprofiler.get_SPNetworkLocationDataType()
    print_data('NETWORK LOCATIONS', network_location)
    managed_client_data = sysprofiler.SPManagedClientDataType()
    print_data('MANAGED CLIENT DATA', managed_client_data)
    memory_data = sysprofiler.get_SPMemoryDataType()
    for item in memory_data:
        print_data('MEMORY DATA', item)
    network_data = sysprofiler.get_SPNetworkDataType()
    for item in network_data:
        print_data('NETWORK DATA', item)
    power_data = sysprofiler.get_SPPowerDataType()
    print_data('POWER DATA', power_data)
    pref_data = sysprofiler.get_SPPrefPaneDataType()
    for item in pref_data:
        print_data('PREFERENCE PANE DATA', item)
    printer_data = sysprofiler.get_SPPrintersDataType()
    for item in printer_data:
        print_data('PRINTER DATA', item)
    sata_data = sysprofiler.get_SPSerialATADataType()
    print_data('SATA DATA', sata_data)
    software_data = sysprofiler.get_SPSoftwareDataType()
    print_data('SOFTWARE DATA', software_data)
    network_volume_data = sysprofiler.get_SPNetworkVolumeDataType()
    for item in network_volume_data:
        print_data('NETWORK VOLUME DATA', item)
    airport_data = sysprofiler.get_SPAirPortDataType()
    print_data('AIRPORT DATA', airport_data)

if __name__ == "__main__":
    main()