WITH source AS (
    SELECT * FROM {{ source('alphabeam', 'ProductCategory') }}
)

select
    ProductCategoryKey,
    EnglishProductCategoryName AS ProductCategory
from source