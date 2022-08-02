import configparser

config = configparser.ConfigParser()
config.read('config.ini')

WALLET_PASSWORD = 'hellooooooo'
WALLET_NAME = 'hellooooooo'

COMPUTER_NAME = config['PLAYER']['COMPUTER_NAME']
LIST_DEVICE = config['PLAYER']['LIST_DEVICE']

SEED_PATH = config['AUTO']['SEED_PATH']

TELEGRAM_TOKEN = '5397582148:AAF6UAF04rrSxWLRG0AxOHTDsJii1AL9rgY'
TELEGRAM_CHAT_ID = '-580836594'
