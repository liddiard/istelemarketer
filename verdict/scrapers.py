import random
import urllib2
from bs4 import BeautifulSoup

import logging


# setup classes/functions

logger = logging.getLogger(__name__)

class Browser(object):
    
    def __init__(self, system, user_agent):
        self.system = system
        self.user_agent = user_agent


browsers = [
    Browser(system="Chrome 31.0 Win7 64-bit", 
            user_agent=("Mozilla/5.0 (Windows NT 6.1; WOW64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/31.0.1650.57 Safari/537.36")),
    Browser(system="Safari 7.0 MacOSX",
            user_agent=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9) "
                        "AppleWebKit/537.71 (KHTML, like Gecko) "
                        "Version/7.0 Safari/537.71")),
    Browser(system="Firefox 25.0 Win7 64-bit",
            user_agent=("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) "
                        "Gecko/20100101 Firefox/25.0")),
    Browser(system="Chrome 31.0 MacOSX",
            user_agent=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/31.0.1650.57 Safari/537.36")),
] # from http://techblog.willshouse.com/2012/01/03/most-common-user-agents/

googlebot = Browser(system="googlebot", 
                    user_agent=("Mozilla/5.0 (compatible; Googlebot/2.1; "
                                "+http://www.google.com/bot.html)"))

def url_to_soup(url):
    request = urllib2.Request(url, headers={'User-Agent': 
                                            random.choice(browsers).user_agent})
    page = urllib2.urlopen(request).read()
    return BeautifulSoup(page)


# scrapers

def eight_hundred_notes(q):
    '''always fails silently: will most likely return False if failing'''
    url = "http://800notes.com/Phone.aspx/1-%s-%s-%s" % (q[:3], q[3:6], q[6:])
    soup = url_to_soup(url)
    if soup.find(id='treeThread').contents:
        return True
    else:
        return False

def caller_complaints(q):
    url = "http://www.callercomplaints.com/SearchResult.aspx?Phone=%s-%s-%s" %\
                                                         (q[:3], q[3:6], q[6:])
    request = urllib2.Request(url, headers={'User-Agent': googlebot.user_agent})
    page = urllib2.urlopen(request).read()
    soup = BeautifulSoup(page)
    print soup.prettify()
    try:
        return int(soup.div(class_='rep_val')[5].string) > 0
    except TypeError:
        logger.error("scraper 'caller_complaints' failed to convert <div> "
                     "value to int.")
        return False # return something workable in the meantime


# aggregation

scrapers = [caller_complaints,]

def run(q):
    results = []
    for scraper in scrapers:
        results.append(scraper(q))
    return True in results
