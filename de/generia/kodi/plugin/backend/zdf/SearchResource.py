from de.generia.kodi.plugin.backend.web.HtmlResource import HtmlResource

from de.generia.kodi.plugin.backend.zdf.Teaser import Teaser
from de.generia.kodi.plugin.backend.zdf.Teaser import parseTeaserArticle
from de.generia.kodi.plugin.backend.zdf.Teaser import compareTeasers

class SearchResource(HtmlResource):

    def __init__(self, url):
        super(SearchResource, self).__init__(url)
        self._tags = []
            
    def parse(self):
        super(SearchResource, self).parse()
        searchColumn = self.content.find('article', class_='search-column')
        loadMore = searchColumn.find('a', class_='load-more')
        if loadMore is not None:
            self.moreUrl = loadMore['href']
        else:
            self.moreUrl = None
            
        articles = self.content.find_all('article', class_='b-content-teaser-item')
        #print "articles: ", len(articles)
        self.teasers = []
        for article in articles:
            teaser = parseTeaserArticle(article)
            self.teasers.append(teaser)

        self.teasers = sorted(self.teasers, cmp=compareTeasers, reverse=True)