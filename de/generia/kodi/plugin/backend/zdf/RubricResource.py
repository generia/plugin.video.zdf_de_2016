from de.generia.kodi.plugin.backend.web.HtmlResource import HtmlResource

from de.generia.kodi.plugin.backend.zdf.Regex import getTagPattern
from de.generia.kodi.plugin.backend.zdf.Regex import getTag
from de.generia.kodi.plugin.backend.zdf.Regex import compile

from de.generia.kodi.plugin.backend.zdf.Teaser import Teaser
from de.generia.kodi.plugin.backend.zdf.Teaser import parseTeaserArticle
from de.generia.kodi.plugin.backend.zdf.Teaser import compareTeasers

sectionPattern = getTagPattern('section', 'b-content-teaser-list')
sectionTitlePattern = compile('<h2 class="[^"]*title[^"]*"[^>]*>([^<]*)</h2>')

articlePattern = getTagPattern('article', 'b-cluster')
clusterTitlePattern = compile('<h2 class="[^"]*cluster-title[^"]*"[^>]*>([^<]*)</h2>')

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
        sectionMatch = sectionPattern.search(self.content)
        pos = 0
        while sectionMatch is not None:
            section = getTag('section', self.content, sectionMatch)
            cluster = self._parseClusterSection(section)
            if cluster is not None:
                self.clusters.append(cluster)
            pos = sectionMatch.end(0) + len(section)
            sectionMatch = sectionPattern.search(self.content, pos)

        
        articleMatch = articlePattern.search(self.content, pos)
        cluster = None
        while articleMatch is not None:
            pos = articleMatch.end(0)
            class_ = articleMatch.group(1)
            if class_.find('b-cluster-teaser') == -1:
                clusterTitleMatch = clusterTitlePattern.search(self.content, pos)
                if clusterTitleMatch is not None:
                    title = clusterTitleMatch.group(1).strip()
                    pos = clusterTitleMatch.end(0)
                    cluster = Cluster(title, [])
                    self.clusters.append(cluster)
            elif cluster is not None:
                teaser = Teaser()
                pos = teaser.parse(self.content, pos, articleMatch)
                if teaser.valid():
                    cluster.teasers.append(teaser)

            articleMatch = articlePattern.search(self.content, pos)

    def _parseClusterSection(self, clusterSection):

        sectionTitleMatch = sectionTitlePattern.search(clusterSection)
        if sectionTitleMatch is None:
            return None
        title = sectionTitleMatch.group(1).strip()
        pos = sectionTitleMatch.end(0)
        
        teasers = []
        while pos != -1:
            teaser = Teaser()
            pos = teaser.parse(clusterSection, pos)
            if teaser.valid():
                teasers.append(teaser)
            
        #teasers = sorted(teasers, cmp=compareTeasers, reverse=True)
        return Cluster(title, teasers)
        
    def parseSoup(self):
        super(RubricResource, self).parse()

        
        self.clusters = []
        clusterSections = self.content.find_all('section', class_='b-content-teaser-list')
        for clusterSection in clusterSections:
            cluster = self._parseClusterSectionSoup(clusterSection)
            if cluster is not None:
                self.clusters.append(cluster)        
        
        clusterArticles = self.content.find_all('article', class_='b-cluster')
        for clusterArticle in clusterArticles:
            cluster = self._parseClusterArticle(clusterArticle)
            if cluster is not None:
                self.clusters.append(cluster)

    def _parseClusterSectionSoup(self, clusterSection):

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
