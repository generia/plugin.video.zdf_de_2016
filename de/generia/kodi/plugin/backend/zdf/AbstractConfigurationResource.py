from de.generia.kodi.plugin.backend.web.HtmlResource import HtmlResource
from de.generia.kodi.plugin.backend.zdf.Regex import compile

apiTokenPattern = compile('<head>.*window.zdfsite\s*=\s*{.*apiToken:\s*\'([^\']*)\'.*</head>')

class AbstractConfigurationResource(HtmlResource):

    def __init__(self, url):
        super(AbstractConfigurationResource, self).__init__(url)
            
    def parse(self):
        super(AbstractConfigurationResource, self).parse()

        self.configApiToken = None
        pos = 0
        apiTokenMatch = apiTokenPattern.search(self.content, pos)
        if apiTokenMatch is not None:
            self.configApiToken = apiTokenMatch.group(1)
            pos = apiTokenMatch.end(0)
            self.content = self.content[pos:len(self.content)]


        
        