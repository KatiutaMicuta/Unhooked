from src.url_analyzer import has_many_hyphens
from src.url_analyzer import uses_ip_address
from src.url_analyzer import has_many_subdomains
import tldextract
from bs4 import BeautifulSoup

def email_domain(email):

    if "@" not in email:
        return None
    
    domain = email.split("@")[-1]
    return domain

def email_analysis(email, html):

    domain = email_domain(email)

    if domain is None:
        return False

    text = BeautifulSoup(html, "html.parser").get_text()

    score = 0 
    reasons = []

    if uses_ip_address(domain):
        reasons.append("The sender's address sits on a bare IP instead of a real domain name. ")
        score += 1

    if has_many_subdomains(domain):
        reasons.append("The sender domain has extra labels to look more trustworthy.")
        score += 1

    if has_many_hyphens(domain):
        reasons.append("Falsified sender identity by adding keywords between dashes.")
        score += 1

    if urgent_language(text):
        reasons.append("The email contains fear-mongering language.")
        score += 0.5

    if any(link_mismatch(link_text, href) for link_text, href in extract_links(html)):
        reasons.append("A link's visible text points to a different domain than its real destination.")
        score += 1

    return {
        "email" : email, 
        "score" : score,
        "reasons" : reasons,
    }

def urgent_language(text):


    if text is None:
        return False

    keywords = [
    "urgent",
    "immediately",
    "act now",
    "verify your account",
    "suspended",
    "unauthorized",
    "confirm your identity",
    "limited time",
    "update your details",
    "failure to respond",
    "within 24 hours",
    "your account will be",
    "security alert",
    "unusual activity",
]
    text = text.lower()
    return any(phrase in text for phrase in keywords)

def link_mismatch(display_text, href):

    display_text = tldextract.extract(display_text).registered_domain

    if display_text == "":
        return False
    
    href = tldextract.extract(href).registered_domain
    return display_text != href
    

def extract_links(html):

    soup = BeautifulSoup(html, "html.parser")

    pairs = []
    for tag in soup.find_all("a"):
        links_text = tag.get_text()
        href = tag.get("href")

        pairs.append((links_text, href))
    return pairs
