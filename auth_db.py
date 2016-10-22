#!/usr/bin/python
#ref: https://gist.github.com/tburgin/77ebd114d59d368b0b4321ca7cf77767

import objc
from ctypes import CDLL, c_void_p, byref
from ctypes.util import find_library

Security = CDLL(find_library("Security.framework"))
AuthorizationRightGet = Security.AuthorizationRightGet
AuthorizationRightSet = Security.AuthorizationRightSet
AuthorizationCreate = Security.AuthorizationCreate

def authorization_right_get(right):
    db_buffer = c_void_p()
    AuthorizationRightGet(right, byref(db_buffer))
    if db_buffer:
        return objc.objc_object(c_void_p=db_buffer).mutableCopy()
    return None

def authorization_right_set(right, value):
    auth_ref = c_void_p()
    AuthorizationCreate(None, None, 0, byref(auth_ref))
    return AuthorizationRightSet(auth_ref, right, value.__c_void_p__(), None, None, None)

db = authorization_right_get("system.preferences")
db["group"] = "everyone"

print db
#authorization_right_set("system.preferences", db)
