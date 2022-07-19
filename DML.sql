
/* Since we are planning to use Flask (Python language) and do not know how the interaction will work between sql query and value sending, we are going to use just values for now.
  However, we will put a comment right next to the query saying that value A will be the input value to do the action.
*/

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

/* Retrieve userAccounts table */
SELECT * FROM userAccounts;

/* Retrieve fiatWallets table */
SELECT * FROM fiatWallets;

/* Retrieve dogecoinWallets table */
SELECT * FROM dogecoinWallets;

/* Retrieve exchangeOrders table */
SELECT * FROM exchangeOrders;

/* Retrieve dogecoinTransactions table */
SELECT * FROM dogecoinTransactions;

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

/* Update a certain userAccounts value */
UPDATE userAccounts SET email = 'kangken@oregonstate.edu', zipCode = "97003", city = "Beaverton"  WHERE userID = 'U1'; 
-- userID is the primary key will always be used for where clause whereas the set clause values will be from user input values from the form (email, zipCode, city).
-- The user is unable to change the userID value.

/* Update a certain fiatWallets value */
UPDATE fiatWallets SET fiatBalance = 431 WHERE fiatWalletID = 'F12348904';
-- fiatWalletID is the primary key will always be used for where clause whereas the set clause values will be from user input values from the form (fiatBalance).
-- The user is unable to change the fiatWalletID value.

/* Update a certain userAccounts value */
UPDATE dogecoinWallets SET dogecoinBalance = 2345 WHERE dogecoinWalletID = 'D98247833';
-- fiatWalletID is the primary key will always be used for where clause whereas the set clause values will be from user input values from the form (dogecoinBalance).
-- The user is unable to change the dogecoinWalletID value and walletAddress.

/* Update a certain userAccounts value */
UPDATE exchangeOrders SET amountFilled = 49683.372543 WHERE exchangeID = 'E6';
-- exchangeID is the primary key will always be used for where clause whereas the set clause values will be from user input values from the form (amountFilled).
-- The user is unable to change the exchangeID, fiatWalletID, dogecoinWalletID, and orderTimestamp value.
-- The orderTimestamp value will be automatically updated when the record is updated.

/* Update a certain userAccounts value */
UPDATE dogecoinTransactions SET amount = 8683986.38387583 WHERE txID = 'T11';
-- txID is the primary key will always be used for where clause whereas the set clause values will be from user input values from the form (amount).
-- The user is unable to change the txID, txTimestamp, dogecoinWalletID, externalWalletAddress, and txHash value.
-- The txTimestamp value will be automatically updated when the record is updated.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- DELETE FROM fiatWallets WHERE fiatWalletID = (SELECT fiatWallets.fiatWalletID FROM fiatWallets INNER JOIN userAccounts ON fiatWallets.fiatWalletID = userAccounts.fiatWalletID AND userAccounts.userID = 'U2');
-- DELETE FROM dogecoinWallets WHERE dogecoinWalletID = (SELECT dogecoinWallets.dogecoinWalletID FROM dogecoinWallets INNER JOIN userAccounts ON dogecoinWallets.dogecoinWalletID = userAccounts.dogecoinWalletID AND userAccounts.userID = 'U2'); 
DELETE FROM userAccounts WHERE userID = 'U2';
-- userID is the primary key will always be used for where clause.
-- When you are delete a record from userAccounts, the associated fiatWallets and dogecoinWallets will be removed as well.

DELETE FROM fiatWallets WHERE fiatWalletID = 'F34072432';
-- fiatWalletID is the primary key will always be used for where clause.

DELETE FROM dogecoinWallets WHERE dogecoinWalletID = 'D88832435';
-- dogecoinWalletID is the primary key will always be used for where clause.

DELETE FROM exchangeOrders WHERE exchangeID = 'E3';
-- exchangeID is the primary key will always be used for where clause.

DELETE FROM dogecoinTransactions WHERE txID = 'T11';
-- txID is the primary key will always be used for where clause.
