#coding=utf-8

# Published 2016
# Author : sebastien at pittet dot org
# Public domain source code
"""
This API provides access to Cave-Link data. It has some interest for cavers.
Following libraries are required :
    $ pip install python-dateutil
"""

from dateutil.parser import *
import time
import re # to use regular expression in python

# HTTP libraries depends upon Python 2 or 3
from sys import version_info
if version_info.major == 3 :
    import urllib.parse, urllib.request
else:
    import urllib2

########################### Common definitions #########################

_CL_NIVEAU_S2_COVA = "http://www.cavelink.com/cl/da.php?s=115&g=1&w=103&l=10"
_CL_NIVEAU_LANCELEAU = "http://www.cavelink.com/cl/da.php?s=142&g=20&w=100&l=10"
_CL_TEMP_SIPHON = "http://www.cavelink.com/cl/da.php?s=106&g=1&w=0&l=10"


default_CL = _CL_NIVEAU_LANCELEAU
#########################################################################

class CaveLinkData:
    """
    Parse the webpage used to export the data and
    provides values back.
    """

    def __init__(self, URL = default_CL):
        webpage = urllib2.Request(URL)
        
        try:
            handle = urllib2.urlopen(webpage)
        except IOError:
            print ('ERROR : unable to get the webpage :-/')

        # Get the HTML page
        htmlContent = handle.read()

        self.rawData = htmlContent.replace(",", "") # remove the separator (comma)      
        self.data = htmlContent.split("<br>")

        for line in self.data: 
            
            match = re.search('(?<=Stn=)\d{3}', line)
            if match:
                self.station = match.group(0)
            
            match = re.search('(?<=Grp=)\d{1,3}', line)
            if match:
                self.group = match.group(0)
            
            match = re.search('(?<=Nr=)\d{1,3}', line)
            if match:
                self.number = match.group(0)
            
            match = re.search('(?<=Einheit : )\D{1}', line)
            if match:
                self.unit = match.group(0).upper() # uppercase (C | M | ?)

    @property

    def station(self):
        return self.station
        
    def group(self):
        return self.group
        
    def number(self):
        return self.number
        
    def unit(self):
        return self.unit
        
    def GetData(self):
        DictValues = {}

        for line in self.data:
            epochDatetime = findDate(line[0:16])
            if epochDatetime:
                # a date was found on this line
                DictValues [epochDatetime] = float(line[17:]) # Create a dict with values
        return DictValues

####################### SOME USEFUL TOOLS ###############################
def toEpoch(value):
    return int(time.mktime(time.strptime(value,"%Y-%m-%d %H:%M:%S")))

def findDate(inputValue):
    try:
        DateTimeString = str(parse(inputValue, ignoretz=True))
    except:
        #if not found, epoch = 0
        DateTimeString = "1970-01-01 00:00:00"
     
    # Convert to epoch date time and return the value   
    return toEpoch(DateTimeString)
######################################################################

    
# auto-test when executed directly

if __name__ == "__main__":

    from sys import exit, stdout, stderr

    # If launched interactively, display OK message
    if stdout.isatty():
        print("lcavelink.py : OK")

    exit(0)
