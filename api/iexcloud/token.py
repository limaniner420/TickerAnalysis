import configparser
import os

# Reads the config.cfg at root of project for token.

def get_token():
    config = configparser.ConfigParser()
    config.read_file(open(os.path.join(os.getcwd(), "config.cfg")))
    return config.get('token', 'token')