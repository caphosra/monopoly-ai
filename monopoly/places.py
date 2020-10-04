import pandas as pd
from typing import List

class PlaceInfo:
    def __init__(self, name: str, kind: int, house: int, prices: List[int]):
        self.name = name
        self.kind = kind
        self.house = house
        self.prices = prices

#
# Load all of the infos about places.
#
def load() -> List[PlaceInfo]:#):
    data = pd.read_excel("./data/Data.xlsx", "PlaceData")

    places = []

    for place in data.values:
        content = PlaceInfo(place[0], place[1], place[2], place[3:])
        places.append(content)

    return places

class PlaceStatus:
    def __init__(self, info: PlaceInfo, player: int, house: int):
        self.info = info
        self.player = player
        self.house = house

    def get_price(self, monopolied: bool) -> int:#):
        price = self.info.prices[self.house]
        if (monopolied and self.house == 0):
            price = price * 2
        return price
