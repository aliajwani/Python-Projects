"""
Ali Ajwani
December 8, 2023
"""

# This code uses classes, objects, text processing and functions to read files and create an inventory list for online stores containing product name, price, quantity, and category

# This class is used to represent the individual products in the store
class Product:
    def __init__(self, name, price, category):
        # Initialize product attributes
        self._name = name
        self._price = price
        self._category = category

    # Define how products are classified
    def __eq__(self, other):
         if isinstance(other, Product):
             if  ((self._name == other._name and self._price == other._price) and (self._category==other._category)):
                return True
             else:
                return False
         else:
            return False

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def get_category(self):
        return self._category

    # Implement string representation
    def __repr__(self):
        rep = 'Product(' + self._name + ',' + str(self._price) + ',' + self._category + ')'
        return rep


# This class provides the basic structure for an inventory system
class Inventory:
    def __init__(self):
        self.inventory = {}

    # This method adds products to the inventory
    def add_to_productInventory(self, productName, productPrice, productQuantity):
        self.inventory[productName] = {
            'price': productPrice,
            'quantity': productQuantity
        }

    # This method adds the quantity of a product
    def add_productQuantity(self, nameProduct, addQuantity):
        if nameProduct in self.inventory:
            self.inventory[nameProduct]['quantity'] += addQuantity

    # This method removes some of a product quantity
    # It is mainly used when a product is added to a customers shopping cart
    def remove_productQuantity(self, nameProduct, removeQuantity):
        if nameProduct in self.inventory and self.inventory[nameProduct]['quantity'] >= removeQuantity:
            self.inventory[nameProduct]['quantity'] -= removeQuantity

    # This method is used to get a products price
    def get_productPrice(self, nameProduct):
        if nameProduct in self.inventory:
            return self.inventory[nameProduct]['price']
        return None

    # This method is used to get a products quantity
    def get_productQuantity(self, nameProduct):
        if nameProduct in self.inventory:
            return self.inventory[nameProduct]['quantity']
        return None

    # This method is used to display the inventory in the correct format
    def display_Inventory(self):
        for product, details in self.inventory.items():
            product_details = f"{product}, {int(details['price'])}, {details['quantity']}"
            print(product_details)


# This class provides the basic structure of a shopping cart
class ShoppingCart:
    def __init__(self, buyerName, inventory):
        self.buyerName = buyerName
        self.inventory = inventory
        self.cart = {}

    # This method adds the items to a customers cart and changes the inventory accordingly
    # This method also provides the required strings to the customer based on the situation
    def add_to_cart(self, nameProduct, requestedQuantity):
        if nameProduct not in self.inventory.inventory:
            return "Product not in inventory"
        if self.inventory.inventory[nameProduct]['quantity'] < requestedQuantity:
            return "Can not fill the order"
        self.inventory.remove_productQuantity(nameProduct, requestedQuantity)
        if nameProduct in self.cart:
            self.cart[nameProduct] += requestedQuantity
        else:
            self.cart[nameProduct] = requestedQuantity
        return "Filled the order"

    # This method removes the items from a customers cart and changes the inventory accordingly
    # This method also provides the required strings to the customer based on the situation
    def remove_from_cart(self, nameProduct, requestedQuantity):
        # Check if the product is in the cart
        if nameProduct not in self.cart:
            return "Product not in the cart"
        if self.cart[nameProduct] < requestedQuantity:
            return "The requested quantity to be removed from cart exceeds what is in the cart"
        self.cart[nameProduct] -= requestedQuantity
        if self.cart[nameProduct] == 0:
            self.cart.pop(nameProduct)
        self.inventory.add_productQuantity(nameProduct, requestedQuantity)
        return "Successful"

    # This method displays the customers shopping cart in the correct format
    def view_cart(self):
        total = 0
        for product, quantity in self.cart.items():
            price = self.inventory.get_productPrice(product)
            print(f"{product} {quantity}")
            total += price * quantity
        print(f"Total: {int(total)}")
        print(f"Buyer Name: {self.buyerName}")


# This class functions a catalog that hold's all the product's information
class ProductCatalog:
    def __init__(self):
        self.catalog = []
        self.low_prices = set()
        self.medium_prices = set()
        self.high_prices = set()

    # This method adds products to the catalog and their category
    def addProduct(self, product):
        for product in product:
            self.catalog.append(product)
            price = product['price']
            if 0 <= price <= 99:
                self.low_prices.add(product['name'])
            elif 100 <= price <= 499:
                self.medium_prices.add(product['name'])
            elif price >= 500:
                self.high_prices.add(product['name'])

    # This method prints how many products are in each category
    def price_category(self):
        print(f"Number of low price items: {len(self.low_prices)}")
        print(f"Number of medium price items: {len(self.medium_prices)}")
        print(f"Number of high price items: {len(self.high_prices)}")

    # This method displays the catalog in the correct format
    def display_catalog(self):
        for product in self.catalog:
            catalog_format = f"Product: {product['name']} Price: {int(product['price'])} Category: {product['category']}"
            print(catalog_format)


# This function reads the files and populates the inventory based on the file
def populate_inventory(filename):
    inventory = Inventory()
    with open(filename, 'r') as file:
        for line in file:
            product_name, price, quantity, _ = line.strip().split(',')
            inventory.add_to_productInventory(product_name, float(price), int(quantity))
    return inventory


# This function reads the files and populates the catalog based on the file
def populate_catalog(fileName):
    catalog = ProductCatalog()
    products = []

    with open(fileName, 'r') as file:
        for line in file:
            name, price, _, category = line.strip().split(',')
            product = {'name': name, 'price': int(price), 'category': category}
            products.append(product)

    catalog.addProduct(products)
    return catalog




