#!/usr/bin/env python

'''
This script collects data from diskutil
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

class Diskutil(object):

    def __init__(self):
        '''Initialize object'''
        self.data = self.get_data()

    def get_data(self):
        '''Returns a dict of all diskutil data'''
        cmd = '/usr/sbin/diskutil', 'list', '-plist'
        task = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
        (out, err) = task.communicate()
        plist = plistlib.readPlistFromString(out)
        return plist

    def get_alldisks(self):
        '''Returns a dict of all disk identifiers'''
        d = self.data
        d1 = {}
        d1['All Disks'] = d['AllDisks']
        return d1

    def get_wholedisks(self):
        '''Returns a dict of all whole disk identifiers'''
        d = self.data
        d1 = {}
        d1['Whole Disks'] = d['WholeDisks']
        return d1

    def get_allpartitions(self):
        '''Returns a dict of all disk partitions'''
        d = self.data
        d1 = {}
        d1['Partitions'] = d['AllDisksAndPartitions']
        return d1

    def get_volumes(self):
        '''Returns a dict of all mounted volumes'''
        d = self.data
        d1 = {}
        d1['Volumes'] = d['VolumesFromDisks']
        return d1

    def get_partitions(self):
        '''Returns a dict of all partitions'''
        d = self.data
        d1 = {}
        disks = d['AllDisks']
        partitions = d['AllDisksAndPartitions']
        for partition in partitions:
            if 'Partitions' in partition:
                for p in partition['Partitions']:
                    if 'MountPoint' in p:
                        d1[p['DeviceIdentifier']] = (
                                                    p['VolumeName'],
                                                    p['Content'],
                                                    p['Size'],
                                                    p['MountPoint']
                                                    )
                    elif 'VolumeName' in p and not 'MountPoint' in p:
                        d1[p['DeviceIdentifier']] = (
                                                    p['VolumeName'],
                                                    p['Content'],
                                                    p['Size'],
                                                    ''
                                                    )
                    else:
                        d1[p['DeviceIdentifier']] = (
                                                    '',
                                                    p['Content'],
                                                    p['Size'],
                                                    ''
                                                    )
            else:
                d1[partition['DeviceIdentifier']] = (
                                                    partition['VolumeName'],
                                                    partition['Content'],
                                                    partition['Size'],
                                                    partition['MountPoint']
                                                    )
        return d1

    def get_bootvolume(self):
        '''Returns the boot volume'''
        d = {}
        p = self.get_partitions()
        for k, v in p.items():
            if '/' in v:
                d['Boot Volume'] = v[0]
        return d

def main():
    du = Diskutil()
    # print du.get_data()
    # print du.get_alldisks()
    # print du.get_wholedisks()
    vol = du.get_volumes()
    for k, v in vol.items():
        print '%s: %s' % (k, v)    
    bv = du.get_bootvolume()
    for k, v in bv.items():
        print '%s: %s' % (k, v)
    p = du.get_partitions()
    for k, v in sorted(p.items()):
        print '%s: %s' % (k, v)
    print du.get_alldisks()
    print du.get_wholedisks()

if __name__ == "__main__":
    main()
