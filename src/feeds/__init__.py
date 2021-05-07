from dataclasses import dataclass


@dataclass(order=True, frozen=True)
class Card:
    name: str = ""
    link: str = ""
    img: str = ""
