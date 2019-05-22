from html.parser import  HTMLParser
import logging

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

    def handle_endtag(self, tag):
        if tag == 'div' and self.__is_parsing_card:
            self.__is_parsing_card = False
            self.cards.append(self.__current_card)
            self.__current_card = {}

    def handle_data(self, data):
        pass
