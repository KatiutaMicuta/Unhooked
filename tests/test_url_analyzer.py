from src.url_analyzer import uses_ip_address, has_many_subdomains, has_many_hyphens, url_analysis, has_userinfo

def test_uses_ip_address():
    assert uses_ip_address("192.168.1.1")


def test_uses_ip_address_ignoresnormaldomain():
    assert not uses_ip_address("bbc.co.uk")


def test_url_analysis_scoresphishurl():
    result = url_analysis("http://www.paypal.com@account.update.paypal.com.secure-login.ru/verify")
    assert result["score"] == 2


def test_url_analysis_scoresnormalurl():
    result = url_analysis("https://www.bbc.co.uk/news")
    assert result["score"] == 0


def test_has_many_subdomains():
    assert has_many_subdomains("account.update.paypal.com.secure-login.ru")


def test_has_many_subdomains_not():
    assert not has_many_subdomains("bbc.co.uk")


def test_has_many_hyphens():
    assert has_many_hyphens("paypal-account-verify-secure.com")


def test_has_many_hyphens_not():
    assert not has_many_hyphens("s3.eu-west-2.amazonaws.com")


def test_has_userinfo():
    assert has_userinfo("http://www.paypal.com@secure-login.ru/verify")


def test_has_userinfo_not():
    assert not has_userinfo("https://example.com/contact?email=alice@example.com")