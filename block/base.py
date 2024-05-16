from abc import ABC, abstractmethod


class ABCBlock(ABC):

    def __init__(self, name):
        self.name = name
        self.outputs = []
        self.inputs = []

    @abstractmethod
    def draw(self):
        pass

    def __repr__(self) -> str:
        return f"{self.name}"

    def add_input(self, block: "ABCBlock"):
        self.inputs.append(block)

    def add_output(self, block: "ABCBlock"):
        self.outputs.append(block)
