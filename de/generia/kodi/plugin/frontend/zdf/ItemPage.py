from de.generia.kodi.plugin.frontend.base.Pagelet import Item        
from de.generia.kodi.plugin.frontend.base.Pagelet import Action        
from de.generia.kodi.plugin.frontend.base.Pagelet import Pagelet        

from de.generia.kodi.plugin.frontend.zdf.Constants import Constants


class ItemPage(Pagelet):


    def _createItem(self, teaser, apiToken):
        item = None
        genre = ''
        sep = ''
        for tag in teaser.tags:
            genre += sep + tag
            sep = ' | '
        title = teaser.title
        if teaser.label is not None and teaser.label != "":
            label = teaser.label
            if teaser.type is not None:
                label = teaser.type.capitalize() + ": " + label
            title = '[' + label + '] ' + title
        title.strip()

        isFolder = False
        if teaser.contentName is not None and teaser.playable:
            action = Action(pagelet='PlayVideo', params={'apiToken': apiToken, 'contentName': teaser.contentName})
            isFolder = False
        else:   
            action = Action(pagelet='RubricPage', params={'apiToken': apiToken, 'rubricUrl': teaser.url})
            self.info("redirecting to rubric-url  '{}' and teaser-title '{}' ...", teaser.url, title)
            isFolder = True
            #return None
        item = Item(title, action, teaser.image, teaser.text, genre, teaser.date, isFolder, teaser.playable)
        return item
