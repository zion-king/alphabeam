WITH source AS (
    SELECT * FROM {{ source('alphabeam', 'Sales') }}
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
    TaxAmt AS TaxAmount,
    Freight
from source