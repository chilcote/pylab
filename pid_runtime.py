#!/usr/bin/python
#ref https://gist.github.com/pudquick/593fda0fd9e0191c748ac00cd4359702

from ctypes import CDLL, util, c_int, c_uint, byref, sizeof
import time

# We just need a large enough buffer for the result
# On 64-bit systems, this struct is 648 bytes, so 1024 bytes is enough
BUFFER_SIZE = 1024

CTL_KERN      =  1
KERN_PROC     = 14
KERN_PROC_PID =  1

libc = CDLL(util.find_library("c"))

def starttime_for_pid(pid):
    mib  = (c_int*4)(CTL_KERN, KERN_PROC, KERN_PROC_PID, pid)
    # allocate the buffer as an array of unsigned integers
    # We're fortunate in that kp_proc.p_starttime.tv_sec is
    # the very first value in this data structure
    proc_buffer = (c_uint*(BUFFER_SIZE/sizeof(c_uint)))()
    size = c_int(BUFFER_SIZE)
    result = libc.sysctl(mib, 4, byref(proc_buffer), byref(size), 0, 0)
    return proc_buffer[0]

def seconds_running(pid):
    start_time = starttime_for_pid(pid)
    if start_time == 0:
        # Process id is not valid
        return -1
    return time.time() - start_time

print seconds_running(504)
