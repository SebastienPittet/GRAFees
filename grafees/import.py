#coding=utf-8

from HTMLParser import HTMLParser
from dateutil.parser import *

# HTTP libraries depends upon Python 2 or 3
from sys import version_info
if version_info.major == 3 :
    import urllib.parse, urllib.request
else:
    from urllib import urlencode
    import urllib2

the_url = 'http://www.cavelink.com/cl/da.php?s=106&g=1&w=101&l=20'
webpage = urllib2.Request(the_url)

def toEpoch(value):
    return int(time.mktime(time.strptime(value,"%Y-%m-%d_%H:%M:%S")))

def findDate(inputValue):
    EpochDateTime = inputValue[0:16]
    return EpochDateTime

class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        print data[:16], data[18:]
        dateTimeFound = parse(data, ignoretz=True)
    
try:
     handle = urllib2.urlopen(webpage)
except IOError:
     print 'Cela a foiré !'
else:
    # Print the HTML page
    htmlContent = handle.read()
    
    # Translate
    htmlContent = htmlContent.replace("Einheit", "Unit")
    htmlContent = htmlContent.replace("Stn=", "Station=")
    htmlContent = htmlContent.replace("Grp=", "Group=")
    htmlContent = htmlContent.replace("<br>", "\r\n")
    
    # Finding spaces and replace by separator
    #htmlContent = htmlContent.replace(" ", "    ") # separator = 4 spaces?
    htmlContent = htmlContent.replace(",", "")
    htmlContent = htmlContent.replace(";:;", ":")
    htmlContent = htmlContent.replace("Unit : m", "Unit=m")
    
    #Separate Header from Data
    contentHeader = htmlContent[:htmlContent.index("=m")+2]
    contentData = htmlContent[htmlContent.index("=m")+2:]   
    print contentHeader
    print contentData

    
    # Besoin de python-dateutil ??
    # Besoin de HTMLParser ???
    