"""
QuickbooksExtractConnector(): Connection between Quickbooks and Database
"""
from os import path
import json
import logging

from datetime import datetime, timedelta
from typing import Dict, List

import requests
import pandas as pd

from intuitlib.client import AuthClient

logger = logging.getLogger('QuickbooksExtractConnector')

GET_ACCOUNTS_URL = '{0}/v3/company/{1}/query?query=select Id, Name from Account STARTPOSITION {2} MAXRESULTS 1000'
GET_EMPLOYEES_URL = '{0}/v3/company/{1}/query?query=select Id, GivenName, FamilyName from Employee STARTPOSITION {2} ' \
                    'MAXRESULTS 1000 '
GET_CLASSES_URL = '{0}/v3/company/{1}/query?query=select Id, Name from Class STARTPOSITION {2} MAXRESULTS 1000'
GET_DEPARTMENTS_URL = '{0}/v3/company/{1}/query?query=select Id, Name from Department STARTPOSITION {2} MAXRESULTS 1000'
GET_HOME_CURRENCY = '{0}/v3/company/{1}/preferences'
GET_EXCHANGE_RATES = "{0}/v3/company/{1}/query?query=select * from ExchangeRate where AsOfDate = '{2}' MAXRESULTS 1000"


class QuickbooksExtractConnector:
    """
    Extract data from Quickbooks and load to Database
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
        return auth_client.refresh_token

    def __get_all(self, url: str, object_type: str) -> List[Dict]:
        """
        Gets ell the objects of a particular type
        :param url: GET URL of object
        :param object_type: type of object
        :return: list of objects
        """
        start_position = 1

        request_url = url.format(self.__base_url, self.__realm_id, start_position)
        data = json.loads(requests.get(url=request_url, headers=self.__request_header).text)

        objects = []

        query_response = data['QueryResponse']

        while query_response:
            objects.extend(query_response[object_type])
            start_position = start_position + 1000

            request_url = url.format(self.__base_url, self.__realm_id, start_position)
            data = json.loads(requests.get(url=request_url, headers=self.__request_header).text)

            query_response = data['QueryResponse']

        return objects

    def create_tables(self):
        """
        Creates DB tables
        :return: None
        """
        basepath = path.dirname(__file__)
        ddl_path = path.join(basepath, 'extract_ddl.sql')
        ddl_sql = open(ddl_path, 'r').read()
        self.__dbconn.executescript(ddl_sql)

    def extract_accounts(self) -> List[str]:
        """
        Extract accounts from Quickbooks
        :return: List of account ids
        """
        logger.info('Extracting accounts from Quickbooks.')

        data = self.__get_all(GET_ACCOUNTS_URL, 'Account')

        logger.info('%s accounts Extracted.', len(data))

        if data:
            df = pd.DataFrame(data)

            df = df[['Id', 'Name']]
            df.to_sql('qbo_extract_accounts', self.__dbconn, if_exists='append', index=False)

            return df['Id'].to_list()

        return []

    def extract_classes(self) -> List[str]:
        """
        Extract classes from Quickbooks
        :return: List of class ids
        """
        logger.info('Extracting classes from Quickbooks.')

        data = self.__get_all(GET_CLASSES_URL, 'Class')

        logger.info('%s classes Extracted.', len(data))

        if data:
            df = pd.DataFrame(data)
            df = df[['Id', 'Name']]
            df.to_sql('qbo_extract_classes', self.__dbconn, if_exists='append', index=False)

            return df['Id'].to_list()

        return []

    def extract_departments(self) -> List[str]:
        """
        Extract departments from Quickbooks
        :return: List of department ids
        """
        logger.info('Extracting departments from Quickbooks.')

        data = self.__get_all(GET_DEPARTMENTS_URL, 'Department')

        logger.info('%s departments Extracted.', len(data))

        if data:
            df = pd.DataFrame(data)
            df = df[['Id', 'Name']]
            df.to_sql('qbo_extract_departments', self.__dbconn, if_exists='append', index=False)

            return df['Id'].to_list()

        return []

    def extract_employees(self) -> List[str]:
        """
        Extract employees from Quickbooks
        :return: List of employee Ids
        """
        logger.info('Extracting employees from Quickbooks.')

        data = self.__get_all(GET_EMPLOYEES_URL, 'Employee')

        logger.info('%s employees Extracted.', len(data))

        if data:
            df = pd.DataFrame(data)
            df = df[['Id', 'GivenName', 'FamilyName']]
            df.to_sql('qbo_extract_employees', self.__dbconn, if_exists='append', index=False)
            return df['Id'].to_list()

        return []

    def extract_exchange_rates(self) -> List[Dict]:
        """
        Extracts currency exchange rates for present day from Quickbooks
        :return: List of exchange rates Dict
        """
        logger.info('Extracting exchange rates from Quickbooks.')

        as_of_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        url = GET_EXCHANGE_RATES.format(self.__base_url, self.__realm_id, as_of_date)
        data = requests.get(url, headers=self.__request_header).text
        exchange_rates = json.loads(data)['QueryResponse']['ExchangeRate']

        logger.info('%s exchange rates Extracted.', len(exchange_rates))

        if data:
            df_exchange_rates = pd.DataFrame(exchange_rates)

            df_exchange_rates = df_exchange_rates[['SourceCurrencyCode', 'TargetCurrencyCode', 'Rate', 'AsOfDate']]

            df_exchange_rates.to_sql('qbo_extract_exchange_rates', self.__dbconn,
                                     if_exists='append', index=False)
            return df_exchange_rates.to_dict(orient='records')

        return []

    def extract_home_currency(self) -> str:
        """
        Extracts home currency of Quickbooks account
        :return: home currency
        """
        request_url = GET_HOME_CURRENCY.format(self.__base_url, self.__realm_id)

        data = json.loads(requests.get(url=request_url, headers=self.__request_header).text)

        currency_dict = [
            {
                'home_currency': data['Preferences']['CurrencyPrefs']['HomeCurrency']['value']
            }
        ]

        df_currency = pd.DataFrame(currency_dict)

        df_currency.to_sql('qbo_extract_home_currency', self.__dbconn, if_exists='append', index=False)

        return currency_dict[0]['home_currency']
