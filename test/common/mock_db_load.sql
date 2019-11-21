-- checks
insert into
qbo_load_checks("bank_account", "entity", "employee_email", "department", "record_date", "id", "currency", "private_note")
values
('142', '67', 'admin1@fyleforqbodemo.com', '7', '2019-09-25', 'C1', 'USD', 'Check Description 1', 'Example Note 1');

insert into
qbo_load_checks("bank_account", "entity", "employee_email", "department", "record_date", "id", "currency", "private_note")
values
('142', '67', 'admin1@fyleforqbodemo.com', '7', '2019-09-26', 'C2', 'USD', 'Check Description 2', 'Example Note 2');

-- check_lineitems

insert into qbo_load_check_lineitems("account", "class", "amount", "description", "check_id", "expense_id")
values ('146', None, 23.98, 'AMAZON', 'C1', 'txUnlP67eNwD');
insert into qbo_load_check_lineitems("account", "class", "amount", "description", "check_id", "expense_id")
values ('146', None, 675.0, 'Testing checks', 'C1', 'txta2oO6f0Fe');

insert into qbo_load_check_lineitems("account", "class", "amount", "description", "check_id", "expense_id")
values ('146', None, 231.981, 'AMAZON', 'C2', 'txUnlP67eNwD');
insert into qbo_load_check_lineitems("account", "class", "amount", "description", "check_id", "expense_id")
values ('146', None, 635.0, 'Testing checks', 'C2', 'txta2oO6f0Fe');