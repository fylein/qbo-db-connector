DROP TABLE IF EXISTS qbo_extract_classes;
DROP TABLE IF EXISTS qbo_extract_departments;
DROP TABLE IF EXISTS qbo_extract_accounts;
DROP TABLE IF EXISTS qbo_extract_employees;
DROP TABLE IF EXISTS qbo_extract_home_currency;
DROP TABLE IF EXISTS qbo_extract_exchange_rates;

CREATE TABLE qbo_extract_classes (
    Id TEXT,
    Name TEXT
);

CREATE TABLE qbo_extract_departments (
    Id TEXT,
    Name TEXT
);

CREATE TABLE qbo_extract_accounts (
    Id TEXT,
    Name TEXT
);

CREATE TABLE qbo_extract_employees (
    Id TEXT,
    GivenName TEXT,
    FamilyName TEXT,
    DisplayName TEXT
);

CREATE TABLE qbo_extract_home_currency (
    home_currency TEXT
);

CREATE TABLE qbo_extract_exchange_rates (
    SourceCurrencyCode TEXT,
    TargetCurrencyCode TEXT,
    Rate REAL,
    AsOfDate DATE
);