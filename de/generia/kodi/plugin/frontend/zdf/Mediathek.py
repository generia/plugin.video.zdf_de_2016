from de.generia.kodi.plugin.backend.zdf.ConfigurationResource import ConfigurationResource
from de.generia.kodi.plugin.backend.zdf.NavigationResource import NavigationResource

from de.generia.kodi.plugin.frontend.base.Pagelet import Item        
from de.generia.kodi.plugin.frontend.base.Pagelet import Action        
from de.generia.kodi.plugin.frontend.base.Pagelet import Pagelet        
from de.generia.kodi.plugin.frontend.base.Pagelet import PageletFactory        

from de.generia.kodi.plugin.frontend.zdf.Constants import Constants
from de.generia.kodi.plugin.frontend.zdf.SearchPage import SearchPage       
from de.generia.kodi.plugin.frontend.zdf.RubricPage import RubricPage       
from de.generia.kodi.plugin.frontend.zdf.PlayVideo import PlayVideo        

class MediathekFactory(PageletFactory):

    def __init__(self):
        super(MediathekFactory, self).__init__()
        
    def createPagelet(self, pageletId, params):
        if pageletId == 'SearchPage':
            return SearchPage()
        if pageletId == 'RubricPage':
            return RubricPage()
        if pageletId == 'PlayVideo':
            return PlayVideo()
        
        return Mediathek()
        

class Mediathek(Pagelet):

    def service(self, request, response):
        configuration = ConfigurationResource(Constants.configUrl)
        configuration.parse()
        apiToken = configuration.apiToken

        response.addFolder('Suche - Soko', Action('SearchPage', {'apiToken': apiToken, 'q':'Soko', 'contentTypes':'episode'}))
        response.addFolder('Suche - ganze Sendungen', Action('SearchPage', {'apiToken': apiToken, 'contentTypes':'episode'}))
        response.addFolder('Suche - Volltext', Action('SearchPage', {'apiToken': apiToken}))

        navigation = NavigationResource(Constants.baseUrl)
        navigation.parse()
        for rubric in navigation.rubrics:
            response.addFolder('Rubrik - ' + rubric.title, Action('RubricPage', {'apiToken': apiToken, 'rubricUrl': rubric.url}))
