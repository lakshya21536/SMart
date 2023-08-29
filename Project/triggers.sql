delimiter //
CREATE TRIGGER send_shipping_notification AFTER UPDATE ON order_
FOR EACH ROW
BEGIN
DECLARE customer_email VARCHAR(100);
IF OLD.Order_Status != 'Shipped' AND NEW.Order_Status = 'Shipped' THEN
SELECT customer.Email INTO customer_email
FROM customer
WHERE customer.Customer_ID = NEW.Customer_ID;
SET @message = CONCAT('Dear Customer, your order with Order ID ', NEW.Order_ID, ' has been shipped!');
INSERT INTO email_notifications (To_Email, Subject_, Message)
VALUES (customer_email, 'Order Shipped!', @message);
END IF;
END // 


CREATE TRIGGER update_payment_amount AFTER UPDATE ON order_
FOR EACH ROW
BEGIN
    IF NEW.Order_Status = 'Confirmed' AND OLD.Order_Status != 'Confirmed' THEN
        UPDATE payment
        SET Amount = (SELECT SUM(pr.Price * pr.Cart_Quantity) 
                      FROM product pr
                      JOIN contains_ c ON pr.Product_id = c.Product_ID
                      WHERE c.Order_ID = NEW.Order_ID)
        WHERE Order_ID = NEW.Order_ID;
    END IF;
END;
