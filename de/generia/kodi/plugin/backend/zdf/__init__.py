
def stripHtml(html):
    if html is None:
        return None
    text = html
    text = text.replace("&amp;", "&")
    text = text.replace("&quot;", "\"")
    text = text.replace("&apos;", "'")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    return text.strip()