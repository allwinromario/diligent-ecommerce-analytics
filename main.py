"""
E-Commerce Data Pipeline - Main Orchestrator

This script automates the complete data pipeline:
1. Generate synthetic e-commerce CSV files
2. Load data into SQLite database
3. Run analytical SQL queries
4. Export results to output.csv

Usage:
    python3 main.py [--skip-data] [--skip-load] [--skip-query]
    
Options:
    --skip-data     Skip data generation (use existing CSV files)
    --skip-load     Skip database loading (use existing database)
    --skip-query    Skip query execution (only generate and load)
    --help          Show this help message
"""

import sys
import os
import subprocess
import sqlite3
import csv
from datetime import datetime
import argparse


# ============================================================================
# CONFIGURATION
# ============================================================================

DATA_DIR = "data"
DB_NAME = "ecommerce.db"
OUTPUT_FILE = "output.csv"

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def print_header(message):
    """Print a formatted header message."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{message.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.END}\n")


def print_step(step_num, total_steps, message):
    """Print a step message."""
    print(f"{Colors.BOLD}{Colors.BLUE}[Step {step_num}/{total_steps}]{Colors.END} {message}")


def print_success(message):
    """Print a success message."""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_error(message):
    """Print an error message."""
    print(f"{Colors.RED}✗ {message}{Colors.END}")


def print_warning(message):
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")


def print_info(message):
    """Print an info message."""
    print(f"  {message}")


# ============================================================================
# PIPELINE STEPS
# ============================================================================

def step_1_generate_data():
    """Step 1: Generate synthetic e-commerce CSV files."""
    print_step(1, 4, "Generating synthetic e-commerce data...")
    
    try:
        # Import and run the data generation module
        import generate_data
        
        print_info("Initializing data generator...")
        
        # Call the main function from generate_data
        generate_data.main()
        
        # Verify CSV files were created
        csv_files = ['customers.csv', 'products.csv', 'orders.csv', 
                     'order_items.csv', 'payments.csv']
        
        for csv_file in csv_files:
            file_path = os.path.join(DATA_DIR, csv_file)
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                with open(file_path, 'r') as f:
                    row_count = sum(1 for _ in f) - 1  # Exclude header
                print_success(f"{csv_file}: {row_count} rows ({file_size:,} bytes)")
            else:
                print_error(f"{csv_file}: NOT FOUND")
                return False
        
        return True
        
    except Exception as e:
        print_error(f"Data generation failed: {e}")
        return False


def step_2_load_database():
    """Step 2: Load CSV data into SQLite database."""
    print_step(2, 4, "Loading data into SQLite database...")
    
    try:
        # Import and run the database loading module
        import load_database
        
        print_info("Creating database schema and loading data...")
        
        # Call the main function from load_database
        load_database.main()
        
        # Verify database was created
        if os.path.exists(DB_NAME):
            db_size = os.path.getsize(DB_NAME)
            print_success(f"Database created: {DB_NAME} ({db_size:,} bytes)")
            
            # Verify table counts
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            tables = ['customers', 'products', 'orders', 'order_items', 'payments']
            total_rows = 0
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                total_rows += count
                print_success(f"Table '{table}': {count} rows")
            
            print_info(f"Total rows in database: {total_rows}")
            conn.close()
            
            return True
        else:
            print_error("Database file not created")
            return False
        
    except Exception as e:
        print_error(f"Database loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def step_3_run_query():
    """Step 3: Run multi-table SQL join query."""
    print_step(3, 4, "Executing multi-table SQL join query...")
    
    try:
        if not os.path.exists(DB_NAME):
            print_error(f"Database '{DB_NAME}' not found. Run with --skip-query=false")
            return False
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # The main multi-table join query
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
        
        print_info("Running multi-table join (customers → orders → order_items → products → payments)...")
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Get column names
        column_names = [description[0] for description in cursor.description]
        
        conn.close()
        
        print_success(f"Query executed successfully: {len(results)} rows returned")
        print_info(f"Columns: {len(column_names)}")
        
        return results, column_names
        
    except Exception as e:
        print_error(f"Query execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def step_4_export_csv(results, column_names):
    """Step 4: Export query results to CSV."""
    print_step(4, 4, "Exporting results to CSV...")
    
    try:
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(column_names)
            
            # Write data rows
            writer.writerows(results)
        
        # Get file stats
        file_size = os.path.getsize(OUTPUT_FILE)
        row_count = len(results)
        
        print_success(f"Results exported to: {OUTPUT_FILE}")
        print_info(f"Rows exported: {row_count}")
        print_info(f"File size: {file_size:,} bytes")
        print_info(f"Columns: {len(column_names)}")
        
        # Display first few rows as preview
        print("\n" + Colors.BOLD + "Preview (first 5 rows):" + Colors.END)
        print("-" * 80)
        
        # Print headers
        header_line = " | ".join(col[:15] for col in column_names[:8])
        print(header_line)
        print("-" * 80)
        
        # Print first 5 rows (limited columns for readability)
        for row in results[:5]:
            row_line = " | ".join(str(val)[:15] if val else "NULL" for val in row[:8])
            print(row_line)
        
        print("-" * 80)
        print(f"... ({row_count - 5} more rows)")
        
        return True
        
    except Exception as e:
        print_error(f"CSV export failed: {e}")
        return False


# ============================================================================
# PIPELINE ORCHESTRATION
# ============================================================================

def run_pipeline(args):
    """Run the complete data pipeline."""
    
    start_time = datetime.now()
    
    print_header("E-COMMERCE DATA PIPELINE - AUTOMATED EXECUTION")
    
    print(f"{Colors.BOLD}Pipeline Configuration:{Colors.END}")
    print(f"  Data Directory:  {DATA_DIR}/")
    print(f"  Database:        {DB_NAME}")
    print(f"  Output File:     {OUTPUT_FILE}")
    print(f"  Skip Data Gen:   {args.skip_data}")
    print(f"  Skip DB Load:    {args.skip_load}")
    print(f"  Skip Query:      {args.skip_query}")
    
    success = True
    
    # Step 1: Generate Data
    if not args.skip_data:
        if not step_1_generate_data():
            print_error("Pipeline failed at Step 1: Data Generation")
            return False
    else:
        print_warning("Skipping Step 1: Data Generation (using existing CSV files)")
    
    # Step 2: Load Database
    if not args.skip_load:
        if not step_2_load_database():
            print_error("Pipeline failed at Step 2: Database Loading")
            return False
    else:
        print_warning("Skipping Step 2: Database Loading (using existing database)")
    
    # Step 3: Run Query
    if not args.skip_query:
        query_result = step_3_run_query()
        if query_result is False:
            print_error("Pipeline failed at Step 3: Query Execution")
            return False
        
        results, column_names = query_result
        
        # Step 4: Export to CSV
        if not step_4_export_csv(results, column_names):
            print_error("Pipeline failed at Step 4: CSV Export")
            return False
    else:
        print_warning("Skipping Steps 3-4: Query Execution and CSV Export")
    
    # Pipeline complete
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print_header("PIPELINE EXECUTION COMPLETE")
    
    print(f"{Colors.BOLD}{Colors.GREEN}✓ All steps completed successfully!{Colors.END}\n")
    print(f"Execution Summary:")
    print(f"  Start Time:      {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  End Time:        {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Total Duration:  {duration:.2f} seconds")
    
    print(f"\n{Colors.BOLD}Generated Files:{Colors.END}")
    
    # List generated files
    files_to_check = [
        (DB_NAME, "SQLite Database"),
        (OUTPUT_FILE, "Query Results CSV"),
        (os.path.join(DATA_DIR, "customers.csv"), "Customers Data"),
        (os.path.join(DATA_DIR, "products.csv"), "Products Data"),
        (os.path.join(DATA_DIR, "orders.csv"), "Orders Data"),
        (os.path.join(DATA_DIR, "order_items.csv"), "Order Items Data"),
        (os.path.join(DATA_DIR, "payments.csv"), "Payments Data"),
    ]
    
    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"  ✓ {description:<25} {file_path:<30} ({file_size:>10,} bytes)")
        else:
            print(f"  ✗ {description:<25} {file_path:<30} (NOT FOUND)")
    
    print(f"\n{Colors.BOLD}Next Steps:{Colors.END}")
    print(f"  • View results:    cat {OUTPUT_FILE}")
    print(f"  • Query database:  sqlite3 {DB_NAME}")
    print(f"  • Run analytics:   python3 run_queries.py")
    
    return True


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for the pipeline."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='E-Commerce Data Pipeline - Automated Execution',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py                    # Run complete pipeline
  python3 main.py --skip-data        # Skip data generation
  python3 main.py --skip-load        # Skip database loading
  python3 main.py --skip-data --skip-load  # Only run query
        """
    )
    
    parser.add_argument('--skip-data', action='store_true',
                        help='Skip data generation (use existing CSV files)')
    parser.add_argument('--skip-load', action='store_true',
                        help='Skip database loading (use existing database)')
    parser.add_argument('--skip-query', action='store_true',
                        help='Skip query execution (only generate and load)')
    
    args = parser.parse_args()
    
    # Run the pipeline
    try:
        success = run_pipeline(args)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_error("\n\nPipeline interrupted by user (Ctrl+C)")
        sys.exit(130)
    except Exception as e:
        print_error(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

