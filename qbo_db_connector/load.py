"""
QuickbooksLoadConnector(): Connection between Quickbooks and Database
"""
from os import path
import json
import logging
from typing import Dict, List
import textwrap

import requests
import pandas as pd

from intuitlib.client import AuthClient

logger = logging.getLogger('QuickbooksLoadConnector')

POST_CHECK_URL = '{0}/v3/company/{1}/purchase?minorversion=38'
POST_JOURNAL_ENTRY_URL = '{0}/v3/company/{1}/journalentry?minorversion=38'
POST_ATTACHMENT_URL = '{0}/v3/company/{1}/attachable'
UPLOAD_FILE_URL = '{0}/v3/company/{1}/upload'


class QuickbooksLoadConnector:
    """
    Extract data from Database and load to Quickbooks
    """
    def __init__(self, config, dbconn):
        self.__config = config
        self.__realm_id = config.get('realm_id')
        self.__base_url = config.get('base_url')
        self.__web_app_url = config.get('web_app_url')

        refresh_token = config.get('refresh_token')

        self.__dbconn = dbconn

        self.__request_header = {
            'Accept': 'application/json',
            'Content-type': 'application/json'
        }

        self.__file_header = {
            'Content-Type': 'multipart/form-data; boundary={0}'.format('YOjcLaTlykb6OxfYJx4O07j1MweeMFem'),
            'Accept': 'application/json',
            'Connection': 'close'
        }

        self.refresh_token = self.__update_refresh_token(refresh_token)

        logger.info('Quickbooks Connection Successful')

    def __update_refresh_token(self, refresh_token: str) -> str:
        """
        Updates and returns the new refresh token
        :param refresh_token: old refresh token
        :return: new refresh token
        """
        auth_client = AuthClient(
            client_id=self.__config.get('client_id'),
            client_secret=self.__config.get('client_secret'),
            redirect_uri=self.__config.get('redirect_uri'),
            environment=self.__config.get('environment')
        )

        auth_client.refresh(refresh_token=refresh_token)

        access_token = auth_client.access_token

        self.__request_header.update({
            'Authorization': 'Bearer {0}'.format(access_token)
        })
        self.__file_header.update({
            'Authorization': 'Bearer {0}'.format(access_token)
        })
        return refresh_token

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

        load_success = False
        url = POST_CHECK_URL.format(self.__base_url, self.__realm_id)

        check: Dict = pd.read_sql_query(
            sql="SELECT * FROM qbo_load_checks where id = '{0}'".format(check_id),
            con=self.__dbconn
        ).to_dict(orient='records')[0]

        qbo_load_check: Dict = self.__construct_check(check, custom_transaction_date,
                                                      custom_private_note, custom_doc_number)

        check_line_items: List[Dict] = pd.read_sql_query(
            sql="SELECT * FROM qbo_load_check_lineitems where check_id = '{0}'".format(check_id),
            con=self.__dbconn).to_dict(orient='records')

        if not check_line_items:
            return load_success, {}

        lines = self.__construct_check_line_items(check_line_items)
        qbo_load_check['Line'] = lines

        response = json.loads(
            requests.post(url, headers=self.__request_header, data=json.dumps(qbo_load_check)).text
        )

        if 'Fault' in response:
            logger.info(response)

            response_error: Dict = {
                'message': response['Fault']['Error'][0]['Message'],
                'code': response['Fault']['Error'][0]['code']
            }
            logger.info('Ouickbooks Bad Request with message: %s, code: %s',
                        response['Fault']['Error'][0]['Message'], response['Fault']['Error'][0]['code'])
            return load_success, response_error

        load_success = True

        loaded_check: Dict = {
            'id': response['Purchase']['Id'],
            'url': '{0}/app/check?txnId={1}'.format(self.__web_app_url, response['Purchase']['Id']),
            'entity': check['employee_email'],
            'record_date': check['record_date'],
            'department': check['department'],
            'amount': response['Purchase']['TotalAmt']
        }
        logger.info('Check with id %s created against expenses', response['Purchase']['Id'])
        return load_success, loaded_check

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

        url = POST_JOURNAL_ENTRY_URL.format(self.__base_url, self.__realm_id)

        load_success = False

        journal_entry: Dict = pd.read_sql_query(
            sql="SELECT * FROM qbo_load_journal_entries where id = '{0}'".format(journal_entry_id),
            con=self.__dbconn
        ).to_dict(orient='records')[0]

        qbo_load_journal_entry: Dict = self.__construct_journal_entry(
            journal_entry=journal_entry, custom_transaction_date=custom_transaction_date,
            custom_private_note=custom_private_note, custom_doc_number=custom_doc_number
        )

        journal_entry_line_items: List[Dict] = pd.read_sql_query(
            sql="SELECT * FROM qbo_load_journal_entry_lineitems where journal_entry_id = '{0}'".format(journal_entry_id),
            con=self.__dbconn
        ).to_dict(orient='records')

        if not journal_entry_line_items:
            return load_success, {}

        qbo_load_journal_entry_line_items: List[Dict] = self.__construct_journal_entry_line_items(
            journal_entry_line_items
        )
        qbo_load_journal_entry['Line'] = qbo_load_journal_entry_line_items

        response = json.loads(
            requests.post(url, headers=self.__request_header, data=json.dumps(qbo_load_journal_entry)).text
        )

        if 'Fault' in response:
            response_error: Dict = {
                'message': response['Fault']['Error'][0]['Message'],
                'code': response['Fault']['Error'][0]['code']
            }
            logger.info('Ouickbooks Bad Request with message: %s, code: %s',
                        response['Fault']['Error'][0]['Message'], response['Fault']['Error'][0]['code'])
            return load_success, response_error

        load_success = True

        loaded_journal_entry: Dict = {
            'id': response['JournalEntry']['Id'],
            'url': '{0}/app/journal?txnId={1}'.format(self.__web_app_url, response['JournalEntry']['Id']),
            'entity': journal_entry['employee_email'],
            'record_date': journal_entry['record_date'],
            'amount': response['JournalEntry']['TotalAmt']
        }

        logger.info('Journal Entry with id %s created', response['JournalEntry']['Id'])
        return load_success, loaded_journal_entry

    @staticmethod
    def __get_content_type(file_name: str) -> str or None:
        """
        Gets content type of supported file types
        :param file_name: name of the file
        :return: content-type or None
        """
        extension = file_name.split('.')[-1]

        content_types: Dict = {
            'ai': 'application/postscript',
            'csv': 'text/csv',
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'eps': 'application/postscript',
            'gif': 'image/gif',
            'jpeg': 'image/jpeg',
            'jpg': 'image/jpg',
            'png': 'image/png',
            'ods': 'application/vnd.oasis.opendocument.spreadsheet',
            'pdf': 'application/pdf',
            'rtf': 'text/rtf',
            'tif': 'image/tiff',
            'txt': 'text/plain',
            'xls': 'application/vnd.ms-excel',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'xml': 'text/xml'
        }

        return content_types.get(extension.lower())

    def __upload_file(self, content, file_name: str) -> Dict:
        """
        Upload file to Quickbooks
        :param content: Content in base64
        :param file_name: name of the file
        :return: Returns file object as Dict
        """
        binary_data = content

        url = UPLOAD_FILE_URL.format(self.__base_url, self.__realm_id)

        boundary = 'YOjcLaTlykb6OxfYJx4O07j1MweeMFem'

        content_type = self.__get_content_type(file_name)

        body = {
            'Content-Type': content_type
        }

        if content_type:
            request_body = textwrap.dedent(
                """
                --%s
                Content-Disposition: form-data; name="file_metadata_01";
                Content-Type: application/json
                %s
                --%s
                Content-Disposition: form-data; name="file_content_01"; filename="%s"
                Content-Type: %s
                Content-Transfer-Encoding: base64

                %s

                --%s--
                """
            ) % (boundary, json.dumps(body), boundary, file_name, content_type, binary_data, boundary)

            response = requests.post(data=str(request_body), headers=self.__file_header, url=url)

            return json.loads(response.text)['AttachableResponse'][0]['Attachable']

        return {}

    def load_attachment(self, ref_id: str, ref_type: str) -> bool:
        """
        Link attachments to objects Quickbooks
        :param ref_id: object id
        :param ref_type: type of object
        :return: True for success, False for failure
        """
        attachment = pd.read_sql_query(
            "select * from qbo_load_attachments where ref_id = '{0}' and ref_type = '{1}'".format(ref_id, ref_type),
            self.__dbconn
        )
        load_success = False

        if len(attachment.index):
            attachment = attachment.to_dict(orient='records')[0]
            url = POST_ATTACHMENT_URL.format(self.__base_url, self.__realm_id)
            file = self.__upload_file(attachment['content'], attachment['filename'])

            if file:
                attachable_ref = [
                    {
                        'EntityRef': {
                            'type': 'Purchase' if ref_type == 'check' else 'JournalEntry',
                            'value': ref_id
                        }
                    }
                ]
                file['AttachableRef'] = attachable_ref
                requests.post(url=url, data=json.dumps(file), headers=self.__request_header)
                load_success = True

        return load_success
