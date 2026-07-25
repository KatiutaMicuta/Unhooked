from src.url_analyzer import has_many_hyphens
from src.url_analyzer import uses_ip_address
from src.url_analyzer import has_many_subdomains

def email_domain(email):

    if "@" not in email:
        return None
    
    domain = email.split("@")[-1]
    return domain

def email_analysis(email):

    domain = email_domain(email)

    if domain is None:
        return False

    reasons = []

    if uses_ip_address(domain):
        reasons.append("The sender's address sits on a bare IP instead of a real domain name. ")

    if has_many_subdomains(domain):
        reasons.append("The sender domain has extra labels to look more trustworthy.")

    if has_many_hyphens(domain):
        reasons.append("Falsified sender identity by adding keywords between dashes.")

    score = len(reasons)
    return {
        "email" : email, 
        "score" : score,
        "reasons" : reasons,
    }
