from de.generia.kodi.plugin.web import JsonResource

from de.generia.kodi.plugin.Constants import Constants
from de.generia.kodi.plugin.zdf.api.ApiResource import ApiResource


class VideoContentResource(ApiResource):

    def __init__(self, url, apiToken):
        super(VideoContentResource, self).__init__(url, apiToken, 'application/vnd.de.zdf.v1.0+json')

    def parse(self):
        super(VideoContentResource, self).parse()
        
        self.title = JsonResource.getValue(self.content, 'title') 
        self.text = JsonResource.getValue(self.content, 'teasertext')
        self.tvService = JsonResource.getValue(self.content, 'tvService')
        
        if 'http://zdf.de/rels/category' in self.content:
            category = self.content['http://zdf.de/rels/category']
            self.genre = JsonResource.getValue(category, 'title')
            
        if 'teaserImageRef' in self.content:
            teaserImageRef = self.content['teaserImageRef']
            layouts = teaserImageRef['layouts']
            if 'original' in layouts:
                self.image = layouts['original']
            else:
                for value in layouts.values():
                    self.image = value
                    break
            
        self.url = None
        if 'mainVideoContent' in self.content:
            mainVideoContent = self.content['mainVideoContent']
            target = mainVideoContent['http://zdf.de/rels/target']
            self.streamInfoUrl = Constants.apiBaseUrl + target['http://zdf.de/rels/streams/ptmd']
