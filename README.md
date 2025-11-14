# Diligent - E-Commerce Data Analytics

A comprehensive data engineering project for generating synthetic e-commerce data, storing it in SQLite, and performing analytical queries.

## Overview

This project demonstrates a complete data pipeline workflow:
- **Synthetic Data Generation**: Creates realistic e-commerce transaction data
- **SQLite Database**: Ingests and stores data in a relational database
- **SQL Analytics**: Performs complex queries for business insights

## Features

- Generate synthetic customer, product, and order data
- Automated database schema creation and data ingestion
- Pre-built SQL queries for common e-commerce analytics:
  - Sales trends and revenue analysis
  - Customer behavior patterns
  - Product performance metrics
  - Inventory tracking

## Tech Stack

- **Python**: Core programming language
- **SQLite**: Lightweight relational database
- **Faker** (if applicable): Synthetic data generation
- **Pandas** (if applicable): Data manipulation

## Getting Started

### Prerequisites

- Python 3.7+
- pip package manager

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd Diligent

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Run the data generation script
python generate_data.py

# Execute SQL queries
python run_queries.py
```

## Project Structure

```
Diligent/
├── data/              # Generated data files
├── database/          # SQLite database files
├── queries/           # SQL query scripts
├── scripts/           # Python scripts
└── README.md
```

## License

This project is licensed under the MIT License.

## Author

Diligent - Data Engineering Project

