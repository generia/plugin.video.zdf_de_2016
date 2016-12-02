from de.generia.kodi.plugin.backend.zdf.LiveTvResource import LiveTvResource
from de.generia.kodi.plugin.backend.zdf.Teaser import Teaser

from de.generia.kodi.plugin.frontend.base.Pagelet import Action        

from de.generia.kodi.plugin.frontend.zdf.Constants import Constants
from de.generia.kodi.plugin.frontend.zdf.ItemPage import ItemPage


class LiveTvPage(ItemPage):

    def service(self, request, response):
        apiToken = request.getParam('apiToken')

        liveTvUrl = Constants.baseUrl + '/live-tv'
        liveTvResource = LiveTvResource(liveTvUrl)
        self._parse(liveTvResource)
        for teaser in liveTvResource.teasers:
            item = self._createItem(teaser, apiToken)
            if item is not None:
                response.addItem(item)
