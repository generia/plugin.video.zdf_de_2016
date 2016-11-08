import urllib
import urllib2

from bs4 import BeautifulSoup
from re import search

from de.generia.kodi.plugin.zdf.SearchResource import SearchResource        
from de.generia.kodi.plugin.zdf.NavigationResource import NavigationResource        
from de.generia.kodi.plugin.zdf.RubricResource import RubricResource        
from de.generia.kodi.plugin.zdf.ConfigurationResource import ConfigurationResource
from de.generia.kodi.plugin.zdf.api.VideoContentResource import VideoContentResource
        
def getUrl(url):
    print "getUrl: " + url
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link

def getSoup(url):
    html = getUrl(url)
    return BeautifulSoup(html, 'html.parser')

def parseContentTeaserItem(article):
    picture = article.find('picture')
    source = picture.find('source', class_='m-16-9')
    srcset = source['data-srcset']
    src = srcset.split(' ')[0]
    
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
    teaserText = article.find('p', class_='teaser-text')
    text = teaserText.string.strip()
    
    date = article.find('dd', class_='video-airing').text.strip()
    print "Teaser: '%s'\n- url='%s'\n- img='%s'\n- date: %s\n- tags: %s\n- description: '%s'\n" % (title, url, src, date, tags, text)
    
# https://www.zdf.de/suche?q=heute-show&from=&to=&sender=alle+Sender&attrs=

baseUrl = "https://www.zdf.de"
configUrl = baseUrl + '/ZDFplayer/configs/zdf/zdf2016/configuration.json'

query = {'q': "heute show"}
queryParams = urllib.urlencode(query)
searchUrl = baseUrl + "/suche?" + queryParams
#searchUrl = "http://www.cloudev.de/"
configuration = ConfigurationResource(configUrl)
configuration.parse()
print "Api-Token: " + configuration.apiToken
'''

searchPage = SearchResource(searchUrl)
searchPage.parse()
for teaser in searchPage.teasers:
    print "- " + str(teaser)
print "load-more: " + searchPage.moreUrl

teaser = searchPage.teasers[1]
videoContentUrl = 'https://api.zdf.de/content/documents/' + teaser.contentName + '.json?profile=player'
videoContent = VideoContentResource(videoContentUrl, configuration.apiToken)
videoContent.parse()

print "Video-Content '" + teaser.contentName + "' -> url: '" + videoContent.url + "'"

navigationResource = NavigationResource(baseUrl)
navigationResource.parse()
for rubric in navigationResource.rubrics:
    print "Rubric: " + str(rubric)
'''
rubricResource = RubricResource(baseUrl + '/filme-serien')
rubricResource.parse()
for cluster in rubricResource.clusters:
    print cluster
    for teaser in cluster.teasers:
        print teaser
'''
soup = getSoup(searchUrl)
#print soup
articles = soup.find_all('article', class_='b-content-teaser-item')
print "articles: ", len(articles)
for article in articles:
    parseContentTeaserItem(article)
'''