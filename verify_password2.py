#!/usr/bin/python
#ref: https://macadmins.slack.com/files/elios/F0JA6JD6V/Untitled.py

from OpenDirectory import *
import getpass

username = getpass.getuser().decode(u"utf-8")
password = getpass.getpass((u"password for %s: " % username).encode(u"utf-8"))

class ODException(Exception):
    '''Base exception for OpenDirectory'''

class ODSessionException(Exception):
    '''ODSessionException'''

class ODNodeException(ODException):
    '''ODNode exception'''

class ODQueryException(ODException):
    '''ODQueryException'''

class ODRecordException(ODException):
    '''ODRecordException'''

class ODPasswordException(ODException):
    '''ODPasswordException'''

def ODverifyPassword(username, password, dsnode='/Search'):
    '''Uses the OpenDirectory framework to verify username and password.

        Input: username, password, and optional DS node name.
        Output: True if username and password are verified
        Exceptions: all sorts!
        '''
    session = ODSession.defaultSession()
    if not session:
        raise ODSessionException('Could not get default Open Directory session')

    node, error = ODNode.nodeWithSession_name_error_(session, dsnode, None)
    if error:
        raise ODNodeException(error)

    query, error = ODQuery.queryWithNode_forRecordTypes_attribute_matchType_queryValues_returnAttributes_maximumResults_error_(
            node,
            kODRecordTypeUsers,
            kODAttributeTypeRecordName,
            kODMatchEqualTo,
            username,
            kODAttributeTypeStandardOnly,
            1,
            None )

    if error:
        raise ODQueryException(error)

    results, error = query.resultsAllowingPartial_error_(False, None)
    if error:
        raise ODQueryException(error)

    if results:
        record = results[0]
        passwordVerified, error = record.verifyPassword_error_(password, None)
        if error and error.code() != 5000: # 5000 means invalid user or password
            raise ODPasswordException(error)

        return passwordVerified
    else:
        # no matching username in DS, so return False
        return False

print ODverifyPassword(username, password)
