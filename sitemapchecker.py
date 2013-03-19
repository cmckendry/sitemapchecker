#!/usr/bin/python
import urllib2, gzip, sys
from xml.dom.minidom import parse, parseString
from time import sleep
from StringIO import StringIO

if len(sys.argv) < 2:
  print "Usage: " + sys.argv[0] + " http://<site>"
  sys.exit(1)

SITE=sys.argv[1]

def getXmlFromUrl(url,zipped=False):
  req = urllib2.Request(url)
  res = urllib2.urlopen(req)
  if zipped:
    buf = StringIO(res.read())
    f = gzip.GzipFile(fileobj=buf)
    data = f.read()
  else:
    data = res.read()
  return data

def checkUrls(dom):
  urls = dom.getElementsByTagName('loc')
  for url in urls:
    realurl = url.childNodes[0].nodeValue
    #print realurl
    req = urllib2.Request(realurl)
    req.get_method = lambda : 'HEAD'
    try:
      res = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
      print str(realurl) + " -- " + str(e)
    #sleep(1)

index = parseString(getXmlFromUrl(SITE + '/sitemap_index.xml'))
maps = index.getElementsByTagName('loc')

for mapfile in maps:
  mapfile = mapfile.childNodes[0].nodeValue
  print mapfile
  doc = parseString(getXmlFromUrl(mapfile,True))
  checkUrls(doc)
