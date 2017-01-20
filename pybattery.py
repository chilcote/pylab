#!/usr/bin/python
#ref: https://gist.github.com/pudquick/134acb5f7423312effcc98ec56679136


import objc
from Foundation import NSBundle

IOKit = NSBundle.bundleWithIdentifier_('com.apple.framework.IOKit')

functions = [("IOServiceGetMatchingService", b"II@"),
             ("IOServiceMatching", b"@*"),
             ("IORegistryEntryCreateCFProperties", b"IIo^@@I"),
            ]

objc.loadBundleFunctions(IOKit, globals(), functions)

def battery_dict():
    battery = IOServiceGetMatchingService(0, IOServiceMatching("AppleSmartBattery"))
    if (battery !=0):
        # we have a battery
        err, props = IORegistryEntryCreateCFProperties(battery, None, None, 0)
        return props

def battery_percent():
    d = battery_dict()
    if d:
        curc = d['CurrentCapacity']
        maxc = d['MaxCapacity']
        perc = 100.*curc/maxc
        return perc

print battery_dict()
print battery_percent()
