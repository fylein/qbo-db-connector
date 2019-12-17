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
