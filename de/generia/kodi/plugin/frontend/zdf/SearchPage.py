import urllib
import urlparse

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
        
        self.info("Timer - creating list items  ...")
        start = self.context.log.start()
        self._addItems(response, searchPage.teasers, apiToken)
        self.info("Timer - creating list items ... done. [{} ms]", self.context.log.stop(start))
        
        if len(searchPage.teasers) == 0:
            return
        
        if self.settings.loadAllSearchResults:
            self._addMoreResults(response, searchPage.moreUrl, apiToken)
        else:
            self._addMoreFolder(response, searchPage.moreUrl, apiToken)

    def _addItems(self, response, teasers, apiToken):
        for teaser in teasers:
            if not self.settings.showOnlyPlayableSearchResults or teaser.playable: 
                item = self._createItem(teaser, apiToken)
                response.addItem(item)

    def _addMoreResults(self, response, moreUrl, apiToken):
        while moreUrl is not None:
            moreUrl = moreUrl.replace('&#x3D;', '=')
            moreUrl = moreUrl.replace('&amp;', '&')

            searchUrl = Constants.baseUrl + moreUrl
            self.info("searching url: '{}' ...", searchUrl)
            searchPage = SearchResource(searchUrl)
            self._parse(searchPage)
            
            if len(searchPage.teasers) > 0:
                self._addItems(response, searchPage.teasers, apiToken)
                moreUrl = searchPage.moreUrl
            else: 
                moreUrl = None
            self.info("found '{}' results.", len(searchPage.teasers))

    def _addMoreFolder(self, response, moreUrl, apiToken):
        if moreUrl is not None:                
            moreAction = self._getMoreAction(moreUrl, apiToken)
            response.addFolder(self._(32017), moreAction)

    def _getMoreAction(self, moreUrl, apiToken):
        i = moreUrl.find('?')
        if i != -1:
            moreQuery = moreUrl[i+1:]
            moreQuery = moreQuery.replace('&#x3D;', '=')
            moreQuery = moreQuery.replace('&amp;', '&')
            searchArgs = urlparse.parse_qs(moreQuery)
            for key, value in searchArgs.iteritems():
                searchArgs[key] = value[0]
            searchArgs['apiToken'] = apiToken
            moreAction = Action('SearchPage', searchArgs)
            return moreAction
        

    def _getKeyboardInput(self):
        keyboard = xbmc.Keyboard('', self._(32005))
        keyboard.doModal()
        text = None
        if keyboard.isConfirmed() and keyboard.getText():
            text = keyboard.getText().replace(" ", "+")
        return text

