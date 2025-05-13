# Advanced OOP Challenge: Inventory Management System

# Objective:
# Design a robust Inventory Management System in Python that can manage different types of products, handle stock operations, sales, and persist data. This challenge is meant to polish your OOP concepts and make you confident in applying them in real-world use cases.

# ---

# *1. Abstract Base Class: Product*

# Use the abc module to make Product an abstract base class.

# Attributes (with encapsulation):

# * _product_id
# * _name
# * _price
# * _quantity_in_stock

# Methods (abstract & concrete):

# * restock(amount)
# * sell(quantity)
# * get_total_value() --> price \ stock
# * __str__() --> formatted product info

# ---

# *2. Subclasses of Product:*

# Create at least 3 different product types, each with extra attributes and overridden behavior where needed:

# * *Electronics* --> warranty_years, brand

# * *Grocery* --> expiry_date, is_expired()

# * *Clothing*  --> size, material

# Each subclass must override __str__() to include their specific info.

# ---

# *3. Class: Inventory*

# This class will manage a collection of products.

# Attributes:

# * _products --> a dict or list of products

# Methods:

# * add_product(product: Product)
# * remove_product(product_id)
# * search_by_name(name)
# * search_by_type(product_type)
# * list_all_products()
# * sell_product(product_id, quantity)
# * restock_product(product_id, quantity)
# * total_inventory_value()
# * remove_expired_products() (for groceries only)

# ---

# 4. Bonus / Extra Features (Optional but encouraged):

# Add the ability to save and *load inventory data* in JSON format:

# * save_to_file(filename)
# * load_from_file(filename)

# Ensure you store all relevant attributes and reconstruct subclasses properly when loading.

# * Implement custom exceptions for cases like:

#   * Selling more than available stock
#   * Adding products with duplicate IDs
#   * Loading invalid product data from file.

# * Add CLI Menu using a while loop for interaction:

#   * Add product
#   * Sell product
#   * Search/view product
#   * Save/Load inventory
#   * Exit

# ---

#  Evaluation Criteria:

# * Clean, well-structured code
# * Proper use of OOP concepts
# * Realistic and reusable class design
# * Error and edge-case handling
# * Code readability and documentation

# ---

# Deadline: Tuesday, 13 May 2025 at 11:59 PM


from abc import ABC, abstractmethod
import datetime
import os
import json



# custom exception classes
# for handling errors related to inventory management
class InventoryError(Exception):
    """Base class for inventory-related exceptions"""
    pass

# for handling specific errors
class InsufficientStockError(InventoryError):
    """Exception raised when trying to sell more items than available in stock"""
    def __init__(self, product_name, requested, available):
        self.product_name = product_name
        self.requested = requested
        self.available = available
        self.message = f"Cannot sell {requested} units of '{product_name}'. Only {available} units available in stock."
        super().__init__(self.message)

# for handling duplicate product IDs
class DuplicateProductIDError(InventoryError):
    """Exception raised when trying to add a product with an ID that already exists"""
    def __init__(self, product_id):
        self.product_id = product_id
        self.message = f"Product with ID {product_id} already exists in the inventory."
        super().__init__(self.message)

# for handling invalid product data
class InvalidProductDataError(InventoryError):
    """Exception raised when trying to load invalid product data from file"""
    def __init__(self, reason):
        self.reason = reason
        self.message = f"Invalid product data: {reason}"
        super().__init__(self.message)


# File path for storing the inventory data
INVENTORY_FILE = "inventory.json"

# Function to save the inventory data to a file
def save_inventory(inventory):
    """Save the inventory data to a file"""
    try:
        # Create a list to store serializable product data
        products_data = []
        
        # Check if inventory is empty
        if not inventory._products:
            print("⚠️ Inventory is empty! Nothing to save.")
            # Still save an empty list to the file
            with open(INVENTORY_FILE, 'w') as file:
                json.dump(products_data, file, indent=4)
            print(f"✅ Empty inventory saved to {INVENTORY_FILE}")
            return True
                
        # If we have products, serialize them
        for product in inventory._products:
            # Common product data
            product_data = {
                "product_id": product._product_id,
                "name": product._name,
                "price": product._price,
                "quantity_in_stock": product._quantity_in_stock,
                "type": product.__class__.__name__
            }
            
            # Add specific attributes based on product type
            if isinstance(product, Electronics):
                product_data["warranty_years"] = product.warranty_years
                product_data["brand"] = product.brand
            elif isinstance(product, Grocery):
                product_data["expiry_date"] = product.expiry_date_str
            elif isinstance(product, Clothing):
                product_data["size"] = product.size
                product_data["material"] = product.material
            
            products_data.append(product_data)
        
        # Write to file
        with open(INVENTORY_FILE, 'w') as file:
            json.dump(products_data, file, indent=4)
            
        print(f"✅ Inventory with {len(products_data)} products saved to {INVENTORY_FILE} successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error saving inventory: {e}")
        return False

