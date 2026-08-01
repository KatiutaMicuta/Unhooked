from src.email_analyzer import email_domain, urgent_language, link_mismatch, extract_links, email_analysis

def test_email_domain():
    assert email_domain("user@example.com") == "example.com"


def test_email_domain_returns_none_withoutanatsign():
    assert email_domain("notanemail") is None


def test_urgent_language():
    assert urgent_language("Your account will be suspended")


def test_urgent_language_safe():
    assert not urgent_language("Hi, are we still meeting tommorow?")


def test_urgent_language():
    assert urgent_language("URGENT: act now")


def test_link_mismatch():
    assert link_mismatch("paypal.com", "http://evil.ru")


def test_link_mismatch_goodlink():
    assert not link_mismatch("bbc.co.uk", "https://bbc.co.uk/news")


def test_link_mismatch_hasnodomain():
    assert not link_mismatch("Click here", "http://evil.ru")


def test_extract_links():
    assert extract_links('<a href="http://a.ru">one.com</a><a href="http://b.ru">two.com</a>') == [("one.com", "http://a.ru"), ("two.com", "http://b.ru")]


def test_extract_links_nolinks():
    assert extract_links('<p> no links here </p>') == []


def test_email_analysis():
    result = email_analysis("billing@secure-login.ru", '<p>URGENT: <a href="http://evil.ru">paypal.com</a></p>')
    assert result["score"] == 1.5


def test_email_analysis_safeemail():
    result = email_analysis("news@bbc.co.uk", '<a href="https://bbc.co.uk/news">bbc.co.uk</a>')
    assert result["score"] == 0


def test_link_mismatch_handlesmissinghref():
    assert not link_mismatch("paypal.com", None)


def test_email_analysis_handleslinkwithouthref():
    result = email_analysis("a@b.com", '<a>paypal.com</a>')
    assert result["score"] == 0