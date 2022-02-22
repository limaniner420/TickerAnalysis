from . import token

def get_URLbase(mode: str = "sandbox", ver: str = "stable"):
    return "https://" + mode + ".iexapis.com/" + ver

def get_URLtoken():
    return "?token=" + token.get_token()

def compose_URL(mid: str = "", mode: str = "sandbox", ver: str = "stable"):
    """ 
    :ticker: Ticker symbol of listed securities on NA exchanges.
    :period: Desired range of data.
    :mode: Specify whether to access sandbox ("sandbox") data or real ("cloud") data. Real data may incur charges. Default sandbox.
    :ver: Specify api version. Default stable.
    """
    return get_URLbase(mode, ver) + mid + get_URLtoken()