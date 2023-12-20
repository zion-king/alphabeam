WITH products AS (
    SELECT * FROM {{ ref("stg_Products")}}
),
product_category AS (
    SELECT * FROM {{ ref("stg_ProductCategory")}}
),
product_subcategory AS (
    SELECT * FROM {{ ref("stg_ProductSubCategory")}}
)

select
    ProductKey,
    ProductName,
    ProductSubcategory,
    ProductCategory,
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
    SellStartDate,
    SellEndDate
FROM products
LEFT JOIN product_subcategory ON product_subcategory.ProductSubcategoryKey = products.ProductSubcategoryKey
LEFT JOIN product_category ON product_subcategory.ProductCategoryKey = product_category.ProductCategoryKey