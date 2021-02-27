from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import logging


class Magicspoiler:

    LINKS = [
        'http://www.magicspoiler.com/mtg-set/time-spiral-remastered/',
        'http://www.magicspoiler.com/mtg-set/strixhaven/'
    ]

    PAGE_SUFFIX = "page/{0}"

    def __init__(self):
        pass

    def get_new_cards(self, already_known_cards):
        return []

    def get_all_cards(self):
        cards = []
        for link in Magicspoiler.LINKS:
            cards.extend(self.__get_all_cards_from_link(link))
        return cards

    def __get_all_cards_from_link(self, link):
        total_cards = []
        page = 1
        cards = self.__get_all_cards_from_page(link, page)
        total_cards.extend(cards)
        while cards:
            cards = self.__get_all_cards_from_page(link, page)
            total_cards.extend(cards)
            page += 1
        return total_cards

    def __get_all_cards_from_page(self, link, page_number):
        try:
            code, html = self.__get_html(link, page_number)
        except HTTPError:
            return []
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
        self.cards = []
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
            self.cards.append(self.__current_card)
            self.__current_card = {}

    def handle_data(self, data):
        pass


if __name__ == '__main__':
   cards = Magicspoiler().get_all_cards()
   a = 1

