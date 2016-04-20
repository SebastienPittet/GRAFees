#!/usr/bin/env python
#coding=utf-8

# HTTP libraries depends upon Python 2 or 3
from sys import version_info
if version_info.major == 3 :
    import urllib.parse, urllib.request
else:
    from urllib import urlencode
    import urllib2

the_url = 'http://www.csavelink.com/cl/da.php?s=106&g=1&w=101&l=20'
req = urllib2.Request(the_url)

try:
     handle = urllib2.urlopen(req)
except IOError:
	Error = True
else:
	Error = False

if Error:
    print "Unable to get HTML content. Ca a foiré :-("
else:
	 # Print the HTML page
	 print handle.read()
