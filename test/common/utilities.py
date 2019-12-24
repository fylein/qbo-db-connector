"""
Common utility for QBO connector tests
"""
import copy
import json
import logging

from os import path
from unittest.mock import Mock

from qbosdk import QuickbooksOnlineSDK
from qbo_db_connector import QuickbooksExtractConnector, QuickbooksLoadConnector

logger = logging.getLogger(__name__)


def dict_factory(cursor, row):
    """
    Sqlite dictionary row factory
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_mock_qbo_dict(filename):
    """
    Get moch qbo dictionary by filename
    :param filename: name of the file
    :return:
    """
    basepath = path.dirname(__file__)
    filepath = path.join(basepath, filename)
    mock_qbo_json = open(filepath, 'r').read()
    mock_qbo_dict = json.loads(mock_qbo_json)
    return mock_qbo_dict


def get_mock_qbo_from_file(filename):
    """
    Returns mock objects for QBO Extract Connectors
    :param: JSON file name
    """
    mock_qbo_dict = get_mock_qbo_dict(filename)
    mock_qbo = Mock()
    mock_qbo.accounts.get.return_value = mock_qbo_dict['accounts']
    mock_qbo.classes.get.return_value = mock_qbo_dict['classes']
    mock_qbo.departments.get.return_value = mock_qbo_dict['departments']
    mock_qbo.employees.get.return_value = mock_qbo_dict['employees']
    mock_qbo.home_currency.get.return_value = mock_qbo_dict['home_currency']
    mock_qbo.exchange_rates.get.return_value = mock_qbo_dict['exchange_rates']
    mock_qbo.purchases.save.return_value = copy.deepcopy(mock_qbo_dict['check_response'])
    mock_qbo.journal_entries.save.return_value = copy.deepcopy(mock_qbo_dict['journal_entry_response'])
    mock_qbo.purchases.post.return_value = copy.deepcopy(mock_qbo_dict['check_sdk_response'])
    mock_qbo.journal_entries.post.return_value = copy.deepcopy(mock_qbo_dict['journal_entry_sdk_response'])
    return mock_qbo


def get_mock_qbo():
    """
    Get mock qbo with data
    """
    return get_mock_qbo_from_file('mock_qbo.json')


def get_mock_qbo_empty():
    """
    Get mock qbo with empty data
    """
    return get_mock_qbo_from_file('mock_qbo_empty.json')


def dict_compare_keys(dictionary1, dictionary2, key_path=''):
    """
    Compare two dicts recursively and see if dict1 has any keys that dict2 does not
    Returns: list of key paths
    """
    res = []
    if not dictionary1:
        return res
    if not isinstance(dictionary1, dict):
        return res
    for k in dictionary1:
        if k not in dictionary2:
            missing_key_path = f'{key_path}->{k}'
            res.append(missing_key_path)
        else:
            if isinstance(dictionary1[k], dict):
                key_path1 = f'{key_path}->{k}'
                res1 = dict_compare_keys(dictionary1[k], dictionary2[k], key_path1)
                res = res + res1
            elif isinstance(dictionary1[k], list):
                key_path1 = f'{key_path}->{k}[0]'
                dv1 = dictionary1[k][0] if len(dictionary1[k]) > 0 else None
                dv2 = dictionary2[k][0] if len(dictionary2[k]) > 0 else None
                res1 = dict_compare_keys(dv1, dv2, key_path1)
                res = res + res1
    return res


def dbconn_table_num_rows(dbconn, tablename):
    """
    Helper function to calculate number of rows
    """
    dbconn.row_factory = dict_factory
    query = f'select count(*) as count from {tablename}'
    return dbconn.cursor().execute(query).fetchone()['count']


def dbconn_table_row_dict(dbconn, tablename):
    """
    Gets one row as dictionary
    :param dbconn: db connection
    :param tablename: name of the table
    :return: db row as dict
    """
    dbconn.row_factory = dict_factory
    query = f'select * from {tablename} limit 1'
    row = dbconn.cursor().execute(query).fetchone()
    return row


def dbconn_get_load_object_by_id(dbconn, tablename, object_id):
    """
    Get load object by Id
    """
    dbconn.row_factory = dict_factory
    query = f"select * from {tablename} where id = '{object_id}'"
    row = dbconn.cursor().execute(query).fetchall()
    return row


def qbo_connect():
    """
    QBO SDK connection
    :return: qbo connection
    """
    file = open('test_credentials.json', 'r')
    quickbooks_config = json.load(file)

    qbo_connection = QuickbooksOnlineSDK(
        client_id=quickbooks_config['client_id'],
        client_secret=quickbooks_config['client_secret'],
        refresh_token=quickbooks_config['refresh_token'],
        realm_id=quickbooks_config['realm_id'],
        environment=quickbooks_config['environment']
    )

    quickbooks_config['refresh_token'] = qbo_connection.refresh_token
    with open('test_credentials.json', 'w') as fp:
        json.dump(quickbooks_config, fp)

    return qbo_connection


def qec(dbconn):
    """
    QBO Connector connection
    :param: db connection
    """
    qbo_extract = QuickbooksExtractConnector(qbo_connection=qbo_connect(), dbconn=dbconn)
    return qbo_extract


def qlc(dbconn):
    """
    QBO Connector connection
    :param: db connection
    """
    qbo_load = QuickbooksLoadConnector(qbo_connection=qbo_connect(), dbconn=dbconn)
    return qbo_load
