SELECT
    p.category,
    SUM(f.sales_amount) AS total_revenue,
    COUNT(f.sales_key) AS total_orders
FROM warehouse.fact_sales f
JOIN warehouse.dim_product p ON f.product_key = p.product_key
GROUP BY p.category
