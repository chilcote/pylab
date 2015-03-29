#!/usr/bin/env python

##############################################################################
# Copyright 2015 Joseph Chilcote
# 
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not
#  use this file except in compliance with the License. You may obtain a copy
#  of the License at
# 
#       http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
##############################################################################

__author__  = 'Joseph Chilcote (chilcote@gmail.com)'
__version__ = '0.0.1'

from Foundation import NSUserNotification
from Foundation import NSUserNotificationCenter
from Foundation import NSUserNotificationDefaultSoundName
from Foundation import NSDate
import sys
import argparse

class Notify(object):
    '''Class to send custom notification'''
    def __init__(self):
        self.notification = NSUserNotification.alloc().init()

    def alert(self, title, subtitle, message, delay=0, sound=False, userInfo={}):
        self.notification.setTitle_(title)
        self.notification.setSubtitle_(subtitle)
        self.notification.setInformativeText_(message)
        self.notification.setDeliveryDate_(NSDate.dateWithTimeInterval_sinceDate_(delay, NSDate.date()))
        self.notification.setUserInfo_(userInfo)
        if sound:
            self.notification.setSoundName_("NSUserNotificationDefaultSoundName")        
        NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(self.notification)

def main():
    '''Main method'''
    parser = argparse.ArgumentParser(description='Send a custom notification on OS X.')
    parser.add_argument('--title', help='title of notification')
    parser.add_argument('--subtitle', help='subtitle of notification')
    parser.add_argument('--message', help='message of notification')
    parser.add_argument('--delay', type=float, help='delay for n seconds')
    parser.add_argument('--sound', help='include audible alert', action='store_true')
    args = parser.parse_args()

    title = args.title if args.title else None
    subtitle = args.subtitle if args.title else None
    message = args.message if args.title else None
    delay = args.delay if args.delay else 0
    sound = True if args.sound else False

    notify = Notify()
    notify.alert(title, subtitle, message, delay, sound=sound)

if __name__ == '__main__':
    main()