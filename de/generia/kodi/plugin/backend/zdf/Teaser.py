from datetime import datetime

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

    return Teaser(title, text, src, url, date, tags, label, type, playable)

def _getIconType(iconClass):
    for c in iconClass:
        if c.startswith('icon-'):
            i = c.rfind('_')
            if i == -1:
                return None
            return c[i+1:]
    return None

    
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
    
    def __init__(self, title, text, image, url, date, tags, label, type, playable):
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
        i = url.rfind('.')
        if i != -1:
            j = url.rfind('/')
            if j != -1:
                self.contentName = url[j+1:i]
                
    def __str__(self):
        return "<Teaser '%s' url='%s'>" % (self.title, self.url)
        