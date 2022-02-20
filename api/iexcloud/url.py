from . import token

def get_URLbase(mode: str = "sandbox", ver: str = "stable"):
    return "https://" + mode + ".iexapis.com/" + ver

def get_URLtoken():
    return "?token=" + token.get_token()

def compose_URL(mid: str = "", end: str = "", mode: str = "sandbox", ver: str = "stable"):
    if mid == None and end == None:
        return None
    return get_URLbase(mode, ver) + mid + end + get_URLtoken()