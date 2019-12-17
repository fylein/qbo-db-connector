"""
QBO DB Connector Integration Tests
"""
import logging

from test.common.utilities import dict_compare_keys, dbconn_table_row_dict
from .conftest import dbconn

logger = logging.getLogger(__name__)


def test_accounts(qbo, mock_qbo):
    """
    Test QBO Extract accounts
    :param qbo: qbo extract instance
    :param mock_qbo: mock instance
    :return: None
    """
    qbo.extract_accounts()
    accounts = dbconn_table_row_dict(dbconn(), 'qbo_extract_accounts')

    mock_accounts = mock_qbo.accounts.all()

    assert dict_compare_keys(accounts, mock_accounts[0]) == [], \
        'qbo_extract.extract_accounts has stuff that mock_qbo.accounts.all doesnt'
    assert dict_compare_keys(mock_accounts[0], accounts) == [], \
        'mock_qbo.accounts.all() has stuff that qbo_extract.extract_accounts doesnt'


def test_employees(qbo, mock_qbo):
    """
    Test QBO Extract employees
    :param qbo: qbo extract instance
    :param mock_qbo: mock instance
    :return: None
    """
    qbo.extract_employees()
    employees = dbconn_table_row_dict(dbconn(), 'qbo_extract_employees')

    mock_employees = mock_qbo.employees.all()

    assert dict_compare_keys(employees, mock_employees[0]) == [], \
        'qbo_extract.extract_employees has stuff that mock_qbo.employees.all doesnt'
    assert dict_compare_keys(mock_employees[0], employees) == [], \
        'mock_qbo.employees.all() has stuff that qbo_extract.extract_employees doesnt'


def test_departments(qbo, mock_qbo):
    """
    Test QBO Extract departments
    :param qbo: qbo extract instance
    :param mock_qbo: mock instance
    :return: None
    """
    qbo.extract_departments()
    departments = dbconn_table_row_dict(dbconn(), 'qbo_extract_departments')

    mock_departments = mock_qbo.departments.all()

    assert dict_compare_keys(departments, mock_departments[0]) == [], \
        'qbo_extract.extract_departments has stuff that mock_qbo.departments.all doesnt'
    assert dict_compare_keys(mock_departments[0], departments) == [], \
        'mock_qbo.departments.all() has stuff that qbo_extract.extract_departments doesnt'


def test_classes(qbo, mock_qbo):
    """
    Test QBO Extract classes
    :param qbo: qbo extract instance
    :param mock_qbo: mock instance
    :return: None
    """
    qbo.extract_classes()
    classes = dbconn_table_row_dict(dbconn(), 'qbo_extract_classes')

    mock_classes = mock_qbo.classes.all()

    assert dict_compare_keys(classes, mock_classes[0]) == [], \
        'qbo_extract.extract_classes has stuff that mock_qbo.classes.all doesnt'
    assert dict_compare_keys(mock_classes[0], classes) == [], \
        'mock_qbo.classes.all() has stuff that qbo_extract.extract_classes doesnt'
    
    
def test_home_currency(qbo, mock_qbo):
    """
    Test QBO Extract home_currency
    :param qbo: qbo extract instance
    :param mock_qbo: mock instance
    :return: None
    """
    qbo.extract_home_currency()
    home_currency = dbconn_table_row_dict(dbconn(), 'qbo_extract_home_currency')

    mock_home_currency = mock_qbo.home_currency.all()

    assert dict_compare_keys(home_currency, mock_home_currency[0]) == [], \
        'qbo_extract.extract_home_currency has stuff that mock_qbo.home_currency.all doesnt'
    assert dict_compare_keys(mock_home_currency[0], home_currency) == [], \
        'mock_qbo.home_currency.all() has stuff that qbo_extract.extract_home_currency doesnt'


def test_exchange_rates(qbo, mock_qbo):
    """
    Test QBO Extract exchange_rates
    :param qbo: qbo extract instance
    :param mock_qbo: mock instance
    :return: None
    """
    qbo.extract_exchange_rates()
    exchange_rates = dbconn_table_row_dict(dbconn(), 'qbo_extract_exchange_rates')

    mock_exchange_rates = mock_qbo.exchange_rates.all()

    assert dict_compare_keys(exchange_rates, mock_exchange_rates[0]) == [], \
        'qbo_extract.extract_exchange_rates has stuff that mock_qbo.exchange_rates.all doesnt'
    assert dict_compare_keys(mock_exchange_rates[0], exchange_rates) == [], \
        'mock_qbo.exchange_rates.all() has stuff that qbo_extract.extract_exchange_rates doesnt'
