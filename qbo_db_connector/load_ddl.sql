DROP TABLE IF EXISTS qbo_load_journal_entries;
DROP TABLE IF EXISTS qbo_load_checks;
DROP TABLE IF EXISTS qbo_load_journal_entry_lineitems;
DROP TABLE IF EXISTS qbo_load_check_lineitems;
DROP TABLE IF EXISTS qbo_load_attachments;

CREATE TABLE qbo_load_journal_entries (
    posting_type TEXT,
    entity TEXT,
    record_date TEXT,
    id TEXT,
    currency TEXT
);

CREATE TABLE qbo_load_journal_entry_lineitems (
    posting_type TEXT,
    account TEXT,
    department TEXT,
    class TEXT,
    entity TEXT,
    amount REAL,
    description TEXT,
    record_date TEXT,
    emp_email TEXT,
    journal_entry_id TEXT,
    currency TEXT,
    expense_id TEXT
);

CREATE TABLE qbo_load_checks (
    bank_account TEXT,
    entity TEXT,
    department TEXT,
    record_date TEXT,
    id TEXT,
    currency TEXT
);

CREATE TABLE qbo_load_check_lineitems (
    posting_type TEXT,
    account TEXT,
    department TEXT,
    class TEXT,
    entity TEXT,
    amount REAL,
    description TEXT,
    record_date TEXT,
    emp_email TEXT,
    check_id TEXT,
    currency TEXT,
    expense_id TEXT
);

CREATE TABLE qbo_load_attachments (
    ref_id TEXT,
    ref_type TEXT,
    content TEXT,
    filename TEXT
);