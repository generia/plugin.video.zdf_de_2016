import urllib
import urllib2
import re

from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
from bs4 import SoupStrainer

from de.generia.kodi.plugin.backend.zdf.Teaser import Teaser

from de.generia.kodi.plugin.backend.zdf.SearchResource import SearchResource        
from de.generia.kodi.plugin.backend.zdf.NavigationResource import NavigationResource        
from de.generia.kodi.plugin.backend.zdf.RubricResource import RubricResource        
from de.generia.kodi.plugin.backend.zdf.ConfigurationResource import ConfigurationResource

from de.generia.kodi.plugin.backend.zdf.api.VideoContentResource import VideoContentResource
        
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
    

def getTagClassPattern(tag, class_):
    return re.compile('<' + tag + '\s*class=[^"]*' + class_ + '[^"]*"\s*>', re.DOTALL)

def getTag(tag, class_, string):
    pattern = getTagClassPattern(tag, class_)
    match = pattern.search(string)
    if match is None:
        return None

    i = match.start(0)
    endTag = '</' + tag + '>'
    j = string.find(endTag, i) + len(endTag)
    result = string[i:j]
    print result

def parseContentTeaserItemRE(article):
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

query = {'q': "Soko Stuttgart"}
queryParams = urllib.urlencode(query)
searchUrl = baseUrl + "/suche?" + queryParams
#searchUrl = "http://www.cloudev.de/"
'''
configuration = ConfigurationResource(configUrl)
configuration.parse()
print "Api-Token: " + configuration.apiToken
'''
'''
searchPage = SearchResource(searchUrl)
searchPage.parse()
for teaser in searchPage.teasers:
    print "- " + str(teaser)
print "load-more: " + searchPage.moreUrl
'''
'''
teaser = searchPage.teasers[1]
videoContentUrl = 'https://api.zdf.de/content/documents/' + teaser.contentName + '.json?profile=player'
videoContent = VideoContentResource(videoContentUrl, configuration.apiToken)
videoContent.parse()

print "Video-Content '" + teaser.contentName + "' -> url: '" + videoContent.url + "'"
'''
'''
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
#soup = getSoup(searchUrl)
html = getUrl(searchUrl)

#teaser = getTag('article', 'b-content-teaser-item')
pos = 0
while pos != -1:
    teaser = Teaser()
    pos = teaser.parse(html, pos)
    if teaser.valid():
        print teaser
    else:
        print "invalid teaser"
'''
'''
#pattern = re.compile('.*<article class="b-content-teaser-item x-column">')
pattern = re.compile('<article\s*class=[^"]*b-content-teaser-item[^"]*"\s*>', re.DOTALL)
match = pattern.search(html)
print match
if match is not None:
    i = match.start(0)
    j = html.find('</article>', i) + len('</article>')
    teaser = html[i:j]
    print teaser
#diagnose(html)
'''
'''
articlesStrainer = SoupStrainer("article")
#articlesStrainer = SoupStrainer("article", class_="b-content-teaser-item")

soup = BeautifulSoup(html, 'html.parser', parse_only=articlesStrainer)
print soup.prettify()

articles = soup.find_all('article', class_='b-content-teaser-item')
print "articles: ", len(articles)
for article in articles:
    parseContentTeaserItem(article)
'''