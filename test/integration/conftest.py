"""
Integration Tests
"""
import logging
import sqlite3

from test.common.utilities import get_mock_qbo, qec, qlc
import pytest

logger = logging.getLogger(__name__)


@pytest.fixture
def mock_qbo():
    """
    Returns mock QBO instance
    """
    return get_mock_qbo()


def dbconn():
    """
    Initializing db connection
    """
    sqlite_db_file = '/tmp/test_qbo.db'
    return sqlite3.connect(sqlite_db_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)


@pytest.fixture(scope='module')
def qbo_extract():
    """
    Returns QBO extract instance
    """
    connection = dbconn()
    return qec(connection)


@pytest.fixture(scope='module')
def qbo_load():
    """
    Returns QBO extract instance
    """
    connection = dbconn()
    return qlc(connection)


@pytest.fixture
def qbo_ex(qbo_extract):
    """
    Return QBO Extract connector objects
    """
    res = qbo_extract
    res.create_tables()
    return res


@pytest.fixture
def qbo_lo(qbo_load):
    """
    Return QBO Extract connector objects
    """
    res = qbo_load
    res.create_tables()
    return res
