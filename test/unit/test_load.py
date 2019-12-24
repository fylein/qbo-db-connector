"""
QBO Load Unit Tests
"""
import logging

from test.common.utilities import dbconn_get_load_object_by_id

logger = logging.getLogger(__name__)


def test_get_qbo_load_check(qlc, dbconn):
    """
    Check load Unit Test
    """
    assert not dbconn_get_load_object_by_id(dbconn, 'qbo_load_checks', 'C1'), 'qbo check id should not exist'

    sql = open('./test/common/mock_db_load.sql').read()
    dbconn.executescript(sql)

    response = qlc.load_check(check_id='C1')
    assert response['id'] == '1453', 'qbo check id not matching'


def test_get_qbo_load_journal_entry(qlc, dbconn):
    """
    Journal Enrty load Unit Test
    """
    assert not dbconn_get_load_object_by_id(dbconn, 'qbo_load_journal_entries', 'J1'), 'qbo je id should not exist'

    sql = open('./test/common/mock_db_load.sql').read()
    dbconn.executescript(sql)

    response = qlc.load_journal_entry(journal_entry_id='J1')
    assert response['id'] == '1467', 'qbo check id not matching'