# Function to load the inventory data from a file
def load_inventory():
    """Load the inventory data from a file"""
    if os.path.exists(INVENTORY_FILE):
        try:
            # Read from file
            with open(INVENTORY_FILE, 'r') as file:
                products_data = json.load(file)
            
            # Create a new inventory
            inventory = Inventory([])
            
            # Recreate products
            for product_data in products_data:
                try:
                    # Check for required fields
                    required_fields = ["product_id", "name", "price", "quantity_in_stock", "type"]
                    for field in required_fields:
                        if field not in product_data:
                            raise InvalidProductDataError(f"Missing required field: {field}")
                    
                    product_type = product_data["type"]
                    
                    if product_type == "Electronics":
                        # Check for Electronics-specific fields
                        if "warranty_years" not in product_data or "brand" not in product_data:
                            raise InvalidProductDataError("Missing Electronics-specific fields")
                        
                        product = Electronics(
                            product_data["product_id"],
                            product_data["name"],
                            product_data["price"],
                            product_data["quantity_in_stock"],
                            product_data["warranty_years"],
                            product_data["brand"]
                        )
                    elif product_type == "Grocery":
                        # Check for Grocery-specific fields
                        if "expiry_date" not in product_data:
                            raise InvalidProductDataError("Missing Grocery-specific fields")
                        
                        product = Grocery(
                            product_data["product_id"],
                            product_data["name"],
                            product_data["price"],
                            product_data["quantity_in_stock"],
                            product_data["expiry_date"]
                        )
                    elif product_type == "Clothing":
                        # Check for Clothing-specific fields
                        if "size" not in product_data or "material" not in product_data:
                            raise InvalidProductDataError("Missing Clothing-specific fields")
                        
                        product = Clothing(
                            product_data["product_id"],
                            product_data["name"],
                            product_data["price"],
                            product_data["quantity_in_stock"],
                            product_data["size"],
                            product_data["material"]
                        )
                    else:
                        raise InvalidProductDataError(f"Unknown product type: {product_type}")
                    
                    inventory._products.append(product)
                    
                except InvalidProductDataError as e:
                    print(f"⚠️ Skipping invalid product: {e}")
                    continue
            
            # Update total_products global variable
            global total_products
            if inventory._products:
                max_id = max(product._product_id for product in inventory._products)
                total_products = max(total_products, max_id)
            
            print(f"📚 Inventory loaded from {INVENTORY_FILE} with {len(inventory._products)} products")
            return inventory
            
        except json.JSONDecodeError:
            print(f"❌ Error loading inventory: Invalid JSON format in {INVENTORY_FILE}")
            return Inventory([])
        except Exception as e:
            print(f"❌ Error loading inventory: {e}")
            return Inventory([])
    else:
        print(f"📝 No inventory file found. Starting with an empty inventory.")
        return Inventory([])


# abstract class to manage other classes
class Product(ABC):
    """An Abstract class using to manage other classes"""

    def __init__(self, product_id: int, name: str, price: int, quantity_in_stock: int):
        self._product_id: int = product_id
        self._name: str = name
        self._price: int = price
        self._quantity_in_stock: int = quantity_in_stock

    @abstractmethod
    def restock(self, amount):
        pass

    @abstractmethod
    def sell(self, quantity):
        pass

    def get_total_value(self):
        return self._price * self._quantity_in_stock

    def __str__(self):
        return f"Name: {self._name}  |  ID: {self._product_id}  |  Price: {self._price}  |  Stock: {self._quantity_in_stock}"


# child class of Product for electronics items
class Electronics(Product):
    """Class which inherit Product and will include all the electronics items"""

    def __init__(
        self,
        product_id,
        name,
        price,
        quantity_in_stock,
        warranty_years: int,
        brand: str,
    ):
        super().__init__(product_id, name, price, quantity_in_stock)
        self.warranty_years = warranty_years
        self.brand = brand

    def restock(self, amount):
        self._quantity_in_stock += amount

    def sell(self, quantity):
        if self._quantity_in_stock >= quantity:
            self._quantity_in_stock -= quantity
        else:
            raise InsufficientStockError(self._name, quantity, self._quantity_in_stock)


    def __str__(self):
        return (
            super().__str__()
            + f"  |  warranty: {self.warranty_years} years  |  brand: {self.brand}"
        )


