from feeds.mythicspoiler import Mythicspoiler
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from urllib.parse import quote
import logging
import os
import time
import datetime


logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s',
                    level=os.environ.get("LOG_LEVEL", logging.INFO))


def notify(bot, card, disable_notifications):
    card_link = quote(card.link, safe='/?:')
    card_img = quote(card.img, safe='/?:')

    button = InlineKeyboardButton("Open in browser", url=card_link)
    markup = InlineKeyboardMarkup([[button]])
    bot.send_photo(os.environ['TELEGRAM_CHAT'], card_img, reply_markup=markup, disable_notification=disable_notifications)


if __name__ == '__main__':
    logging.info("Starting!")
    telegram_bot = Bot(os.environ['BOT_TOKEN'])
    feed = Mythicspoiler()
    actual_cards = feed.get_all_cards()
    cache = {card.link for card in actual_cards}
    logging.info("Cache filled with actual data. Waiting for next iteration")
    time.sleep(15 * 60)
    while True:
        logging.info("Starting new iteration")
        new_cards = feed.get_new_cards(cache)
        current_hour = datetime.datetime.now().hour
        disable_notifications = current_hour < 8 or current_hour > 22
        for card in new_cards:
            logging.info("New card:" + card.link + " - " + card.img)
            cache.add(card.link)
            notify(telegram_bot, card, disable_notifications)
        logging.info("Iteration finished")
        time.sleep(15 * 60)
