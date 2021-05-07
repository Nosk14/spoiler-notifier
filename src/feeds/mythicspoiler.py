from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from feeds import Card
import logging


class Mythicspoiler:

    LINKS = [
        'http://mythicspoiler.com/newspoilers.html'
    ]

    BASE_URL = 'http://mythicspoiler.com/'

    def __init__(self):
        pass

    def get_new_cards(self, already_known_cards):
        all_cards = self.get_all_cards()
        return {c for c in all_cards if c.link not in already_known_cards}

    def get_all_cards(self):
        cards = set()
        for link in Mythicspoiler.LINKS:
            cards.update(self.__get_all_cards_from_link(link))
        return cards

    def __get_all_cards_from_link(self, link):
        try:
            code, html = self.__get_html(link,)
        except HTTPError:
            return set()
        parser = MythicspoilerParser()
        parser.feed(html)
        return parser.cards

    def __get_html(self, link):
        rq = Request(link, headers={'User-Agent': "Mozilla/5.0"})
        with urlopen(rq) as web:
            return web.getcode(), web.read().decode("utf-8")


class MythicspoilerParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.__is_parsing_card = False
        self.cards = set()
        self.__current_card = {'name': ''}

    def error(self, message):
        logging.error(message)

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and ('class', 'grid-card') in attrs:
            self.__is_parsing_card = True
        elif self.__is_parsing_card and tag == 'a':
            self.__current_card['link'] = Mythicspoiler.BASE_URL + list(filter(lambda att: att[0] == 'href', attrs))[0][1].strip()
        elif self.__is_parsing_card and tag == 'img':
            self.__current_card['img'] = Mythicspoiler.BASE_URL + list(filter(lambda att: att[0] == 'src', attrs))[0][1].strip()

    def handle_endtag(self, tag):
        if tag == 'a' and self.__is_parsing_card:
            self.__is_parsing_card = False
            self.cards.add(Card(**self.__current_card))
            self.__current_card = {'name': ''}

    def handle_data(self, data):
        pass


if __name__ == '__main__':
    m = Mythicspoiler()
    new_cards = m.get_new_cards([])
    l = list(new_cards)
    l.sort()
    a = 1
