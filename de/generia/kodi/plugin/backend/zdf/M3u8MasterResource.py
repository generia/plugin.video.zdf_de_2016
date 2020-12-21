from de.generia.kodi.plugin.backend.web.Resource import Resource
from de.generia.kodi.plugin.backend.zdf.Regex import compile

bandwidthPattern = compile('BANDWIDTH=([^,]*),')

class M3u8MasterResource(Resource):

    def __init__(self, url, accept='application/vnd.apple.mpegurl'):
        super(M3u8MasterResource, self).__init__(url, accept)
        self.programMap = dict()
        
    def parse(self):
        super(M3u8MasterResource, self).parse()
        lines = self.content.split("\n")
        i = 0
        bandwith = None
        for line in lines:
            line = line.strip()
            if line.startswith("#"):
                if line.startswith("#EXT-X-STREAM-INF:"):
                    match = bandwidthPattern.search(line)
                    if match is not None:
                        bandwith = int(match.group(1))
            elif line != "":
                streamUrl = line
                if bandwith is not None:
                    self.programMap[bandwith] = streamUrl

    def getBestStreamUrl(self):
        maxBandwidth = -1
        for bandwidth in self.programMap.keys():
            if bandwidth > maxBandwidth:
                maxBandwidth = bandwidth
        if maxBandwidth != -1:
            return self.programMap[maxBandwidth]
        return None