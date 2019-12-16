"""
Integration Tests
"""
import logging
import os
import sqlite3

from test.common.utilities import get_mock_qbo, qbo_connect
import pytest

logger = logging.getLogger(__name__)


@pytest.fixture
def mock_qbo():
    """
    Returns mock QBO instance
    """
    return get_mock_qbo()


@pytest.fixture
def dbconn():
    """
    Initializing db connection
    """
    sqlite_db_file = '/tmp/test_qbo.db'
    if os.path.exists(sqlite_db_file):
        os.remove(sqlite_db_file)
    return sqlite3.connect(sqlite_db_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)


@pytest.fixture(scope='module')
def qbo_extract():
    """
    Returns QBO extract instance
    """
    return qbo_connect(dbconn)


@pytest.fixture
def qbo():
    """
    Return QBO Extract connector objects
    """
    res = qbo_extract()
    res.create_tables()
    return res
