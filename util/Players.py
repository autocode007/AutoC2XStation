from abc import abstractmethod

from util.Player import Player


class Players:

    @abstractmethod
    def find_by_index(self, index: int) -> Player:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Player:
        pass

    @abstractmethod
    def quitall(self):
        pass
