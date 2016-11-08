from de.generia.kodi.plugin.backend.web.HtmlResource import HtmlResource

from de.generia.kodi.plugin.backend.zdf.Teaser import Teaser
from de.generia.kodi.plugin.backend.zdf.Teaser import parseTeaserArticle
from de.generia.kodi.plugin.backend.zdf.Teaser import compareTeasers


class Cluster(object):

    def __init__(self, title, teasers):
        self.title = title
        self.teasers = teasers
                        
    def __str__(self):
        return "<Cluster '%s' teasers='%d'>" % (self.title, len(self.teasers))
    
    
class RubricResource(HtmlResource):

    def __init__(self, url):
        super(RubricResource, self).__init__(url)
            
    def parse(self):
        super(RubricResource, self).parse()

        
        self.clusters = []
        clusterSections = self.content.find_all('section', class_='b-content-teaser-list')
        for clusterSection in clusterSections:
            cluster = self._parseClusterSection(clusterSection)
            if cluster is not None:
                self.clusters.append(cluster)        
        
        clusterArticles = self.content.find_all('article', class_='b-cluster')
        for clusterArticle in clusterArticles:
            cluster = self._parseClusterArticle(clusterArticle)
            if cluster is not None:
                self.clusters.append(cluster)

    def _parseClusterSection(self, clusterSection):

        h2 = clusterSection.find('h2', class_='title');
        if h2 is None:
            return None
        title = h2.text
        if title is not None:
            title = title.strip()
        else:
            return None
        
        teasers = []
        teaserArticles = clusterSection.find_all('article', class_='b-content-teaser-item')
        for teaserArticle in teaserArticles:
            teaser = parseTeaserArticle(teaserArticle)
            if teaser is not None:
                teasers.append(teaser)
            
        teasers = sorted(teasers, cmp=compareTeasers, reverse=True)
        return Cluster(title, teasers)

    
    def _parseClusterArticle(self, clusterArticle):
        h2 = clusterArticle.find('h2', class_='cluster-title');
        if h2 is None:
            return None
        title = h2.text
        if title is not None:
            title = title.strip()
        else:
            return None
        
        teasers = []
        teaserArticles = clusterArticle.find_all('article', class_='b-cluster-teaser')
        for teaserArticle in teaserArticles:
            teaser = parseTeaserArticle(teaserArticle)
            if teaser is not None:
                teasers.append(teaser)
            
        teasers = sorted(teasers, cmp=compareTeasers, reverse=True)
        return Cluster(title, teasers)
