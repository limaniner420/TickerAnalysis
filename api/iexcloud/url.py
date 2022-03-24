from . import token

def get_URLbase(mode: str = "sandbox", ver: str = "stable"):
    return "https://" + mode + ".iexapis.com/" + ver

def get_URLtoken(mode: str = "sandbox"):
    return "?token=" + token.get_token(mode)

def compose_URL(mid: str = "", mode: str = "sandbox", ver: str = "stable"):
    """ 
    mid: Endpoint with parameters.
    mode: Specify whether to access sandbox ("sandbox") data or real ("cloud") data. Real data may incur charges. Default sandbox.
    ver: Specify api version. Default stable.
    """
    return get_URLbase(mode, ver) + mid + get_URLtoken(mode)