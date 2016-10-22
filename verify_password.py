#!/usr/bin/python
#ref: https://gist.github.com/pudquick/3403867841b047bc0332

import getpass
username = getpass.getuser().decode(u"utf-8")
password = getpass.getpass((u"password for %s: " % username).encode(u"utf-8"))

from OpenDirectory import *

session = ODSession.defaultSession()
node, error = ODNode.nodeWithSession_type_error_(session, kODNodeTypeAuthentication, None)
query, error = ODQuery.queryWithNode_forRecordTypes_attribute_matchType_queryValues_returnAttributes_maximumResults_error_( \
    node, kODRecordTypeUsers,
    kODAttributeTypeRecordName, kODMatchEqualTo, username,
    kODAttributeTypeNativeOnly, 0, None)
result, error = query.resultsAllowingPartial_error_(False, None)
record = result[0]
result, error = record.verifyPassword_error_(password, None)
print result
