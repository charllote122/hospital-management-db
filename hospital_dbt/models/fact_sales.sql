SELECT
    f.order_id,
    f.date_key,
    c.customer_name,
    c.city,
    f.sales_amount
FROM warehouse.fact_sales f
JOIN warehouse.dim_customer c ON f.customer_key = c.customer_key
