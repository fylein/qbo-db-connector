"""
QuickbooksExtractConnector(): Connection between Quickbooks and Database
"""
from os import path
import logging

from typing import Dict, List
import pandas as pd

from qbosdk import QuickbooksOnlineSDK

logger = logging.getLogger('QuickbooksExtractConnector')


class QuickbooksExtractConnector:
    """
    Extract data from Quickbooks and load to Database
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
        ddl_path = path.join(basepath, 'extract_ddl.sql')
        ddl_sql = open(ddl_path, 'r').read()
        self.__dbconn.executescript(ddl_sql)

    def extract_accounts(self) -> List[str]:
        """
        Extract accounts from Quickbooks
        :return: List of account ids
        """
        logger.info('Extracting accounts from Quickbooks.')

        data = self.__qbo_connection.accounts.get()

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

        data = self.__qbo_connection.classes.get()

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

        data = self.__qbo_connection.departments.get()

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

        data = self.__qbo_connection.employees.get()

        logger.info('%s employees Extracted.', len(data))

        if data:
            df = pd.DataFrame(data)

            if 'GivenName' not in df:
                df['GivenName'] = None

            if 'FamilyName' not in df:
                df['FamilyName'] = None

            if 'DisplayName' not in df:
                df['DisplayName'] = None

            df = df[['Id', 'GivenName', 'FamilyName', 'DisplayName']]
            df.to_sql('qbo_extract_employees', self.__dbconn, if_exists='append', index=False)
            return df['Id'].to_list()

        return []

    def extract_exchange_rates(self) -> List[Dict]:
        """
        Extracts currency exchange rates for present day from Quickbooks
        :return: List of exchange rates Dict
        """
        logger.info('Extracting exchange rates from Quickbooks.')

        exchange_rates = self.__qbo_connection.exchange_rates.get()

        logger.info('%s exchange rates Extracted.', len(exchange_rates))

        if exchange_rates:
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
        logger.info('Extracting home currency')

        data = self.__qbo_connection.preferences.get()

        currency_dict = [
            {
                'home_currency': data['CurrencyPrefs']['HomeCurrency']['value']
            }
        ]

        logger.info('home currency extracted')

        df_currency = pd.DataFrame(currency_dict)

        df_currency.to_sql('qbo_extract_home_currency', self.__dbconn, if_exists='append', index=False)

        return currency_dict[0]['home_currency']
