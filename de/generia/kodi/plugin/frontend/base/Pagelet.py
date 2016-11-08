import urllib

class Log(object):
    def __init__(self):
        pass
    
    def debug(self, message):
        pass
    
    def info(self, message):
        pass

    def warn(self, message):
        pass
    
    def error(self, message):
        pass
    
    
class Context(object):
    def __init__(self, log):
        self.log = log
    
    def getLog(self):
        return self.log
    
class Request(object):
    def __init__(self, context, baseUrl, handle, params):
        self.context = context
        self.baseUrl = baseUrl
        self.handle = handle
        self.params = params
    
class Response(object):
    def __init__(self, context, baseUrl, handle):
        self.context = context
        self.baseUrl = baseUrl
        self.handle = handle

    def addItem(self):
        pass
    
    def addFolder(self, title, action):
        item = Item(title, action=action, image='DefaultFolder.png', isFolder=True)
        self.addItem(item);
        
    def sendError(self, message, action):
        pass
        
    def sendInfo(self, message, action):
        pass
    
    def encodeUrl(self, action):
        if action is None:
            return None
        query = ''
        url = ''
        if action.params is not None and len(action.params) >  0:
            query = urllib.urlencode(action.params)
        if action.pagelet is not None:
            if query != '':
                query = '&' + query
            url = self.baseUrl + '?pagelet=' + action.pagelet + query
        else:
            url = action.url
        return url 
    
class Item(object):
    def __init__(self, title, action, image=None, text=None, genre=None, date=None, isFolder=False, isPlayable=False):
        self.title = title
        self.action = action
        self.image = image
        self.text = text
        self.genre = genre
        self.date = date
        self.isFolder = isFolder
        self.isPlayable = isPlayable

class Action(object):
    def __init__(self, pagelet=None, params={}, url=None):
        self.pagelet = pagelet
        self.params = params
        self.url = url


class Pagelet(object):

    def __init__(self):
        pass
         
    def init(self, context):
        self.context = context

    def service(self, request, response):
        pass
        

class PageletFactory(object):

    def __init__(self):
        pass
                 
    def createPagelet(self, pageletId, params):
        pass
        
