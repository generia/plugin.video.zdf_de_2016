import urllib
import urllib2
import ssl

class Resource(object):

    def __init__(self, url, accept):
        self.url = url
        self.accept = accept
        
    def parse(self):
        self.content = self._getUrl();
    
    def _getUrl(self):
        print "_getUrl: " + self.url
        request = self._createRequest()
        # check, if ssl has certificate verification by default and turn it off
        if '_create_unverified_context' in dir(ssl):
            response = urllib2.urlopen(request, context=ssl._create_unverified_context())
        else:
            response = urllib2.urlopen(request)
            
        content = response.read()
        response.close()
        return content
                
    def _createRequest(self):
        request = urllib2.Request(self.url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
        request.add_header('Accept', self.accept)
        return request
