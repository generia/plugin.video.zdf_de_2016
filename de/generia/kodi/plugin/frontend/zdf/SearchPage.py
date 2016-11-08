import urllib

import xbmc
import xbmcplugin

from de.generia.kodi.plugin.backend.zdf.SearchResource import SearchResource       

from de.generia.kodi.plugin.frontend.base.Pagelet import Item        
from de.generia.kodi.plugin.frontend.base.Pagelet import Action        
from de.generia.kodi.plugin.frontend.base.Pagelet import Pagelet        

from de.generia.kodi.plugin.frontend.zdf.Constants import Constants
from de.generia.kodi.plugin.frontend.zdf.ItemPage import ItemPage


class SearchPage(ItemPage):

    def service(self, request, response):
        apiToken = request.params['apiToken']
        query = dict(request.params)
        del query['apiToken']
        
        if 'q' not in query:
            keyboard = xbmc.Keyboard('', self._(32005))
            keyboard.doModal()
            if keyboard.isConfirmed() and keyboard.getText():
                text = keyboard.getText().replace(" ", "+")
                query['q'] = text
            else:
                response.sendInfo(self._(32006))
                return

        queryParams = urllib.urlencode(query)
        searchUrl = Constants.baseUrl + "/suche?" + queryParams
        
        self.context.log.debug("SearchPage - searching url: '{0}' ...", searchUrl)
        searchPage = SearchResource(searchUrl)
        searchPage.parse()
        self.context.log.debug("SearchPage - found '{0}' results.", len(searchPage.teasers))
        if searchPage.moreUrl is not None:
            self.context.log.debug("SearchPage - load-more-url: '{0}'.", searchPage.moreUrl)

        for teaser in searchPage.teasers:
            item = self._createItem(teaser, apiToken)
            response.addItem(item)
            