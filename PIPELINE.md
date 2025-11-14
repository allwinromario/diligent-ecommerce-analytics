# E-Commerce Data Pipeline Documentation

## Overview

This project implements a complete end-to-end data pipeline for e-commerce analytics:

```
CSV Generation → SQLite Loading → Multi-Table Queries → CSV Export
```

## Pipeline Architecture

### Orchestrator: `main.py`

The main orchestrator script automates all pipeline steps in sequence.

**Key Features:**
- ✅ Modular architecture (import existing scripts as modules)
- ✅ Command-line options for flexible execution
- ✅ Colored terminal output for better UX
- ✅ Comprehensive error handling
- ✅ Execution time tracking
- ✅ File verification and statistics

### Pipeline Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    MAIN.PY ORCHESTRATOR                     │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   STEP 1     │───▶│   STEP 2     │───▶│   STEP 3     │
│ Generate CSVs│    │  Load SQLite │    │ Run Queries  │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
  data/*.csv          ecommerce.db           output.csv
```

## Pipeline Steps

### Step 1: Data Generation (`generate_data.py`)

**Function:** Creates synthetic e-commerce datasets using Faker library

**Inputs:** None (uses random seed for reproducibility)

**Outputs:**
- `data/customers.csv` (100-300 records)
- `data/products.csv` (100-300 records)
- `data/orders.csv` (100-300 records)
- `data/order_items.csv` (150-300 records)
- `data/payments.csv` (one per order)

**Features:**
- Realistic data generation (names, emails, addresses, products)
- Proper foreign key relationships
- Business logic (discounts, fees, order statuses)
- Validation checks

**Execution Time:** ~0.1 seconds

### Step 2: Database Loading (`load_database.py`)

**Function:** Creates SQLite database and loads CSV data

**Inputs:**
- CSV files from `data/` directory

**Outputs:**
- `ecommerce.db` (~156 KB)

**Features:**
- Auto-schema detection from CSV headers
- Primary key constraints
- Foreign key constraints with CASCADE/RESTRICT
- Performance indexes (6 indexes)
- Data integrity verification
- Summary statistics

**Schema:**
```sql
customers (PK: customer_id)
    ↓ FK
orders (PK: order_id, FK: customer_id)
    ↓ FK                    ↓ FK
order_items (FK: order_id, product_id)    payments (FK: order_id)
    ↓ FK
products (PK: product_id)
```

**Execution Time:** ~0.02 seconds

### Step 3: Query Execution (Embedded in `main.py`)

**Function:** Executes multi-table SQL join query

**Inputs:**
- `ecommerce.db`

**Outputs:**
- `output.csv` (220 rows, 20 columns)

**Query Logic:**
```sql
SELECT 
    customer info,
    product info,
    order details,
    payment info,
    calculated transaction value
FROM customers
    INNER JOIN orders
    INNER JOIN order_items
    INNER JOIN products
    INNER JOIN payments
ORDER BY order_date DESC
```

**Features:**
- 5-table join across all entities
- Transaction value calculations
- Sorted by latest orders
- CSV export with headers

**Execution Time:** <0.1 seconds

## Command-Line Interface

### Basic Usage

```bash
# Run complete pipeline
python3 main.py
```

### Advanced Options

```bash
# Skip data generation (use existing CSV files)
python3 main.py --skip-data

# Skip database loading (use existing database)
python3 main.py --skip-load

# Only generate data and load database (no query)
python3 main.py --skip-query

# Show help
python3 main.py --help
```

### Use Cases

**Development Mode:**
```bash
# Generate new data and run full pipeline
python3 main.py
```

**Testing Mode:**
```bash
# Test database loading only
python3 main.py --skip-data --skip-query

# Test query execution only
python3 main.py --skip-data --skip-load
```

**Production Mode:**
```bash
# Generate fresh data and full pipeline
python3 main.py
```

## Output Formats

### Terminal Output

The orchestrator provides rich terminal output:
- ✅ **Colored headers** for visual organization
- ✅ **Step-by-step progress** (Step 1/4, 2/4, etc.)
- ✅ **Success/Error indicators** (✓ green, ✗ red, ⚠ yellow)
- ✅ **Execution summary** with timing
- ✅ **File statistics** (size, row counts)
- ✅ **Preview of results** (first 5 rows)

### CSV Output (`output.csv`)

**Format:** Standard CSV with headers

**Columns (20):**
1. customer_id
2. customer_name
3. customer_email
4. customer_segment
5. order_id
6. order_date
7. order_status
8. product_id
9. product_name
10. product_category
11. quantity
12. unit_price
13. discount
14. item_total
15. subtotal
16. transaction_value
17. payment_method
18. payment_status
19. transaction_fee
20. order_total

**Sample Row:**
```csv
14,David Fisher,lbyrd@example.net,New,56,2025-11-12,Pending,35,High Performance Consider Automotive,Automotive,5,419.61,0.0,2098.05,2098.05,2098.05,PayPal,Completed,115.52,4463.76
```

## Error Handling

### Validation Checks

1. **CSV File Existence:** Verifies all 5 CSV files were created
2. **Database Creation:** Confirms database file exists
3. **Table Population:** Validates row counts match CSV files
4. **Foreign Key Integrity:** Checks all FK relationships
5. **Query Execution:** Ensures query returns results

### Error Messages

```bash
# Data generation error
✗ Data generation failed: [error details]

# Database loading error
✗ Database loading failed: [error details]

# Query execution error
✗ Query execution failed: [error details]
```

### Exit Codes

- `0` - Success
- `1` - Pipeline failure
- `130` - User interrupt (Ctrl+C)

## Performance Metrics

**Full Pipeline Execution:**
- **Total Time:** ~0.75 seconds
- **Data Generation:** ~0.1 seconds
- **Database Loading:** ~0.02 seconds
- **Query Execution:** ~0.05 seconds
- **CSV Export:** ~0.05 seconds

**Data Volume:**
- **Total CSV Files:** 5 files, ~75 KB
- **Database Size:** ~156 KB
- **Output CSV:** ~39 KB
- **Total Rows:** 823 database rows → 220 result rows

## Production Deployment

### Prerequisites

```bash
python3 --version  # 3.7+
pip install -r requirements.txt
```

### Deployment Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/allwinromario/diligent-ecommerce-analytics.git
   cd diligent-ecommerce-analytics
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Pipeline**
   ```bash
   python3 main.py
   ```

4. **Verify Output**
   ```bash
   ls -lh output.csv ecommerce.db
   ```

### Automation

**Cron Job (Daily Execution):**
```bash
# Run pipeline daily at 2 AM
0 2 * * * cd /path/to/Diligent && python3 main.py >> logs/pipeline.log 2>&1
```

**Shell Script:**
```bash
#!/bin/bash
cd /path/to/Diligent
python3 main.py
if [ $? -eq 0 ]; then
    echo "Pipeline completed successfully"
    # Additional post-processing
else
    echo "Pipeline failed"
    # Send alert
fi
```

## Extensibility

### Adding New Steps

```python
def step_5_custom_analysis():
    """Step 5: Custom analysis logic."""
    print_step(5, 5, "Running custom analysis...")
    # Your code here
    return True
```

### Modifying Queries

Edit the SQL query in `step_3_run_query()` function in `main.py`:

```python
query = """
    SELECT 
        -- Add/modify columns
    FROM customers c
        -- Add/modify joins
    WHERE ...
    ORDER BY ...
"""
```

### Custom Export Formats

Add new export functions:

```python
def export_to_json(results, column_names):
    """Export results to JSON format."""
    import json
    data = [dict(zip(column_names, row)) for row in results]
    with open('output.json', 'w') as f:
        json.dump(data, f, indent=2)
```

## Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'faker'`
```bash
pip install faker pandas
```

**Issue:** Database is locked
```bash
# Close any SQLite connections
rm ecommerce.db
python3 main.py
```

**Issue:** Permission denied
```bash
chmod +x main.py
python3 main.py
```

## Best Practices

1. ✅ **Always run full pipeline** for consistency
2. ✅ **Version control output** if needed for tracking
3. ✅ **Monitor execution time** for performance regression
4. ✅ **Validate output CSV** before downstream processing
5. ✅ **Backup database** before schema changes
6. ✅ **Use --skip options** only for testing/development

## Monitoring

### Key Metrics to Track

- Pipeline execution time
- Data volume (row counts, file sizes)
- Error rates
- Query performance
- Disk usage

### Logging

Add logging to track pipeline execution:

```python
import logging

logging.basicConfig(
    filename='pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

---

**Last Updated:** November 14, 2025  
**Version:** 1.0  
**Maintainer:** Diligent Project Team

