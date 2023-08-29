-- Transaction 1: Update the price of a specific product.
-- Transaction 2: Update the inventory quantity for the same product.

-- Explanation: These two transactions are non-conflicting as they involve different columns in 
-- the product table. Transaction 1 updates the price of a specific product, while Transaction 2 
-- updates the inventory quantity for the same product. These transactions do not affect the same 
-- rows or columns, so they can be executed concurrently without conflict.

START TRANSACTION;

UPDATE `product`
SET `Price` = 15.99
WHERE `Product_id` = 123;

COMMIT;
START TRANSACTION;

UPDATE `product`
SET `Inventory_Quantity` = `Inventory_Quantity` - 1
WHERE `Product_id` = 123;

COMMIT;


-- Transaction 1: Read operation
-- Reads the customer name and address from the "Customers" table.
-- Transaction 2: Read operation
-- Reads the product details from the "Products" table.
-- In this example, both transactions are read operations and access different tables in the database.
-- Therefore, they are non-conflicting and can be executed concurrently without any issues

START TRANSACTION;

SELECT * FROM product WHERE Product_id = 1;

COMMIT;
START TRANSACTION;

SELECT * FROM customer WHERE Customer_ID = 1;

COMMIT;

-- Since these Transactions are operating on different sets of data and do not interfere
--  with each other's updates, they can be executed concurrently without causing any conflicts. 
-- Calculate the total cost of an order and update the payment status to "Paid". 
START TRANSACTION;
-- calculate the total cost of the order
SELECT SUM(p.Price * p.Cart_Quantity) AS total_cost
FROM product p
JOIN contains_ c ON c.product_id = p.product_id
WHERE c.order_id = 2;
-- Update the payment status to "Paid" And Update the Amount
UPDATE Payment
SET payment_status = 'Paid', Amount = (SELECT SUM(p.Price * p.Cart_Quantity)
FROM product p
JOIN contains_ c ON c.product_id = p.product_id
WHERE c.order_id = 2)
WHERE order_id = 2;
COMMIT;
-- Update the order status to "Shipped" and assign a delivery driver to the order. 
START TRANSACTION;
-- update the order status to "Shipped"
UPDATE orders
SET order_status = 'Shipped'
WHERE order_id = 2;
-- assign a delivery driver to the order
UPDATE order_
SET driver_id = (
  SELECT Driver_ID FROM deliverydriver ORDER BY RAND() LIMIT 1
)
WHERE order_id = 2;
COMMIT;


-- These two transactions are non-conflicting because they are modifying different products
--  in the same table. The first transaction updates the prices of products 1 and 2, while the
--  second transaction updates the inventory quantity of product 4. Since these updates are on
--  different products, they do not conflict with each other and can be executed concurrently without any issues. 

START TRANSACTION;
-- Display product ID 1
SELECT Product_id, Availability, Product_Description, Price, ProductName, Inventory_Quantity FROM product WHERE Product_id = 1;
-- Decrease price of product 1 by 50
UPDATE product SET Price = Price - 50 WHERE Product_id = 1;
-- Display product ID 2
SELECT Product_id, Availability, Product_Description, Price, ProductName, Inventory_Quantity FROM product WHERE Product_id = 2;
-- Increase price of product 2 by 100
UPDATE product SET Price = Price + 100 WHERE Product_id = 2;
COMMIT;

START TRANSACTION;
-- Display product ID 4
SELECT Product_id, Availability, Product_Description, Price, ProductName, Inventory_Quantity FROM product WHERE Product_id = 4;
-- Update inventory quantity of product 4
UPDATE product SET Inventory_Quantity = 100 WHERE Product_id = 4;
COMMIT;


