from de.generia.kodi.plugin.backend.web.HtmlResource import HtmlResource

from de.generia.kodi.plugin.backend.zdf import stripHtml
from de.generia.kodi.plugin.backend.zdf.Regex import getTagPattern
from de.generia.kodi.plugin.backend.zdf.Regex import getTag
from de.generia.kodi.plugin.backend.zdf.Regex import compile

from de.generia.kodi.plugin.backend.zdf.Teaser import Teaser


sectionListPattern = getTagPattern('[^ ]*', 'b-content-teaser-list')
sectionTitlePattern = compile('<h2 class="[^"]*title[^"]*"[^>]*>([^<]*)</h2>')
sectionItemPattern = getTagPattern('article', 'b-content-teaser-item')

clusterListPattern = getTagPattern('article', 'b-cluster m-filter')
clusterTitlePattern = compile('<h2 class="[^"]*cluster-title[^"]*"[^>]*>([^<]*)</h2>')
clusterItemPattern = getTagPattern('article', 'b-cluster-teaser')

class Cluster(object):

    def __init__(self, title, listType, listStart, listEnd=-1):
        self.title = title
        self.listType = listType
        self.listStart = listStart
        self.listEnd = listEnd
        self.teasers = []
                        
    def __str__(self):
        return "<Cluster '%s' teasers='%d'>" % (self.title, len(self.teasers))
    
    
class RubricResource(HtmlResource):

    def __init__(self, url, listType=None, listStart=-1, listEnd=-1):
        super(RubricResource, self).__init__(url)
        self.listType = listType
        self.listStart = listStart
        self.listEnd = listEnd
            
    #
    # NOTE: content-teaser-lists and cluster-teaser-lists can occur in arbitrary order
    #
    def parse(self):
        super(RubricResource, self).parse()

        self.clusters = []
        if self.listType is None:
            pos = 0
            match = self._getNextMatch(self.content, pos)
            while match is not None:
                pos = match.end(0)
                class_ = match.group(1)
                titlePattern = clusterTitlePattern
                listType = 'cluster'
                if class_.find('b-content-teaser-list') != -1:
                    titlePattern = sectionTitlePattern
                    listType = 'content'
                    
                titleMatch = titlePattern.search(self.content, pos)
                if titleMatch is not None:
                    title = stripHtml(titleMatch.group(1))
                    pos = titleMatch.end(0)
                    cluster = Cluster(title, listType, pos)
                    self.clusters.append(cluster)
    
                match = self._getNextMatch(self.content, pos)
                if match is not None:
                    cluster.listEnd = match.start(0)-1
                else:
                    cluster.listEnd = len(self.content)-1

        else:
            cluster = Cluster(None, self.listType, self.listStart, self.listEnd)
            self.clusters.append(cluster)
            itemPattern = sectionItemPattern
            if self.listType == 'cluster':
                itemPattern = clusterItemPattern
            pos = self.listStart
            itemMatch = itemPattern.search(self.content, pos)
            while pos < self.listEnd and itemMatch is not None:
                teaser = Teaser()
                pos = teaser.parse(self.content, pos, itemMatch)
                if teaser.valid():
                    cluster.teasers.append(teaser)

                itemMatch = itemPattern.search(self.content, pos)

    def parse2(self):
        super(RubricResource, self).parse()

        self.clusters = []
        pos = 0
        match = self._getNextMatch(self.content, pos)
        cluster = None
        while match is not None:
            pos = match.end(0)
            class_ = match.group(1)
            if self._isListMatch(class_):
                titlePattern = clusterTitlePattern
                if class_.find('b-content-teaser-list') != -1:
                    titlePattern = sectionTitlePattern
                titleMatch = titlePattern.search(self.content, pos)
                if titleMatch is not None:
                    title = stripHtml(titleMatch.group(1))
                    pos = titleMatch.end(0)
                    cluster = Cluster(title, [])
                    self.clusters.append(cluster)
            elif cluster is not None:
                teaser = Teaser()
                pos = teaser.parse(self.content, pos, match)
                if teaser.valid():
                    cluster.teasers.append(teaser)

            match = self._getNextMatch(self.content, pos)
            
    def _isListMatch(self, class_):
        return class_.find('b-content-teaser-list') != -1 or class_.find('b-cluster m-filter') != -1 
    
    def _getNextMatch(self, string, pos=0):
        sectionListMatch = sectionListPattern.search(string, pos)
        clusterListMatch = clusterListPattern.search(string, pos)
        if sectionListMatch is None and clusterListMatch is None:
            return None
        
        if sectionListMatch is not None and clusterListMatch is None:
            return sectionListMatch
         
        if sectionListMatch is None and clusterListMatch is not None:
            return clusterListMatch
        
        if sectionListMatch.start(0) < clusterListMatch.start(0):
            return sectionListMatch
        
        return clusterListMatch
        '''        
        sectionMatch = sectionPattern.search(self.content)
        pos = 0
        cluster = None
        while sectionMatch is not None:
            pos = sectionMatch.end(0)
            class_ = sectionMatch.group(1)
            if class_.find('b-content-teaser-item') == -1:
                sectionTitleMatch = sectionTitlePattern.search(self.content, pos)
                if sectionTitleMatch is not None:
                    title = stripHtml(sectionTitleMatch.group(1))
                    pos = sectionTitleMatch.end(0)
                    cluster = Cluster(title, [])
                    self.clusters.append(cluster)
            elif cluster is not None:
                teaser = Teaser()
                pos = teaser.parse(self.content, pos, sectionMatch)
                if teaser.valid():
                    cluster.teasers.append(teaser)

            sectionMatch = sectionPattern.search(self.content, pos)


        # parse cluster teasers        
        articleMatch = articlePattern.search(self.content, pos)
        cluster = None
        while articleMatch is not None:
            pos = articleMatch.end(0)
            class_ = articleMatch.group(1)
            if class_.find('b-cluster-teaser') == -1:
                clusterTitleMatch = clusterTitlePattern.search(self.content, pos)
                if clusterTitleMatch is not None:
                    title = stripHtml(clusterTitleMatch.group(1))
                    pos = clusterTitleMatch.end(0)
                    cluster = Cluster(title, [])
                    self.clusters.append(cluster)
            elif cluster is not None:
                teaser = Teaser()
                pos = teaser.parse(self.content, pos, articleMatch)
                if teaser.valid():
                    cluster.teasers.append(teaser)

            articleMatch = articlePattern.search(self.content, pos)
        '''
            
    def _parseClusterSection(self, clusterSection):

        sectionTitleMatch = sectionTitlePattern.search(clusterSection)
        if sectionTitleMatch is None:
            return None
        title = stripHtml(sectionTitleMatch.group(1))
        pos = sectionTitleMatch.end(0)
        
        teasers = []
        while pos != -1:
            teaser = Teaser()
            pos = teaser.parse(clusterSection, pos)
            if teaser.valid():
                teasers.append(teaser)
            
        #teasers = sorted(teasers, cmp=compareTeasers, reverse=True)
        return Cluster(title, teasers)
