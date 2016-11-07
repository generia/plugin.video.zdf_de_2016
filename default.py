import sys
import urlparse
import xbmc
import xbmcgui
import xbmcplugin


from de.generia.kodi.plugin.Pagelet import Log
from de.generia.kodi.plugin.Pagelet import Context
from de.generia.kodi.plugin.Pagelet import Request
from de.generia.kodi.plugin.Pagelet import Response
from de.generia.kodi.plugin.Pagelet import Action

from de.generia.kodi.plugin.Mediathek import MediathekFactory


class XbmcLog(Log):
    def __init__(self, prefix):
        super(XbmcLog, self).__init__()
        self.prefix = prefix
        
    def _log(self, level, message, *args):
        parts = []
        for arg in args:
            part = arg
            if isinstance(arg, basestring):
                part = arg.encode('ascii', 'ignore')
            parts.append(part)
        msg = self.prefix + message.format(*parts)
        xbmc.log(msg, level=level)

    def debug(self, message, *args):
        self._log(xbmc.LOGNOTICE, message, *args)
    
    def info(self, message, *args):
        self._log(xbmc.LOGINFO, message, *args)

    def warn(self, message, *args):
        self._log(xbmc.LOGWARNING, message, *args)
    
    def error(self, message, *args):
        self._log(xbmc.LOGERROR, message, *args)

class XbmcRequest(Request):
    def __init__(self, context, baseUrl, handle, params):
        super(XbmcRequest, self).__init__(context, baseUrl, handle, params)
    
class XbmcResponse(Response):
    def __init__(self, context, baseUrl, handle):
        super(XbmcResponse, self).__init__(context, baseUrl, handle)
    
    def addItem(self, item):
        if item is None:
            return
        title = item.title
        if item.genre is not None:
            title = '[' + item.genre + '] ' + title
        #if item.action is not None and 'contentName' in item.action.params:
        #    title += ' [' + item.action.params['contentName'] +']'
        li = xbmcgui.ListItem(title, item.text)
        li.setArt({'poster': item.image, 'banner': item.image, 'thumb': item.image, 'icon': item.image, 'fanart': item.image})
        li.setInfo(type="Video", infoLabels={"Title": item.title})
        li.setProperty('IsPlayable', 'false')
        url = self.encodeUrl(item.action)
        #li.addContextMenuItems(['Item-Menu', 'RunPlugin(plugin://'+ self.handle +'/'])
        self.context.log.info('{0} -> {1}',     item.isFolder, url)
        xbmcplugin.addDirectoryItem(handle=self.handle, url=url, listitem=li, isFolder=item.isFolder)

    def close(self):
        xbmcplugin.endOfDirectory(self.handle)
        
    def sendError(self, message, action=Action()):
        self._sendMessage(xbmcgui.NOTIFICATION_ERROR, "Error", message, action)
        
    def sendInfo(self, message, action=Action()):
        self._sendMessage(xbmcgui.NOTIFICATION_INFO, "Info", message, action)
        
    def _sendMessage(self, level, caption, message, action=Action()):
        dialog = xbmcgui.Dialog()
        dialog.notification(caption, message, level)
        url = self.encodeUrl(action)
        self.context.log.info("Response - send{0} '{1}', redirecting to '{2}'", caption, message, url)
        listItem = xbmcgui.ListItem()
        xbmcplugin.setResolvedUrl(self.handle, False, listItem)

baseUrl = sys.argv[0]
handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
pageletId = None
params = {}
for key, value in args.iteritems():
    if key == 'pagelet':
        pageletId = value[0];
    else:
        params[key] = value[0]
        
log = XbmcLog('ZDF Mediathek 2016 [' + str(handle) + ']: ')
log.debug('Plugin - baseUrl={0}, query={1}', baseUrl, sys.argv[2][0:])
context = Context(log)
factory = MediathekFactory()
pagelet = factory.createPagelet(pageletId, params)
pagelet.init(context)
request = XbmcRequest(context, baseUrl, handle, params)
response = XbmcResponse(context, baseUrl, handle)

pagelet.service(request, response)
response.close()
