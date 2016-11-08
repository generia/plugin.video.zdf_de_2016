import urllib

import xbmc
import xbmcgui

from de.generia.kodi.plugin.backend.zdf.api.VideoContentResource import VideoContentResource
from de.generia.kodi.plugin.backend.zdf.api.StreamInfoResource import StreamInfoResource

from de.generia.kodi.plugin.frontend.base.Pagelet import Pagelet        

from de.generia.kodi.plugin.frontend.zdf.Constants import Constants


class PlayVideo(Pagelet):
 
    def service(self, request, response):
        apiToken = request.params['apiToken']
        contentName = request.params['contentName']

        item = None
        if contentName is not None:
            try:
                dialog = xbmcgui.DialogProgressBG()
                dialog.create('Play Video', 'Downloading video information ...')
                videoContentUrl = Constants.apiBaseUrl + '/content/documents/' + contentName + '.json?profile=player'
                self.context.log.debug("PlayVideo - downloading video-content-url '{0}' ...", videoContentUrl)
                videoContent = VideoContentResource(videoContentUrl, Constants.apiBaseUrl, apiToken)
                videoContent.parse()
                
                if videoContent.streamInfoUrl is None:
                    self.context.log.warn("PlayVideo - can't find stream-info-url in video-content '{0}' in content '{1}'", contentName, videoContent.content)
                    response.sendError("con't find stream-info-url in video-content '" + contentName +"'", Action('SearchPage'))
                    return
            
                dialog.update(percent=50, message='Downloading stream information ...')
                self.context.log.debug("PlayVideo - downloading stream-info-url '{0}' ...", videoContent.streamInfoUrl)
                streamInfo = StreamInfoResource(videoContent.streamInfoUrl, apiToken)
                streamInfo.parse()
                
                url = streamInfo.streamUrl
                if url is None:
                    self.context.log.warn("PlayVideo - can't find stream-url in stream-info-url '{0}' in content '{1}'", videoContent.streamInfoUrl, streamInfo.content)
                    response.sendError("con't find stream-info-url in video-content '" + contentName +"'", Action('SearchPage'))
                    return

                image = videoContent.image
                item = xbmcgui.ListItem(videoContent.title)
                item.setArt({'poster': image, 'banner': image, 'thumb': image, 'icon': image, 'fanart': image})
                
                dialog.update(percent=90, message='Starting video player ...')
                xbmc.Player().play(url, item)
    
            finally:
                dialog.close();
            
