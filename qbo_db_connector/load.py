"""
QuickbooksLoadConnector(): Connection between Quickbooks and Database
"""
from os import path
import logging
from typing import Dict, List

import pandas as pd

from qbosdk import QuickbooksOnlineSDK

logger = logging.getLogger('QuickbooksLoadConnector')


class QuickbooksLoadConnector:
    """
    Extract data from Database and load to Quickbooks
    """
    def __init__(self, qbo_connection: QuickbooksOnlineSDK, dbconn):
        self.__qbo_connection = qbo_connection
        self.__dbconn = dbconn

    def create_tables(self):
        """
        Creates DB tables
        :return: None
        """
        basepath = path.dirname(__file__)
        ddl_path = path.join(basepath, 'load_ddl.sql')
        ddl_sql = open(ddl_path, 'r').read()
        self.__dbconn.executescript(ddl_sql)

    @staticmethod
    def __construct_check_line_items(check_line_items: List[Dict]) -> List[Dict]:
        """
        Create check line items
        :param check_line_items: list of check line items extracted from database
        :return: constructed line items
        """
        lines = []

        for line in check_line_items:
            line = {
                'Description': line['description'],
                'DetailType': 'AccountBasedExpenseLineDetail',
                'Amount': line['amount'],
                'AccountBasedExpenseLineDetail': {
                    'AccountRef': {
                        'value': line['account']
                    },
                    'ClassRef': {
                        'value': line['class']
                    }
                }
            }
            lines.append(line)

        return lines

    @staticmethod
    def __construct_check(check: Dict, custom_transaction_date: str = None,
                          custom_private_note: str = None, custom_doc_number: str = None) -> Dict:
        """
        Create a check
        :param check: check object extracted from database
        :param custom_transaction_date: To be sent when transaction date needs to be changed.
        :param custom_private_note: To be sent when private note needs to be changed.
        :return: constructed check
        """
        qbo_load_check = {
            'PaymentType': 'Check',
            'AccountRef': {
                'value': check['bank_account']
            },
            'EntityRef': {
                'value': check['entity']
            },
            'DepartmentRef': {
                'value': check['department']
            },
            'TxnDate': custom_transaction_date if custom_transaction_date else check['record_date'],
            "CurrencyRef": {
                "value": check['currency']
            },
            'PrivateNote': custom_private_note if custom_private_note else check['private_note'],
            'Line': [],
            'DocNumber': custom_doc_number
        }

        return qbo_load_check

    def load_check(self, check_id: str, custom_transaction_date: str = None,
                   custom_private_note: str = None, custom_doc_number: str = None) -> (bool, Dict):
        """
        Load check to Quicbooks
        :param custom_doc_number: Custom doc number
        :param custom_private_note: To be sent when private note needs to be changed.
        :param custom_transaction_date: To be sent when transaction date needs to be changed.
        :param check_id: Check id to be loaded
        :return: True for successful export or False for True, Successful or Unsuccessful response Dict
        """
        logger.info('Loading checks in to Quickbooks.')

        check: Dict = pd.read_sql_query(
            sql="SELECT * FROM qbo_load_checks where id = '{0}'".format(check_id),
            con=self.__dbconn
        ).to_dict(orient='records')[0]

        qbo_load_check: Dict = self.__construct_check(check, custom_transaction_date,
                                                      custom_private_note, custom_doc_number)

        check_line_items: List[Dict] = pd.read_sql_query(
            sql="SELECT * FROM qbo_load_check_lineitems where check_id = '{0}'".format(check_id),
            con=self.__dbconn).to_dict(orient='records')

        assert check_line_items, 'check line items do not exists stopping export'

        lines = self.__construct_check_line_items(check_line_items)
        qbo_load_check['Line'] = lines

        response = self.__qbo_connection.purchases.post(qbo_load_check)

        loaded_check: Dict = {
            'id': response['Purchase']['Id'],
            'url': '{0}/app/check?txnId={1}'.format(self.__qbo_connection.web_app_url, response['Purchase']['Id']),
            'entity': check['employee_email'],
            'record_date': check['record_date'],
            'department': check['department'],
            'amount': response['Purchase']['TotalAmt']
        }
        logger.info('Check with id %s created against expenses', response['Purchase']['Id'])
        return loaded_check

    @staticmethod
    def __construct_journal_entry_line_items(journal_entry_line_items: List[Dict]) -> List[Dict]:
        """
        Create journal entry line items
        :param journal_entry_line_items: list of journal entry line items extracted from database
        :return: constructed line items
        """
        lines = []

        for line in journal_entry_line_items:
            line = {
                'DetailType': 'JournalEntryLineDetail',
                'Amount': line['amount'],
                'Description': line['description'],
                'JournalEntryLineDetail': {
                    'PostingType': line['posting_type'],
                    'AccountRef': {
                        'value': line['account']
                    },
                    'DepartmentRef': {
                        'value': line['department']
                    },
                    'ClassRef': {
                        'value': line['class']
                    },
                    'Entity': {
                        'EntityRef': {
                            'value': line['entity']
                        }
                    }
                }
            }
            lines.append(line)

        return lines

    @staticmethod
    def __construct_journal_entry(journal_entry: Dict, custom_transaction_date: str = None,
                                  custom_private_note: str = None, custom_doc_number: str = None) -> Dict:
        """
        Create a journal entry
        :param journal_entry: journal entry object extracted from database
        :param custom_transaction_date: To be sent when transaction date needs to be changed.
        :param custom_private_note: To be sent when private note needs to be changed.
        :return: constructed journal entry
        """
        qbo_load_journal_entry = {
            'TxnDate': custom_transaction_date if custom_transaction_date else journal_entry['record_date'],
            'PrivateNote': custom_private_note if custom_private_note else journal_entry['private_note'],
            'Line': [],
            'CurrencyRef': {
                "value": journal_entry['currency']
            },
            'DocNumber': custom_doc_number
        }

        return qbo_load_journal_entry

    def load_journal_entry(self, journal_entry_id: str, custom_transaction_date: str = None,
                           custom_private_note: str = None, custom_doc_number: str = None):
        """
        Load journal entry to Quickbooks
        :param custom_doc_number: Doc number for journal_entry
        :param journal_entry_id: Journal Entry unique id
        :param custom_transaction_date: To be sent when transaction date needs to be changed.
        :param custom_private_note: To be sent when private note needs to be changed.
        :return: True for successful export or False for True, Successful or Unsuccessful response Dict
        """
        logger.info('Loading journal entries in to Quickbooks.')

        journal_entry: Dict = pd.read_sql_query(
            sql="SELECT * FROM qbo_load_journal_entries where id = '{0}'".format(journal_entry_id),
            con=self.__dbconn
        ).to_dict(orient='records')[0]

        qbo_load_journal_entry: Dict = self.__construct_journal_entry(
            journal_entry=journal_entry, custom_transaction_date=custom_transaction_date,
            custom_private_note=custom_private_note, custom_doc_number=custom_doc_number
        )

        journal_entry_line_items: List[Dict] = pd.read_sql_query(
            sql="SELECT * FROM qbo_load_journal_entry_lineitems where journal_entry_id = '{0}'".format(
                journal_entry_id),
            con=self.__dbconn
        ).to_dict(orient='records')

        assert journal_entry_line_items, 'check line items do not exists stopping export'

        qbo_load_journal_entry_line_items: List[Dict] = self.__construct_journal_entry_line_items(
            journal_entry_line_items
        )
        qbo_load_journal_entry['Line'] = qbo_load_journal_entry_line_items

        response = self.__qbo_connection.journal_entries.post(qbo_load_journal_entry)

        loaded_journal_entry: Dict = {
            'id': response['JournalEntry']['Id'],
            'url': '{0}/app/journal?txnId={1}'.format(self.__qbo_connection.web_app_url,
                                                      response['JournalEntry']['Id']),
            'entity': journal_entry['employee_email'],
            'record_date': journal_entry['record_date'],
            'amount': response['JournalEntry']['TotalAmt']
        }

        logger.info('Journal Entry with id %s created', response['JournalEntry']['Id'])
        return loaded_journal_entry

    def load_attachments(self, ref_id: str, ref_type: str, prep_id: str) -> List:
        """
        Link attachments to objects Quickbooks
        :param prep_id: prep id for export
        :param ref_id: object id
        :param ref_type: type of object
        :return: True for success, False for failure
        """
        attachments = pd.read_sql_query(
            "select * from qbo_load_attachments where prep_id = '{0}' and ref_type = '{1}'".format(prep_id, ref_type),
            self.__dbconn
        )

        logger.info('Loading attachments to QBO')

        if len(attachments.index):
            responses = []
            for attachment in attachments.to_dict(orient='records'):
                response = self.__qbo_connection.attachments.post(
                    ref_id=ref_id,
                    ref_type=ref_type,
                    content=attachment['content'],
                    file_name=attachment['filename']
                )
                responses.append(response)
            return responses
        return []
