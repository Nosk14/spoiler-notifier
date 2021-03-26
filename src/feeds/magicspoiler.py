from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from dataclasses import dataclass
import logging


class Magicspoiler:

    LINKS = [
        'http://www.magicspoiler.com/mtg-set/strixhaven/'
    ]

    PAGE_SUFFIX = "page/{0}"

    def __init__(self):
        pass

    def get_new_cards(self, already_known_cards):
        all_cards = self.get_all_cards()
        return {c for c in all_cards if c.link not in already_known_cards}

    def get_all_cards(self):
        cards = set()
        for link in Magicspoiler.LINKS:
            cards.update(self.__get_all_cards_from_link(link))
        return cards

    def __get_all_cards_from_link(self, link):
        total_cards = set()
        page = 1
        cards = self.__get_all_cards_from_page(link, page)
        total_cards.update(cards)
        while len(cards) > 0:
            cards = self.__get_all_cards_from_page(link, page)
            total_cards.update(cards)
            page += 1
        return total_cards

    def __get_all_cards_from_page(self, link, page_number):
        try:
            code, html = self.__get_html(link, page_number)
        except HTTPError:
            return set()
        parser = MagicSpoilerParser()
        parser.feed(html)
        return parser.cards

    def __get_html(self, link, page_number):
        url = link + Magicspoiler.PAGE_SUFFIX.format(page_number)
        rq = Request(url, headers={'User-Agent': "Mozilla/5.0"})
        with urlopen(rq) as web:
            return web.getcode(), web.read().decode("utf-8")


class MagicSpoilerParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.__is_parsing_card = False
        self.cards = set()
        self.__current_card = {}

    def error(self, message):
        logging.error(message)

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and len(list(filter(lambda att: att[1] == 'spoiler-set-card', attrs))) > 0:
            self.__is_parsing_card = True
        elif self.__is_parsing_card and tag == 'a':
            self.__current_card['link'] = list(filter(lambda att: att[0] == 'href', attrs))[0][1]
        elif self.__is_parsing_card and tag == 'img':
            self.__current_card['img'] = list(filter(lambda att: att[0] == 'src', attrs))[0][1]
            self.__current_card['name'] = list(filter(lambda att: att[0] == 'alt', attrs))[0][1]

    def handle_endtag(self, tag):
        if tag == 'div' and self.__is_parsing_card:
            self.__is_parsing_card = False
            self.cards.add(Card(**self.__current_card))
            self.__current_card = {}

    def handle_data(self, data):
        pass


@dataclass(order=True, frozen=True)
class Card:
    name: str = ""
    link: str = ""
    img: str = ""


if __name__ == '__main__':
    m = Magicspoiler()
    new_cards = m.get_new_cards([])
    l = list(new_cards)
    l.sort()
    a = 1
