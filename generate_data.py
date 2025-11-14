"""
Synthetic E-Commerce Data Generator

This script generates realistic e-commerce datasets with proper relational integrity.
Creates 5 CSV files: customers, products, orders, order_items, and payments.
"""

import random
import csv
from datetime import datetime, timedelta
from faker import Faker
import os

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)

# Ensure data directory exists
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Configuration for number of records
NUM_CUSTOMERS = random.randint(100, 300)
NUM_PRODUCTS = random.randint(100, 300)
NUM_ORDERS = random.randint(100, 300)
NUM_ORDER_ITEMS = random.randint(150, 300)
NUM_PAYMENTS = NUM_ORDERS  # One payment per order

print("=" * 60)
print("E-COMMERCE DATA GENERATOR")
print("=" * 60)
print(f"Generating {NUM_CUSTOMERS} customers...")
print(f"Generating {NUM_PRODUCTS} products...")
print(f"Generating {NUM_ORDERS} orders...")
print(f"Generating {NUM_ORDER_ITEMS} order items...")
print(f"Generating {NUM_PAYMENTS} payments...")
print("=" * 60)


# ============================================================================
# 1. GENERATE CUSTOMERS
# ============================================================================

def generate_customers():
    """Generate customer records with realistic data."""
    customers = []
    
    for customer_id in range(1, NUM_CUSTOMERS + 1):
        customer = {
            'customer_id': customer_id,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'address': fake.street_address(),
            'city': fake.city(),
            'state': fake.state_abbr(),
            'zip_code': fake.zipcode(),
            'country': 'USA',
            'created_at': fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S'),
            'customer_segment': random.choice(['Regular', 'Premium', 'VIP', 'New'])
        }
        customers.append(customer)
    
    # Write to CSV
    filename = os.path.join(DATA_DIR, 'customers.csv')
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=customers[0].keys())
        writer.writeheader()
        writer.writerows(customers)
    
    print(f"✓ Generated {len(customers)} customers -> {filename}")
    return customers


# ============================================================================
# 2. GENERATE PRODUCTS
# ============================================================================

def generate_products():
    """Generate product records with realistic categories and pricing."""
    products = []
    
    # Product categories with realistic price ranges
    categories = {
        'Electronics': (50, 2000),
        'Clothing': (15, 200),
        'Home & Kitchen': (10, 500),
        'Books': (5, 50),
        'Sports & Outdoors': (20, 300),
        'Beauty & Personal Care': (8, 100),
        'Toys & Games': (10, 150),
        'Automotive': (15, 500),
        'Food & Grocery': (5, 100),
        'Health & Wellness': (10, 200)
    }
    
    product_prefixes = {
        'Electronics': ['Smart', 'Pro', 'Ultra', 'Premium', 'Wireless', 'Digital'],
        'Clothing': ['Classic', 'Modern', 'Casual', 'Formal', 'Comfort', 'Style'],
        'Home & Kitchen': ['Essential', 'Deluxe', 'Professional', 'Premium', 'Eco'],
        'Books': ['The Art of', 'Guide to', 'Complete', 'Mastering', 'Introduction to'],
        'Sports & Outdoors': ['Pro', 'Adventure', 'Elite', 'Performance', 'Outdoor'],
        'Beauty & Personal Care': ['Natural', 'Organic', 'Premium', 'Luxury', 'Essential'],
        'Toys & Games': ['Fun', 'Educational', 'Creative', 'Action', 'Adventure'],
        'Automotive': ['Premium', 'Heavy Duty', 'Professional', 'Universal', 'High Performance'],
        'Food & Grocery': ['Organic', 'Fresh', 'Gourmet', 'Natural', 'Premium'],
        'Health & Wellness': ['Natural', 'Organic', 'Premium', 'Advanced', 'Essential']
    }
    
    for product_id in range(1, NUM_PRODUCTS + 1):
        category = random.choice(list(categories.keys()))
        price_min, price_max = categories[category]
        prefix = random.choice(product_prefixes[category])
        
        product = {
            'product_id': product_id,
            'product_name': f"{prefix} {fake.word().capitalize()} {category.split()[0]}",
            'category': category,
            'price': round(random.uniform(price_min, price_max), 2),
            'cost': round(random.uniform(price_min * 0.4, price_min * 0.7), 2),
            'stock_quantity': random.randint(0, 500),
            'supplier': fake.company(),
            'created_at': fake.date_time_between(start_date='-3y', end_date='-1y').strftime('%Y-%m-%d %H:%M:%S'),
            'rating': round(random.uniform(3.0, 5.0), 1)
        }
        products.append(product)
    
    # Write to CSV
    filename = os.path.join(DATA_DIR, 'products.csv')
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products)
    
    print(f"✓ Generated {len(products)} products -> {filename}")
    return products


# ============================================================================
# 3. GENERATE ORDERS
# ============================================================================

