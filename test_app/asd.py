import httplib
from urlparse import urlparse

def checkUrl(url):
    p = urlparse(url)
    conn = httplib.HTTPConnection(p.netloc)
    conn.request('HEAD', p.path)
    resp = conn.getresponse()
    return resp.status < 400

if __name__ == '__main__':
    print checkUrl('http://www.stackoverflow.com') # True
    print checkUrl('http://ajency.in/') # False
