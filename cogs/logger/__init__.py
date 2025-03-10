import logging
from logging.handlers import TimedRotatingFileHandler

from cogs.logger.logger import Logger

msg_logger = logging.getLogger("messages")
msg_logger.setLevel(logging.INFO)
msg_handler = TimedRotatingFileHandler(
    filename="servers/logs/L", when="midnight",
    interval=1, encoding='utf-8', backupCount=31
    )
msg_handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s'))
msg_handler.suffix = "%d.%m.%Y.log"
msg_logger.addHandler(msg_handler)

logging.addLevelName(21, "MSG")
logging.addLevelName(22, "REACT")
logging.addLevelName(23, "EDIT")
logging.addLevelName(24, "DEL")
logging.addLevelName(25, "COMM")


disnake_logger = logging.getLogger("disnake")
disnake_logger.setLevel(logging.INFO)
disnake_handler = logging.FileHandler(filename='disnake.log', encoding='utf-8', mode='w')
disnake_handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s'))
disnake_logger.addHandler(disnake_handler)


def setup(bot):
    bot.add_cog(Logger(bot, msg_logger))


def teardown(_):
    msg_logger.removeHandler(msg_handler)
    msg_handler.close()
