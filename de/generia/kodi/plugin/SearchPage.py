
import urllib
import xbmc
import xbmcplugin
from de.generia.kodi.plugin.zdf.SearchResource import SearchResource       
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
        searchPage = SearchResource(searchUrl)
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
        title = teaser.title
        if teaser.label is not None and teaser.label != "":
            title = '[' + teaser.label + '] ' + title
        title.strip()

        if teaser.contentName is not None and teaser.playable:
            action = Action(pagelet='PlayVideo', params={'apiToken': apiToken, 'contentName': teaser.contentName})
        else:   
            action = Action(pagelet='RubrikPage', params={'apiToken': apiToken, 'rubrikUrl': teaser.url})
            self.context.log.info("SearchPage - redirecting to rubric-url  '{0}' and teaser-title '{1}' ...", teaser.url, title)
        item = Item(title, action, teaser.image, teaser.text, genre, teaser.date)
        return item
