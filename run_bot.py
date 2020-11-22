from bot import Bot
from conf import BOT_IDENTIFIER, DISC_TOKEN

client: Bot = Bot(BOT_IDENTIFIER)
client.run(DISC_TOKEN)
