from abc import ABC, abstractmethod


class ABCBlock(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def draw(self):
        pass

    def __repr__(self) -> str:
        return f"{self.name}"

