import os
from configparser import ConfigParser

parser = ConfigParser()

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
parser.read(ROOT_PATH + "/config.ini")

CARD_MAKER_CONFIG = dict(parser.items("CARDMAKER_CONF"))
SPREADSHEET_CONF = dict(parser.items("EXCEL_CONF"))
