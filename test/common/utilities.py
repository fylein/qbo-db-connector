import copy
import json
import logging
import os
from os import path
from unittest.mock import Mock

logger = logging.getLogger(__name__)


def get_mock_qbo_dict(filename):
    """
    Get moch qbo dictionary by filename
    :param filename: name of the file
    :return:
    """
    basepath = path.dirname(__file__)
    filepath = path.join(basepath, filename)
    mock_xero_json = open(filepath, 'r').read()
    mock_qbo_dict = json.loads(mock_xero_json)
    return mock_qbo_dict


def get_mock_qbo_from_file(filename):
    mock_qbo_dict = get_mock_qbo_dict(filename)
    mock_xero = Mock()
    mock_xero.contacts.all.return_value = mock_qbo_dict['employees']
    mock_xero.trackingcategories.all.return_value = mock_qbo_dict['accounts']
    mock_xero.invoices.all.return_value = mock_qbo_dict['invoices_all']
    mock_xero.invoices.filter.return_value = mock_qbo_dict['invoices_all']
    mock_xero.invoices.get.return_value = mock_qbo_dict['invoices_get']
    mock_xero.accounts.all.return_value = mock_qbo_dict['accounts']

    mock_xero.invoices.save.return_value = copy.deepcopy(mock_qbo_dict['invoices_get'][0:1])
    return mock_xero


def get_mock_qbo():
    return get_mock_qbo_from_file('mock_xero.json')


def get_mock_xero_empty():
    return get_mock_qbo_from_file('mock_xero_empty.json')


def dict_compare_keys(d1, d2, key_path=''):
    """
    Compare two dicts recursively and see if dict1 has any keys that dict2 does not
    Returns: list of key paths
    """
    res = []
    if not d1:
        return res
    if not isinstance(d1, dict):
        return res
    for k in d1:
        if k not in d2:
            missing_key_path = f'{key_path}->{k}'
            res.append(missing_key_path)
        else:
            if isinstance(d1[k], dict):
                key_path1 = f'{key_path}->{k}'
                res1 = dict_compare_keys(d1[k], d2[k], key_path1)
                res = res + res1
            elif isinstance(d1[k], list):
                key_path1 = f'{key_path}->{k}[0]'
                dv1 = d1[k][0] if len(d1[k]) > 0 else None
                dv2 = d2[k][0] if len(d2[k]) > 0 else None
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
    query = f'select * from {tablename} limit 1'
    row = dbconn.cursor().execute(query).fetchone()
    return dict(row)


# def xero_connect():
#     XERO_PRIVATE_KEYFILE = os.environ.get('XERO_PRIVATE_KEYFILE', None)
#     XERO_CONSUMER_KEY = os.environ.get('XERO_CONSUMER_KEY', None)
#     if XERO_PRIVATE_KEYFILE is None:
#         raise Exception('XERO_PRIVATE_KEYFILE is not set')
#     if XERO_CONSUMER_KEY is None:
#         raise Exception('XERO_CONSUMER_KEY is not set')
#     with open(XERO_PRIVATE_KEYFILE) as keyfile:
#         rsa_key = keyfile.read()
#     credentials = PrivateCredentials(XERO_CONSUMER_KEY, rsa_key)
#     # used to connect to xero
#     return Xero(credentials)
