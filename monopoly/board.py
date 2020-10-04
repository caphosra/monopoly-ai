import numpy as np
from typing import List
import random

from monopoly import placekind
from monopoly import places

class MonopolyBoard:
    def __init__(self, player: int, do_log = True):
        self.place_infos: List[places.PlaceStatus] = []

        for info in places.load():
            self.place_infos.append(places.PlaceStatus(info, 1, 3))

        self.assets: List[int] = [];
        self.player_place: List[int] = [];
        for count in range(player):
            self.assets.append(1500)
            self.player_place.append(0)

        self.turn = -1
        self.do_log = do_log

    def log(self, text):
        if self.do_log:
            print(text)

    def cycle(self):
        for i in range(len(self.player_place)):
            self.dice()

    def dice(self, double: int = 0):
        if double == 0:
            self.turn = (self.turn + 1) % len(self.player_place)

        place_kind = self.place_infos[self.player_place[self.turn]].info.kind

        num1 = random.randint(1, 6)
        num2 = random.randint(1, 6)

        # When the player was jailed
        if place_kind == placekind.JAIL:
            if num1 == num2:
                self.player_place[self.turn] = 11 + num1 + num2
                self.log(f"Player{self.turn} is now released")
                self.log(f"Player{self.turn} moves to {self.place_infos[self.player_place[self.turn]].info.name}")
            else:
                self.player_place[self.turn] = 41
                self.log(f"Player{self.turn} spends 1 turn in the jail")
            return
        if place_kind == placekind.JAIL2:
            if num1 == num2:
                self.player_place[self.turn] = 11 + num1 + num2
                self.log(f"Player{self.turn} is now released")
                self.log(f"Player{self.turn} moves to {self.place_infos[self.player_place[self.turn]].info.name}")
            else:
                self.player_place[self.turn] = 42
                self.log(f"Player{self.turn} spends 2 turn in the jail")
            return
        if place_kind == placekind.JAIL3:
            self.log(f"Player{self.turn} is now released")
            self.player_place[self.turn] = 11

        self.player_place[self.turn] = self.player_place[self.turn] + num1 + num2

        # When the player passes GO
        if self.player_place[self.turn] >= 40:
            self.log(f"Player{self.turn} gets $200 for passing GO")
            self.assets[self.turn] = self.assets[self.turn] + 200
            self.player_place[self.turn] = self.player_place[self.turn] % 40

        self.log(f"Player{self.turn} moves to {self.place_infos[self.player_place[self.turn]].info.name}")

        place_kind = self.place_infos[self.player_place[self.turn]].info.kind

        # When the player lands Go To Jail
        if place_kind == placekind.GOTOJAIL:
            self.log(f"Player{self.turn}, you are jailed!")
            self.player_place[self.turn] = 40
            return

        # When the player lands the other player's place
        if 1 <= place_kind <= 8:
            info = self.place_infos[self.player_place[self.turn]]
            self.assets[self.turn] = self.assets[self.turn] - info.get_price(True)
            self.assets[info.player] = self.assets[info.player] + info.get_price(True)
            self.log(f"Player{self.turn} pays ${info.get_price(True)} to Player{info.player}")

        # When doubled
        if num1 == num2:
            if double < 2:
                self.dice(double + 1)
            else:
                self.log(f"Player{self.turn}, you are jailed due to doubling three times!")
                self.player_place[self.turn] = 40

    def randomize(self) -> None:#):
        for i in range(len(self.player_place)):
            self.player_place[i] = random.randint(0, 42)

        for i in range(len(self.place_infos)):
            info = self.place_infos[i]
            info.player = random.randint(0, len(self.player_place) - 1)
            info.house = random.randint(0, 5)
            self.place_infos[i] = info

    def to_matrix(self, assets_scale) -> np.array:#):
        player_infos = []
        for player in range(len(self.player_place)):
            places = []
            for place in range(len(self.place_infos)):
                player_houses = 0.0
                if self.place_infos[place].player == player:
                    player_houses = self.place_infos[place].house / 5.0
                player_is_here = float(self.player_place[player] == place) * (self.assets[player] * assets_scale)
                places.append([player_houses, player_is_here])
            player_infos.append(places)
        return np.array(player_infos)

    def __str__(self):
        text = "----- Current status -----\n"
        for i in range(len(self.player_place)):
            text = text + f"Player{i}: ${self.assets[i]} {self.place_infos[self.player_place[i]].info.name}\n"
        text = text + "--------------------------"
        return text
