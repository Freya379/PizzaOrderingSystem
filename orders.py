from products import BasePizza, PizzaDecorator
from interfaces import Item, PizzaSize, CouponStrategy
from stores import StoreConfiguration
from abc import ABC, abstractmethod
from typing import List, Optional

class Order:
    """Basic Order class"""
    
    def __init__(self):
        self.items: List[Item] = []
        self.coupon: Optional[CouponStrategy] = None
    
    def add_item(self, item: Item):
        self.items.append(item)
    
    def apply_coupon(self, coupon: CouponStrategy):
        self.coupon = coupon
    
    def calculate_subtotal(self) -> float:
        return sum(item.get_cost() for item in self.items)
    
    def calculate_total_cost(self) -> float:
        subtotal = self.calculate_subtotal()
        if self.coupon:
            return self.coupon.apply_discount(subtotal, self.items)
        return subtotal
    
    def get_order_summary(self) -> str:
        if not self.items:
            return "Empty Order"
        
        summary = "Order Details:\n"
        for i, item in enumerate(self.items, 1):
            summary += f"{i}. {item.get_description()} - ${item.get_cost():.2f}\n"
        
        subtotal = self.calculate_subtotal()
        summary += f"\nSubtotal: ${subtotal:.2f}"
        
        if self.coupon:
            total = self.calculate_total_cost()
            discount = subtotal - total
            summary += f"\nCoupon Applied: {self.coupon.get_description()}"
            summary += f"\nDiscount Amount: -${discount:.2f}"
            summary += f"\nFinal Total: ${total:.2f}"
        else:
            summary += f"\nTotal: ${subtotal:.2f}"
        
        return summary

class StoreOrder(Order):
    """Order with store-specific configuration support"""
    
    def __init__(self, store_config: StoreConfiguration):
        super().__init__()
        self.store_config = store_config
    
    def get_order_summary(self) -> str:
        if not self.items:
            return "Order is empty"
        
        summary = f"Order Details - {self.store_config.store_name}:\n"
        for i, item in enumerate(self.items, 1):
            summary += f"{i}. {item.get_description()} - ${item.get_cost():.2f}\n"
        
        subtotal = self.calculate_subtotal()
        summary += f"\nSubtotal: ${subtotal:.2f}"
        
        if self.coupon:
            total = self.calculate_total_cost()
            discount = subtotal - total
            summary += f"\nCoupon Applied: {self.coupon.get_description()}"
            summary += f"\nDiscount Amount: -${discount:.2f}"
            summary += f"\nFinal Total: ${total:.2f}"
        else:
            summary += f"\nTotal: ${subtotal:.2f}"
        
        return summary