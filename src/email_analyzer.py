from src.url_analyzer import has_many_hyphens
from src.url_analyzer import uses_ip_address


def email_domain(email):

    if "@" not in email:
        return None
    
    domain = email.split("@")[-1]
    return domain