# Quick Start Guide

## 🚀 Run Complete Pipeline in One Command

```bash
python3 main.py
```

That's it! This single command will:
1. ✅ Generate synthetic e-commerce data (5 CSV files)
2. ✅ Create SQLite database with proper schema
3. ✅ Execute multi-table SQL join query  
4. ✅ Export results to `output.csv`

**Expected Output:**
```
===============================================================================
                 E-COMMERCE DATA PIPELINE - AUTOMATED EXECUTION                 
===============================================================================

[Step 1/4] Generating synthetic e-commerce data...
✓ customers.csv: 263 rows
✓ products.csv: 128 rows
✓ orders.csv: 106 rows
✓ order_items.csv: 220 rows
✓ payments.csv: 106 rows

[Step 2/4] Loading data into SQLite database...
✓ Database created: ecommerce.db
✓ Table 'customers': 263 rows
✓ Table 'products': 128 rows
✓ Table 'orders': 106 rows
✓ Table 'order_items': 220 rows
✓ Table 'payments': 106 rows

[Step 3/4] Executing multi-table SQL join query...
✓ Query executed successfully: 220 rows returned

[Step 4/4] Exporting results to CSV...
✓ Results exported to: output.csv

===============================================================================
                          PIPELINE EXECUTION COMPLETE                           
===============================================================================

✓ All steps completed successfully!

Total Duration:  0.75 seconds
```

---

## 📋 What Gets Created

| File | Description | Size | Rows |
|------|-------------|------|------|
| `data/customers.csv` | Customer data | ~35 KB | 263 |
| `data/products.csv` | Product catalog | ~12 KB | 128 |
| `data/orders.csv` | Order records | ~13 KB | 106 |
| `data/order_items.csv` | Line items | ~7 KB | 220 |
| `data/payments.csv` | Payment transactions | ~8 KB | 106 |
| `ecommerce.db` | SQLite database | ~156 KB | 823 |
| `output.csv` | Query results | ~39 KB | 220 |

---

## 🎯 View Results

```bash
# View first 10 rows of output
head -n 11 output.csv | column -t -s ','

# Query the database
sqlite3 ecommerce.db "SELECT * FROM customers LIMIT 5;"

# Count records
wc -l output.csv

# Check file sizes
ls -lh *.csv *.db
```

---

## ⚙️ Advanced Options

```bash
# Skip data generation (reuse existing CSV files)
python3 main.py --skip-data

# Skip database loading (reuse existing database)
python3 main.py --skip-load

# Only generate data and load database
python3 main.py --skip-query

# Show help
python3 main.py --help
```

---

## 🔧 Individual Steps (Optional)

If you prefer running steps individually:

```bash
# Step 1: Generate data
python3 generate_data.py

# Step 2: Load database
python3 load_database.py

# Step 3: Run analytics
python3 run_queries.py
```

---

## 📊 Sample Output Data

**output.csv** contains joined data from all 5 tables:

```csv
customer_name,product_name,quantity,total_price,payment_method,order_date
David Fisher,High Performance Consider Auto,5,2098.05,PayPal,2025-11-12
Jeremiah Norris,Formal Rest Clothing,9,1704.60,Google Pay,2025-11-11
Angela Ryan,Outdoor Work Sports,9,1421.73,PayPal,2025-11-10
...
```

---

## 🛠️ Prerequisites

```bash
# Python 3.7+
python3 --version

# Install dependencies
pip install -r requirements.txt
```

**requirements.txt:**
```
faker==20.1.0
pandas==2.1.4
```

---

## 📚 Next Steps

- **Explore database:** `sqlite3 ecommerce.db`
- **Run custom queries:** Edit `queries.sql`
- **Analyze results:** Import `output.csv` into Excel/Pandas
- **Modify pipeline:** Edit `main.py` for custom steps
- **Read documentation:** See `PIPELINE.md` for details

---

## ❓ Troubleshooting

**Issue:** `ModuleNotFoundError: No module named 'faker'`
```bash
pip install faker pandas
```

**Issue:** "Database is locked"
```bash
rm ecommerce.db
python3 main.py
```

**Issue:** Permission denied
```bash
chmod +x main.py
python3 main.py
```

---

## 📈 Expected Performance

- **Execution Time:** ~0.75 seconds
- **Data Generated:** ~75 KB CSV files
- **Database Size:** ~156 KB
- **Output Size:** ~39 KB
- **Total Rows:** 823 → 220 (after join)

---

## ✅ Success Indicators

You'll know the pipeline succeeded when you see:

1. ✓ All CSV files created in `data/` directory
2. ✓ `ecommerce.db` file exists (~156 KB)
3. ✓ `output.csv` file exists (~39 KB)
4. ✓ "All steps completed successfully!" message
5. ✓ Exit code 0

---

**For detailed documentation, see:**
- `README.md` - Project overview
- `PIPELINE.md` - Pipeline architecture
- `DATA_SUMMARY.md` - Dataset details

