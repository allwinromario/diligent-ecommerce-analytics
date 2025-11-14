"""
SQLite ETL Script - E-Commerce Data Loader

This script loads synthetic e-commerce data from CSV files into a SQLite database
with proper schema, primary keys, and foreign key relationships.
"""

import sqlite3
import csv
import os
from datetime import datetime

# Configuration
DATA_DIR = "data"
DB_NAME = "ecommerce.db"

# CSV file mappings
CSV_FILES = {
    'customers': 'customers.csv',
    'products': 'products.csv',
    'orders': 'orders.csv',
    'order_items': 'order_items.csv',
    'payments': 'payments.csv'
}

print("=" * 70)
print("E-COMMERCE DATABASE LOADER")
print("=" * 70)
print(f"Database: {DB_NAME}")
print(f"Source: {DATA_DIR}/ directory")
print("=" * 70)


def create_connection():
    """Create a database connection to SQLite database."""
    try:
        # Remove existing database if it exists
        if os.path.exists(DB_NAME):
            os.remove(DB_NAME)
            print(f"\n✓ Removed existing database: {DB_NAME}")
        
        conn = sqlite3.connect(DB_NAME)
        print(f"✓ Created new database: {DB_NAME}")
        
        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON")
        print("✓ Enabled foreign key constraints")
        
        return conn
    except sqlite3.Error as e:
        print(f"✗ Error connecting to database: {e}")
        return None


