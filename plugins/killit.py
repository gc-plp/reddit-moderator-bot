from modbot import hook
from praw.models import Message
import logging
import os
import time
import signal

logger = logging.getLogger("plugin")
selfkill_int = 60 * 60 *6

def kill_me():
    os.kill(os.getpid(), signal.SIGTERM)

@hook.periodic(first="5", period="10")
def check_inbox(bot, reddit):

    reset_body = bot.config["reset"]["body"]
    reset_authors = bot.config["reset"]["authors"].replace(" ", "").split(",")

    for item in reddit.inbox.unread(limit=None):
        item.mark_read()
        if isinstance(item, Message):
            logger.info("Got message from %s: %s/%s" % (item.author, item.subject, item.body))

            if item.body == reset_body and item.author in reset_authors:
                logger.info("Exiting")
                kill_me()


@hook.periodic(first=str(selfkill_int))
def killself(bot, reddit):
    while len(bot.plugin_threads) > 1:
        time.sleep(0.1)
        logger.debug("Killing. Waiting for %d threads" % len(bot.plugin_threads))
    kill_me()
