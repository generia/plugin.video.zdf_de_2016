from __builtin__ import type

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
        