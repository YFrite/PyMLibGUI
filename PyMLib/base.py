from abc import ABC, abstractmethod
from typing import Optional, Self


class BaseModel(ABC):
    @abstractmethod
    def fit(self, **kwargs) -> Self:
        pass

    @abstractmethod
    def predict(self, **kwargs):
        pass
