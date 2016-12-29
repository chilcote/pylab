#!/usr/bin/python

import urllib2
import subprocess
import os
import json

site = 'chilcote'
repo = 'outset'

url = 'https://api.github.com/repos/%s/%s/releases/latest' % (site, repo)

response = urllib2.urlopen(url)
d = json.loads(response.read())
print d['name']
