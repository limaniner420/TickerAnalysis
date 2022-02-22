import requests as req
from . import url

def quote(ticker: str, mode: str = "sandbox", ver: str = "stable"):
    """ 
    :ticker: Ticker symbol of listed securities on NA exchanges.
    :mode: Specify whether to access sandbox ("sandbox") data or real ("cloud") data. Polling real data may incur charges. Default sandbox.
    :ver: Specify api version. Default stable.
    """

    url_final = url.compose_URL("/stock/{0}/quote".format(ticker), mode = mode, ver = ver)
    r = req.get(url = url_final)

    r.raise_for_status()
    return r.json()

def hist_price(ticker: str, period: str, mode: str = "sandbox", ver: str = "stable"):
    """ 
    :ticker: Ticker symbol of listed securities on NA exchanges.
    :period: Desired range of data.
    :mode: Specify whether to access sandbox ("sandbox") data or real ("cloud") data. Polling real data may incur charges. Default sandbox.
    :ver: Specify api version. Default stable.
    """
    
    url_final = url.compose_URL("/stock/{0}/chart/{1}".format(ticker, period), mode = mode, ver = ver)
    r = req.get(url = url_final, params = {"chartCloseOnly": True})

    r.raise_for_status()
    return r.json()