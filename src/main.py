from urllib.request import Request, urlopen
from htmlparsers import MagicSpoilerParser
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from random import randint
import os
import time


SPOILERS_WEB = "http://www.magicspoiler.com/mtg-set/modern-horizons/"
CACHE_PATH = "/usr/local/etc/mtg_spoiler_cache.txt"


def get_cards():
    rq = Request(SPOILERS_WEB, headers={'User-Agent' : "Mozilla/5.0"})
    with urlopen(rq) as web:
        html = web.read().decode("utf-8")

    p = MagicSpoilerParser()
    p.feed(html)
    return p.cards


def load_cache(cache):
    with open(CACHE_PATH, 'r') as fin:
        for line in fin:
            cache.add(line)


def write_new_values_to_cache(values):
    with open(CACHE_PATH, 'a') as fout:
        for value in values:
            fout.write(value+"\n")


def notify(bot, card):
    button = InlineKeyboardButton("Open in browser", url=card['link'])
    markup = InlineKeyboardMarkup([[button]])
    bot.send_photo(os.environ['TELEGRAM_CHAT'], card['img'], reply_markup=markup)


if __name__ == '__main__':
    bot = Bot(os.environ['BOT_TOKEN'])
    cache = set()
    load_cache(cache)
    new_values = []
    while True:
        cards = get_cards()
        for card in cards:
            if card['link'] not in cache:
                cache.add(card['link'])
                new_values.append(card['link'])
                notify(bot, card)
        write_new_values_to_cache(new_values)
        new_values = []
        time.sleep(10 * 60 + randint(-120, 120))
