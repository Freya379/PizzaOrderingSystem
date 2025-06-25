from products import Pizza
from interfaces import Item, PizzaSize, CouponStrategy
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class StoreConfiguration:
    """Store configuration class"""
    
    def __init__(self, store_id: str, store_name: str):
        self.store_id = store_id
        self.store_name = store_name
        self.pizza_base_prices: Dict[PizzaSize, float] = {}
        self.topping_prices: Dict[str, float] = {}
        self.other_item_prices: Dict[str, float] = {}
    
    def set_pizza_base_prices(self, prices: Dict[PizzaSize, float]):
        self.pizza_base_prices = prices
    
    def set_topping_prices(self, prices: Dict[str, float]):
        self.topping_prices = prices
    
    def set_other_item_prices(self, prices: Dict[str, float]):
        self.other_item_prices = prices
    
    def get_pizza_base_price(self, size: PizzaSize) -> float:
        return self.pizza_base_prices.get(size, 0.0)
    
    def get_topping_price(self, topping_name: str) -> float:
        return self.topping_prices.get(topping_name, 0.0)
    
    def get_item_price(self, item_type: str, size_or_quantity=None) -> float:
        if size_or_quantity:
            key = f"{item_type}_{size_or_quantity}"
            return self.other_item_prices.get(key, 0.0)
        return self.other_item_prices.get(item_type, 0.0)

class StoreManager:
    """Store manager"""
    
    def __init__(self):
        self.stores: Dict[str, StoreConfiguration] = {}
        self._setup_default_stores()
    
    def _setup_default_stores(self):
        """Initialize default store configurations"""
        
        # Downtown store - premium pricing
        downtown = StoreConfiguration("001", "Downtown Store")
        downtown.set_pizza_base_prices({
            PizzaSize.SMALL: 12.0,
            PizzaSize.MEDIUM: 18.0,
            PizzaSize.LARGE: 24.0
        })
        downtown.set_topping_prices({
            "cheese": 2.5,
            "pepperoni": 3.5,
            "mushroom": 2.0
        })
        downtown.set_other_item_prices({
            "coke_small": 2.5,
            "coke_regular": 3.5,
            "coke_large": 4.5,
            "wings_per_piece": 1.8
        })
        
        # Suburban store - standard pricing
        suburban = StoreConfiguration("002", "Suburban Store")
        suburban.set_pizza_base_prices({
            PizzaSize.SMALL: 10.0,
            PizzaSize.MEDIUM: 15.0,
            PizzaSize.LARGE: 20.0
        })
        suburban.set_topping_prices({
            "cheese": 2.0,
            "pepperoni": 3.0,
            "mushroom": 1.5
        })
        suburban.set_other_item_prices({
            "coke_small": 2.0,
            "coke_regular": 3.0,
            "coke_large": 4.0,
            "wings_per_piece": 1.5
        })
        
        # Student district store - discount pricing
        student = StoreConfiguration("003", "Student District Store")
        student.set_pizza_base_prices({
            PizzaSize.SMALL: 8.0,
            PizzaSize.MEDIUM: 12.0,
            PizzaSize.LARGE: 16.0
        })
        student.set_topping_prices({
            "cheese": 1.5,
            "pepperoni": 2.5,
            "mushroom": 1.0
        })
        student.set_other_item_prices({
            "coke_small": 1.5,
            "coke_regular": 2.5,
            "coke_large": 3.5,
            "wings_per_piece": 1.2
        })
        
        self.stores["001"] = downtown
        self.stores["002"] = suburban
        self.stores["003"] = student 
    
    def get_store(self, store_id: str) -> Optional[StoreConfiguration]:
        return self.stores.get(store_id)
    
    def add_store(self, store: StoreConfiguration):
        self.stores[store.store_id] = store

# Store-specific product classes
class StorePizza(Pizza):
    """Store-specific pizza implementation"""   
    def __init__(self, base_type: str, size: PizzaSize, store_config: StoreConfiguration):
        self.base_type = base_type
        self.size = size
        self.store_config = store_config
    
    def get_description(self) -> str:
        return f"{self.size.value} {self.base_type} pizza"
    
    def get_cost(self) -> float:
        return self.store_config.get_pizza_base_price(self.size)
    
    def get_toppings(self) -> List[tuple]:
        return []
# Becase different stores will have different prices so need a a StorePizzaDecorator here: pizza+ store_config
class StorePizzaDecorator(Pizza):
    """Store-specific pizza decorator"""  
    def __init__(self, pizza: Pizza, store_config: StoreConfiguration):
        self.pizza = pizza
        self.store_config = store_config
    
    def get_description(self) -> str:
        return self.pizza.get_description()
    
    def get_cost(self) -> float:
        return self.pizza.get_cost()
    
    def get_toppings(self) -> List[tuple]:
        if hasattr(self.pizza, 'get_toppings'):
            return self.pizza.get_toppings()
        return []

class StoreCheeseTopping(StorePizzaDecorator):
    def get_description(self) -> str:
        return self.pizza.get_description() + ", cheese"
    
    def get_cost(self) -> float:
        cheese_price = self.store_config.get_topping_price("cheese")
        return self.pizza.get_cost() + cheese_price
    
    def get_toppings(self) -> List[tuple]:
        cheese_price = self.store_config.get_topping_price("cheese")
        return self.pizza.get_toppings() + [("cheese", cheese_price)]

class StorePepperoniTopping(StorePizzaDecorator):
    def get_description(self) -> str:
        return self.pizza.get_description() + ", pepperoni"
    
    def get_cost(self) -> float:
        pepperoni_price = self.store_config.get_topping_price("pepperoni")
        return self.pizza.get_cost() + pepperoni_price
    
    def get_toppings(self) -> List[tuple]:
        pepperoni_price = self.store_config.get_topping_price("pepperoni")
        return self.pizza.get_toppings() + [("pepperoni", pepperoni_price)]

class StoreMushroomTopping(StorePizzaDecorator):
    def get_description(self) -> str:
        return self.pizza.get_description() + ", mushroom"
    
    def get_cost(self) -> float:
        mushroom_price = self.store_config.get_topping_price("mushroom")
        return self.pizza.get_cost() + mushroom_price
    
    def get_toppings(self) -> List[tuple]:
        mushroom_price = self.store_config.get_topping_price("mushroom")
        return self.pizza.get_toppings() + [("mushroom", mushroom_price)]

class StoreCoke(Item):
    """Store-specific cola implementation"""
    def __init__(self, size: str, store_config: StoreConfiguration):
        self.size = size
        self.store_config = store_config
    
    def get_description(self) -> str:
        return f"{self.size} coke"
    
    def get_cost(self) -> float:
        return self.store_config.get_item_price("coke", self.size)

class StoreWings(Item):
    def __init__(self, quantity: int, store_config: StoreConfiguration):
        self.quantity = quantity
        self.store_config = store_config
    
    def get_description(self) -> str:
        return f"{self.quantity} chicken wings"
    
    def get_cost(self) -> float:
        price_per_piece = self.store_config.get_item_price("wings_per_piece")
        return self.quantity * price_per_piece