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

# HTTP libraries depends upon Python 2 or 3
from sys import version_info
if version_info.major == 3 :
    import urllib.parse, urllib.request
else:
    from urllib import urlencode
    import urllib2

########################### Common definitions #########################

_CL_NIVEAU_S2_COVA = "http://www.cavelink.com/cl/da.php?s=115&g=1&w=103&l=10"

#########################################################################

default_CL = _CL_NIVEAU_S2_COVA

class GetCaveLinkData:
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
    
        # Translate
        htmlContent = htmlContent.replace("Einheit", "Unit")
        htmlContent = htmlContent.replace("Stn=", "Station=")
        htmlContent = htmlContent.replace("Grp=", "Group=")
        htmlContent = htmlContent.replace("<br>", "\r\n")
        htmlContent = htmlContent.replace(",", "")
        #htmlContent = htmlContent.replace(";:;", ":")
        htmlContent = htmlContent.replace("Unit : m", "Unit=m")

        #Separate Header from Data
        self.contentHeader = htmlContent[:htmlContent.index("=m")+2]
        self.contentData = htmlContent[htmlContent.index("=m")+5:]   

    @property
    def GetHeader(self):
        
        return self.contentHeader
        
    def GetData(self):
        lines = self.contentData.split("\r\n")
        DictValues = {}

        for line in lines:
            epochDatetime = findDate(line[0:16])
            if epochDatetime:
                DictValues [epochDatetime] = line[17:] # Creation dictionnaire de valeurs
            else:
                #skip the line
                print ("Error, no date found by parser :-/")
        return DictValues

####################### SOME USEFUL TOOLS ###############################
def toEpoch(value):
    return int(time.mktime(time.strptime(value,"%Y-%m-%d %H:%M:%S")))

def findDate(inputValue):
    try:
        DateTimeString = str(parse(inputValue, ignoretz=True))
    except:
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
