# Quickbooks Online Database Connector
Connects Quickbooks online to a database to transfer information to and fro.

## Installation

This project requires [Python 3+](https://www.python.org/downloads/).

1. Download this project and use it (copy it in your project, etc).
2. Install it from [pip](https://pypi.org).

        $ pip install qbo-db-connector

## Usage

To use this connector you'll need these Quickbooks credentials used for OAuth2 authentication: **client ID**, **client secret** and **refresh token**.

This connector is very easy to use.
```python
import logging
import sqlite3

from qbo_db_connector import QuickbooksExtractConnector, QuickbooksLoadConnector


dbconn = sqlite3.connect('/tmp/temp.db')

logger = logging.getLogger('Quickbooks usage')
logging.basicConfig(
    format='%(asctime)s %(name)s: %(message)s', level=logging.INFO, handlers=[logging.StreamHandler()]
)

quickbooks_config = {
    'client_id': '<CLIENT ID>',
    'client_secret': '<CLIENT SECRET>',
    'realm_id': '<REALM ID>',
    'refresh_token': '<REFRESH TOKEN>',
    'base_url': '<API BASE URL>',
    'environment': '<ENVIRONMENT>',
    'web_app_url': '<QUICKBOOKS WEB APP URL>'
}

logger.info('Quickbooks db connector usage')

quickbooks_extract = QuickbooksExtractConnector(config=quickbooks_config, dbconn=dbconn)
quickbooks_load = QuickbooksLoadConnector(config=quickbooks_config, dbconn=dbconn)

# make sure you save the updated refresh token
refresh_token = quickbooks_extract.refresh_token

# extracting
quickbooks_extract.extract_employees()
quickbooks_extract.extract_accounts()
quickbooks_extract.extract_classes()
quickbooks_extract.extract_departments()
quickbooks_extract.extract_home_currency()
quickbooks_extract.extract_exchange_rates()

# loading
quickbooks_load.load_check(check_id='100')
quickbooks_load.load_journal_entry(journal_entry_id='800')
quickbooks_load.load_attachment(ref_id='100', ref_type='check')
```

## Contribute

To contribute to this project follow the steps

* Fork and clone the repository.
* Run `pip install -r requirements.txt`
* Setup pylint precommit hook
    * Create a file `.git/hooks/pre-commit`
    * Copy and paste the following lines in the file - 
        ```bash
        #!/usr/bin/env bash 
        git-pylint-commit-hook
        ```
     * Run `chmod +x .git/hooks/pre-commit`
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
