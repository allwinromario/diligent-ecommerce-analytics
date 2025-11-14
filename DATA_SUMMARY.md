# Generated E-Commerce Data Summary

## Dataset Overview

This document provides a summary of the synthetic e-commerce datasets generated for the Diligent project.

### Generated Files

| File | Records | Size | Description |
|------|---------|------|-------------|
| customers.csv | 263 | 35 KB | Customer master data with demographics |
| products.csv | 128 | 12 KB | Product catalog with pricing and inventory |
| orders.csv | 106 | 13 KB | Order transactions with shipping details |
| order_items.csv | 220 | 6.6 KB | Line items for each order |
| payments.csv | 106 | 8.1 KB | Payment records for each order |

### Data Characteristics

#### Customers
- **Customer Segments**: Regular, Premium, VIP, New
- **Geographic Coverage**: USA (all 50 states)
- **Time Range**: Created over the last 2 years
- **Attributes**: Full contact information, address, phone, email

#### Products
- **Categories**: 10 distinct categories
  - Electronics ($50-$2,000)
  - Clothing ($15-$200)
  - Home & Kitchen ($10-$500)
  - Books ($5-$50)
  - Sports & Outdoors ($20-$300)
  - Beauty & Personal Care ($8-$100)
  - Toys & Games ($10-$150)
  - Automotive ($15-$500)
  - Food & Grocery ($5-$100)
  - Health & Wellness ($10-$200)
- **Ratings**: 3.0 to 5.0 stars
- **Stock Levels**: 0 to 500 units

#### Orders
- **Order Statuses**:
  - Delivered: ~65%
  - Shipped: ~15%
  - Processing: ~10%
  - Pending: ~5%
  - Cancelled: ~5%
- **Time Range**: Orders placed in the last 12 months
- **Average Processing Time**: 1-7 days to ship, 2-10 days to deliver

#### Order Items
- **Quantity Range**: 1-10 items per line item
- **Discounts**: ~20% of items have discounts (5-20% off)
- **Average Items per Order**: ~2 items

#### Payments
- **Payment Methods**:
  - Credit Card
  - Debit Card
  - PayPal
  - Apple Pay
  - Google Pay
  - Bank Transfer
- **Payment Status**:
  - Completed: ~85%
  - Pending: ~5%
  - Failed: ~5%
  - Refunded: ~5%
- **Transaction Fees**: 2-3% of payment amount

### Relational Integrity

✅ **All Foreign Key Relationships Verified**

```
customers (customer_id)
    ↓
orders (customer_id FK)
    ↓
order_items (order_id FK) → products (product_id FK)
    ↓
payments (order_id FK)
```

### Usage Examples

#### Load Data in Python

```python
import pandas as pd

# Load datasets
customers = pd.read_csv('data/customers.csv')
products = pd.read_csv('data/products.csv')
orders = pd.read_csv('data/orders.csv')
order_items = pd.read_csv('data/order_items.csv')
payments = pd.read_csv('data/payments.csv')

# Example: Join orders with customers
merged = orders.merge(customers, on='customer_id')
print(merged[['order_id', 'first_name', 'last_name', 'total_amount']].head())
```

#### Sample Analytics Queries

1. **Top 5 Customers by Total Spend**
2. **Best Selling Products by Category**
3. **Monthly Revenue Trends**
4. **Average Order Value by Customer Segment**
5. **Payment Method Distribution**
6. **Order Status Breakdown**
7. **Product Inventory Levels**
8. **Customer Lifetime Value**

### Next Steps

1. Load data into SQLite database
2. Create indexed tables for optimal query performance
3. Implement analytical SQL queries
4. Build visualization dashboards
5. Generate business intelligence reports

---

*Generated: November 14, 2025*  
*Random Seed: 42 (for reproducibility)*

