import configparser
import os

# Reads the config.cfg at root of project for token.

def get_token(mode: str = "sandbox"):
    """ 
    Reads token from config.cfg at root directory of project.
    """
    config = configparser.ConfigParser()
    config.read_file(open(os.path.join(os.getcwd(), "config.cfg")))
    return config.get('token', 'token_IEX_sandbox') if mode == "sandbox" else config.get('token', 'token_IEX_prod')