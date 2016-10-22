#!/usr/bin/python
#ref https://macadmins.slack.com/files/frogor/F0JCE3YUS/-.py

from ctypes import CDLL, c_uint, byref, create_string_buffer
libc = CDLL('/usr/lib/libc.dylib')

def sysctl(name, isString=True):
    size = c_uint(0)
    # Find out how big our buffer will be
    libc.sysctlbyname(name, None, byref(size), None, 0)
    # Make the buffer
    buf = create_string_buffer(size.value)
    # Re-run, but provide the buffer
    libc.sysctlbyname(name, buf, byref(size), None, 0)
    if isString:
        return buf.value
    else:
        return buf.raw

print sysctl('kern.uuid')
print sysctl('kern.hostname')
print sysctl('hw.model')
print sysctl('kern.osversion')
print sysctl('kern.netboot')
