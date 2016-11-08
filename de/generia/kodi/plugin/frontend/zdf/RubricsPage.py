from de.generia.kodi.plugin.backend.zdf.NavigationResource import NavigationResource

from de.generia.kodi.plugin.frontend.base.Pagelet import Action        

from de.generia.kodi.plugin.frontend.zdf.Constants import Constants
from de.generia.kodi.plugin.frontend.zdf.ItemPage import ItemPage


class RubricsPage(ItemPage):

    def service(self, request, response):
        apiToken = request.params['apiToken']

        navigation = NavigationResource(Constants.baseUrl)
        navigation.parse()
        for rubric in navigation.rubrics:
            response.addFolder('Rubrik - ' + rubric.title, Action('RubricPage', {'apiToken': apiToken, 'rubricUrl': rubric.url}))