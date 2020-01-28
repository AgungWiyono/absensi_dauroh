from configparser import ConfigParser

parser = ConfigParser()
parser.read("config.ini")

CARD_MAKER_CONFIG = dict(parser.items("CARDMAKER_CONF"))
