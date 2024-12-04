# Internal-Assessment-Budgetting-System
 Internal-Assessment-Budgetting-System
import psycopg2
import threading
from CTkTable import *
#https://github.com/Akascape/CTkTable

from math import *
import re
import pygame
import 

## SQL Startup Query
```SQL
-- Drop existing tables if they exist
DROP TABLE IF EXISTS transactionTable;
DROP TABLE IF EXISTS transactionType;
DROP TABLE IF EXISTS Balance;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS goodwillBranch;
DROP TABLE IF EXISTS notes;

-- Create goodwillBranch table
CREATE TABLE goodwillBranch (
    BranchId INT NOT NULL,
    branchName VARCHAR(200) NOT NULL,
    branchAddress VARCHAR(200) NOT NULL,
    branchPhoneNumber INT,
    PRIMARY KEY (BranchId)
);

-- Create Inventory table
CREATE TABLE Inventory (
    InventoryId INT NOT NULL,
    InventoryName VARCHAR(200) NOT NULL,
    InventoryValue FLOAT NOT NULL,
    InventoryType VARCHAR(10),
    BranchId INT NOT NULL,
    GoodsStatus VARCHAR(7), -- Bought, sold, or donate
    PRIMARY KEY (InventoryId),
    FOREIGN KEY (BranchId) REFERENCES goodwillBranch(BranchId)
);

-- Create Balance table
CREATE TABLE Balance (
    BalanceID INT NOT NULL,
    BalanceAmount FLOAT,
    DateOfChange DATE,
    TransactionId INT,
    PRIMARY KEY (BalanceID),
    FOREIGN KEY (TransactionId) REFERENCES transactionTable(TransactionId)
);

-- Create transactionType table
CREATE TABLE transactionType (
    transactionTypeId INT NOT NULL,
    balanceID INT NOT NULL,
    InventoryId INT NOT NULL,
    PRIMARY KEY (transactionTypeId),
    FOREIGN KEY (balanceID) REFERENCES Balance(BalanceID),
    FOREIGN KEY (InventoryId) REFERENCES Inventory(InventoryId)
);

-- Create transactionTable table
CREATE TABLE transactionTable (
    transactionId INT NOT NULL, 
    transactorFrom VARCHAR(30) NOT NULL,
    transactionTo VARCHAR(30) NOT NULL, 
    transactionDate DATE,
    transactionType VARCHAR(5), -- CASH/ ITEM
    transactionTypeId INT,
    PRIMARY KEY (transactionId),
    FOREIGN KEY (transactionTypeId) REFERENCES transactionType(transactionTypeId)
);

-- Create notes table
CREATE TABLE notes (
    noteid SERIAL PRIMARY KEY,
    notename VARCHAR(200) NOT NULL,
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial data
INSERT INTO goodwillBranch (BranchId, branchName, branchAddress, branchPhoneNumber) VALUES (0, 'none', 'none', 0);
INSERT INTO Inventory (InventoryId, InventoryName, InventoryValue, InventoryType, BranchId, GoodsStatus) VALUES (0, 'none', 0, 'none', 0, 'none');
INSERT INTO Balance (BalanceID, BalanceAmount, DateOfChange, TransactionId) VALUES (0, 0, NULL, 0);
INSERT INTO notes (notename, note) VALUES ('Sample Note', 'This is a sample note content');
```