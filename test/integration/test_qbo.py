"""
QBO DB Connector Integration Tests
"""
import logging

from test.common.utilities import dict_compare_keys, dbconn_table_row_dict
from .conftest import dbconn

logger = logging.getLogger(__name__)


def test_accounts(qbo_ex, mock_qbo):
    """
    Test QBO Extract accounts
    :param qbo_ex: qbo_ex extract instance
    :param mock_qbo: mock instance
    :return: None
    """
    qbo_ex.extract_accounts()
    accounts = dbconn_table_row_dict(dbconn(), 'qbo_extract_accounts')

    mock_accounts = mock_qbo.accounts.get()

    assert dict_compare_keys(accounts, mock_accounts[0]) == [], \
        'qbo_extract.extract_accounts has stuff that mock_qbo.accounts.get doesnt'
    assert dict_compare_keys(mock_accounts[0], accounts) == [], \
        'mock_qbo.accounts.get() has stuff that qbo_extract.extract_accounts doesnt'


def test_employees(qbo_ex, mock_qbo):
    """
    Test QBO Extract employees
    :param qbo_ex: qbo_ex extract instance
    :param mock_qbo: mock instance
    :return: None
    """
    qbo_ex.extract_employees()
    employees = dbconn_table_row_dict(dbconn(), 'qbo_extract_employees')

    mock_employees = mock_qbo.employees.get()

    assert dict_compare_keys(employees, mock_employees[0]) == [], \
        'qbo_extract.extract_employees has stuff that mock_qbo.employees.get doesnt'
    assert dict_compare_keys(mock_employees[0], employees) == [], \
        'mock_qbo.employees.get() has stuff that qbo_extract.extract_employees doesnt'


def test_departments(qbo_ex, mock_qbo):
    """
    Test QBO Extract departments
    :param qbo_ex: qbo_ex extract instance
    :param mock_qbo: mock instance
    :return: None
    """
    qbo_ex.extract_departments()
    departments = dbconn_table_row_dict(dbconn(), 'qbo_extract_departments')

    mock_departments = mock_qbo.departments.get()

    assert dict_compare_keys(departments, mock_departments[0]) == [], \
        'qbo_extract.extract_departments has stuff that mock_qbo.departments.get doesnt'
    assert dict_compare_keys(mock_departments[0], departments) == [], \
        'mock_qbo.departments.get() has stuff that qbo_extract.extract_departments doesnt'


def test_classes(qbo_ex, mock_qbo):
    """
    Test QBO Extract classes
    :param qbo_ex: qbo_ex extract instance
    :param mock_qbo: mock instance
    :return: None
    """
    qbo_ex.extract_classes()
    classes = dbconn_table_row_dict(dbconn(), 'qbo_extract_classes')

    mock_classes = mock_qbo.classes.get()

    assert dict_compare_keys(classes, mock_classes[0]) == [], \
        'qbo_extract.extract_classes has stuff that mock_qbo.classes.get doesnt'
    assert dict_compare_keys(mock_classes[0], classes) == [], \
        'mock_qbo.classes.get() has stuff that qbo_extract.extract_classes doesnt'


def test_home_currency(qbo_ex, mock_qbo):
    """
    Test QBO Extract home_currency
    :param qbo_ex: qbo_ex extract instance
    :param mock_qbo: mock instance
    :return: None
    """
    qbo_ex.extract_home_currency()
    home_currency = dbconn_table_row_dict(dbconn(), 'qbo_extract_home_currency')

    mock_home_currency = mock_qbo.home_currency.get()

    assert dict_compare_keys(home_currency, mock_home_currency[0]) == [], \
        'qbo_extract.extract_home_currency has stuff that mock_qbo.home_currency.get doesnt'
    assert dict_compare_keys(mock_home_currency[0], home_currency) == [], \
        'mock_qbo.home_currency.get() has stuff that qbo_extract.extract_home_currency doesnt'


def test_exchange_rates(qbo_ex, mock_qbo):
    """
    Test QBO Extract exchange_rates
    :param qbo_ex: qbo_ex extract instance
    :param mock_qbo: mock instance
    :return: None
    """
    qbo_ex.extract_exchange_rates()
    exchange_rates = dbconn_table_row_dict(dbconn(), 'qbo_extract_exchange_rates')

    mock_exchange_rates = mock_qbo.exchange_rates.get()

    assert dict_compare_keys(exchange_rates, mock_exchange_rates[0]) == [], \
        'qbo_extract.extract_exchange_rates has stuff that mock_qbo.exchange_rates.get doesnt'
    assert dict_compare_keys(mock_exchange_rates[0], exchange_rates) == [], \
        'mock_qbo.exchange_rates.get() has stuff that qbo_extract.extract_exchange_rates doesnt'


def test_load_checks(qbo_lo, mock_qbo):
    """
    Test QBO Load checks
    :param qbo_lo: qbo load instance
    :param mock_qbo: mock instance
    :return: None
    """
    sql = open('./test/common/mock_db_load.sql').read()
    dbconn().executescript(sql)

    check = qbo_lo.load_check(check_id='C1')
    mock_check = mock_qbo.purchases.save()

    assert dict_compare_keys(check, mock_check['Purchase']) == [], \
        'qbo_load.load_check has stuff that mock_qbo.load_check doesnt'
    assert dict_compare_keys(mock_check['Purchase'], check) == [], \
        'mock_qbo.load_check has stuff that qbo_load.load_check doesnt'


def test_load_journal_entries(qbo_lo, mock_qbo):
    """
    Test QBO Load journal_entries
    :param qbo_lo: qbo load instance
    :param mock_qbo: mock instance
    :return: None
    """
    sql = open('./test/common/mock_db_load.sql').read()
    dbconn().executescript(sql)

    journal_entry = qbo_lo.load_journal_entry(journal_entry_id='J1')
    mock_journal_entry = mock_qbo.journal_entries.save()

    assert dict_compare_keys(journal_entry, mock_journal_entry['JournalEntry']) == [], \
        'qbo_load.load_journal_entry has stuff that mock_qbo.load_journal_entry doesnt'
    assert dict_compare_keys(mock_journal_entry['JournalEntry'], journal_entry) == [], \
        'mock_qbo.load_journal_entry has stuff that qbo_load.load_journal_entry doesnt'
