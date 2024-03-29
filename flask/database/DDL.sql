/*
Authors:        Mark Jordan, Kenneth Kang
Course:         CS340 - Intro to Databases
Instructors:    Dr. Michael. Curry, Danielle Safonte
Project:        Step 4 DRAFT
Due:            2022-07-28
Description:    Data Definition queries for DOGE-X.
*/


SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

CREATE OR REPLACE TABLE fiatWallets (
  fiatWalletID varchar(50) NOT NULL PRIMARY KEY, /* It will have a prefix of 'F' followed by an int combination */
  fiatWalletName varchar(50),
  fiatBalance decimal(15,2) NOT NULL
);

CREATE OR REPLACE TABLE dogecoinWallets (
  dogecoinWalletID varchar(50) NOT NULL PRIMARY KEY, /* It will have a prefix of 'D' followed by an int combination */
  walletAddress varchar(100) NOT NULL UNIQUE,
  dogecoinBalance decimal(18,9) NOT NULL
);

CREATE OR REPLACE TABLE userAccounts (
  userID varchar(50) NOT NULL PRIMARY KEY, /* It will have a prefix of 'U' followed by an int combination */
  firstName varchar(100) NOT NULL,
  lastName varchar(100) NOT NULL,
  address varchar(500) NOT NULL,
  city varchar(100) NOT NULL,
  state varchar(2) NOT NULL,
  zipCode varchar(50) NOT NULL,
  phoneNumber varchar(50) NOT NULL,
  email varchar(100) NOT NULL,
  password varchar(50) NOT NULL,
  fiatWalletID varchar(50) NOT NULL UNIQUE,
  dogecoinWalletID varchar(50) NOT NULL UNIQUE,
  CONSTRAINT FK_userAccounts_with_fiatWalletID FOREIGN KEY (fiatWalletID) REFERENCES fiatWallets(fiatWalletID) ON DELETE CASCADE,
  CONSTRAINT FK_userAccounts_with_dogecoinWalletID FOREIGN KEY (dogecoinWalletID) REFERENCES dogecoinWallets(dogecoinWalletID) ON DELETE CASCADE
);

CREATE OR REPLACE TABLE exchangeOrders(
  exchangeID varchar(50) NOT NULL PRIMARY KEY, /* It will have a prefix of 'E' followed by an int combination */
  fiatWalletID varchar(50),
  dogecoinWalletID varchar(50),
  orderTimestamp TIMESTAMP NOT NULL,
  orderType varchar(50) NOT NULL,
  orderDirection varchar(50) NOT NULL,
  amountFilled decimal(18,9) NOT NULL,
  orderPrice decimal(15,2) NOT NULL,
  CONSTRAINT FK_exchangeOrders_with_fiatWalletID FOREIGN KEY (fiatWalletID) REFERENCES fiatWallets(fiatWalletID) ON DELETE SET NULL,
  CONSTRAINT FK_exchangeOrders_with_dogecoinWalletID FOREIGN KEY (dogecoinWalletID) REFERENCES dogecoinWallets(dogecoinWalletID) ON DELETE SET NULL
);

CREATE OR REPLACE TABLE dogecoinTransactions (
  txID varchar(50) NOT NULL PRIMARY KEY, /* It will have a prefix of 'T' followed by an int combination */
  txTimestamp TIMESTAMP NOT NULL,
  amount decimal(18,9) NOT NULL,
  txDirection varchar(50) NOT NULL,
  dogecoinWalletID varchar(50) NOT NULL, /* It will have a prefix of 'D' followed by an int combination */
  externalWalletAddress varchar(100) NOT NULL,
  txHash varchar(100) NOT NULL UNIQUE,
  CONSTRAINT FX_dogecoinTransactions_with_dogecoinWalletID FOREIGN KEY (dogecoinWalletID) REFERENCES dogecoinWallets(dogecoinWalletID) ON DELETE CASCADE
);

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

