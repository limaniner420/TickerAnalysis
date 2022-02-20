import requests as req
from . import url

def quote(ticker: str, mode: str = "sandbox", ver: str = "stable"):

    url_final = url.compose_URL("/stock/{0}/quote".format(ticker))
    r = req.get(url = url_final)

    r.raise_for_status()
    return r.json()
            
def hist_price(ticker: str, period: str, mode: str = "sandbox", ver: str = "stable"):

    url_final = url.compose_URL("/stock/{0}/chart/{1}".format(ticker, period), mode = mode, ver = ver)
    r = req.get(url = url_final, params = {"chartCloseOnly": True})

    r.raise_for_status()
    return r.json()