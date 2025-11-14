"""
E-Commerce Analytics SQL Queries

This script executes analytical SQL queries on the e-commerce database
and displays results in formatted tables.
"""

import sqlite3
import sys

# Database configuration
DB_NAME = "ecommerce.db"


def create_connection():
    """Create a database connection to SQLite database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)


def print_table(headers, rows, title=None):
    """Print results as a formatted ASCII table."""
    
    if title:
        print("\n" + "=" * 120)
        print(f"{title:^120}")
        print("=" * 120)
    
    if not rows:
        print("\nNo results found.")
        return
    
    # Calculate column widths
    col_widths = [len(str(header)) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)) if cell is not None else 4)
    
    # Print header
    print()
    header_line = " | ".join(str(headers[i]).ljust(col_widths[i]) for i in range(len(headers)))
    print(header_line)
    print("-" * len(header_line))
    
    # Print rows
    for row in rows:
        row_line = " | ".join(
            str(cell).ljust(col_widths[i]) if cell is not None else "NULL".ljust(col_widths[i])
            for i, cell in enumerate(row)
        )
        print(row_line)
    
    print(f"\nTotal rows: {len(rows)}")
    print("=" * 120)


def query_full_transaction_details():
    """
    Query 1: Complete Transaction Details
    
    Joins all 5 tables to show complete transaction information including:
    - Customer information
    - Product details
    - Order quantities and pricing
    - Payment method
    - Transaction dates
    
    Calculates total transaction value per order item and orders by latest date.
    """
    
    query = """
    SELECT 
        -- Customer Information
        c.customer_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        c.email AS customer_email,
        c.customer_segment,
        
        -- Order Information
        o.order_id,
        DATE(o.order_date) AS order_date,
        o.status AS order_status,
        
        -- Product Information
        p.product_id,
        p.product_name,
        p.category AS product_category,
        
        -- Order Item Details
        oi.quantity,
        ROUND(oi.unit_price, 2) AS unit_price,
        ROUND(oi.discount, 2) AS discount,
        ROUND(oi.total, 2) AS item_total,
        
        -- Transaction Value Calculation
        ROUND(oi.quantity * oi.unit_price, 2) AS subtotal,
        ROUND(oi.quantity * oi.unit_price - oi.discount, 2) AS transaction_value,
        
        -- Payment Information
        py.payment_method,
        py.status AS payment_status,
        ROUND(py.transaction_fee, 2) AS transaction_fee,
        
        -- Order Summary
        ROUND(o.total_amount, 2) AS order_total
        
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    INNER JOIN products p ON oi.product_id = p.product_id
    INNER JOIN payments py ON o.order_id = py.order_id
    
    ORDER BY o.order_date DESC, o.order_id, oi.order_item_id
    """
    
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        headers = [
            "Customer ID", "Customer Name", "Email", "Segment",
            "Order ID", "Order Date", "Status",
            "Product ID", "Product Name", "Category",
            "Qty", "Unit Price", "Discount", "Item Total",
            "Subtotal", "Transaction Value",
            "Payment Method", "Payment Status", "Fee", "Order Total"
        ]
        
        print_table(headers, results, "COMPLETE TRANSACTION DETAILS - ALL TABLES JOINED")
        
        return results
        
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        conn.close()


def query_simplified_transaction_view():
    """
    Query 2: Simplified Transaction View (As Requested)
    
    Clean, readable output with essential columns:
    - Customer name
    - Product name  
    - Quantity
    - Total price (transaction value)
    - Payment method
    - Order date
    """
    
    query = """
    SELECT 
        c.first_name || ' ' || c.last_name AS customer_name,
        p.product_name,
        oi.quantity,
        ROUND(oi.total, 2) AS total_price,
        py.payment_method,
        DATE(o.order_date) AS order_date
        
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    INNER JOIN products p ON oi.product_id = p.product_id
    INNER JOIN payments py ON o.order_id = py.order_id
    
    ORDER BY o.order_date DESC
    """
    
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        headers = [
            "Customer Name",
            "Product Name",
            "Quantity",
            "Total Price",
            "Payment Method",
            "Order Date"
        ]
        
        print_table(headers, results, "SIMPLIFIED TRANSACTION VIEW - ESSENTIAL COLUMNS")
        
        return results
        
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        conn.close()


def query_revenue_by_category():
    """Query 3: Revenue Analysis by Product Category"""
    
    query = """
    SELECT 
        p.category,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.quantity) AS total_units_sold,
        ROUND(SUM(oi.total), 2) AS total_revenue,
        ROUND(AVG(oi.total), 2) AS avg_transaction_value,
        ROUND(SUM(oi.discount), 2) AS total_discounts
        
    FROM products p
    INNER JOIN order_items oi ON p.product_id = oi.product_id
    INNER JOIN orders o ON oi.order_id = o.order_id
    
    GROUP BY p.category
    ORDER BY total_revenue DESC
    """
    
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        headers = [
            "Category",
            "Total Orders",
            "Units Sold",
            "Total Revenue",
            "Avg Transaction",
            "Total Discounts"
        ]
        
        print_table(headers, results, "REVENUE ANALYSIS BY PRODUCT CATEGORY")
        
        return results
        
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        conn.close()


def query_customer_lifetime_value():
    """Query 4: Customer Lifetime Value Analysis"""
    
    query = """
    SELECT 
        c.customer_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        c.customer_segment,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.quantity) AS total_items_purchased,
        ROUND(SUM(oi.total), 2) AS lifetime_value,
        ROUND(AVG(o.total_amount), 2) AS avg_order_value,
        MAX(DATE(o.order_date)) AS last_order_date
        
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    
    GROUP BY c.customer_id, c.first_name, c.last_name, c.customer_segment
    ORDER BY lifetime_value DESC
    LIMIT 20
    """
    
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        headers = [
            "Customer ID",
            "Customer Name",
            "Segment",
            "Total Orders",
            "Items Purchased",
            "Lifetime Value",
            "Avg Order Value",
            "Last Order Date"
        ]
        
        print_table(headers, results, "TOP 20 CUSTOMERS BY LIFETIME VALUE")
        
        return results
        
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        conn.close()


def query_payment_method_analysis():
    """Query 5: Payment Method Performance Analysis"""
    
    query = """
    SELECT 
        py.payment_method,
        COUNT(DISTINCT o.order_id) AS total_transactions,
        ROUND(SUM(py.payment_amount), 2) AS total_amount,
        ROUND(AVG(py.payment_amount), 2) AS avg_transaction_amount,
        ROUND(SUM(py.transaction_fee), 2) AS total_fees,
        ROUND(AVG(py.transaction_fee), 2) AS avg_fee_per_transaction,
        COUNT(CASE WHEN py.status = 'Completed' THEN 1 END) AS successful_payments,
        COUNT(CASE WHEN py.status = 'Failed' THEN 1 END) AS failed_payments,
        ROUND(
            COUNT(CASE WHEN py.status = 'Completed' THEN 1 END) * 100.0 / COUNT(*), 
            2
        ) AS success_rate_percent
        
    FROM payments py
    INNER JOIN orders o ON py.order_id = o.order_id
    
    GROUP BY py.payment_method
    ORDER BY total_amount DESC
    """
    
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        headers = [
            "Payment Method",
            "Transactions",
            "Total Amount",
            "Avg Amount",
            "Total Fees",
            "Avg Fee",
            "Successful",
            "Failed",
            "Success Rate %"
        ]
        
        print_table(headers, results, "PAYMENT METHOD PERFORMANCE ANALYSIS")
        
        return results
        
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        conn.close()


def main():
    """Main function to run all queries."""
    
    print("\n" + "=" * 120)
    print("E-COMMERCE DATABASE ANALYTICS".center(120))
    print(f"Database: {DB_NAME}".center(120))
    print("=" * 120)
    
    # Check if database exists
    import os
    if not os.path.exists(DB_NAME):
        print(f"\n✗ Error: Database '{DB_NAME}' not found!")
        print("Please run 'python3 load_database.py' first to create the database.")
        sys.exit(1)
    
    print("\nRunning analytical queries...")
    
    # Query 1: Simplified view (as requested)
    print("\n[1/5] Running simplified transaction view query...")
    query_simplified_transaction_view()
    
    # Query 2: Complete details
    print("\n[2/5] Running complete transaction details query...")
    query_full_transaction_details()
    
    # Query 3: Revenue by category
    print("\n[3/5] Running revenue analysis query...")
    query_revenue_by_category()
    
    # Query 4: Customer lifetime value
    print("\n[4/5] Running customer lifetime value query...")
    query_customer_lifetime_value()
    
    # Query 5: Payment method analysis
    print("\n[5/5] Running payment method analysis query...")
    query_payment_method_analysis()
    
    print("\n" + "=" * 120)
    print("ALL QUERIES COMPLETED SUCCESSFULLY".center(120))
    print("=" * 120 + "\n")


if __name__ == "__main__":
    main()

