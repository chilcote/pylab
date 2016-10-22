#!/usr/bin/python

from SystemConfiguration import (SCDynamicStoreCopyConsoleUser,
                                 SCDynamicStoreCreate,
                                 SCDynamicStoreCopyValue
                                )

# Using SCDynamicStoreCopyConsoleUser
console_user = SCDynamicStoreCopyConsoleUser(None, None, None)[0]
console_uid = SCDynamicStoreCopyConsoleUser(None, None, None)[1]
console_gid = SCDynamicStoreCopyConsoleUser(None, None, None)[2]
print console_user
print console_uid
print console_gid


# Using SCDynamicStoreCreate, SCDynamicStoreCopyValue
net_config = SCDynamicStoreCreate(None, "net", None, None)
console_user = SCDynamicStoreCopyValue(net_config, "State:/Users/ConsoleUser")
#print console_user
print console_user['Name']
print console_user['UID']
print console_user['GID']

