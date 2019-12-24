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
from qbosdk import QuickbooksOnlineSDK

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
    'environment': '<ENVIRONMENT>',
}

logger.info('Quickbooks db connector usage')

connection = QuickbooksOnlineSDK(
    client_id=quickbooks_config['client_id'],
    client_secret=quickbooks_config['client_secret'],
    refresh_token=quickbooks_config['refresh_token'],
    realm_id=quickbooks_config['realm_id'],
    environment=quickbooks_config['environment']
)

quickbooks_extract = QuickbooksExtractConnector(qbo_connection=connection, dbconn=dbconn)
quickbooks_load = QuickbooksLoadConnector(qbo_connection=connection, dbconn=dbconn)

# make sure you save the updated refresh token
refresh_token = connection.refresh_token

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
quickbooks_load.load_attachments(ref_id='100', ref_type='Purchase')
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
* Make necessary changes
* Run unit tests to ensure everything is fine

## Unit Tests

To run unit tests, run pytest in the following manner:

```
python -m pytest test/unit
```

You should see something like this:
```
================================================================== test session starts ==================================================================
-------------------------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------------------------
2019-12-24 12:10:46 [    INFO] test.unit.test_mocks: Testing mock data (test_mocks.py:18)
PASSED                                                                                                                                                                                                                                                                   [ 69%]
test/unit/test_mocks.py::test_dbconn_mock_setup
-------------------------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------------------------
2019-12-24 12:10:46 [    INFO] test.unit.test_mocks: Testing mock dbconn (test_mocks.py:29)
PASSED                                                                                                                                                                                                                                                                   [ 76%]
test/unit/test_mocks.py::test_qec_mock_setup                                                                                           [100%]

=================================================================== 3 passed in 0.10s ===================================================================

```

## Integration Tests

To run integration tests, you will need a mechanism to connect to a real qbo account. Save this info in a test_credentials.json file in your root directory:

```json
{
  "client_id": "<client_id>",
  "client_secret": "<client_secret>",
  "realm_id": "<realm_id>",
  "refresh_token": "<refresh_token>",
  "environment": "<environment sandbox / production>"
}
```

## Code coverage

To get code coverage report, run this command:

```bash
---------- coverage: platform darwin, python 3.7.4-final-0 -----------
Name                           Stmts   Miss  Cover
--------------------------------------------------
qbo_db_connector/__init__.py       2      0   100%
qbo_db_connector/extract.py       79      3    96%
qbo_db_connector/load.py          71      9    87%
--------------------------------------------------
TOTAL                            152     12    92%
```

To get an html report, run this command:

```bash
python -m pytest --cov=qbo_db_connector --cov-report html:cov_html
```

We want to maintain code coverage of more than 90% for this project at all times.

Please note that maintaining a score of 10 is important as the CI pylint action fails when a pull request is opened

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