/* Insert userAccounts Data */
INSERT INTO userAccounts (userID, firstName, lastName, address, city, state, zipCode, phoneNumber, email, password, fiatWalletID, dogecoinWalletID)
VALUES ('U0', 'Kenneth', 'Kang', '123 SW 201 St', 'Portland', 'OR', '97005', '8398741723', 'kkang@gmail.com', '12345a', 'F0', 'D0'),
('U1', 'Mark', 'Jordan', '1800 Lacassie Ave', 'Walnut Creek', 'CA', '94596', '4151234567', 'jjord@hotmail.com', '6789uu', 'F1', 'D1'),
('U2', 'Soo', 'Kim', '14 41nd St', 'New York', 'NY', '10018', '2125459457', 'skim@outlook.com', '89o4aa0', 'F2', 'D2'),
('U3', 'Hae-in', 'Shin', '20 42nd St', 'New York', 'NY', '10018', '2129834776', 'hshin@gmail.com', '456eo7843', 'F3', 'D3'),
('U4', 'Min-kyu', 'Lee', '15916 Rivers Cove', 'Austin', 'TX', '78717', '5124094797', 'mklee@gmail.com', '78787eu', 'F4', 'D4');

/* Insert fiatWallets Data */
INSERT INTO fiatWallets (fiatWalletID, fiatWalletName, fiatBalance)
VALUES ('F0' ,'Wallet 1', 55),
('F1', 'Wallet 2', 15789),
('F2','Wallet 3', 	34578),
('F3', 'Wallet 4', 555),
('F4','Wallet 5', 357890);

/* Insert dogecoinWallets Data */
INSERT INTO dogecoinWallets (dogecoinWalletID, walletAddress, dogecoinBalance)
VALUES ('D0', 'D8XskzpskY1fGxBrfWMu65AWF1LSFeAvkF', 1514),
('D1', 'DGJNetovmNoBZiF5YymLfcc4R8LAQeewkz', 25789),
('D2',	'D9wfpqQU4PCZRmDpAqvH6hmau7dEBBJFTq',	4444),
('D3',	'DP9jzRmr54eszobQgFsvu2Qgi55DaJBmmy',	155090),
('D4',	'DEb5KeZAJKeqQ6ugoCZ6fHrBRHHkEkLdQS',	2345);

/* Insert exchangeOrders Data */
INSERT INTO exchangeOrders (exchangeID, fiatWalletID, dogecoinWalletID, orderTimestamp, orderType, orderDirection, amountFilled, orderPrice)
VALUES ('E0', 'F1', 'D1', '2022-06-23 13:10:11', 'Market', 'Buy', 1523.129447890, 198.01),
('E1', 'F4', 'D4', '2022-06-23 15:10:15', 'Market', 'Buy', 5553.242000320, 721.92),
('E2', 'F2', 'D2', '2022-06-24 04:10:10', 'Limit', 'Sell', 32342.342477430, 4204.50),
('E3', 'F2', 'D2', '2022-06-24 13:10:11', 'Limit', 'Buy',134.666399920, 17.51),
('E4', 'F0', 'D0', '2022-06-25 15:10:15', 'Market', 'Sell', 7238.823912389, 941.05),
('E5', 'F2', 'D2', '2022-06-26 04:10:10', 'Limit', 'Sell', 50.005672253, 6.50),
('E6', 'F1', 'D1', '2022-06-26 13:10:11', 'Market', 'Sell', 5150.999422253, 669.63),
('E7', 'F3', 'D3', '2022-06-27 15:10:15', 'Market', 'Buy', 460.002422253, 59.80),
('E8', 'F3', 'D3', '2022-06-27 04:10:10', 'Stop-Limit', 'Sell', 70.902424453, 9.22),
('E9', 'F3', 'D3', '2022-06-27 13:10:11', 'Market', 'Sell', 22.023568253, 2.86),
('E10', 'F2', 'D2', '2022-06-28 15:10:15', 'Market', 'Buy', 15550.002477253, 2021.50),
('E11', 'F0', 'D0', '2022-06-28 04:10:10', 'Market', 'Buy', 990.222422253, 128.73),
('E12', 'F1', 'D1', '2022-06-29 13:10:12', 'Stop-Limit', 'Sell', 250.332493253, 32.54),
('E13', 'F2', 'D2', '2022-06-29 15:10:15', 'Market', 'Buy', 5650.002439253, 734.50),
('E14', 'F0', 'D0', '2022-06-30 04:10:10', 'Market', 'Buy', 150.992422253, 19.63),
('E15', 'F0', 'D0', '2022-07-01 13:10:11', 'Limit', 'Sell', 100.112422253, 13.01),
('E16', 'F1', 'D1', '2022-07-02 15:10:15', 'Limit', 'Sell', 20.444422753, 2.66),
('E17', 'F2', 'D2', '2022-07-03 04:10:10', 'Market', 'Buy', 15550.012422253, 2021.50);

