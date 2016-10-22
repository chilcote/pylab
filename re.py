#!/usr/bin/env python
# example using re.compile

import re

phoneNumRegex = re.compile(r'(\d\d\d)-(\d\d\d-\d\d\d\d)')
mo = phoneNumRegex.search('My number is 206-555-1212')
print mo.groups()
