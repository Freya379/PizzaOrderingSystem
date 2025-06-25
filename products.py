from interfaces import Item, PizzaSize
from abc import abstractmethod
from typing import List

class Pizza(Item):
    pass

class BasePizza(Pizza):
    def __init__(self, base_type: str, size: PizzaSize):
        self.base_type = base_type
        self.size = size
    
    def get_description(self) -> str:
        return f"{self.size.value} {self.base_type} pizza"
    
    def get_cost(self) -> float:
        size_prices = {
            PizzaSize.SMALL: 10.0,
            PizzaSize.MEDIUM: 15.0,
            PizzaSize.LARGE: 20.0
        }
        return size_prices[self.size]
    
    def get_toppings(self) -> List[tuple]:
        """返回配料列表 - Follow-up 4需要"""
        return []

class PizzaDecorator(Pizza):
    def __init__(self, pizza: Pizza):
        self.pizza = pizza
    
    def get_description(self) -> str:
        return self.pizza.get_description()
    
    def get_cost(self) -> float:
        return self.pizza.get_cost()
    
    def get_toppings(self) -> List[tuple]:
        if hasattr(self.pizza, 'get_toppings'):
            return self.pizza.get_toppings()
        return []

class CheeseTopping(PizzaDecorator):
    def get_description(self) -> str:
        return self.pizza.get_description() + ", cheese"
    
    def get_cost(self) -> float:
        return self.pizza.get_cost() + 2.0
    
    def get_toppings(self) -> List[tuple]:
        return self.pizza.get_toppings() + [("cheese", 2.0)]

class PepperoniTopping(PizzaDecorator):
    def get_description(self) -> str:
        return self.pizza.get_description() + ", pepperoni"
    
    def get_cost(self) -> float:
        return self.pizza.get_cost() + 3.0
    
    def get_toppings(self) -> List[tuple]:
        return self.pizza.get_toppings() + [("pepperoni", 3.0)]

class MushroomTopping(PizzaDecorator):
    def get_description(self) -> str:
        return self.pizza.get_description() + ", mushroom"
    
    def get_cost(self) -> float:
        return self.pizza.get_cost() + 1.5
    
    def get_toppings(self) -> List[tuple]:
        return self.pizza.get_toppings() + [("mushroom", 1.5)]
    
class Coke(Item):
    def __init__(self, size: str = "regular"):
        self.size = size
    
    def get_description(self) -> str:
        return f"{self.size} coke"
    
    def get_cost(self) -> float:
        size_prices = {
            "small": 2.0,
            "regular": 3.0,
            "large": 4.0
        }
        return size_prices.get(self.size, 3.0)

class Wings(Item):
    def __init__(self, quantity: int = 6):
        self.quantity = quantity
    
    def get_description(self) -> str:
        return f"{self.quantity} chicken wings"
    
    def get_cost(self) -> float:
        return self.quantity * 1.5