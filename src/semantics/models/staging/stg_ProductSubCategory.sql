WITH source AS (
    SELECT * FROM {{ source('alphabeam', 'ProductSubcategory') }}
)

select
    ProductSubcategoryKey,
    EnglishProductSubcategoryName AS ProductSubcategory,
    ProductCategoryKey
from source