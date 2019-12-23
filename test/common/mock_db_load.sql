-- checks
insert into
qbo_load_checks("bank_account", "entity", "employee_email", "department", "record_date", "id", "currency", "private_note")
values
('142', '67', 'admin1@fyleforqbodemo.com', '7', '2019-09-25', 'C1', 'USD', 'Check Description 1');

insert into
qbo_load_checks("bank_account", "entity", "employee_email", "department", "record_date", "id", "currency", "private_note")
values
('142', '67', 'admin1@fyleforqbodemo.com', '7', '2019-09-26', 'C2', 'USD', 'Check Description 2');

-- check_lineitems

insert into qbo_load_check_lineitems("account", "class", "amount", "description", "check_id", "expense_id")
values ('146', null, 23.98, 'AMAZON', 'C1', 'txUnlP67eNwD');
insert into qbo_load_check_lineitems("account", "class", "amount", "description", "check_id", "expense_id")
values ('146', null, 675.0, 'Testing checks', 'C1', 'txta2oO6f0Fe');

insert into qbo_load_check_lineitems("account", "class", "amount", "description", "check_id", "expense_id")
values ('146', null, 231.981, 'AMAZON', 'C2', 'txUnlP67eNwD');
insert into qbo_load_check_lineitems("account", "class", "amount", "description", "check_id", "expense_id")
values ('146', null, 635.0, 'Testing checks', 'C2', 'txta2oO6f0Fe');

-- journal entries
insert into
qbo_load_journal_entries("employee_email", "record_date", "id", "currency", "private_note")
values
('admin1@fyleforqbodemo.com', '2019-09-25', 'J1', 'USD', 'Journal Entry Description 1');

insert into
qbo_load_journal_entries("employee_email", "record_date", "id", "currency", "private_note")
values
('admin1@fyleforqbodemo.com', '2019-09-26', 'J2', 'USD', 'Journal Entry Description 2');

-- journal entry lineitems

insert into qbo_load_journal_entry_lineitems("posting_type", "entity",
"account", "department", "class", "amount", "description", "journal_entry_id", "expense_id")
values ('Debit', '67', '146', '7', null, 23.98, 'AMAZON', 'J1', 'txUnlP67eNwD');
insert into qbo_load_journal_entry_lineitems("posting_type", "entity",
"account", "department", "class", "amount", "description", "journal_entry_id", "expense_id")
values ('Credit', '67', '161', '7', null, 23.98, 'AMAZON', 'J1', 'txUnlP67eNwD');

insert into qbo_load_journal_entry_lineitems("posting_type", "entity",
"account", "department", "class", "amount", "description", "journal_entry_id", "expense_id")
values ('Debit', '67', '146', '7', null, 23.98, 'AMAZON', 'J2', 'txta2oO6f0Fe');
insert into qbo_load_journal_entry_lineitems("posting_type", "entity",
"account", "department", "class", "amount", "description", "journal_entry_id", "expense_id")
values ('Credit', '67', '161', '7', null, 23.98, 'AMAZON', 'J2', 'txta2oO6f0Fe');