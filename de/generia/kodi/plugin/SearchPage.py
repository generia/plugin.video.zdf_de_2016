
import urllib
import xbmc
import xbmcplugin
from de.generia.kodi.plugin.zdf.SearchPageResource import SearchPageResource       
from de.generia.kodi.plugin.Constants import Constants

from de.generia.kodi.plugin.Pagelet import Item        
from de.generia.kodi.plugin.Pagelet import Action        
from de.generia.kodi.plugin.Pagelet import Pagelet        



class SearchPage(Pagelet):

    def service(self, request, response):
        apiToken = request.params['apiToken']
        query = dict(request.params)
        del query['apiToken']
        
        if 'q' not in query:
            keyboard = xbmc.Keyboard('', 'Suche')
            keyboard.doModal()
            if keyboard.isConfirmed() and keyboard.getText():
                text = keyboard.getText().replace(" ", "+")
                query['q'] = text
            else:
                response.sendInfo("Empty search string")
                return

        queryParams = urllib.urlencode(query)
        searchUrl = Constants.baseUrl + "/suche?" + queryParams
        
        self.context.log.debug("SearchPage - searching url: '{0}' ...", searchUrl)
        searchPage = SearchPageResource(searchUrl)
        searchPage.parse()
        self.context.log.debug("SearchPage - found '{0}' results.", len(searchPage.teasers))
        if searchPage.moreUrl is not None:
            self.context.log.debug("SearchPage - load-more-url: '{0}'.", searchPage.moreUrl)

        for teaser in searchPage.teasers:
            item = self._createItem(teaser, apiToken)
            response.addItem(item)
            

    def _createItem(self, teaser, apiToken):
        item = None
        genre = ''
        sep = ''
        for tag in teaser.tags:
            genre += sep + tag
            sep = ' | '
        if teaser.contentName is not None and teaser.playable:
            title = teaser.title
            if teaser.label is not None:
                title = '[' + teaser.label + '] ' + title
            action = Action(pagelet='PlayVideo', params={'apiToken': apiToken, 'contentName': teaser.contentName})
            item = Item(teaser.title, action, teaser.image, teaser.text, genre)
        else:   
            self.context.log.warn("SearchPage - can't find content-name for teaser-url '{0}' and teaser-title '{1}', skipping item ...", teaser.url, teaser.title)
            #item = Item(teaser.title, None, teaser.image, teaser.text, genre)
        return item
