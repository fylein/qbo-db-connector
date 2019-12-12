DROP TABLE IF EXISTS qbo_load_journal_entries;
DROP TABLE IF EXISTS qbo_load_checks;
DROP TABLE IF EXISTS qbo_load_journal_entry_lineitems;
DROP TABLE IF EXISTS qbo_load_check_lineitems;
DROP TABLE IF EXISTS qbo_load_attachments;

CREATE TABLE qbo_load_journal_entries (
    employee_email TEXT,
    record_date TEXT,
    id TEXT,
    currency TEXT,
    private_note TEXT
);

CREATE TABLE qbo_load_journal_entry_lineitems (
    posting_type TEXT,
    entity TEXT,
    account TEXT,
    department TEXT,
    class TEXT,
    amount REAL,
    description TEXT,
    journal_entry_id TEXT,
    expense_id TEXT
);

CREATE TABLE qbo_load_checks (
    bank_account TEXT,
    entity TEXT,
    employee_email TEXT,
    department TEXT,
    record_date TEXT,
    id TEXT,
    currency TEXT,
    private_note TEXT
);

CREATE TABLE qbo_load_check_lineitems (
    account TEXT,
    class TEXT,
    amount REAL,
    description TEXT,
    check_id TEXT,
    expense_id TEXT
);

CREATE TABLE qbo_load_attachments (
    ref_id TEXT,
    prep_id TEXT,
    ref_type TEXT,
    content TEXT,
    filename TEXT
);