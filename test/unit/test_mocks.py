"""
Mock Environment Tests
"""
import sqlite3
import logging

from test.common.utilities import dict_compare_keys, dbconn_table_num_rows

import pytest

logger = logging.getLogger(__name__)


def test_qbo_mock_setup(qbo):
    """
    Testing mock data
    """
    logger.info('Testing mock data')

    assert qbo.accounts.get()[0]['Id'] == '140', 'qbo mock setup is broken'
    assert qbo.departments.get()[0]['Name'] == 'Bebe Rexha', 'qbo mock setup is broken'
    assert qbo.employees.get() != [], 'qbo employees get should not return empty List'


def test_dbconn_mock_setup(dbconn):
    """
    Test mock dbconn
    """
    logger.info('Testing mock dbconn')

    with pytest.raises(sqlite3.OperationalError):
        dbconn_table_num_rows(dbconn, 'qbo_extract_accounts')


def test_qec_mock_setup(qec, dbconn):
    """
    Testing Extract connector with mock instance
    """
    logger.info('Testing Extract connector with mock instance')

    qec.create_tables()
    assert dbconn_table_num_rows(dbconn, 'qbo_extract_accounts') == 0, 'Unclean db'
    assert dbconn_table_num_rows(dbconn, 'qbo_extract_classes') == 0, 'Unclean db'
    assert dbconn_table_num_rows(dbconn, 'qbo_extract_employees') == 0, 'Unclean db'


def test_dict_compare():
    """
    Testing dict compare function
    """
    logger.info('Testing dict compare function')

    d1 = {
        'k1': 'xxx', 'k2': 2, 'k3': [1, 2], 'k4': {'k41': [2], 'k42': {'k421': 20}}
    }
    d2 = {
        'k1': 'xyx', 'k3': [1, 2], 'k4': {'k42': {'k421': 20}}
    }
    d3 = {
        'k1': 'xyz', 'k3': [3, 2], 'k4': {'k42': {'k421': 40}}
    }
    assert dict_compare_keys(d1, d2) == ['->k2', '->k4->k41'], 'not identifying diff properly'
    assert dict_compare_keys(d2, d3) == [], 'should return no diff'


def test_qlc_mock_setup(qlc, dbconn):
    """
    Testing Load Connector with mock instance
    """
    logger.info('Testing Load Connector with mock instance')

    qlc.create_tables()
    sqlpath = './test/common/mock_db_load.sql'
    sql = open(sqlpath, 'r').read()
    dbconn.executescript(sql)

    assert dbconn_table_num_rows(dbconn, 'qbo_load_checks') == 2, 'Unclean db'
    assert dbconn_table_num_rows(dbconn, 'qbo_load_check_lineitems') == 4, 'Unclean db'
