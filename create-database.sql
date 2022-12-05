--SQLite
DROP TABLE IF EXISTS Salesperson;
DROP TABLE IF EXISTS Mechanic;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Sales;
DROP TABLE IF EXISTS Vehicle;
DROP TABLE IF EXISTS Service;
DROP TABLE IF EXISTS Equipment;
DROP TABLE IF EXISTS Part;

CREATE TABLE Salesperson (
    sp_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    sp_name VARCHAR(32) NOT NULL,
    sp_position VARCHAR(32)         --ADDED
);

CREATE TABLE Mechanic (
    m_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    m_name VARCHAR(32) NOT NULL,
    m_position VARCHAR(32)         --ADDED
);

CREATE TABLE Customer (
    c_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    c_name VARCHAR(32) NOT NULL,
    c_phone CHAR(10) NOT NULL
);

CREATE TABLE Sales (
    s_invoiceNo INTEGER PRIMARY KEY AUTOINCREMENT,
    s_date DATE NOT NULL,
    s_VIN CHAR(17) UNIQUE,
    s_spID DECIMAL(3,0) NOT NULL,
    s_cID DECIMAL(3,0) NOT NULL,
    s_MSRP DECIMAL(8,2) NOT NULL,
    s_totalCost DECIMAL(8,2) NOT NULL
);

CREATE TABLE Vehicle (
    v_VIN CHAR(17) PRIMARY KEY,
    v_year DECIMAL(4,0) NOT NULL,
    v_make VARCHAR(32) NOT NULL,
    v_model VARCHAR(32) NOT NULL,
    v_trim VARCHAR(16),
    v_color VARCHAR(16) NOT NULL,
    v_MSRP DECIMAL(8,2),
    v_status VARCHAR(32) NOT NULL
);

CREATE TABLE Service (
    sv_workOrderNo INTEGER PRIMARY KEY AUTOINCREMENT,
    sv_serviceType VARCHAR(32) NOT NULL,
    sv_date DATE NOT NULL,
    sv_VIN CHAR(17) NOT NULL,
    sv_partKey DECIMAL(3,0),
    sv_equipmentKey DECIMAL(3,0),
    sv_cID DECIMAL(3,0),
    sv_mID DECIMAL(3,0) NOT NULL,
    sv_partCost DECIMAL(5,2), 
    sv_partQty DECIMAL(3,0),                 --ADDED
    sv_completed BOOL NOT NULL
);

CREATE TABLE Equipment (
    e_equipmentKey INTEGER PRIMARY KEY AUTOINCREMENT,
    e_name VARCHAR(32) NOT NULL,
    e_comment VARCHAR(63) 
);

CREATE TABLE Part (
    p_partKey INTEGER PRIMARY KEY AUTOINCREMENT,
    p_partName VARCHAR(32) NOT NULL,
    p_isOEM BOOL NOT NULL,
    p_partCost DECIMAL(3,0) NOT NULL
);

.mode "csv"
.separator ","
.cd /home/alvin/Desktop/CSE111/CSE-111-Project-Chester-Tim
--local path you may have to set this first (relative not working for some reason)

.import data/Customer.csv Customer
.import data/Equipment.csv Equipment
.import data/Mechanic.csv Mechanic
.import data/Part.csv Part
.import data/Sales.csv Sales
.import data/Salesperson.csv Salesperson
.import data/Service.csv Service
.import data/Vehicle.csv Vehicle 