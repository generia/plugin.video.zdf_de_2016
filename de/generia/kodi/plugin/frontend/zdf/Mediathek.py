import os

import xbmc

from xbmcaddon import Addon

from de.generia.kodi.plugin.backend.zdf.ConfigurationResource import ConfigurationResource
from de.generia.kodi.plugin.backend.zdf.NavigationResource import NavigationResource

from de.generia.kodi.plugin.frontend.base.Pagelet import Item        
from de.generia.kodi.plugin.frontend.base.Pagelet import Action        
from de.generia.kodi.plugin.frontend.base.Pagelet import Pagelet        
from de.generia.kodi.plugin.frontend.base.Pagelet import PageletFactory        

from de.generia.kodi.plugin.frontend.zdf.Constants import Constants
from de.generia.kodi.plugin.frontend.zdf.SearchPage import SearchPage       
from de.generia.kodi.plugin.frontend.zdf.SearchHistoryPage import SearchHistoryPage       
from de.generia.kodi.plugin.frontend.zdf.RubricsPage import RubricsPage       
from de.generia.kodi.plugin.frontend.zdf.RubricPage import RubricPage       
from de.generia.kodi.plugin.frontend.zdf.PlayVideo import PlayVideo        

from de.generia.kodi.plugin.frontend.zdf.data.SearchHistory import SearchHistory       


class MediathekFactory(PageletFactory):
    settings = None
    
    def __init__(self, settings=None):
        super(MediathekFactory, self).__init__()
        self.settings = settings
        
    def createPagelet(self, pageletId, params):
        if pageletId == 'SearchPage':
            return SearchPage(self._createSearchHistory())
        if pageletId == 'SearchHistoryPage':
            return SearchHistoryPage(self._createSearchHistory())
        if pageletId == 'RubricsPage':
            return RubricsPage()
        if pageletId == 'RubricPage':
            return RubricPage()
        if pageletId == 'PlayVideo':
            return PlayVideo()
        
        return Mediathek()
        
    def _createSearchHistory(self):
        addon = Addon()
        profileDir = xbmc.translatePath(addon.getAddonInfo('profile'))
        storeFile  = os.path.join(profileDir, 'searchHistory.txt') 
        return SearchHistory(storeFile, self.settings.searchHistorySize)

class Mediathek(Pagelet):

    def service(self, request, response):
        configuration = ConfigurationResource(Constants.configUrl)
        self._parse(configuration)
        apiToken = configuration.apiToken

        response.addFolder(self._(32030), Action('SearchHistoryPage', {'apiToken': apiToken }))
        response.addFolder(self._(32001), Action('SearchPage', {'apiToken': apiToken, 'contentTypes':'episode'}))
        response.addFolder(self._(32002), Action('SearchPage', {'apiToken': apiToken}))

        response.addFolder(self._(32003), Action('RubricsPage', {'apiToken': apiToken}))