def generate_orders(customers):
    """Generate order records linked to customers."""
    orders = []
    
    order_statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
    status_weights = [0.05, 0.10, 0.15, 0.65, 0.05]  # Most orders are delivered
    
    for order_id in range(1, NUM_ORDERS + 1):
        # Random customer
        customer = random.choice(customers)
        
        # Order date within the last year
        order_date = fake.date_time_between(start_date='-1y', end_date='now')
        
        # Shipping date (1-7 days after order)
        shipped_date = order_date + timedelta(days=random.randint(1, 7))
        
        # Delivery date (2-10 days after shipping)
        delivery_date = shipped_date + timedelta(days=random.randint(2, 10))
        
        status = random.choices(order_statuses, weights=status_weights)[0]
        
        order = {
            'order_id': order_id,
            'customer_id': customer['customer_id'],
            'order_date': order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': status,
            'shipping_address': f"{fake.street_address()}, {fake.city()}, {fake.state_abbr()} {fake.zipcode()}",
            'shipped_date': shipped_date.strftime('%Y-%m-%d %H:%M:%S') if status in ['Shipped', 'Delivered'] else None,
            'delivery_date': delivery_date.strftime('%Y-%m-%d %H:%M:%S') if status == 'Delivered' else None,
            'total_amount': 0.0  # Will be calculated from order items
        }
        orders.append(order)
    
    # Write to CSV
    filename = os.path.join(DATA_DIR, 'orders.csv')
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=orders[0].keys())
        writer.writeheader()
        writer.writerows(orders)
    
    print(f"✓ Generated {len(orders)} orders -> {filename}")
    return orders


# ============================================================================
# 4. GENERATE ORDER ITEMS
# ============================================================================

def generate_order_items(orders, products):
    """Generate order items with FK relationships to orders and products."""
    order_items = []
    order_totals = {order['order_id']: 0.0 for order in orders}
    
    item_id = 1
    
    for _ in range(NUM_ORDER_ITEMS):
        # Random order and product
        order = random.choice(orders)
        product = random.choice(products)
        
        # Realistic quantity (1-10 items)
        quantity = random.randint(1, 10)
        
        # Price at time of order (may differ slightly from current price)
        price_variation = random.uniform(0.95, 1.05)
        unit_price = round(product['price'] * price_variation, 2)
        
        # Calculate subtotal
        subtotal = round(unit_price * quantity, 2)
        
        # Apply discount for some items
        discount = 0.0
        if random.random() < 0.2:  # 20% chance of discount
            discount = round(subtotal * random.uniform(0.05, 0.20), 2)
        
        total = round(subtotal - discount, 2)
        
        order_item = {
            'order_item_id': item_id,
            'order_id': order['order_id'],
            'product_id': product['product_id'],
            'quantity': quantity,
            'unit_price': unit_price,
            'discount': discount,
            'total': total
        }
        order_items.append(order_item)
        
        # Update order total
        order_totals[order['order_id']] += total
        
        item_id += 1
    
    # Write to CSV
    filename = os.path.join(DATA_DIR, 'order_items.csv')
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=order_items[0].keys())
        writer.writeheader()
        writer.writerows(order_items)
    
    print(f"✓ Generated {len(order_items)} order items -> {filename}")
    
    # Update order totals in the orders list
    for order in orders:
        order['total_amount'] = round(order_totals[order['order_id']], 2)
    
    # Re-write orders CSV with updated totals
    filename = os.path.join(DATA_DIR, 'orders.csv')
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=orders[0].keys())
        writer.writeheader()
        writer.writerows(orders)
    
    return order_items


# ============================================================================
# 5. GENERATE PAYMENTS
# ============================================================================

def generate_payments(orders):
    """Generate payment records for each order."""
    payments = []
    
    payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Apple Pay', 'Google Pay', 'Bank Transfer']
    payment_statuses = ['Completed', 'Pending', 'Failed', 'Refunded']
    status_weights = [0.85, 0.05, 0.05, 0.05]
    
    for payment_id, order in enumerate(orders, start=1):
        # Payment date (same as order date or slightly after)
        order_date = datetime.strptime(order['order_date'], '%Y-%m-%d %H:%M:%S')
        payment_date = order_date + timedelta(minutes=random.randint(0, 30))
        
        status = random.choices(payment_statuses, weights=status_weights)[0]
        
        # Payment amount matches order total
        payment_amount = order['total_amount']
        
        # Add transaction fee (2-3% of amount)
        transaction_fee = round(payment_amount * random.uniform(0.02, 0.03), 2)
        
        payment = {
            'payment_id': payment_id,
            'order_id': order['order_id'],
            'payment_date': payment_date.strftime('%Y-%m-%d %H:%M:%S'),
            'payment_method': random.choice(payment_methods),
            'payment_amount': payment_amount,
            'transaction_fee': transaction_fee,
            'status': status,
            'transaction_id': fake.uuid4()[:16].upper()
        }
        payments.append(payment)
    
    # Write to CSV
    filename = os.path.join(DATA_DIR, 'payments.csv')
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=payments[0].keys())
        writer.writeheader()
        writer.writerows(payments)
    
    print(f"✓ Generated {len(payments)} payments -> {filename}")
    return payments


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function to generate all datasets."""
    print("\nStarting data generation...\n")
    
    # Generate all datasets in order
    customers = generate_customers()
    products = generate_products()
    orders = generate_orders(customers)
    order_items = generate_order_items(orders, products)
    payments = generate_payments(orders)
    
    print("\n" + "=" * 60)
    print("DATA GENERATION COMPLETE!")
    print("=" * 60)
    print(f"\nAll CSV files saved in '{DATA_DIR}/' directory:")
    print(f"  • customers.csv ({NUM_CUSTOMERS} records)")
    print(f"  • products.csv ({NUM_PRODUCTS} records)")
    print(f"  • orders.csv ({NUM_ORDERS} records)")
    print(f"  • order_items.csv ({len(order_items)} records)")
    print(f"  • payments.csv ({NUM_PAYMENTS} records)")
    print("\n✓ All datasets have proper FK relationships maintained")
    print("=" * 60)


if __name__ == "__main__":
    main()

