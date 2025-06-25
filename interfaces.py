
from abc import ABC, abstractmethod
from enum import Enum
from typing import List

class PizzaSize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large" 

# 所有的 abstract API
class Item(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass
    
    @abstractmethod
    def get_cost(self) -> float:
        pass

class CouponStrategy(ABC):  
    @abstractmethod
    def apply_discount(self, original_cost: float, items: List[Item] = None) -> float:
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        pass

