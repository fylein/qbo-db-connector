"""
Common utility for QBO connector tests
"""
import json
import logging

from os import path
from unittest.mock import Mock

from qbo_db_connector.extract import QuickbooksExtractConnector

logger = logging.getLogger(__name__)


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
    mock_qbo.accounts.all.return_value = mock_qbo_dict['employees']
    mock_qbo.classes.all.return_value = mock_qbo_dict['classes']
    mock_qbo.departments.all.return_value = mock_qbo_dict['departments']
    mock_qbo.employees.all.return_value = mock_qbo_dict['employees']
    mock_qbo.home_currency.all.return_value = mock_qbo_dict['home_currency']
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
    query = f'select count(*) from {tablename}'
    return dbconn.cursor().execute(query).fetchone()[0]


def dbconn_table_row_dict(dbconn, tablename):
    """
    Gets one row as dictionary
    :param dbconn: db connection
    :param tablename: name of the table
    :return: db row as dict
    """
    query = f'select * from {tablename} limit 1'
    row = dbconn.cursor().execute(query).fetchone()
    return row


def qbo_connect(dbconn):
    """
    QBO Connector connection
    :param: db connection
    """
    file = open('test_credentials.json', 'r')
    qbo_credentials = json.load(file)

    qbo_extract = QuickbooksExtractConnector(config=qbo_credentials, dbconn=dbconn)
    qbo_credentials['refresh_token'] = qbo_extract

    with open('result.json', 'w') as fp:
        json.dump(qbo_credentials, fp)
    return qbo_extract
