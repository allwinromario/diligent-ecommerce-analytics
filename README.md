# Diligent - Synthetic E-Commerce Data Pipeline

<div align="center">

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**An automated data engineering pipeline for e-commerce analytics**

[Quick Start](#quick-start) • [Documentation](#documentation) • [Tech Stack](#tech-stack-used)

</div>

---

## 📋 Project Overview

**Diligent** is a complete end-to-end data pipeline that demonstrates modern data engineering practices for e-commerce analytics. The project automatically generates synthetic transaction data, loads it into a relational database, and executes complex analytical queries—all with a single command.

### What This Project Does

This pipeline simulates a real-world e-commerce data warehouse workflow:

1. **Generates Realistic Data** - Creates synthetic customer, product, order, and payment records using the Faker library
2. **Builds a Database** - Loads data into SQLite with proper schemas, primary keys, foreign keys, and indexes
3. **Runs Analytics** - Executes multi-table SQL joins to generate business insights
4. **Exports Results** - Saves query output to CSV for further analysis

### Purpose

The primary goal is to create **realistic e-commerce datasets** and demonstrate **analytical data joins** across multiple related tables. This project is useful for:

- Learning data engineering workflows
- Testing SQL queries on realistic data
- Prototyping e-commerce analytics pipelines
- Demonstrating ETL (Extract, Transform, Load) processes
- Portfolio demonstration of data engineering skills

---

## 💡 Cursor Prompts Used

This project was built entirely using **Cursor AI** with strategic prompts. Below are all the prompts used, organized by development phase for easy replication.

### Phase 1: Git Setup & Initial Project Structure

```
You are my Git assistant. 

1. Initialize a new Git repository in this folder. 
2. Create a README.md describing this project (synthetic e-commerce data generation + SQLite ingestion + SQL queries). 
3. Create a .gitignore for Python projects. 
4. Connect this project to a new GitHub repository (ask me only for repo name and GitHub token). 
5. Commit all files with message "Initial commit - setup project". 
6. Push the code to the main branch and confirm successful push.
```
*Creates Git repository, initial README, .gitignore, and connects to GitHub*

---

### Phase 2: Synthetic Data Generation

```
Generate Python code that produces synthetic e-commerce datasets. 

1. Create 5 CSV files: customers, products, orders, order_items, payments. 
2. Use Faker for names, dates, emails, phone numbers, addresses. 
3. Each file must have 100–300 records with realistic relationships. 
4. Add random but meaningful values (quantities, prices, payment modes). 
5. Save all CSVs in a /data folder. 
6. Ensure primary–foreign key consistency across all datasets.
```
*Generates `generate_data.py` script with Faker library for realistic synthetic data*

---

### Phase 3: Database ETL (SQLite Ingestion)

```
Generate Python ETL code to ingest all 5 CSV files into an SQLite database. 

1. Create ecommerce.db. 
2. Create tables: customers, products, orders, order_items, payments. 
3. Auto-detect schema from CSV headers. 
4. Insert all rows from each CSV into their respective tables. 
5. Add primary keys and foreign keys exactly matching the synthetic data. 
6. Print row counts after loading to verify success.
```
*Creates `load_database.py` script for automated ETL with schema detection*

---

### Phase 4: SQL Multi-Table Joins

```
Create an SQL query that joins multiple tables in ecommerce.db. 

1. Join customers → orders → order_items → products → payments. 
2. Output customer name, product name, quantity, total price, payment method, order date. 
3. Calculate total transaction value per order item. 
4. Order results by latest order date. 
5. Return a clean and readable SQL query. 
6. Also generate Python code that executes this SQL and prints results as a table.
```
*Creates `run_queries.py` and `queries.sql` with multi-table join queries*

---

### Phase 5: Pipeline Automation

```
Combine all steps into a single automation:
1. Generate synthetic e-commerce CSV files. 
2. Build and load them into SQLite. 
3. Run the multi-table SQL join query. 
4. Save output as output.csv. 
5. Create a main.py that runs all pipelines in sequence. 
6. Ensure the full project structure is production-clean.
```
*Creates `main.py` orchestrator for one-command pipeline execution*

---

### Phase 6: Comprehensive Documentation

```
Create documentation for this project:

1. Overview: synthetic e-commerce workflow. 
2. Files generated and their schema. 
3. Steps: Data generation → SQLite ingestion → SQL querying. 
4. How to run main.py. 
5. How to push to GitHub. 
6. Provide a professional README.md with instructions and examples.
```
*Creates comprehensive README.md, PIPELINE.md, QUICKSTART.md, DEPLOYMENT.md*

---

### Phase 7: README Enhancement

```
Update the README.md with a complete project overview:

1. Add a clear explanation of the Synthetic E-Commerce Data Pipeline project.
2. Include sections: Data Generation, SQLite Ingestion, SQL Queries, and Output.
3. Describe the purpose: creating realistic datasets and running analytical joins.
4. Document the folder structure: /data, /scripts, main.py, ecommerce.db, output.csv.
5. Add a "Tech Stack Used" section (Python, Faker, SQLite, Cursor).
6. Ensure the README is simple, clean, and professional.
```
*Restructures README.md with clearer sections and professional formatting*

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/allwinromario/diligent-ecommerce-analytics.git
cd diligent-ecommerce-analytics

# Install dependencies
pip install -r requirements.txt

# Run complete pipeline (one command!)
python3 main.py
```

**That's it!** The pipeline will automatically:
- Generate 5 CSV files with synthetic data (~800 rows)
- Create SQLite database with proper schema
- Execute multi-table SQL queries
- Export results to `output.csv`

**Execution Time:** ~0.75 seconds

---

### 4. Output

**File:** `output.csv` (~39 KB, 220 rows)

The query results are exported to CSV format with complete transaction details.

**Output Columns (20):**
- Customer info: ID, name, email, segment
- Product info: ID, name, category
- Order details: ID, date, status, total
- Transaction: quantity, price, discount, value
- Payment: method, status, fee

**Sample Output:**
```csv
customer_name,product_name,quantity,total_price,payment_method,order_date
David Fisher,High Performance Automotive,5,2098.05,PayPal,2025-11-12
Jeremiah Norris,Formal Rest Clothing,9,1704.60,Google Pay,2025-11-11
```

---

## 📁 Project Structure

```
diligent-ecommerce-analytics/
│
├── 📂 data/                      # Generated CSV files
│   ├── customers.csv             # Customer master data
│   ├── products.csv              # Product catalog
│   ├── orders.csv                # Order transactions
│   ├── order_items.csv           # Order line items
│   └── payments.csv              # Payment records
│
├── 🚀 main.py                    # Pipeline orchestrator (435 lines)
├── 📊 generate_data.py           # Data generation (340 lines)
├── 💾 load_database.py           # Database ETL (465 lines)
├── 📈 run_queries.py             # Query executor (403 lines)
├── 🔍 queries.sql                # SQL library (10 queries)
│
├── 🗄️ ecommerce.db               # SQLite database (~156 KB)
├── 📄 output.csv                 # Query results (~39 KB)
│
├── 📋 requirements.txt           # Python dependencies
├── 📝 README.md                  # This file
├── 📖 PIPELINE.md                # Architecture documentation
├── ⚡ QUICKSTART.md              # Quick reference
├── 📊 DATA_SUMMARY.md            # Dataset details
├── 🔒 .gitignore                 # Git ignore rules
└── 📜 LICENSE                    # MIT License
```

**Code Statistics:**
- Python: 1,643 lines (4 scripts)
- SQL: 253 lines (10 queries)
- Documentation: 1,500+ lines (6 files)
- **Total: 3,400+ lines**

---

## 🛠️ Tech Stack Used

### Programming Languages
- **Python 3.7+** - Core programming language for data generation and ETL

### Libraries & Tools
- **Faker 20.1.0** - Generates realistic synthetic data (names, emails, addresses, dates)
- **Pandas 2.1.4** - Data manipulation and CSV operations
- **SQLite 3** - Lightweight relational database (built into Python)

### Development Tools
- **Cursor** - AI-powered code editor used for development
- **Git** - Version control
- **GitHub** - Code repository hosting

### Data Pipeline Components
- **CSV** - Data storage format (human-readable)
- **SQL** - Query language for data analysis
- **SQLite** - Embedded database engine

### Key Technologies
```
┌─────────────────┐
│     Python      │ → Core language
└────────┬────────┘
         │
    ┌────▼────┐
    │  Faker  │ → Synthetic data generation
    └────┬────┘
         │
    ┌────▼────┐
    │ Pandas  │ → Data manipulation
    └────┬────┘
         │
    ┌────▼────┐
    │ SQLite  │ → Relational database
    └────┬────┘
         │
    ┌────▼────┐
    │   CSV   │ → Output format
    └─────────┘
```

---

## 💻 Usage Examples

### Complete Pipeline (Recommended)

```bash
# Run all steps automatically
python3 main.py
```

**Output:**
```
✓ Generated 5 CSV files (823 rows)
✓ Created SQLite database (156 KB)
✓ Executed SQL queries (220 results)
✓ Exported to output.csv

Total time: 0.75 seconds
```

### Individual Steps

```bash
# Step 1: Generate data only
python3 generate_data.py

# Step 2: Load database only
python3 load_database.py

# Step 3: Run queries only
python3 run_queries.py

# Step 4: Query database directly
sqlite3 ecommerce.db "SELECT * FROM customers LIMIT 5;"
```

### Advanced Options

```bash
# Skip data generation (reuse existing CSVs)
python3 main.py --skip-data

# Skip database loading (reuse existing DB)
python3 main.py --skip-load

# Only run query and export
python3 main.py --skip-data --skip-load

# Show help
python3 main.py --help
```

---

## 🗄️ Database Schema

### Tables

| Table | Rows | Primary Key | Foreign Keys |
|-------|------|-------------|--------------|
| `customers` | 263 | customer_id | - |
| `products` | 128 | product_id | - |
| `orders` | 106 | order_id | customer_id |
| `order_items` | 220 | order_item_id | order_id, product_id |
| `payments` | 106 | payment_id | order_id |
| **Total** | **823** | **5 PKs** | **4 FKs** |

### Relationships

```
┌──────────────┐
│  CUSTOMERS   │
│  (PK: id)    │
└──────┬───────┘
       │ 1:N
       ▼
┌──────────────┐         ┌─────────────┐
│   ORDERS     │ 1:1     │  PAYMENTS   │
│  (PK: id)    ├────────►│  (PK: id)   │
│  (FK: cust)  │         │  (FK: order)│
└──────┬───────┘         └─────────────┘
       │ 1:N
       ▼
┌──────────────┐
│ ORDER_ITEMS  │
│  (PK: id)    │
│  (FK: order) │
│  (FK: prod)  ├─────┐
└──────────────┘     │
                     │ N:1
                     ▼
              ┌──────────────┐
              │   PRODUCTS   │
              │   (PK: id)   │
              └──────────────┘
```


---

## 🔧 Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

```bash
# Clone repository
git clone https://github.com/allwinromario/diligent-ecommerce-analytics.git
cd diligent-ecommerce-analytics

# Install dependencies
pip install -r requirements.txt

# Verify installation
python3 main.py --help
```

### Dependencies

```txt
faker==20.1.0    # Synthetic data generation
pandas==2.1.4    # Data manipulation
```

---

## 🧪 Testing

### Verify Installation

```bash
# Test complete pipeline
python3 main.py

# Verify outputs
ls -lh data/*.csv
ls -lh ecommerce.db output.csv

# Check database
sqlite3 ecommerce.db ".tables"
```

### Expected Results

✅ 5 CSV files in `data/` directory  
✅ `ecommerce.db` file (~156 KB)  
✅ `output.csv` file (~39 KB, 220 rows)  
✅ No errors during execution  
✅ Total time < 1 second

---

## 🐙 GitHub Deployment

### Push to GitHub

```bash
# Stage all changes
git add .

# Commit with message
git commit -m "Add comprehensive e-commerce data pipeline"

# Push to main branch
git push origin main
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👤 Author

**Allwin Romario**

- GitHub: [@allwinromario](https://github.com/allwinromario)
- Repository: [diligent-ecommerce-analytics](https://github.com/allwinromario/diligent-ecommerce-analytics)

---

## 🙏 Acknowledgments

- **Faker** - Synthetic data generation library
- **SQLite** - Lightweight database engine
- **Pandas** - Data manipulation tools
- **Cursor** - AI-powered development environment

---

<div align="center">

**⭐ If you find this project helpful, please star the repository!**

Made with ❤️ by [Allwin Romario](https://github.com/allwinromario)

</div>
