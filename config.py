import os
from configparser import ConfigParser

parser = ConfigParser()
parser.read("config.ini")

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
CARD_MAKER_CONFIG = dict(parser.items("CARDMAKER_CONF"))
SPREADSHEET_CONF = dict(parser.items("EXCEL_CONF"))
