
from de.generia.kodi.plugin.zdf.RubricResource import RubricResource       
from de.generia.kodi.plugin.Constants import Constants

from de.generia.kodi.plugin.Pagelet import Item        
from de.generia.kodi.plugin.Pagelet import Action        
from de.generia.kodi.plugin.Pagelet import Pagelet        



class RubricPage(Pagelet):

    def service(self, request, response):
        apiToken = request.params['apiToken']
        rubricUrl = request.params['rubricUrl']
        clusterTitle = None
        if 'clusterTitle' in request.params:
            clusterTitle = request.params['clusterTitle']

        self.context.log.info('Info: rubric-page: url={0}', rubricUrl)

        rubricResource = RubricResource(Constants.baseUrl + rubricUrl)
        rubricResource.parse()
        clusters = rubricResource.clusters
        
        if clusterTitle is not None:
            cluster = self._getCluster(clusters, clusterTitle)
            if cluster is not None:
                self._renderCluster(cluster, response, apiToken)
            else:
                self.context.log.warn("RubricPage - can't find cluster-title '{0}' in rubric-url '{1}'", clusterTitle, rubricUrl)
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
            #self.context.log.info("RubricPage - 1. render cluster '{0}' ...", clusterTitle)
            action = Action(pagelet='RubricPage', params={'apiToken': apiToken, 'rubricUrl': rubricUrl, 'clusterTitle': clusterTitle})
            item = Item(cluster.title, action, isFolder=True)
            response.addItem(item)            
    
    def _renderCluster(self, cluster, response, apiToken):
        for teaser in cluster.teasers:
            #self.context.log.info("RubricPage - 2. render cluster '{0}' ...", cluster.title)
            item = self._createItem(teaser, apiToken)
            if item is not None:
                response.addItem(item)
            else:
                self.context.log.warn("RubricPage - can't find content-name for teaser-url '{0}' and teaser-title '{1}', skipping item ...", teaser.url, teaser.title)
            
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
            #action = Action(pagelet='RubricPage', params={'apiToken': apiToken, 'rubricUrl': '/comedy'})
            item = Item(teaser.title, action, teaser.image, teaser.text, genre, teaser.date)
    
        return item
        