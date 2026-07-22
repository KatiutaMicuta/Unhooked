from urllib.parse import urlparse

#checking if the url is an IP address
def uses_ip_address(url):

    host = urlparse(url).hostname
    if host is None: 
        return False  
    
    parts = host.split(".")
    
    return len(parts) == 4 and all(part.isdigit() for part in parts)

#checking if the URL is hiding the real destination behind @
def has_userinfo(url):

    netloc = urlparse(url).netloc
    return "@" in netloc

#if URL has more than 4 subdomains it's usually suspicious
def has_many_subdomains(url):
    
    host = urlparse(url).hostname
    if host is None:
        return False
    
    parts = host.split(".")
    return len(parts) > 4
    
