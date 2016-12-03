from de.generia.kodi.plugin.frontend.base.Pagelet import Action        

from de.generia.kodi.plugin.frontend.zdf.Constants import Constants
from de.generia.kodi.plugin.frontend.zdf.ItemPage import ItemPage


class ShowsAzPage(ItemPage):

    def service(self, request, response):
        apiToken = request.getParam('apiToken')

        rubricBaseUrl = '/sendungen-a-z?group='
        groups = []
        for i in range (0, 25):
            group = chr(ord('a') + i)
            groups.append(group)
        groups.append('0 - 9')
        
        for group in groups:
            url = rubricBaseUrl + group.replace(' ', '+')
            response.addFolder(self._(32038, group.upper()), Action('RubricPage', {'apiToken': apiToken, 'rubricUrl': url}))
        