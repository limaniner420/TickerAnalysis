import requests as req
from . import url


def quote(symbol: str, mode: str = "sandbox", ver: str = "stable"):
    """ 
    symbol: Symbol of listed securities on NA exchanges.
    mode: Specify whether to access sandbox ("sandbox") data or real ("cloud") data. Polling real data may incur charges. Default sandbox.
    ver: Specify api version. Default stable.
    """

    url_final = url.compose_URL("/stock/{0}/quote".format(symbol), mode = mode, ver = ver)
    r = req.get(url = url_final)

    r.raise_for_status()
    return r.json()

def hist_price(symbol: str, range: str, mode: str = "sandbox", ver: str = "stable"):
    """ 
    symbol: Symbol of listed securities on NA exchanges.
    range: Desired range of data in calendar days.
    mode: Specify whether to access sandbox ("sandbox") data or real ("cloud") data. Polling real data may incur charges. Default sandbox.
    ver: Specify api version. Default stable.
    """
    
    url_final = url.compose_URL("/stock/{0}/chart/{1}".format(symbol, range), mode = mode, ver = ver)
    r = req.get(url = url_final, params = {"chartCloseOnly": True})

    r.raise_for_status()
    return r.json()

def batch(symbols: list[str], types: list[str], range: str = None, params_ex: dict[str] = None, mode: str = "sandbox", ver: str = "stable"):

    """ 
    symbols: List of symbols of listed securities on NA exchanges.
    types: List of endpoints to be queried.
    range: Desired range of data in calendar days. Only applicable if chart is specified in types). Optional.
    params_ex: list of applicable parameters for each endpoint. Optional.
    mode: Specify whether to access sandbox ("sandbox") data or real ("cloud") data. Polling real data may incur charges. Default sandbox.
    ver: Specify api version. Default stable.
    """
    symbols_str = ','.join(symbols)
    types_str = ','.join(types)
    
    url_final = url.compose_URL("/stock/market/batch", mode = mode, ver = ver)
    
    params_dict = {
        "symbols"   : symbols_str,
        "types"     : types_str,
    }
    if("chart" in types and range != None):
        params_dict["range"] = range
    if(params_ex != None):
        params_dict.update(params_ex)

    r = req.get(url = url_final, params = params_dict)

    r.raise_for_status()
    return r.json()