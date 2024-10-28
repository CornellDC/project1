"""
Constants for Canadian currency.
"""
NICKEL = 0.05
DIME = 0.10
QUARTER = 0.25
LOONIE = 1.00
TOONIE = 2

class item():
    def __init__(self, name, price:float, stock:int):
        self.name = name
        self.price = price
        self.stock  = stock

    def __str__(self):
        return self.name

    def set_price(self, price):
        self.price = price

    def sell(self):
        if self.stock >= 1:
            self.stock -= 1
        else:
            print("Not available")

    def restock(self, amount):
        self.stock += amount

chocolate = item("Chocolate",1, 10)
cola = item("Cola",1, 10)
gum = item("Bubble Gum",0.10, 10)
crisps = item("Crisps",1, 15)
milk = item("2% Milk",2, 10)
chocolate_milk = item("Chocolate Milk",2.50, 5)

items = [chocolate,cola,gum,crisps,milk,chocolate_milk]

# for item in items:
#     print(item)