/* Insert dogecoinTransactions Data */
INSERT INTO dogecoinTransactions (txID, txTimestamp, amount, txDirection, dogecoinWalletID, externalWalletAddress, txHash)
VALUES ('T0', '2022-06-27 13:10:11', 6200.056347843, 'Deposit', 'D1', 'DP9jzRmr54eszobQgFsvu2Qgi55DaJBmmy', '92b1588447ab7f6857ae63185e2046a5a4aa3db0e79c8988f44a90219119245b'),
('T1', '2022-06-28 15:10:15', 145.023459043, 'Deposit', 'D4', 'DAu9awAQWtbD3KR1bNKjNvtR7NhMvyGc4z', '7707ddd1931c7ecd937f7edd717c8c7d1cf78947d880384a5a21576ba5f155d5'),
('T2', '2022-06-28 04:10:10', 45000.189089043, 'Deposit', 'D2', 'DTJFYN36jz1qx4wLiqQ5Atj3YuxPty8HyD', '802ccc8407e45018c639b978210b1c7bba874ae701501cffb40b8af4171145f7'),
('T3', '2022-06-29 13:10:12', 2356.034569043, 'Withdrawal', 'D1', 'D6wm6g81qAfmZswUaB7HqkGHLWeabnDZwp', '38f9e947d84b45a3ad10d97dd1e2d601113858e4a982f992f35f0336ebc19e4a'),
('T4', '2022-06-29 15:10:15', 23.057779043, 'Deposit', 'D2', 'DC74MnmyVKZfZGKFAT7Q89jLKtcWyk5EsU', 'c744430e9cde0d588cfc7ce0ac5b3d58358a5351073df2d1ce3e35c7b66fc5e7'),
('T5', '2022-06-30 04:10:10', 42000.056278043, 'Withdrawal', 'D2', 'DC74MnmyVKZfZGKFAT7Q89jLKtcWyk5EsU', '2ff385f8f65385054668414631e4e596cc3fbbe43e57b158c56f4626b5aef359'),
('T6', '2022-07-01 13:10:11', 246.222789043, 'Withdrawal', 'D3', 'DGt8UzqzwGcMeZYS11aSrHunFJVckxFvsG', '97576dc75a02d1381c056c403b2318346989a48f48fc7431bba4f6c300abe6bd'),
('T7', '2022-07-02 15:10:15', 17778.111789043, 'Deposit', 'D0', 'DP9jzRmr54eszobQgFsvu2Qgi55DaJBmmy', 'ca29be2a6d1d5b57afef7daefec09a2e731faaee38e5e6a0ee2bd17aa389491f'),
('T8', '2022-07-03 04:10:10', 89782.266636043, 'Withdrawal', 'D1', 'DGt8UzqzwGcMeZYS11aSrHunFJVckxFvsG', '82b1588447ab7f6857ae63185d2046a5a4aa3db0d79c8988f44c90219119245b'),
('T9', '2022-07-05 13:10:11', 298.056229043, 'Withdrawal', 'D0', 'DFvmPfgRtjAG8FFv9UuBs4ffjCkE8q9YPn', '50d94ee75ee361ed84e7897a951204872fefb7c8049adc783e6877362e803e4a'),
('T10', '2022-07-05 15:10:15', 5554.056783893, 'Withdrawal', 'D1', 'DC74MnmyVKZfZGKFAT7Q89jLKtcWyk5EsU', '04184882ecd8db602829f04cc9453f18d822e4ef1e15032755840f007311af79'),
('T11', '2022-07-06 04:10:10', 6788.993289043, 'Deposit', 'D3', 'DRWjzTVtUERKpmieESBxjwb5wH9BuBB3mA', 'cd8435768a7aca7537d28109889a311d1a6b647c00e0aa146887e42e1b8cb057'),
('T12', '2022-07-06 13:10:11', 155000.111789043, 'Deposit', 'D1', 'DDzejugjtXPUZrUtTAojBPAop4U4fYHfZn', '1e2e6b087ac2b8f025e730d340be4dfaa7c29080a82c181c4d551919a517b506'),
('T13', '2022-07-06 15:10:15', 4782.756744443, 'Withdrawal', 'D2', 'DP9jzRmr54eszobQgFsvu2Qgi55DaJBmmy', '0bd1489941f263d0076efe3b4e980299d67ac918cba49c6b3245d5980175eeec');

-- -- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
SET FOREIGN_KEY_CHECKS=1;
COMMIT;
