import random
import urllib2
from bs4 import BeautifulSoup


# setup classes/functions

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

if os.environ.get('PROXIMO_URL', '') != '':
    proxy  = urllib2.ProxyHandler({'http': os.environ.get('PROXIMO_URL', '')})
    auth   = urllib2.HTTPBasicAuthHandler()
    opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

def url_to_soup(url):
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
              'Accept-Encoding': 'none',
              'Accept-Language': 'en-US,en;q=0.8',
              'Connection': 'keep-alive'}
    header['User-Agent'] = random.choice(browsers).user_agent 
    request = urllib2.Request(url, headers=header)
    page = urllib2.urlopen(request).read()
    return BeautifulSoup(page)


# scrapers

def eight_hundred_notes(q):
    url = "http://800notes.com/Phone.aspx/1-%s-%s-%s" % (q[:3], q[3:6], q[6:])
    soup = url_to_soup(url)
    result = dict(name='800notes.com', url=url)
    # see if the element with id "treeTread" has any contents
    if soup.find(id='treeThread').contents:
        result['verdict'] = True
    else:
        result['verdict'] = False
    return result

def who_called_us(q):
    url = "http://whocalled.us/lookup/%s" % q
    soup = url_to_soup(url)
    result = dict(name='whocalled.us', url=url)
    # look for an element anywhere on the page with id "calls"
    if soup.find(id='calls'):
        result['verdict'] = True
    else:
        result['verdict'] = False
    return result

def why_call_me(q):
    url = "http://www.whycall.me/%s-%s-%s.html" % (q[:3], q[3:6], q[6:])
    soup = url_to_soup(url)
    result = dict(name='whycall.me', url=url)
    # look for an element anywhere on the page with id "complaint"
    if soup.find(id='complaint'):
        result['verdict'] = True
    else:
        result['verdict'] = False
    return result


# aggregation

# scrapers = [why_call_me,]
scrapers = [eight_hundred_notes, who_called_us, why_call_me]

def run(q):
    results = []
    for scraper in scrapers:
        results.append(scraper(q))
    return results
