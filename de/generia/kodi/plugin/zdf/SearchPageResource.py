from de.generia.kodi.plugin.web.HtmlResource import HtmlResource
from de.generia.kodi.plugin.zdf.Teaser import Teaser

class SearchPageResource(HtmlResource):

    def __init__(self, url):
        super(SearchPageResource, self).__init__(url)
        self._tags = []
            
    def parse(self):
        super(SearchPageResource, self).parse()
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
            teaser = self._parseArticle(article)
            self.teasers.append(teaser)

    def _parseArticle(self, article):
        picture = article.find('picture')
        source = picture.find('source', class_='m-16-9')
        srcset = source['data-srcset']
        src = srcset.split(' ')[0]
        
        teaserLabel = article.find('div', class_='teaser-label')
        label = None
        type = None
        if teaserLabel is not None:            
            label = teaserLabel.text.strip()
            icon = teaserLabel.find('span', class_='icon')
            type = self.getIconType(icon['class']) 

        teaserTitle = article.find('h3', class_='teaser-title')
        genre = teaserTitle.find(itemprop='genre')
        tags = []
        if genre is not None:
            parts = genre.text.split('|')
            for part in parts:
                tags.append(part.strip())
    
        a = teaserTitle.find('a', itemprop='url')
        url = a['href'].strip()
        title = a.text.strip()
        icon = a.find('span', class_='title-icon')
        playable = False
        if icon is not None:
            urlType = self.getIconType(icon['class']) 
            playable = urlType != None and urlType == 'play'
        
        teaserText = article.find('p', class_='teaser-text')
        text = teaserText.string.strip()
        
        date = article.find('dd', class_='video-airing').text.strip()
        return Teaser(title, text, src, url, date, tags, label, type, playable)

    def getIconType(self, iconClass):
        for c in iconClass:
            if c.startswith('icon-'):
                i = c.rfind('_')
                if i == -1:
                    return None
                return c[i+1:]
        return None