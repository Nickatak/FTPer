import pathlib

from bot.types import Path


BASE_DIR: Path = pathlib.Path(__file__).parent
DOMAIN_NAME: str = 'localhost:5000'
TEMPLATE_DIR: Path = BASE_DIR.joinpath('templates')
UPLOAD_DIR: Path = BASE_DIR.joinpath('downloads')
# Discord settings.
BOT_IDENTIFIER: str = '!'
DISC_TOKEN: str = 'Nzc5NDk0NTU3ODU4NTI5MzAw.X7hW4A.3C2HkLi4QTEcupKZzfnowK553AY'

#DB Settings.
DB_URL: str = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='Nickatak',pw='root',url='localhost',db='discbot')

