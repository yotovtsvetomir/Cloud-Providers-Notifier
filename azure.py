#!/usr/bin/env python
import json
from pymongo import MongoClient
import urllib2
from bs4 import BeautifulSoup
import string
import re
from shortid import ShortId
from dateutil.parser import parse
from datetime import datetime
import string



#Connect  DB SA
client = MongoClient()
db = client.azure
posts = db.posts


response = urllib2.urlopen('https://azure.microsoft.com/en-us/status/history/')
res = response.read()
soup = BeautifulSoup(res, "html.parser")
bod = soup.body


#### Clean the html and JS,Jquery ####
def cleanWebCode(paragraph):
    #### Kill all script and style elements ####

    #for script in paragraph(["script", "style"]):
    #    script.extract()    # rip it out
    #### Get text (BeautifulSoup) ####
    text = paragraph.get_text()
    #### Break into lines and remove leading and trailing space on each ####
    lines = (line.strip() for line in text.splitlines())
    #### Break multi-headlines into a line each ####
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    #### Drop blank lines ####
    text = '\n'.join(chunk for chunk in chunks if chunk)
    #### Remove non ascii characters and encode everything to UTF 8 ####
    #printable = set(string.printable)
    #cleantext = filter(lambda x: x in printable, text)
    #return cleantext
    return text


cleantext = cleanWebCode(bod)
start = cleantext.find('Date:')
end = cleantext.find('Go Social')
cloudinfo2 = cleantext[start:end]
start2 = cloudinfo2.find('2017')
cloudinfo = cloudinfo2[start2+4:end]

sstart = cloudinfo.find('/')


ss = re.findall("\d{1}/",cloudinfo)


#Loop through all posts
for i in range(len(ss)):
        #check for last post
        spl = [m.start() for m in re.finditer(r"\d{1}/",cloudinfo)]
        if len(spl) < 2:
            break
        else:
            sstop = [m.start() for m in re.finditer(r"\d{1}/",cloudinfo)][1]
            #Divide a single blockpost
            blockpost = cloudinfo[sstart-1:sstop]

            #Find the date and time
            occuretime = re.findall("\d{2}:\d{2}", blockpost)
            occuredate = blockpost[0:4]
            #Gather summary
            summary = blockpost.strip()[4:end]

            if len(occuretime) > 1:
                s = occuretime[0]
                s2 = s[0:5]
                fstr = "2017" + s2 + " " + occuredate
                f = fstr.strip()
                cleandate = datetime.strptime(f, '%Y%H:%M %m/%d')

            #Generate ID
            sid = ShortId()
            s = (sid.generate())
            #Orginize Data
            az = "Microsoft Azure Status post"
            data = {
            '_id' : s,
            'published' : cleandate,
            'title' : az,
            'summary': summary
            }

            post_id = posts.insert_one(data).inserted_id
            #Remove from the whole text
            cloudinfo = cloudinfo.replace(blockpost, '')
            print "Update and Populate Azure Cloud Health Status"
