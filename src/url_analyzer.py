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

#see how many - are there IN THE SUBDOMAIN LABELS
def has_many_hyphens(url):
    host = urlparse(url).hostname
    if host is None:
        return False
    
    parts = 

#giving the user a rundown of the URL issues (if any)    
def url_analysis(url):

    reasons = []

    if uses_ip_address(url):
        reasons.append("Uses a raw IP address instead of a domain name.")

    if has_userinfo(url):
        reasons.append("The link is hiding the real destination behind a '@'.")

    if has_many_subdomains(url):
        reasons.append("The URL has a suspicious amount of subdomains.")

    score = len(reasons)
    return {
        "url" : url, 
        "score" : score,
        "reasons" : reasons,
    }
