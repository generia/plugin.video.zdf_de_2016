from de.generia.kodi.plugin.backend.zdf.RubricResource import RubricResource       

from de.generia.kodi.plugin.frontend.base.Pagelet import Item        
from de.generia.kodi.plugin.frontend.base.Pagelet import Action        
from de.generia.kodi.plugin.frontend.base.Pagelet import Pagelet        

from de.generia.kodi.plugin.frontend.zdf.Constants import Constants
from de.generia.kodi.plugin.frontend.zdf.ItemPage import ItemPage


class RubricPage(ItemPage):

    def service(self, request, response):
        apiToken = request.params['apiToken']
        rubricUrl = request.params['rubricUrl']
        clusterTitle = None
        if 'clusterTitle' in request.params:
            clusterTitle = request.params['clusterTitle']

        self.info('rubric-page: url={}', rubricUrl)

        rubricResource = RubricResource(Constants.baseUrl + rubricUrl)
        self._parse(rubricResource)
        clusters = rubricResource.clusters
        
        if clusterTitle is not None:
            cluster = self._getCluster(clusters, clusterTitle)
            if cluster is not None:
                self._renderCluster(cluster, response, apiToken)
            else:
                self.warn("can't find cluster-title '{}' in rubric-url '{}'", clusterTitle, rubricUrl)
        else:
            self._renderClusters(clusters, response, apiToken, rubricUrl)
            
    def _getCluster(self, clusters, clusterTitle):
        for cluster in clusters:
            if cluster.title.encode('ascii', 'ignore') == clusterTitle:
                return cluster
        return None
        
    def _renderClusters(self, clusters, response, apiToken, rubricUrl):
        for cluster in clusters:
            clusterTitle = cluster.title.encode('ascii', 'ignore')
            action = Action(pagelet='RubricPage', params={'apiToken': apiToken, 'rubricUrl': rubricUrl, 'clusterTitle': clusterTitle})
            item = Item(cluster.title, action, isFolder=True)
            response.addItem(item)            
    
    def _renderCluster(self, cluster, response, apiToken):
        for teaser in cluster.teasers:
            item = self._createItem(teaser, apiToken)
            if item is not None:
                response.addItem(item)
            else:
                self.warn("can't find content-name for teaser-url '{}' and teaser-title '{}', skipping item ...", teaser.url, teaser.title)
        