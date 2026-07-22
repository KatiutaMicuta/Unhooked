from urllib.parse import urlparse

#chechking if the url is an IP address
def uses_ip_address(url):

    host = urlparse(url).hostname
    if host is None: 
        return False  
    
    parts = host.split(".")
    
    return len(parts) == 4 and all(part.isdigit() for part in parts)

def has_userinfo(url):

    netloc = urlparse(url).netloc
    
    return "@" in netloc