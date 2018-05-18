import urllib
import urllib2
import re

from de.generia.kodi.plugin.backend.zdf.Teaser import Teaser

from de.generia.kodi.plugin.backend.zdf.SearchResource import SearchResource        
from de.generia.kodi.plugin.backend.zdf.NavigationResource import NavigationResource        
from de.generia.kodi.plugin.backend.zdf.RubricResource import RubricResource        
from de.generia.kodi.plugin.backend.zdf.LiveTvResource import LiveTvResource        
from de.generia.kodi.plugin.backend.zdf.VideoResource import VideoResource        
from de.generia.kodi.plugin.backend.zdf.TeaserLazyloadResolver import TeaserLazyloadResolver       

from de.generia.kodi.plugin.backend.zdf.api.VideoContentResource import VideoContentResource
from de.generia.kodi.plugin.backend.zdf.api.StreamInfoResource import StreamInfoResource

from de.generia.kodi.plugin.frontend.zdf.Constants import Constants

        
def getUrl(url):
    print "getUrl: " + url
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link
    
# https://www.zdf.de/suche?q=heute-show&from=&to=&sender=alle+Sender&attrs=

baseUrl = Constants.baseUrl
apiBaseUrl = Constants.apiBaseUrl

query = {'q': "Die Chefin"}
queryParams = urllib.urlencode(query)
searchUrl = baseUrl + "/suche?" + queryParams
#searchUrl = "http://www.cloudev.de/"

'''
streamInfoUrl = 'https://api.zdf.de/tmd/2/ngplayer_2_3/vod/ptmd/mediathek/170209_sendung_sok8'
streamInfo = StreamInfoResource(streamInfoUrl, configuration.apiToken)
streamInfo.parse()
print "streamUrl: " + streamInfo.streamUrl + ", subTitleUrl: " + streamInfo.subTitlesUrl + "'"
'''
'''
searchPage = SearchResource(searchUrl)
searchPage.parse()
print str(searchPage.resultsPerPage) + " - #" + str(searchPage.results)
for teaser in searchPage.teasers:
    print "- " + str(teaser)
if searchPage.moreUrl is not None:
    print "load-more: " + searchPage.moreUrl
'''
'''
#teaser = searchPage.teasers[1]
#videoContentUrl = 'https://api.zdf.de/content/documents/' + teaser.contentName + '.json?profile=player'
#videoContentUrl = 'https://api.zdf.de/content/documents/heute-journal-vom-9-juni-2017-100.json?profile=player'
#videoContentUrl = 'https://api.zdf.de/content/documents/zdf-live-beitrag-100.json?profile=player'
#videoContentUrl = 'https://api.zdf.de/content/documents/heute-show---der-jahresrueckblick-vom-15-dezember-2017-100.json?profile=player'
videoContentUrl = 'https://api.zdf.de/content/documents/zdf/comedy/heute-show/heute-show---der-jahresrueckblick-vom-15-dezember-2017-100.json?profile=player'
apiToken = '71f18d1df774fbf61390bd6bf419e8e17dd7f484'
videoContent = VideoContentResource(videoContentUrl, apiBaseUrl, apiToken)
videoContent.parse()
'''
#print "Video-Content url: '" + videoContent.streamInfoUrl + "'"
'''
navigationResource = NavigationResource(baseUrl)
navigationResource.parse()
for rubric in navigationResource.rubrics:
    print "Rubric: " + str(rubric)
'''
'''
liveTvResource = LiveTvResource(baseUrl + '/live-tv')
liveTvResource.parse()
for teaser in liveTvResource.teasers:
    print "Teaser: " + str(teaser)
'''
'''
video = '/content/documents/heute-journal-vom-2-november-2017-100.json?profile=player'
https://api.zdf.de/content/documents/heute-show---der-jahresrueckblick-vom-15-dezember-2017-100.json?profile=player
videoResource = VideoResource(baseUrl + video)
videoResource.parse()
print "Video-Resource apiToken: '" + videoResource.configApiToken + "'"
'''
#rubric = '/krimi'
#rubric = '/dokumentation/zdf-history'
#rubric = '/doku-wissen/themenseite-doku-wissen-astronomie-100.html'
#rubric = '/meist-gesehen'
#rubric = '/politik/phoenix-runde'
#rubric = '/barrierefreiheit-im-zdf'
#rubric = '/comedy/neo-magazin-mit-jan-boehmermann'
#rubric = '/nachrichten'
#rubric =  '/comedy-show'
rubric =  '/'
rubricResource = RubricResource(baseUrl + rubric)
rubricResource.parse()
for teaser in rubricResource.teasers:
    print teaser
testCluster = None
testIndex = 2
i = 0
for cluster in rubricResource.clusters:
    i = i + 1
    if testIndex == i or testCluster is None:
        testCluster = cluster
    print str(i) + ":" + str(cluster)
    for teaser in cluster.teasers:
        print teaser

rubricResource = RubricResource(baseUrl + rubric, testCluster.listType, testCluster.listStart, testCluster.listEnd)
rubricResource.parse()
teaserLazyloadResolver = TeaserLazyloadResolver()
for cluster in rubricResource.clusters:
    print cluster
    cluster.teasers.extend(teaserLazyloadResolver.resolveTeasers(cluster.lazyloadTeasers))
    for teaser in cluster.teasers:
        print teaser

'''
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
'''