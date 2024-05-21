import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

CONF = {
    'USER': os.getenv('USER'),
    'PASSWORD': os.getenv('PASSWORD'),
    'HOST': os.getenv('HOST'),
    'DBNAME': os.getenv('DBNAME'),
    'DEBUG': bool(os.getenv('DEBUG')),

    'APP_NAME': os.getenv('APP_NAME'),
    'API_ID': os.getenv('API_ID'),
    'API_HASH': os.getenv('API_HASH'),
    'BOT_TOKEN': os.getenv('BOT_TOKEN'),


    'WORDS': set(word.strip() for word in os.getenv('WORDS').split(', ')),
}
