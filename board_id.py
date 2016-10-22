#!/usr/bin/python
# ref: https://gist.github.com/bruienne/f81ea88253629abaf5f9

import objc
import plistlib

class attrdict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

ServerInformation = attrdict()
ServerInformation_bundle = objc.loadBundle('ServerInformation', ServerInformation, \
    bundle_path='/System/Library/PrivateFrameworks/ServerInformation.framework')

platformsupport = plistlib.readPlist('/System/Library/CoreServices/PlatformSupport.plist')
#
disabledsystems = platformsupport.get('SupportedBoardIds')
#
print('------------------------------------------------------------\n%i Board IDs in list\n------------------------------------------------------------\n' % len(disabledsystems))

unmatchedboardids = []

for system in disabledsystems:
    for modelid in ServerInformation.ServerInformationComputerModelInfo.modelPropertiesForBoardIDs_([system]):
        if system not in modelid:
            print('Board ID: %s = System ID: %s' % (system, modelid))
        else:
            unmatchedboardids.append(system)

if len(unmatchedboardids) > 0:
    print('------------------------------------------------------------')
    for boardid in unmatchedboardids:
        print('-- No match for Board ID %s --' % boardid)
    print('------------------------------------------------------------\n')
