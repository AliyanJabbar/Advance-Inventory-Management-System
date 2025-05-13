# 📦 Advanced OOP Challenge: Inventory Management System

## 🚀 Objective
Design a robust Inventory Management System in Python that utilizes core object-oriented programming (OOP) principles. This system should be capable of managing multiple product types, handling inventory operations (like sales and restocking), and saving/loading data. This project aims to reinforce OOP concepts and demonstrate real-world problem-solving skills.

---

## 📐 System Architecture

### 1. 🧱 Abstract Base Class: `Product`
- **Module:** `abc`
- **Encapsulated Attributes:**
  - `_product_id`
  - `_name`
  - `_price`
  - `_quantity_in_stock`

- **Methods:**
  - `restock(amount)`
  - `sell(quantity)`
  - `get_total_value()` → Returns `_price * _quantity_in_stock`
  - `__str__()` → Formatted string displaying product info

---

### 2. 🔌 Product Subclasses

#### 🖥️ `Electronics`
- **Additional Attributes:**
  - `warranty_years`
  - `brand`
- **Overrides:** `__str__()`

#### 🥫 `Grocery`
- **Additional Attributes:**
  - `expiry_date`
- **Additional Methods:**
  - `is_expired()` → Boolean
- **Overrides:** `__str__()`

#### 👕 `Clothing`
- **Additional Attributes:**
  - `size`
  - `material`
- **Overrides:** `__str__()`

---

### 3. 🗃️ `Inventory` Class

Manages a collection of products.

- **Attribute:**
  - `_products` → Dictionary with `product_id` as key and `Product` instance as value

- **Methods:**
  - `add_product(product: Product)`
  - `remove_product(product_id)`
  - `search_by_name(name)`
  - `search_by_type(product_type)`
  - `list_all_products()`
  - `sell_product(product_id, quantity)`
  - `restock_product(product_id, quantity)`
  - `total_inventory_value()`
  - `remove_expired_products()` → For `Grocery` type only

---

## 💡 Bonus / Extra Features

### 💾 Data Persistence (JSON)
- `save_to_file(filename)`
- `load_from_file(filename)`  
Handles all attributes and reconstructs subclass instances correctly.

### ⚠️ Custom Exceptions
- `InsufficientStockError` → Selling more than available
- `DuplicateProductIDError` → Adding a product with an existing ID
- `InvalidProductDataError` → Loading invalid data from JSON

### 🧑‍💻 CLI Interface
Basic command-line interface using a `while` loop:
- Add Product
- Sell Product
- Search/View Product
- Restock Product
- List All Products
- Remove Expired Products
- Save Inventory
- Load Inventory
- Exit

---

## ✅ Evaluation Criteria

- ✅ Clean and well-structured code
- ✅ Proper use of OOP principles (abstraction, inheritance, encapsulation, polymorphism)
- ✅ Realistic and reusable class design
- ✅ Edge case and error handling
- ✅ Clear, readable code with documentation/comments

---

## ⏰ Deadline
**Tuesday, 13 May 2025 at 11:59 PM**

---

> 💡 Tip: Make sure your code is modular and testable. Aim for clarity and reusability in your design.