# child class of Product for grocery items
class Grocery(Product):
    """Class which inherit Product and will include all the Grocery items"""

    def __init__(
        self,
        product_id,
        name,
        price,
        quantity_in_stock,
        expiry_date: str,
    ):
        super().__init__(product_id, name, price, quantity_in_stock)
        self.expiry_date_str = expiry_date
        self.expiry_date = self._parse_date(expiry_date)
    def _parse_date(self, date_str):
        """Convert DD/MM/YYYY string to datetime object"""
        try:
            day, month, year = map(int, date_str.split('/'))
            return datetime.datetime(year, month, day)
        except ValueError:
            print(f"⚠️ Invalid date format: {date_str}. Using current date instead.")
            return datetime.datetime.now()

    def restock(self, amount):
        self._quantity_in_stock += amount

    def sell(self, quantity):
        if self._quantity_in_stock >= quantity:
            self._quantity_in_stock -= quantity
        else:
            raise InsufficientStockError(self._name, quantity, self._quantity_in_stock)       
    
    def is_expired(self, current_date=None):
        """Check if product is expired compared to given date or today"""
        if current_date is None:
            current_date = datetime.datetime.now()
        return self.expiry_date < current_date
    
    def __str__(self):
        return super().__str__() + f"  |  Expriry: {self.expiry_date_str}"


# child class of Product for Clothing items
class Clothing(Product):
    """Class which inherit Product and will include all the Grocery items"""

    def __init__(
        self, product_id, name, price, quantity_in_stock, size: str, material: str
    ):
        super().__init__(product_id, name, price, quantity_in_stock)
        self.size = size
        self.material = material

    def restock(self, amount):
        self._quantity_in_stock += amount

    def sell(self, quantity):
        if self._quantity_in_stock >= quantity:
            self._quantity_in_stock -= quantity
        else:
            raise InsufficientStockError(self._name, quantity, self._quantity_in_stock)
        
    def __str__(self):
        return (
            super().__str__() + f"  |  Size: {self.size}  |  Material: {self.material}"
        )


