-- ============================================================================
-- E-COMMERCE DATABASE ANALYTICAL QUERIES
-- ============================================================================
-- Database: ecommerce.db
-- Description: SQL queries for analyzing e-commerce transactions
-- ============================================================================


-- ============================================================================
-- QUERY 1: Complete Transaction Details (All Tables Joined)
-- ============================================================================
-- Joins customers → orders → order_items → products → payments
-- Outputs: customer name, product name, quantity, total price, payment method, order date
-- Calculates: total transaction value per order item
-- Sorts by: latest order date first
-- ============================================================================

SELECT 
    -- Customer Information
    c.first_name || ' ' || c.last_name AS customer_name,
    
    -- Product Information
    p.product_name,
    p.category AS product_category,
    
    -- Order Item Details
    oi.quantity,
    ROUND(oi.total, 2) AS total_price,
    
    -- Transaction Value Calculation
    ROUND(oi.quantity * oi.unit_price, 2) AS subtotal,
    ROUND(oi.discount, 2) AS discount_applied,
    ROUND(oi.quantity * oi.unit_price - oi.discount, 2) AS transaction_value,
    
    -- Payment Information
    py.payment_method,
    py.status AS payment_status,
    
    -- Order Information
    DATE(o.order_date) AS order_date,
    o.status AS order_status
    
FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    INNER JOIN products p ON oi.product_id = p.product_id
    INNER JOIN payments py ON o.order_id = py.order_id
    
ORDER BY o.order_date DESC, o.order_id;


-- ============================================================================
-- QUERY 2: Simplified Transaction View (Essential Columns Only)
-- ============================================================================
-- Clean, readable output with just the core transaction details
-- ============================================================================

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
    
ORDER BY o.order_date DESC;


-- ============================================================================
-- QUERY 3: Revenue Analysis by Product Category
-- ============================================================================

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
ORDER BY total_revenue DESC;


-- ============================================================================
-- QUERY 4: Customer Lifetime Value (Top 20)
-- ============================================================================

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
LIMIT 20;


-- ============================================================================
-- QUERY 5: Payment Method Performance Analysis
-- ============================================================================

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
ORDER BY total_amount DESC;


-- ============================================================================
-- QUERY 6: Top Selling Products
-- ============================================================================

SELECT 
    p.product_id,
    p.product_name,
    p.category,
    COUNT(DISTINCT oi.order_id) AS times_ordered,
    SUM(oi.quantity) AS total_units_sold,
    ROUND(SUM(oi.total), 2) AS total_revenue,
    ROUND(AVG(oi.unit_price), 2) AS avg_selling_price,
    p.stock_quantity AS current_stock
    
FROM products p
    INNER JOIN order_items oi ON p.product_id = oi.product_id
    
GROUP BY p.product_id, p.product_name, p.category, p.stock_quantity
ORDER BY total_revenue DESC
LIMIT 20;


-- ============================================================================
-- QUERY 7: Monthly Revenue Trends
-- ============================================================================

SELECT 
    STRFTIME('%Y-%m', o.order_date) AS year_month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.quantity) AS total_items_sold,
    ROUND(SUM(oi.total), 2) AS monthly_revenue,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value,
    COUNT(DISTINCT o.customer_id) AS unique_customers
    
FROM orders o
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    
WHERE o.status != 'Cancelled'
GROUP BY year_month
ORDER BY year_month DESC;


-- ============================================================================
-- QUERY 8: Customer Segment Performance
-- ============================================================================

SELECT 
    c.customer_segment,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.total), 2) AS segment_revenue,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value,
    ROUND(SUM(oi.total) / COUNT(DISTINCT c.customer_id), 2) AS revenue_per_customer,
    ROUND(COUNT(DISTINCT o.order_id) * 1.0 / COUNT(DISTINCT c.customer_id), 2) AS orders_per_customer
    
FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    
GROUP BY c.customer_segment
ORDER BY segment_revenue DESC;


-- ============================================================================
-- QUERY 9: Order Status Breakdown
-- ============================================================================

SELECT 
    o.status,
    COUNT(*) AS order_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS percentage,
    ROUND(SUM(o.total_amount), 2) AS total_value,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value,
    MIN(DATE(o.order_date)) AS earliest_order,
    MAX(DATE(o.order_date)) AS latest_order
    
FROM orders o
GROUP BY o.status
ORDER BY order_count DESC;


-- ============================================================================
-- QUERY 10: Product Inventory Alert (Low Stock)
-- ============================================================================

SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.stock_quantity,
    COUNT(oi.order_item_id) AS times_ordered,
    SUM(oi.quantity) AS total_units_sold,
    CASE 
        WHEN p.stock_quantity = 0 THEN 'OUT OF STOCK'
        WHEN p.stock_quantity < 50 THEN 'CRITICAL'
        WHEN p.stock_quantity < 100 THEN 'LOW'
        ELSE 'ADEQUATE'
    END AS stock_status
    
FROM products p
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    
GROUP BY p.product_id, p.product_name, p.category, p.stock_quantity
HAVING p.stock_quantity < 100
ORDER BY p.stock_quantity ASC, total_units_sold DESC;


-- ============================================================================
-- END OF QUERIES
-- ============================================================================

