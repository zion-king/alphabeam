WITH sales AS (
    SELECT * FROM {{ ref("stg_sales")}}
)

select
    OrderDate,
    ShipDate,
    ProductKey,
    CustomerKey,
    SalesOrderNumber,
    SalesOrderLineNumber,
    OrderQuantity,
    UnitPrice,
    ExtendedAmount,
    UnitPriceDiscountPct,
    DiscountAmount,
    ProductStandardCost,
    TotalProductCost,
    SalesAmount,
    TaxAmount,
    Freight
from sales