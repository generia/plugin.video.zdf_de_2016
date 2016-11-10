from datetime import datetime

from de.generia.kodi.plugin.backend.zdf.Regex import getTagPattern
from de.generia.kodi.plugin.backend.zdf.Regex import getTag
from de.generia.kodi.plugin.backend.zdf.Regex import compile

def parseTeaserArticle(article):
    if 'm-hidden' in article.get('class'):
        return None
    
    picture = article.find('picture')
    src = None
    if picture is not None:
        source = picture.find('source', class_='m-16-9')
        srcset = source['data-srcset']
        src = srcset.split(' ')[0]
    
    teaserLabel = article.find('div', class_='teaser-label')
    label = None
    type = None
    if teaserLabel is not None:            
        label = teaserLabel.text.strip()
        icon = teaserLabel.find('span', class_='icon')
        type = _getIconType(icon['class']) 

    teaserTitle = article.find('h3', class_='teaser-title')
    if teaserTitle is None:
        return None
    
    genre = teaserTitle.find('span', class_='teaser-cat')
    tags = []
    if genre is not None:
        parts = genre.text.split('|')
        for part in parts:
            tags.append(part.strip())

    a = teaserTitle.find('a', itemprop='url')
    if a is None:
        return None
    url = a['href'].strip()
    if  url[0:1] != '/':
        return None
    title = a.text.strip()
    
    # shorten title, if double with second tag
    if len(tags) > 1:
        tag = tags[1]
        if tag == title[0:len(tag)]:
            title = title[len(tag):].strip()
    
    icon = a.find('span', class_='title-icon')
    playable = False
    if icon is not None:
        urlType = _getIconType(icon['class']) 
        playable = urlType != None and urlType == 'play'
    
    teaserText = article.find('p', class_='teaser-text')
    text = None
    if teaserText is not None and teaserText.string is not None:
        text = teaserText.string.strip()
    
    airing = article.find('dd', class_='video-airing')
    date = None
    if airing is not None:
        date = airing.text.strip()

    teaser = Teaser()
    teaser.init(title, text, src, url, date, tags, label, type, playable)
    return teaser


def _getIconType(iconClass):
    for c in iconClass:
        if c.startswith('icon-'):
            i = c.rfind('_')
            if i == -1:
                return None
            return c[i+1:]
    return None

teaserPattern = getTagPattern('article', 'b-content-teaser-item')
sourcePattern = compile('<source\s*class="m-16-9"[^>]*data-srcset="([^"]*)"')
labelPattern = getTagPattern('div', 'teaser-label')
iconPattern = compile('<span\s*class="icon-[0-9]*_([^ ]*) icon">')
catPattern = compile('<span class="teaser-cat"[^>]*>([^<]*)</span>')
aPattern = compile('<a href="([^"]*)"[^>]*>')
titleIconPattern = compile('<span\s*class="title-icon icon-[0-9]*_([^"]*)">')
textPattern = compile('<p class="teaser-text"[^>]*>([^<]*)</p>')
datePattern = compile('<dd class="video-airing"[^>]*>([^<]*)</dd>')

    
def compareTeasers(t1, t2):
    if t1 is None and t2 is None:
        return 0
    if t1 is None and t2 is not None:
        return 1
    if t1 is not None and t2 is None:
        return -1
    
    '''
    if t1.date is not None and t2.date is not None:
        d1 = datetime.strptime(t1.date, "%d.%m.%Y")
        d2 = datetime.strptime(t2.date, "%d.%m.%Y")
        return d1.toordinal() - d2.toordinal()
    '''
    if t1.date is not None and t2.date is None:
        return 1
        
    if t1.date is None and t2.date is not None:
        return -1
    
    if t1.title < t2.title:
        return -1
    
    if t1.title > t2.title:
        return 1
    
    return 0

class Teaser(object):
    title = None
    text = None
    image = None
    url = None
    date = None
    tags = None
    label = None
    type = None
    playable = False
    contentName = None
    
    def __init__(self):
        pass
               
    def init(self, title, text, image, url, date, tags, label, type, playable):
        self.title = title
        self.text = text
        self.image = image
        self.url = url
        self.date = date
        self.tags = tags
        self.label = label
        self.type = type
        self.playable = playable
        self.contentName = None
        if url is not None:
            i = url.rfind('.')
            if i != -1:
                j = url.rfind('/')
                if j != -1:
                    self.contentName = url[j+1:i]
                    
    def valid(self):
        return self.title is not None and self.url is not None and self.url[0:1] == '/' 
     
    def __str__(self):
        return "<Teaser '%s' url='%s'>" % (self.title, self.url)
        

    def parse(self, string, pos=0, teaserMatch=None):
        if teaserMatch is None:
            teaserMatch = teaserPattern.search(string, pos)
        if teaserMatch is None:
            return -1
        class_ = teaserMatch.group(1)
        if class_.find('m-hidden') != -1:
            return -1
        
        article = getTag('article', string, teaserMatch)
        endPos = teaserMatch.start(0) + len(article)
        
        sourceMatch = sourcePattern.search(article)
        src = None
        if sourceMatch is not None:
            srcset = sourceMatch.group(1)
            src = srcset.split(' ')[0]
            pos = sourceMatch.end(0)
        
        labelMatch = labelPattern.search(article, pos)
        label = None
        type = None
        if labelMatch is not None:        
            labelTags = getTag('div', article, labelMatch)
            iconMatch = iconPattern.search(labelTags)
            if iconMatch is not None:    
                type = iconMatch.group(1)
            i = labelTags.find('</span>') + len('</span>')
            j = labelTags.rfind('</div>')
            pos = j + len('</div>') 
            label = labelTags[i:j]
            label = label.replace('<strong>', '')
            label = label.replace('</strong>', '')
            label = label.strip()
            
        catMatch = catPattern.search(article, pos)
        genre = None
        category = None
        tags = []
        if catMatch is not None:
            parts = catMatch.group(1).strip().split('|')
            if len(parts) > 0:
                genre = parts[0].strip()
                tags.append(genre)
            if len(parts) > 1:
                category = parts[1].strip()
                tags.append(category) 
            pos = catMatch.end(0)
            
        aMatch = aPattern.search(article, pos)
        title = None
        url = None
        playable = False
        if aMatch is not None:
            url = aMatch.group(1).strip()        
            pos = aMatch.end(0)
            i = pos
            j = article.find('</a>', i)
            iconMatch = titleIconPattern.search(article, pos)
            if iconMatch is not None:    
                playable =  iconMatch.group(1) == 'play'
                i = article.find('</span>', pos) + len('</span>')
            title = article[i:j]
            title = title.replace('<strong>', '')
            title = title.replace('</strong>', '')
            title = title.strip()
            pos = j + len('</a>') 
    
        textMatch = textPattern.search(article, pos)
        text = None
        if textMatch is not None:
            text = textMatch.group(1).strip()
            pos = textMatch.end(0)
            
        dateMatch = datePattern.search(article, pos)
        date = None
        if dateMatch is not None:
            date = dateMatch.group(1).strip()
            pos = dateMatch.end(0)
    
        self.init(title, text, src, url, date, tags, label, type, playable)
        return endPos
