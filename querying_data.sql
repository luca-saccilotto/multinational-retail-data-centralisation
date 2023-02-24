-- Perform a query to get the number of stores by country
SELECT country_code, COUNT(*) 
FROM dim_store_details 
GROUP BY country_code 
ORDER BY COUNT(*) DESC;

-- Perform a query to get the location that has the highest number of stores
SELECT locality, COUNT(*) 
FROM dim_store_details 
GROUP BY locality 
ORDER BY COUNT(*) DESC;

-- Perform a query to find out which months typically have the most sales
SELECT ROUND(SUM(product_price * product_quantity)::numeric, 0) AS total_sales, dim_date_times.month
FROM dim_products
JOIN orders_table
ON dim_products.product_code = orders_table.product_code
JOIN dim_date_times
ON orders_table.date_uuid = dim_date_times.date_uuid
GROUP BY dim_date_times.month
ORDER BY total_sales DESC;

-- Perform a query to find out how many sales are coming from online