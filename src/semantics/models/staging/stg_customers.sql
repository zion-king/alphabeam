WITH source AS (
    SELECT * FROM {{ source('alphabeam', 'Customers') }}
)

select
    CustomerKey,
    Name,
    BirthDate,
    MaritalStatus,
    Gender,
    YearlyIncome,
    NumberChildrenAtHome AS NumberChildren,
    Occupation,
    HouseOwnerFlag,
    NumberCarsOwned,
    Phone AS PhoneNumber,
    DateFirstPurchase
from source