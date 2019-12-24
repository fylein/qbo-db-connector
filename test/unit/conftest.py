"""
Unit Test Configuration
"""
import logging
import os
import sqlite3

from test.common.utilities import get_mock_qbo

import pytest
from qbo_db_connector import QuickbooksExtractConnector, QuickbooksLoadConnector

logger = logging.getLogger(__name__)


@pytest.fixture
def qbo():
    """
    Quickbooks Online SDK Mock Object
    """
    return get_mock_qbo()


@pytest.fixture
def dbconn():
    """
    Make DB Connection
    :return: DB Connection
    """
    sqlite_db_file = '/tmp/test_qbo.db'
    if os.path.exists(sqlite_db_file):
        os.remove(sqlite_db_file)
    conn = sqlite3.connect(sqlite_db_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    return conn


@pytest.fixture
def qec(qbo, dbconn):
    """
    Quickbooks Extract instance with mock connection
    """
    res = QuickbooksExtractConnector(qbo_connection=qbo, dbconn=dbconn)
    res.create_tables()
    return res


@pytest.fixture
def qlc(qbo, dbconn):
    """
    Quickbooks Load instance with mock connection
    """
    res = QuickbooksLoadConnector(qbo_connection=qbo, dbconn=dbconn)
    res.create_tables()
    return res
