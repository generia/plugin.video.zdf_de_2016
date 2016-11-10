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
            self.info("Timer - getting search-string from keyboard ...")
            start = self.context.log.start()
            text = self._getKeyboardInput()
            self.info("Timer - getting search-string from keyboard ... done. [{} ms]", self.context.log.stop(start))
            if text is not None:
                query['q'] = text
            else:
                response.sendInfo(self._(32006))
                return

        queryParams = urllib.urlencode(query)
        searchUrl = Constants.baseUrl + "/suche?" + queryParams
        
        self.debug("searching url: '{}' ...", searchUrl)
        searchPage = SearchResource(searchUrl)
        self._parse(searchPage)
        self.debug("found '{}' results.", len(searchPage.teasers))
        
        if len(searchPage.teasers) == 0:
            response.sendInfo(self._(32013))
        
        if searchPage.moreUrl is not None:
            self.debug("load-more-url: '{}'.", searchPage.moreUrl)

        self.info("Timer - creating list items  ...")
        start = self.context.log.start()
        for teaser in searchPage.teasers:
            item = self._createItem(teaser, apiToken)
            response.addItem(item)
        self.info("Timer - creating list items ... done. [{} ms]", self.context.log.stop(start))

    def _getKeyboardInput(self):
        keyboard = xbmc.Keyboard('', self._(32005))
        keyboard.doModal()
        text = None
        if keyboard.isConfirmed() and keyboard.getText():
            text = keyboard.getText().replace(" ", "+")
        return text

