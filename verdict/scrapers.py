import random
import urllib2
from bs4 import BeautifulSoup

class Browser(object):
    
    def __init__(self, system, user_agent):
        self.system = system
        self.user_agent = user_agent


# from http://techblog.willshouse.com/2012/01/03/most-common-user-agents/
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
]

def eight_hundred_notes(q):
    url = "http://800notes.com/Phone.aspx/1-%s-%s-%s" % (q[:3], q[3:6], q[6:])
    request = urllib2.Request(url, headers={'User-Agent': 
                                            random.choice(browsers).user_agent})
    page = urllib2.urlopen(request).read()
    soup = BeautifulSoup(page)
    if soup.find(id='treeThread').contents:
        return True
    else:
        return False

scrapers = [eight_hundred_notes,]

def run(q):
    results = []
    for func in scrapers:
        results.append(func(q))
    return True in results
