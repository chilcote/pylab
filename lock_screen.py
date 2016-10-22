#!/usr/bin/python
## ref: https://gist.github.com/pudquick/350ba6411df3be77d32a

from ctypes import CDLL

loginPF = CDLL('/System/Library/PrivateFrameworks/login.framework/Versions/Current/login')
result = loginPF.SACLockScreenImmediate()
