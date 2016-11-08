from de.generia.kodi.plugin.zdf.ConfigurationResource import ConfigurationResource
from de.generia.kodi.plugin.zdf.NavigationResource import NavigationResource
from de.generia.kodi.plugin.Constants import Constants

from de.generia.kodi.plugin.SearchPage import SearchPage       
from de.generia.kodi.plugin.RubricPage import RubricPage       
from de.generia.kodi.plugin.PlayVideo import PlayVideo        

from de.generia.kodi.plugin.Pagelet import Item        
from de.generia.kodi.plugin.Pagelet import Action        
from de.generia.kodi.plugin.Pagelet import Pagelet        
from de.generia.kodi.plugin.Pagelet import PageletFactory        

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
