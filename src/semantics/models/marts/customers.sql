WITH customers AS (
    SELECT * FROM {{ ref("stg_customers")}}
)

select
    CustomerKey AS customer_key,
    Name AS name,
    BirthDate AS birth_date,
    CASE
        WHEN MaritalStatus = 'S' THEN 'Single'
        WHEN MaritalStatus = 'M' THEN 'Married'
    END AS marital_status,
    CASE
        WHEN Gender = 'F' THEN 'Female'
        WHEN Gender = 'M' THEN 'Male'
    END AS gender,
    YearlyIncome AS yearly_income,
    NumberChildren AS number_children,
    Occupation AS occupation,
    CASE
        WHEN HouseOwnerFlag = 0 THEN 'No'
        WHEN HouseOwnerFlag = 1 THEN 'Yes'
    END AS house_owner,
    NumberCarsOwned AS cars_owned,
    PhoneNumber AS phone_number,
    DateFirstPurchase AS date_first_purchase
from customers