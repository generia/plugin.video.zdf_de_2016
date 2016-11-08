from de.generia.kodi.plugin.backend.web.HtmlResource import HtmlResource


class Rubric(object):

    def __init__(self, title, url):
        self.title = title
        self.url = url
                        
    def __str__(self):
        return "<Rubric '%s' url='%s'>" % (self.title, self.url)
    
    
class NavigationResource(HtmlResource):

    def __init__(self, url):
        super(NavigationResource, self).__init__(url)
            
    def parse(self):
        super(NavigationResource, self).parse()
        topBar = self.content.find('nav', class_='top-bar-section')
        leftNav = topBar.find('ul', class_='left-nav')
        dropdownList = leftNav.find('ul', class_='dropdown-list')
        dropdownLinks = dropdownList.find_all('a', class_='dropdown-link')

        self.rubrics = []
        for dropdownLink in dropdownLinks:
            rubric = self._parseDropdownLink(dropdownLink)
            if rubric is not None:
                self.rubrics.append(rubric)

    def _parseDropdownLink(self, dropdownLink):
        title = dropdownLink.get('data-title');
        if title is not None:
            title = title.strip()
        else:
            return None
        url = dropdownLink.get('href');
        if url is not None:
            url = url.strip()
        else:
            return None

        return Rubric(title, url)
