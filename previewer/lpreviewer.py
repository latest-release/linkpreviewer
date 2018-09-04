import urllib.request
from bs4 import BeautifulSoup
try:
    import simplejson as json
except ImportError:
    import json 
    
def retrieve_webpage(url, headers=None):
    """
    @ url domain we want to retrieve
    """
    try:
        html = None 
        if not url:
            raise ValueError("Expecetd url got none instead")
        
        if url.startswith("www."):
            # Include protocol
            url = "http://" + url 
        with urllib.request.urlopen(url) as response:
            html = response.read()
        
        return html 
    except Exception as e:
        raise 
        
def parse_webpage(html_content=None, url=None, default_parser="html.parser", prettify=False):
    """
    @ html_content: The content we downloaded that we want to parse.
    @ url: If the content is none, we should be given url to download.
    @ default_parser
    """
    def get_favicon(soup):
        """
        @ soup--> Beautiful soup object.
        """
        favicon_link = page_soup.find_all('link', rel="shortcut icon")
        if not favicon_link:
            favicon_link = page_soup.find_all('link', rel="Shortcut Icon")
        
        if not favicon_link:
            favicon_link = page_soup.find_all('link', rel="SHORTCUT ICON")
            
        if not favicon_link:
            favicon_link = page_soup.find_all('link', rel="icon")
            
        #if not favicon_img:
        favicon_img = page_soup.find_all('img')
        if(favicon_img):
            img = favicon_img[0]
            return img.get('src')
            
        if favicon_link:
            return favicon_link[0].get("href")
    
    def replace_trailing(s):
        if s[-1]=='/':
            return (s[:-1])
        else:
            return s
        
    def search_description(soup):
        """
        We want to search for page description.
        """
        meta = page_soup.find_all("meta", property="og:description")
        if meta:
            return meta[0].get("content")
        
    try:
        if not html_content and not url:
            raise ValueError("html_content is None and url is None, pass any of them")
            
        if not html_content:
            html_content = retrieve_webpage(url)
        
        page_soup = BeautifulSoup(html_content, default_parser)
        
        if prettify:
            return page_soup.prettify()
        
        title = page_soup.title.string
        favicon = get_favicon(page_soup)
        if favicon:
            if(favicon.startswith("/")):
                favicon = replace_trailing(url) + favicon
        description = search_description(page_soup)
        
        # Return dictionary
        return {"title":title, "favicon":favicon, "description":description}
    except Exception as e:
        raise 

if __name__=="__main__":
    
    url = "https://www.nytimes.com/2018/05/07/nyregion/new-york-attorney-general-eric-schneiderman-abuse.html"
    content = parse_webpage(None, url=url, prettify=False)
    print(content)
