WITH sales AS (
    SELECT * FROM {{ ref("stg_sales")}}
)

select
    {{ dbt_utils.generate_surrogate_key(['SalesOrderNumber', 'SalesOrderLineNumber']) }} as sales_key,
    {{dbt.date_trunc('day','OrderDate')}} as ordered_at,
    OrderDate AS order_date,
    ShipDate AS ship_date,
    ProductKey AS product_key,
    CustomerKey AS customer_key,
    SalesOrderNumber AS sales_order_number,
    SalesOrderLineNumber AS sales_order_line_number,
    SUM(OrderQuantity) AS quantity_total,
    AVG(OrderQuantity) AS quantity_average,
    SUM(UnitPrice) AS price_total,
    AVG(UnitPrice) AS price_average,
    SUM(DiscountAmount) AS discount_amount_total,
    AVG(DiscountAmount) AS discount_amount_average,
    SUM(TotalProductCost) AS product_cost_total,
    AVG(TotalProductCost) AS product_cost_average,
    SUM(SalesAmount) AS revenue_total,
    AVG(SalesAmount) AS revenue_average
from sales
group by 1, 2, 3, 4, 5, 6, 7, 8