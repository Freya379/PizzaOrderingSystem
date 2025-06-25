from products import BasePizza, PizzaDecorator
from interfaces import Item, PizzaSize, CouponStrategy
from abc import ABC, abstractmethod
from typing import List

# ============================================================================
# Use Strategy Pattern for Different Promotion's method/algorithm/ strategy
# ============================================================================

class CouponStrategy(ABC):
    @abstractmethod
    def apply_discount(self, original_cost: float, items: List[Item] = None) -> float:
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        pass

class FixedDiscountCoupon(CouponStrategy):
    def __init__(self, discount_amount: float):
        self.discount_amount = discount_amount
    
    def apply_discount(self, original_cost: float, items: List[Item] = None) -> float:
        return max(0, original_cost - self.discount_amount)
    
    def get_description(self) -> str:
        return f"FIxed Discount: ${self.discount_amount:.2f}"

class PercentageDiscountCoupon(CouponStrategy):  
    def __init__(self, discount_percentage: float):
        self.discount_percentage = discount_percentage
    
    def apply_discount(self, original_cost: float, items: List[Item] = None) -> float:
        return original_cost * (1 - self.discount_percentage / 100)
    
    def get_description(self) -> str:
        return f"% Discount is:  {self.discount_percentage}%"

class MinimumSpendCoupon(CouponStrategy):
    def __init__(self, minimum_spend: float, discount_amount: float):
        self.minimum_spend = minimum_spend
        self.discount_amount = discount_amount
    
    def apply_discount(self, original_cost: float, items: List[Item] = None) -> float:
        if original_cost >= self.minimum_spend:
            return max(0, original_cost - self.discount_amount)
        return original_cost
    
    def get_description(self) -> str:
        return f"Spend at least ${self.minimum_spend:.2f}, You get ${self.discount_amount:.2f}"

class BuyOneGetOneCoupon(CouponStrategy):
    def __init__(self, target_item_type: type):
        self.target_item_type = target_item_type
    
    def apply_discount(self, original_cost: float, items: List[Item] = None) -> float:
        if not items:
            return original_cost
        
        # Find the item that is undergoing with this buy one get one free promotion
        target_items = [item for item in items if isinstance(item, self.target_item_type)]
        
        if len(target_items) >= 2:
            cheapest_item = min(target_items, key=lambda x: x.get_cost())
            discount = cheapest_item.get_cost()
            return max(0, original_cost - discount)
        
        return original_cost
    
    def get_description(self) -> str:
        return f"{self.target_item_type.__name__} Buy One Get One"

# Toppings Promotion Strategies
class CheapestToppingFreeCoupon(CouponStrategy):
    """Free cheapest topping coupon"""
    
    def apply_discount(self, original_cost: float, items: List[Item] = None) -> float:
        if not items:
            return original_cost
        
        # Collect topping information from all pizzas
        all_toppings = []
        for item in items:
            if isinstance(item, (BasePizza, PizzaDecorator)):
                if hasattr(item, 'get_toppings'):
                    toppings = item.get_toppings()
                    all_toppings.extend(toppings)
        
        if not all_toppings:
            return original_cost
        
        # Find the cheapest topping
        cheapest_topping = min(all_toppings, key=lambda x: x[1])
        discount = cheapest_topping[1]
        
        return max(0, original_cost - discount)
    
    def get_description(self) -> str:
        return "Free cheapest topping"

class MultiToppingDiscountCoupon(CouponStrategy):
    """Multiple toppings discount"""
    
    def __init__(self, free_count: int = 1):
        self.free_count = free_count
    
    def apply_discount(self, original_cost: float, items: List[Item] = None) -> float:
        if not items:
            return original_cost
        
        # Collect all toppings
        all_toppings = []
        for item in items:
            if isinstance(item, (BasePizza, PizzaDecorator)):
                if hasattr(item, 'get_toppings'):
                    toppings = item.get_toppings()
                    all_toppings.extend(toppings)
        
        if len(all_toppings) < self.free_count:
            return original_cost
        
        # Sort by price and make the cheapest ones free
        sorted_toppings = sorted(all_toppings, key=lambda x: x[1])
        discount = sum(topping[1] for topping in sorted_toppings[:self.free_count])
        
        return max(0, original_cost - discount)
    
    def get_description(self) -> str:
        return f"Free {self.free_count} cheapest toppings"