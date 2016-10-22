#!/usr/bin/python
#ref https://gist.github.com/pudquick/c7dd1262bd81a32663f0

import objc
from Foundation import NSBundle

IOKit_bundle = NSBundle.bundleWithIdentifier_('com.apple.framework.IOKit')

functions = [("IOServiceGetMatchingService", b"II@"),
             ("IOServiceMatching", b"@*"),
             ("IORegistryEntryCreateCFProperty", b"@I@@I"),
            ]

objc.loadBundleFunctions(IOKit_bundle, globals(), functions)

def io_key(keyname):
    return IORegistryEntryCreateCFProperty(IOServiceGetMatchingService(0, IOServiceMatching("IOPlatformExpertDevice")), keyname, None, 0)

def battery_info(keyname):
    return IORegistryEntryCreateCFProperty(IOServiceGetMatchingService(0, IOServiceMatching("AppleSmartBattery")), keyname, None, 0)

def get_hardware_uuid():
    return io_key("IOPlatformUUID")

def get_hardware_serial():
    return io_key("IOPlatformSerialNumber")

def get_battery_charge():
    return battery_info("FullyCharged")

def get_battery_capacity():
    return battery_info("CurrentCapacity")

print get_hardware_uuid()
print get_hardware_serial()
print get_battery_charge()
print get_battery_capacity()
