# PizzaOrderingSystem
LLD code Practise

Pizza Ordering System
Inspired by recent Amazon OOD question.
A comprehensive Python-based pizza ordering system that demonstrates multiple design patterns including Decorator, Strategy, and Factory patterns. The system supports customizable pizzas, multiple item types, flexible coupon systems, and multi-store configurations with differential pricing.
Features

Customizable Pizza Builder: Create pizzas with various crusts, sizes, and toppings
Multi-Item Orders: Support for pizzas, drinks, and sides in a single order
Flexible Coupon System: Multiple discount strategies including fixed amount, percentage, BOGO, and topping-specific discounts
Multi-Store Support: Different pricing configurations for different store locations
Extensible Architecture: Easy to add new items, toppings, and discount strategies

Project Structure
pizzaOrderingSystem/
├── interfaces.py          # Abstract base classes and interfaces
├── couponsStrategy.py     # Coupon and discount strategies
├── orders.py             # Order management system
├── products.py           # Pizza and product implementations
└── stores.py             # Multi-store configuration system

**Design Patterns Used**
1. Decorator Pattern

Used for: Pizza toppings system
Classes: PizzaDecorator, CheeseTopping, PepperoniTopping, MushroomTopping
Benefit: Dynamically add toppings to pizzas without modifying the base pizza class

2. Strategy Pattern

Used for: Coupon and discount system
Classes: CouponStrategy, FixedDiscountCoupon, PercentageDiscountCoupon, BuyOneGetOneCoupon
Benefit: Easy to add new discount types without modifying existing code

3. Factory Pattern (Configuration)

Used for: Store-specific product creation
Classes: StoreManager, StoreConfiguration
Benefit: Centralized management of different store configurations
