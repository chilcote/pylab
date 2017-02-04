#!/usr/bin/python
#ref https://gist.github.com/pudquick/8107bb7b6e8d63eaddec7042c081e656

from ctypes import CDLL, c_uint, byref, create_string_buffer
libc = CDLL('/usr/lib/libc.dylib')

def sysctl(name):
    size = c_uint(0)
    libc.sysctlbyname(name, None, byref(size), None, 0)
    buf = create_string_buffer(size.value)
    libc.sysctlbyname(name, buf, byref(size), None, 0)
    return buf.value

def is_mac_vm():
  return 'VMM' in sysctl('machdep.cpu.features').split(' ')

print is_mac_vm()
print sysctl('machdep.cpu.features')
print sysctl('kern.boottime').split()
print sysctl('hw.model')
print sysctl('kern.osversion')
print sysctl('kern.hostname')
