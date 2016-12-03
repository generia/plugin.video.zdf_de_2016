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
from de.generia.kodi.plugin.frontend.zdf.search.SearchPage import SearchPage       
from de.generia.kodi.plugin.frontend.zdf.search.SearchMenuPage import SearchMenuPage       
from de.generia.kodi.plugin.frontend.zdf.search.SearchHistoryPage import SearchHistoryPage       
from de.generia.kodi.plugin.frontend.zdf.RubricsPage import RubricsPage       
from de.generia.kodi.plugin.frontend.zdf.RubricPage import RubricPage       
from de.generia.kodi.plugin.frontend.zdf.LiveTvPage import LiveTvPage       
from de.generia.kodi.plugin.frontend.zdf.ShowsAzPage import ShowsAzPage       
from de.generia.kodi.plugin.frontend.zdf.PlayVideo import PlayVideo        

from de.generia.kodi.plugin.frontend.zdf.search.SearchHistory import SearchHistory       


class MediathekFactory(PageletFactory):
    settings = None
    
    def __init__(self, settings=None):
        super(MediathekFactory, self).__init__()
        self.settings = settings
        
    def createPagelet(self, pageletId, params):
        if pageletId == 'SearchPage':
            return SearchPage(self._createSearchHistory())
        if pageletId == 'SearchMenuPage':
            return SearchMenuPage()
        if pageletId == 'SearchHistoryPage':
            return SearchHistoryPage(self._createSearchHistory())
        if pageletId == 'RubricsPage':
            return RubricsPage()
        if pageletId == 'RubricPage':
            return RubricPage()
        if pageletId == 'LiveTvPage':
            return LiveTvPage()
        if pageletId == 'ShowsAzPage':
            return ShowsAzPage()
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

        response.addFolder(self._(32005), Action('SearchMenuPage', {'apiToken': apiToken}))

        response.addFolder(self._(32003), Action('RubricsPage', {'apiToken': apiToken}))

        response.addFolder(self._(32031), Action('RubricPage', {'apiToken': apiToken, 'rubricUrl': '/bestbewertet'}))
        response.addFolder(self._(32032), Action('RubricPage', {'apiToken': apiToken, 'rubricUrl': '/meist-gesehen'}))
        response.addFolder(self._(32037), Action('ShowsAzPage', {'apiToken': apiToken}))
        #response.addFolder(self._(32034), Action('RubricPage', {'apiToken': apiToken, 'rubricUrl': '/barrierefreiheit-im-zdf'}))
        response.addFolder(self._(32036), Action('RubricPage', {'apiToken': apiToken, 'rubricUrl': '/sendung-verpasst'}))

        response.addFolder(self._(32035), Action('LiveTvPage', {'apiToken': apiToken}))
