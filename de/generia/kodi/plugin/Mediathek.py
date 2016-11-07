from de.generia.kodi.plugin.zdf.ConfigurationResource import ConfigurationResource
from de.generia.kodi.plugin.Constants import Constants

from de.generia.kodi.plugin.SearchPage import SearchPage       
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
        if pageletId == 'PlayVideo':
            return PlayVideo()
        
        return Mediathek()
        

class Mediathek(Pagelet):

    def service(self, request, response):
        configuration = ConfigurationResource(Constants.configUrl)
        configuration.parse()
        apiToken = configuration.apiToken

        response.addFolder('Suche - ganze Sendungen', Action('SearchPage', {'apiToken': apiToken, 'contentTypes':'episode'}))
        response.addFolder('Suche - Volltext', Action('SearchPage', {'apiToken': apiToken}))
        response.addFolder('Suche Soko', Action('SearchPage', {'apiToken': apiToken, 'q':'Soko', 'contentTypes':'episode'}))
        
        '''
        url = 'https://nrodlzdf-a.akamaihd.net/de/zdf/15/07/150728_ersteweltkrieg1_inf/12/150728_ersteweltkrieg1_inf_1456k_p13v11.mp4'
        img = 'https://www.zdf.de/assets/erster-weltkrieg-legendaere-seeschlachten-kampf-vor-dem-100~768x432?cb=1476403737878'
        item = Item('Seeschlachten', Action(url=url), img)
        response.addItem(item)
        '''