# class inventory to manage collection of products
class Inventory:
    def __init__(self, products):
        self._products = products

    # adding a product
    def add_product(self, product: Product):
        self._products.append(product)
        
    # removing a product by product_id
    def remove_product(self, product_id):
        original_length = len(self._products)
        self._products = [product for product in self._products if product._product_id != product_id]
        
        if len(self._products) < original_length:
            print(f"✅ Product with ID {product_id} removed successfully!")
            return True
        else:
            print(f"❌ No product with ID {product_id} found.")
            return False
    
    # searching products by name
    def search_by_name(self, name):
        matching_products = [product for product in self._products if name.lower() in product._name.lower()]
        
        if matching_products:
            print(f"\n----- Products matching '{name}' -----")
            for i, product in enumerate(matching_products, 1):
                print(f"{i}. {product}")
            print("-----------------------------\n")
            return matching_products
        else:
            print(f"❌ No products found matching '{name}'.")
            return []
    
    # searching products by type (Electronics, Grocery, Clothing)
    def search_by_type(self, product_type):
        matching_products = [product for product in self._products 
                            if product.__class__.__name__.lower() == product_type.lower()]
        
        if matching_products:
            print(f"\n----- Products of type '{product_type}' -----")
            for i, product in enumerate(matching_products, 1):
                print(f"{i}. {product}")
            print("-----------------------------\n")
            return matching_products
        else:
            print(f"❌ No products found of type '{product_type}'.")
            return []
    
    # listing all products
    def list_all_products(self):
        if not self._products:
            print("⚠️  Inventory is empty!")
            return
        
        print("\n----- Current Inventory -----")
        for i, product in enumerate(self._products, 1):
            print(f"{i}. {product}")
        print("-----------------------------\n")
    
    # selling a product by product_id and quantity
    def sell_product(self, product_id, quantity):
        for product in self._products:
            if product._product_id == product_id:
                try:
                    product.sell(quantity)
                    print(f"✅ Sold {quantity} units of '{product._name}'.")
                    return True
                except InsufficientStockError as e:
                    print(f"❌ {e}")
                    return False
        
        print(f"❌ No product with ID {product_id} found.")
        return False
    
    # restocking a product by product_id and quantity
    def restock_product(self, product_id, quantity):
        for product in self._products:
            if product._product_id == product_id:
                product.restock(quantity)
                print(f"✅ Restocked {quantity} units of '{product._name}'. New stock: {product._quantity_in_stock}")
                return True
        
        print(f"❌ No product with ID {product_id} found.")
        return False
    
    # calculating total inventory value
    def total_inventory_value(self):
        total_value = sum(product.get_total_value() for product in self._products)
        print(f"📊 Total Inventory Value: ${total_value}")
        return total_value
    
    # removing expired products (for groceries only)
    def remove_expired_products(self, current_date_str):
        # Parse the current date string to datetime object
        try:
            day, month, year = map(int, current_date_str.split('/'))
            current_date = datetime.datetime(year, month, day)
        except ValueError:
            print(f"⚠️ Invalid date format: {current_date_str}. Using today's date instead.")
            current_date = datetime.datetime.now()
        
        expired_products = []
        
        # Identify expired products
        for product in self._products:
            if isinstance(product, Grocery):
                if product.is_expired(current_date):
                    expired_products.append(product)
        
        # Remove expired products
        if expired_products:
            for product in expired_products:
                self._products.remove(product)
                print(f"🗑️ Removed expired product: {product._name} (Expiry: {product.expiry_date_str})")
            
            print(f"✅ Removed {len(expired_products)} expired products.")
            return expired_products
        else:
            print("✅ No expired products found.")
            return []
        
    # save inventory to file
    def save_to_file(self, filename):
        """Save the inventory data to a JSON file"""
        try:
            # Create a list to store serializable product data
            products_data = []
            
            # Check if inventory is empty
            if not self._products:
                print("⚠️ Inventory is empty! Nothing to save.")
                # Still save an empty list to the file
                with open(filename, 'w') as file:
                    json.dump(products_data, file, indent=4)
                print(f"✅ Empty inventory saved to {filename}")
                return True
                
            # If we have products, serialize them
            for product in self._products:
                # Common product data
                product_data = {
                    "product_id": product._product_id,
                    "name": product._name,
                    "price": product._price,
                    "quantity_in_stock": product._quantity_in_stock,
                    "type": product.__class__.__name__
                }
                
                # Add specific attributes based on product type
                if isinstance(product, Electronics):
                    product_data["warranty_years"] = product.warranty_years
                    product_data["brand"] = product.brand
                elif isinstance(product, Grocery):
                    product_data["expiry_date"] = product.expiry_date_str
                elif isinstance(product, Clothing):
                    product_data["size"] = product.size
                    product_data["material"] = product.material
                
                products_data.append(product_data)
            
            # Write to file
            with open(filename, 'w') as file:
                json.dump(products_data, file, indent=4)
                
            print(f"✅ Inventory with {len(products_data)} products saved to {filename} successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error saving inventory: {e}")
            return False


# assigning ids by calculating total products
total_products = 1

