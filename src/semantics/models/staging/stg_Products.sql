WITH source AS (
    SELECT * FROM {{ source('alphabeam', 'Products') }}
)

select
    ProductKey,
    ProductSubcategoryKey,
    ProductName,
    StandardCost,
    Color,
    SafetyStockLevel,
    ListPrice,
    Size,
    SizeRange,
    Weight,
    DaysToManufacture,
    ProductLine,
    DealerPrice,
    Class,
    ModelName,
    Description,
    Status,
    StartDate AS SellStartDate,
    EndDate AS SellEndDate
from source