def create_tables(conn):
    """Create all tables with proper schema, primary keys, and foreign keys."""
    
    cursor = conn.cursor()
    
    print("\n" + "=" * 70)
    print("CREATING TABLES")
    print("=" * 70)
    
    # Table 1: Customers
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            country TEXT,
            created_at TIMESTAMP,
            customer_segment TEXT
        )
    """)
    print("✓ Created table: customers")
    
    # Table 2: Products
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            cost REAL,
            stock_quantity INTEGER DEFAULT 0,
            supplier TEXT,
            created_at TIMESTAMP,
            rating REAL CHECK(rating >= 0 AND rating <= 5)
        )
    """)
    print("✓ Created table: products")
    
    # Table 3: Orders
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TIMESTAMP NOT NULL,
            status TEXT NOT NULL,
            shipping_address TEXT,
            shipped_date TIMESTAMP,
            delivery_date TIMESTAMP,
            total_amount REAL DEFAULT 0.0,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
    """)
    print("✓ Created table: orders (FK: customer_id → customers)")
    
    # Table 4: Order Items
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            unit_price REAL NOT NULL,
            discount REAL DEFAULT 0.0,
            total REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products (product_id)
                ON DELETE RESTRICT
                ON UPDATE CASCADE
        )
    """)
    print("✓ Created table: order_items (FK: order_id → orders, product_id → products)")
    
    # Table 5: Payments
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL UNIQUE,
            payment_date TIMESTAMP NOT NULL,
            payment_method TEXT NOT NULL,
            payment_amount REAL NOT NULL,
            transaction_fee REAL DEFAULT 0.0,
            status TEXT NOT NULL,
            transaction_id TEXT UNIQUE,
            FOREIGN KEY (order_id) REFERENCES orders (order_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
    """)
    print("✓ Created table: payments (FK: order_id → orders)")
    
    # Create indexes for better query performance
    print("\n" + "-" * 70)
    print("CREATING INDEXES")
    print("-" * 70)
    
    cursor.execute("CREATE INDEX idx_orders_customer ON orders(customer_id)")
    print("✓ Created index: idx_orders_customer")
    
    cursor.execute("CREATE INDEX idx_orders_date ON orders(order_date)")
    print("✓ Created index: idx_orders_date")
    
    cursor.execute("CREATE INDEX idx_order_items_order ON order_items(order_id)")
    print("✓ Created index: idx_order_items_order")
    
    cursor.execute("CREATE INDEX idx_order_items_product ON order_items(product_id)")
    print("✓ Created index: idx_order_items_product")
    
    cursor.execute("CREATE INDEX idx_products_category ON products(category)")
    print("✓ Created index: idx_products_category")
    
    cursor.execute("CREATE INDEX idx_payments_order ON payments(order_id)")
    print("✓ Created index: idx_payments_order")
    
    conn.commit()


def load_csv_to_table(conn, table_name, csv_file):
    """Load data from CSV file into the specified table."""
    
    csv_path = os.path.join(DATA_DIR, csv_file)
    
    if not os.path.exists(csv_path):
        print(f"✗ CSV file not found: {csv_path}")
        return 0
    
    cursor = conn.cursor()
    row_count = 0
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            
            # Get column names from CSV header
            columns = csv_reader.fieldnames
            
            # Prepare INSERT statement
            placeholders = ','.join(['?' for _ in columns])
            column_names = ','.join(columns)
            insert_sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
            
            # Insert rows
            for row in csv_reader:
                # Convert empty strings to None for NULL values
                values = [val if val != '' else None for val in row.values()]
                cursor.execute(insert_sql, values)
                row_count += 1
        
        conn.commit()
        print(f"✓ Loaded {row_count:,} rows into {table_name}")
        return row_count
        
    except sqlite3.Error as e:
        print(f"✗ Error loading {table_name}: {e}")
        conn.rollback()
        return 0
    except Exception as e:
        print(f"✗ Unexpected error loading {table_name}: {e}")
        conn.rollback()
        return 0


def verify_data(conn):
    """Verify data integrity and foreign key relationships."""
    
    cursor = conn.cursor()
    
    print("\n" + "=" * 70)
    print("DATA VERIFICATION")
    print("=" * 70)
    
    # Row counts
    tables = ['customers', 'products', 'orders', 'order_items', 'payments']
    total_rows = 0
    
    print("\nTable Row Counts:")
    print("-" * 70)
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        total_rows += count
        print(f"  {table:<20} {count:>10,} rows")
    
    print("-" * 70)
    print(f"  {'TOTAL':<20} {total_rows:>10,} rows")
    
    # Foreign key integrity checks
    print("\n" + "-" * 70)
    print("Foreign Key Integrity Checks:")
    print("-" * 70)
    
    # Check orders -> customers
    cursor.execute("""
        SELECT COUNT(*) FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
    """)
    orphan_orders = cursor.fetchone()[0]
    status = "✓ PASS" if orphan_orders == 0 else f"✗ FAIL ({orphan_orders} orphans)"
    print(f"  orders → customers:     {status}")
    
    # Check order_items -> orders
    cursor.execute("""
        SELECT COUNT(*) FROM order_items oi
        LEFT JOIN orders o ON oi.order_id = o.order_id
        WHERE o.order_id IS NULL
    """)
    orphan_items = cursor.fetchone()[0]
    status = "✓ PASS" if orphan_items == 0 else f"✗ FAIL ({orphan_items} orphans)"
    print(f"  order_items → orders:   {status}")
    
    # Check order_items -> products
    cursor.execute("""
        SELECT COUNT(*) FROM order_items oi
        LEFT JOIN products p ON oi.product_id = p.product_id
        WHERE p.product_id IS NULL
    """)
    orphan_products = cursor.fetchone()[0]
    status = "✓ PASS" if orphan_products == 0 else f"✗ FAIL ({orphan_products} orphans)"
    print(f"  order_items → products: {status}")
    
    # Check payments -> orders
    cursor.execute("""
        SELECT COUNT(*) FROM payments p
        LEFT JOIN orders o ON p.order_id = o.order_id
        WHERE o.order_id IS NULL
    """)
    orphan_payments = cursor.fetchone()[0]
    status = "✓ PASS" if orphan_payments == 0 else f"✗ FAIL ({orphan_payments} orphans)"
    print(f"  payments → orders:      {status}")
    
    # Business logic checks
    print("\n" + "-" * 70)
    print("Business Logic Checks:")
    print("-" * 70)
    
    # Check order totals match sum of order items
    cursor.execute("""
        SELECT COUNT(*) FROM orders o
        WHERE ABS(o.total_amount - (
            SELECT COALESCE(SUM(oi.total), 0)
            FROM order_items oi
            WHERE oi.order_id = o.order_id
        )) > 0.01
    """)
    mismatched_totals = cursor.fetchone()[0]
    status = "✓ PASS" if mismatched_totals == 0 else f"⚠ WARNING ({mismatched_totals} mismatches)"
    print(f"  Order totals accurate:  {status}")
    
    # Check payment amounts match order totals
    cursor.execute("""
        SELECT COUNT(*) FROM payments p
        JOIN orders o ON p.order_id = o.order_id
        WHERE ABS(p.payment_amount - o.total_amount) > 0.01
    """)
    mismatched_payments = cursor.fetchone()[0]
    status = "✓ PASS" if mismatched_payments == 0 else f"⚠ WARNING ({mismatched_payments} mismatches)"
    print(f"  Payment amounts match:  {status}")


def generate_summary_stats(conn):
    """Generate summary statistics about the loaded data."""
    
    cursor = conn.cursor()
    
    print("\n" + "=" * 70)
    print("SUMMARY STATISTICS")
    print("=" * 70)
    
    # Customer segments distribution
    print("\nCustomer Segments:")
    cursor.execute("""
        SELECT customer_segment, COUNT(*) as count
        FROM customers
        GROUP BY customer_segment
        ORDER BY count DESC
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]:<15} {row[1]:>5} customers")
    
    # Product categories distribution
    print("\nProduct Categories:")
    cursor.execute("""
        SELECT category, COUNT(*) as count, 
               ROUND(AVG(price), 2) as avg_price
        FROM products
        GROUP BY category
        ORDER BY count DESC
        LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]:<25} {row[1]:>3} products (Avg: ${row[2]:,.2f})")
    
    # Order status distribution
    print("\nOrder Status:")
    cursor.execute("""
        SELECT status, COUNT(*) as count,
               ROUND(AVG(total_amount), 2) as avg_value
        FROM orders
        GROUP BY status
        ORDER BY count DESC
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]:<15} {row[1]:>5} orders (Avg: ${row[2]:,.2f})")
    
    # Payment methods distribution
    print("\nPayment Methods:")
    cursor.execute("""
        SELECT payment_method, COUNT(*) as count,
               ROUND(SUM(payment_amount), 2) as total_revenue
        FROM payments
        WHERE status = 'Completed'
        GROUP BY payment_method
        ORDER BY count DESC
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]:<20} {row[1]:>3} payments (${row[2]:,.2f})")
    
    # Overall metrics
    print("\nOverall Metrics:")
    cursor.execute("SELECT ROUND(SUM(total_amount), 2) FROM orders")
    total_revenue = cursor.fetchone()[0]
    print(f"  Total Revenue:          ${total_revenue:,.2f}")
    
    cursor.execute("SELECT ROUND(AVG(total_amount), 2) FROM orders")
    avg_order_value = cursor.fetchone()[0]
    print(f"  Average Order Value:    ${avg_order_value:,.2f}")
    
    cursor.execute("SELECT COUNT(DISTINCT customer_id) FROM orders")
    active_customers = cursor.fetchone()[0]
    print(f"  Active Customers:       {active_customers:,}")
    
    cursor.execute("SELECT ROUND(AVG(quantity), 2) FROM order_items")
    avg_quantity = cursor.fetchone()[0]
    print(f"  Avg Items per Line:     {avg_quantity}")


def main():
    """Main ETL process."""
    
    start_time = datetime.now()
    
    # Step 1: Create database connection
    print("\nStep 1: Creating database connection...")
    conn = create_connection()
    
    if not conn:
        print("✗ Failed to create database connection. Exiting.")
        return
    
    try:
        # Step 2: Create tables
        print("\nStep 2: Creating database schema...")
        create_tables(conn)
        
        # Step 3: Load data from CSV files
        print("\n" + "=" * 70)
        print("LOADING DATA FROM CSV FILES")
        print("=" * 70 + "\n")
        
        total_loaded = 0
        load_order = ['customers', 'products', 'orders', 'order_items', 'payments']
        
        for table_name in load_order:
            csv_file = CSV_FILES[table_name]
            rows = load_csv_to_table(conn, table_name, csv_file)
            total_loaded += rows
        
        print(f"\n{'─' * 70}")
        print(f"Total rows loaded: {total_loaded:,}")
        
        # Step 4: Verify data integrity
        verify_data(conn)
        
        # Step 5: Generate summary statistics
        generate_summary_stats(conn)
        
        # Final success message
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("\n" + "=" * 70)
        print("DATABASE CREATION COMPLETE!")
        print("=" * 70)
        print(f"Database file: {DB_NAME}")
        print(f"Total time: {duration:.2f} seconds")
        print(f"Status: ✓ SUCCESS")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Error during ETL process: {e}")
    
    finally:
        # Close connection
        if conn:
            conn.close()
            print("\n✓ Database connection closed")


if __name__ == "__main__":
    main()