def run_inventory_system(inventory):
    """Main function to run the inventory management system menu loop"""
    condition = True
    print(
        "--------------- Welcome to Advance OOP Inventory Management System! ---------------"
    )
    
    while condition:
        print(
            "~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            "1. ➕ Add a Product\n"
            "2. ❎ Remove a Product\n"
            "3. 🔍 Search For a Product\n"
            "4. 📚 Display All Products\n"
            "5. 💰 Sell a Product\n"
            "6. 📦 Restock a Product\n"
            "7. 📊 View Inventory Value\n"
            "8. 🗑️  Remove Expired Products\n"
            "9. 💾 Save Inventory\n"
            "10. 📂 Load Inventory\n"
            "11. 🚪 Exit\n"
            "~~~~~~~~~~~~~~~~~~~~~~~~~"
        )
        
        opt = input("🔢 Enter Your Choice in Numbers (1-11): ")
        
        try:
            # ADDING A PRODUCT
            if opt == "1":
                add_product_menu(inventory)
            
            # REMOVING A PRODUCT
            elif opt == "2":
                product_id = int(input("Enter the ID of the product to remove: "))
                inventory.remove_product(product_id)
            
            # SEARCH FOR A PRODUCT
            elif opt == "3":
                search_product_menu(inventory)
            
            # DISPLAY ALL PRODUCTS
            elif opt == "4":
                inventory.list_all_products()
            
            # SELL A PRODUCT
            elif opt == "5":
                product_id = int(input("Enter the product ID to sell: "))
                quantity = int(input("Enter quantity to sell: "))
                inventory.sell_product(product_id, quantity)
            
            # RESTOCK A PRODUCT
            elif opt == "6":
                product_id = int(input("Enter the product ID to restock: "))
                quantity = int(input("Enter quantity to add: "))
                inventory.restock_product(product_id, quantity)
            
            # VIEW INVENTORY VALUE
            elif opt == "7":
                inventory.total_inventory_value()
            
            # REMOVE EXPIRED PRODUCTS
            elif opt == "8":
                current_date = input("Enter current date (DD/MM/YYYY): ")
                inventory.remove_expired_products(current_date)
            
            # SAVE INVENTORY
            elif opt == "9":
                save_inventory(inventory)
            
            # LOAD INVENTORY
            elif opt == "10":
                loaded_inventory = load_inventory()
                if loaded_inventory and loaded_inventory._products:
                    inventory._products = loaded_inventory._products
                    global total_products
                    # Update total_products to be at least the highest product ID
                    for product in inventory._products:
                        total_products = max(total_products, product._product_id)
                    print(f"✅ Loaded {len(inventory._products)} products.")
            # EXIT
            elif opt == "11":
                condition = False
                print("👋 Goodbye! Thank you for using the Inventory Management System.")
            
            else:
                print("⚠️  Please select from numbers given above (1-11)!")
                
        except ValueError:
            print("❌ Please enter a valid number!")
        except Exception as e:
            print(f"❌ Something went wrong: {e}")


def add_product_menu(inventory):
    """Function to handle the add product menu"""
    print(
        "~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        "1. Electronics\n"
        "2. Grocery\n"
        "3. Clothing\n"
        "~~~~~~~~~~~~~~~~~~~~~~~~~"
    )
    
    sub_opt = input("In which category do you want to add product? 🔢 Enter Your Choice (1-3): ")
    
    try:
        global total_products
        product_id = total_products + 1  # Auto-increment product ID
        name = input("Enter the product's name: ")
        price = int(input("Enter the Price: "))
        quantity_in_stock = int(input("Enter the quantity available in stock: "))
        
        if sub_opt == "1":  # Electronics
            warranty_years = int(input("Enter warranty years: "))
            brand = input("Enter brand name: ")
            new_product = Electronics(product_id, name, price, quantity_in_stock, warranty_years, brand)
            inventory.add_product(new_product)
            print(f"✅ Electronics product '{name}' added successfully!")
            
        elif sub_opt == "2":  # Grocery
            expiry_date = input("Enter expiry date (DD/MM/YYYY): ")
            new_product = Grocery(product_id, name, price, quantity_in_stock, expiry_date)
            inventory.add_product(new_product)
            print(f"✅ Grocery product '{name}' added successfully!")
            
        elif sub_opt == "3":  # Clothing
            size = input("Enter size (S/M/L/XL): ")
            material = input("Enter material: ")
            new_product = Clothing(product_id, name, price, quantity_in_stock, size, material)
            inventory.add_product(new_product)
            print(f"✅ Clothing product '{name}' added successfully!")
            
        else:
            print("⚠️  Please enter a valid option (1-3)!")
            return
            
        total_products += 1  # Increment the total products counter
        
    except ValueError:
        print("❌ Please enter valid numeric values for price, quantity, etc.")
    except Exception as e:
        print(f"❌ Something went wrong: {e}")


def search_product_menu(inventory):
    """Function to handle the search product menu"""
    print(
        "~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        "1. Search by Name\n"
        "2. Search by Type (Electronics/Grocery/Clothing)\n"
        "~~~~~~~~~~~~~~~~~~~~~~~~~"
    )
    
    search_opt = input("🔢 Enter your choice (1-2): ")
    
    if search_opt == "1":
        name = input("Enter product name to search: ")
        inventory.search_by_name(name)
    elif search_opt == "2":
        product_type = input("Enter product type (Electronics/Grocery/Clothing): ")
        inventory.search_by_type(product_type)
    else:
        print("⚠️ Please enter a valid option (1-2)!")


# Main code execution
if __name__ == "__main__": #ensure that the script is being run directly not imported
    # Initialize inventory with sample products
    inventory = load_inventory() #trying to load inventory or starting with an empty one
    
    # Run the inventory management system
    run_inventory_system(inventory)
    