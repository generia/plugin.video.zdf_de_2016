import sys
import urllib
import urlparse
import time

from de.generia.kodi.plugin.Pagelet import Request
from de.generia.kodi.plugin.Pagelet import Response

from de.generia.kodi.plugin.Mediathek import Mediathek
from de.generia.kodi.plugin.Mediathek import MediathekFactory

class MockRequest(Request):
    def __init__(self, baseUrl, handle, params):
        super(MockRequest, self).__init__(baseUrl, handle, params)
    
class MockResponse(Response):
    def __init__(self, baseUrl, handle):
        super(MockResponse, self).__init__(baseUrl, handle)
    
    def addItem(self, item):
        url = self.encodeUrl(item.action)
        print "addItem: '" + str(item.title) + "' [" + str(item.isFolder) + "/" + str(self.handle) + "]"
        print "- action.url='" + str(url) + "'"
        print "- action.image='" + str(item.image) + "'"
        print "- action.text='" + str(item.text) + "'"

    def close(self):
        print "close.\n"


def servePage(argv):
    baseUrl = argv[0]
    handle = int(argv[1])
    args = urlparse.parse_qs(argv[2][1:])
    pageletId = None
    params = {}
    for key, value in args.iteritems():
        if key == 'pagelet':
            pageletId = value[0];
        else:
            params[key] = value[0]
            
    factory = MediathekFactory()
    pagelet = factory.createPagelet(pageletId, params)
    
    request = MockRequest(baseUrl, handle, params)
    response = MockResponse(baseUrl, handle)
    
    pagelet.service(request, response)
    response.close()

servePage(["http://mockthek", "1234567", "?p1=v1&p2=v2"])
servePage(["http://mockthek", "1234567", "?pagelet=SearchPage&q=NEO+Magazin+Royale&contentTypes=episode"])
