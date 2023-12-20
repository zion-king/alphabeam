WITH customers AS (
    SELECT * FROM {{ ref("stg_customers")}}
)

select
    CustomerKey,
    Name As fullName,
    BirthDate,
    CASE
        WHEN MaritalStatus = 'S' THEN 'Single'
        WHEN MaritalStatus = 'M' THEN 'Married'
    END AS MaritalStatus,
    CASE
        WHEN Gender = 'F' THEN 'Female'
        WHEN Gender = 'M' THEN 'Male'
    END AS Gender,
    YearlyIncome,
    NumberChildren,
    Occupation,
    CASE
        WHEN HouseOwnerFlag = 0 THEN 'No'
        WHEN HouseOwnerFlag = 1 THEN 'Yes'
    END AS HouseOwner,
    NumberCarsOwned,
    PhoneNumber,
    DateFirstPurchase
from customers