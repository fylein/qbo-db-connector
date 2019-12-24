"""
Extract Unit Tests
"""
import logging

from test.common.utilities import (dbconn_table_num_rows, dbconn_table_row_dict,
                                   dict_compare_keys, get_mock_qbo_empty)
from qbo_db_connector import QuickbooksExtractConnector

logger = logging.getLogger(__name__)


def test_accounts(qbo, qec, dbconn):
    """
    Test Extract Accounts
    :param qbo: mock qbo sdk object
    :param qec: qbo extract connection
    :param dbconn: sqlite db connection
    :return: None
    """
    qec.create_tables()
    accounts = qec.extract_accounts()
    qbo_data = qbo.accounts.get()[0]
    db_data = dbconn_table_row_dict(dbconn, 'qbo_extract_accounts')
    assert dict_compare_keys(db_data, qbo_data) == [], 'db table has some columns that xero doesnt'
    assert dbconn_table_num_rows(dbconn, 'qbo_extract_accounts') == len(qbo.accounts.get()), 'row count mismatch'
    assert len(accounts) == 67, 'return value messed up'


def test_employees(qbo, qec, dbconn):
    """
    Test Extract Employees
    :param qbo: mock qbo sdk object
    :param qec: qbo extract connection
    :param dbconn: sqlite db connection
    :return: None
    """
    qec.create_tables()
    employees = qec.extract_employees()
    qbo_data = qbo.employees.get()[0]
    db_data = dbconn_table_row_dict(dbconn, 'qbo_extract_employees')
    assert dict_compare_keys(db_data, qbo_data) == [], 'db table has some columns that xero doesnt'
    assert dbconn_table_num_rows(dbconn, 'qbo_extract_employees') == len(qbo.employees.get()), 'row count mismatch'
    assert len(employees) == 7, 'return value messed up'


def test_departments(qbo, qec, dbconn):
    """
    Test Extract Departments
    :param qbo: mock qbo sdk object
    :param qec: qbo extract connection
    :param dbconn: sqlite db connection
    :return: None
    """
    qec.create_tables()
    departments = qec.extract_departments()
    qbo_data = qbo.departments.get()[0]
    db_data = dbconn_table_row_dict(dbconn, 'qbo_extract_departments')
    assert dict_compare_keys(db_data, qbo_data) == [], 'db table has some columns that xero doesnt'
    assert dbconn_table_num_rows(dbconn, 'qbo_extract_departments') == len(qbo.departments.get()), 'row count mismatch'
    assert len(departments) == 14, 'return value messed up'


def test_classes(qbo, qec, dbconn):
    """
    Test Extract Classes
    :param qbo: mock qbo sdk object
    :param qec: qbo extract connection
    :param dbconn: sqlite db connection
    :return: None
    """
    qec.create_tables()
    classes = qec.extract_classes()
    qbo_data = qbo.classes.get()[0]
    db_data = dbconn_table_row_dict(dbconn, 'qbo_extract_classes')
    assert dict_compare_keys(db_data, qbo_data) == [], 'db table has some columns that xero doesnt'
    assert dbconn_table_num_rows(dbconn, 'qbo_extract_classes') == len(qbo.classes.get()), 'row count mismatch'
    assert len(classes) == 7, 'return value messed up'


def test_exchange_rates(qbo, qec, dbconn):
    """
    Test Extract Exchange Rates
    :param qbo: mock qbo sdk object
    :param qec: qbo extract connection
    :param dbconn: sqlite db connection
    :return: None
    """
    qec.create_tables()
    exchange_rates = qec.extract_exchange_rates()
    qbo_data = qbo.exchange_rates.get()[0]
    db_data = dbconn_table_row_dict(dbconn, 'qbo_extract_exchange_rates')
    assert dict_compare_keys(db_data, qbo_data) == [], 'db table has some columns that xero doesnt'
    assert dbconn_table_num_rows(dbconn, 'qbo_extract_exchange_rates') == len(qbo.exchange_rates.get()), \
        'row count mismatch'
    assert len(exchange_rates) == 144, 'return value messed up'


def test_empty(dbconn):
    """
    Test Extract Empty lists
    :param dbconn: sqlite db connection
    :return: None
    """
    qbo = get_mock_qbo_empty()
    res = QuickbooksExtractConnector(qbo_connection=qbo, dbconn=dbconn)
    res.create_tables()
    assert res.extract_accounts() == []
    assert res.extract_departments() == []
    assert res.extract_classes() == []
    assert res.extract_employees() == []
    assert res.extract_exchange_rates() == []
