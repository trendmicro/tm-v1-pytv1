## PyTMV1: Python Library for Trend Vision One
[![Build](https://github.com/trendmicro/tm-v1-pytv1/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/trendmicro/tm-v1-pytv1/actions/workflows/build.yml)
[![Lint](https://github.com/trendmicro/tm-v1-pytv1/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/trendmicro/tm-v1-pytv1/actions/workflows/lint.yml)
[![Test](https://github.com/trendmicro/tm-v1-pytv1/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/trendmicro/tm-v1-pytv1/actions/workflows/test.yml)
[![Coverage](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2Ft0mz06%2F6c39ef59cc8beb9595e91fc96793de5b%2Fraw%2Fcoverage.json)](https://github.com/trendmicro/tm-v1-pytv1/actions/workflows/coverage.yml)
[![Pypi: version](https://img.shields.io/pypi/v/pytmv1)](https://pypi.org/project/pytmv1)
[![Downloads](https://pepy.tech/badge/pytmv1)](https://pepy.tech/project/pytmv1)
[![Python: version](https://img.shields.io/pypi/pyversions/pytmv1)](https://pypi.org/project/pytmv1)
[![License: apache](https://img.shields.io/pypi/l/pytmv1)](https://spdx.org/licenses/Apache-2.0.html)
[![Types - mypy](https://img.shields.io/badge/types-mypy-blue.svg)](http://mypy-lang.org)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


#### Prerequisites
Using this project requires at least [Python 3.7](https://www.python.org/downloads/).

#### Features

- A thread-safe client for your application.
- HTTP pooling capabilities.
- Easy integration with Trend Vision One APIs.


#### Configuration
| parameter        | description                                          |
|:-----------------|:-----------------------------------------------------|
| name             | Identify the application using this library.         |
| token            | Authentication token created for your account.       |
| url              | Vision One API url this client connects to.          |
| pool_connections | Number of connection pools to cache (defaults to 1). |
| pool_maxsize     | Maximum size of the pool (defaults to 1).            |

#### Quick start
Installation
```
pip install pytmv1
```

Usage

```python
>> > import pytmv1
>> > client = pytmv1.client("MyApplication", "Token", "https://api.xdr.trendmicro.com")
>> > result = client.list_exceptions()
>> > result.response
GetExceptionListResp(
    next_link=None,
    items=[
        ExceptionObject(
            url='https://*.example.com/path1/*',
            type= < ObjectType.URL: 'url' >,
last_modified_date_time = '2023-01-12T14:05:37Z',
description = 'object description'
)
]
)
>> > result.result_code
ResultCode.SUCCESS
```


#### Build the project
Set virtual env
```console
python3 -m venv venv
source venv/bin/activate
```
Install dependencies
```console
pip install -e ".[dev]"
```
Build
```console
hatch build
```
Run unit tests
```console
pytest --verbose ./tests/unit
```
Run integration tests
  - `$url`: Vision One API url (i.e: https://api.xdr.trendmicro.com)
    
```console
pytest --mock-url="$url" --verbose ./tests/integration
```

Supported APIs
--------------
| Python                                                        | Vision One                                                                                                                                                                         |
|:--------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Connectivity**                                              |                                                                                                                                                                                    |
| `test_connectivity`                                           | [Check availability of service](https://automation.trendmicro.com/xdr/api-v3#tag/Connectivity/paths/~1v3.0~1healthcheck~1connectivity/get)                                         |
| **API Keys**                                                  |                                                                                                                                                                                    |
| `create_api_keys`                                             | [Create API Keys](https://automation.trendmicro.com/xdr/api-v3#tag/API-Keys/paths/~1v3.0~1iam~1apiKeys/post)                                                                       |
| `delete_api_keys`                                             | [Delete API keys](https://automation.trendmicro.com/xdr/api-v3#tag/API-Keys/paths/~1v3.0~1iam~1apiKeys~1delete/post)                                                               |
| `update_api_key`                                              | [Update API key](https://automation.trendmicro.com/xdr/api-v3#tag/API-Keys/paths/~1v3.0~1iam~1apiKeys~1%7Bid%7D/patch)                                                             |
| `get_api_key`                                                 | [Get API key](https://automation.trendmicro.com/xdr/api-v3#tag/API-Keys/paths/~1v3.0~1iam~1apiKeys~1%7Bid%7D/get)                                                                  |
| `get_api_key_list`                                            | [List API keys](https://automation.trendmicro.com/xdr/api-v3#tag/API-Keys/paths/~1v3.0~1iam~1apiKeys/get)                                                                          |
| **Common**                                                    |                                                                                                                                                                                    |
| `get_task_result/get_base_task_result`                        | [Download response task results](https://automation.trendmicro.com/xdr/api-v3#tag/Common/paths/~1v3.0~1response~1tasks~1%7Bid%7D/get)                                              |
| **Custom Scripts**                                            |                                                                                                                                                                                    |
| `get_custom_script_list`                                      | [List custom scripts](https://automation.trendmicro.com/xdr/api-v3#tag/Custom-Script/paths/~1v3.0~1response~1customScripts/get)                                                    |
| `add_custom_script`                                           | [Add custom script](https://automation.trendmicro.com/xdr/api-v3#tag/Custom-Script/paths/~1v3.0~1response~1customScripts/post)                                                     |
| `update_custom_script`                                        | [Update custom script](https://automation.trendmicro.com/xdr/api-v3#tag/Custom-Script/paths/~1v3.0~1response~1customScripts~1%7Bid%7D~1update/post)                                |
| `download_custom_script`                                      | [Download custom script](https://automation.trendmicro.com/xdr/api-v3#tag/Custom-Script/paths/~1v3.0~1response~1customScripts~1%7Bid%7D/get)                                       |
| `delete_custom_script`                                        | [Delete custom script](https://automation.trendmicro.com/xdr/api-v3#tag/Custom-Script/paths/~1v3.0~1response~1customScripts~1%7Bid%7D/delete)                                      |
| `run_custom_script`                                           | [Run custom script](https://automation.trendmicro.com/xdr/api-v3#tag/Custom-Script/paths/~1v3.0~1response~1endpoints~1runScript/post)                                              |
| **Domain Account**                                            |                                                                                                                                                                                    |
| `disable_account`                                             | [Disable user account](https://automation.trendmicro.com/xdr/api-v3#tag/Domain-Account/paths/~1v3.0~1response~1domainAccounts~1disable/post)                                       |                                                                                                                   
| `enable_account`                                              | [Enable user account](https://automation.trendmicro.com/xdr/api-v3#tag/Domain-Account/paths/~1v3.0~1response~1domainAccounts~1enable/post)                                         |
| `reset_password_account`                                      | [Force password reset](https://automation.trendmicro.com/xdr/api-v3#tag/Domain-Account/paths/~1v3.0~1response~1domainAccounts~1resetPassword/post)                                 |
| `sign_out_account`                                            | [Force sign out](https://automation.trendmicro.com/xdr/api-v3#tag/Domain-Account/paths/~1v3.0~1response~1domainAccounts~1signOut/post)                                             |
| **Email**                                                     |                                                                                                                                                                                    |
| `delete_email_message`                                        | [Delete email message](https://automation.trendmicro.com/xdr/api-v3#tag/Email/paths/~1v3.0~1response~1emails~1delete/post)                                                         |
| `quarantine_email_message`                                    | [Quarantine email message](https://automation.trendmicro.com/xdr/api-v3#tag/Email/paths/~1v3.0~1response~1emails~1quarantine/post)                                                 |
| `restore_email_message`                                       | [Restore email message](https://automation.trendmicro.com/xdr/api-v3#tag/Email/paths/~1v3.0~1response~1emails~1restore/post)                                                       |
| **Endpoint**                                                  |                                                                                                                                                                                    |
| `collect_file`                                                | [Collect file](https://automation.trendmicro.com/xdr/api-v3#tag/Endpoint/paths/~1v3.0~1response~1endpoints~1collectFile/post)                                                      |
| `isolate_endpoint`                                            | [Isolate endpoint](https://automation.trendmicro.com/xdr/api-v3#tag/Endpoint/paths/~1v3.0~1response~1endpoints~1isolate/post)                                                      |
| `restore_endpoint`                                            | [Restore endpoint](https://automation.trendmicro.com/xdr/api-v3#tag/Endpoint/paths/~1v3.0~1response~1endpoints~1restore/post)                                                      |
| `terminate_process`                                           | [Terminate process](https://automation.trendmicro.com/xdr/api-v3#tag/Endpoint/paths/~1v3.0~1response~1endpoints~1terminateProcess/post)                                            |
| **Sandbox Analysis**                                          |                                                                                                                                                                                    |
| `download_sandbox_analysis_result`                            | [Download analysis results](https://automation.trendmicro.com/xdr/api-v3#tag/Sandbox-Analysis/paths/~1v3.0~1sandbox~1analysisResults~1{id}~1report/get)                            |
| `download_sandbox_investigation_package`                      | [Download investigation package](https://automation.trendmicro.com/xdr/api-v3#tag/Sandbox-Analysis/paths/~1v3.0~1sandbox~1analysisResults~1{id}~1investigationPackage/get)         |
| `get_sandbox_analysis_result`                                 | [Get analysis results](https://automation.trendmicro.com/xdr/api-v3#tag/Sandbox-Analysis/paths/~1v3.0~1sandbox~1analysisResults~1{id}/get)                                         |
| `get_sandbox_submission_status`                               | [Get submission status](https://automation.trendmicro.com/xdr/api-v3#tag/Sandbox-Analysis/paths/~1v3.0~1sandbox~1tasks~1{id}/get)                                                  |
| `get_sandbox_suspicious_list`                                 | [Download suspicious object list](https://automation.trendmicro.com/xdr/api-v3#tag/Sandbox-Analysis/paths/~1v3.0~1sandbox~1analysisResults~1{id}~1suspiciousObjects/get)           |
| `submit_file_to_sandbox`                                      | [Submit file to sandbox](https://automation.trendmicro.com/xdr/api-v3#tag/Sandbox-Analysis/paths/~1v3.0~1sandbox~1files~1analyze/post)                                             |
| `submit_urls_to_sandbox`                                      | [Submit URLs to sandbox](https://automation.trendmicro.com/xdr/api-v3#tag/Sandbox-Analysis/paths/~1v3.0~1sandbox~1urls~1analyze/post)                                              |
| **Search**                                                    |                                                                                                                                                                                    |
| `get_email_activity_data` `consume_email_activity_data`       | [Get email activity data](https://automation.trendmicro.com/xdr/api-v3#tag/Search/paths/~1v3.0~1search~1emailActivities/get)                                                       |
| `get_email_activity_data_count`                               | [Get email activity data count](https://automation.trendmicro.com/xdr/api-v3#tag/Search/paths/~1v3.0~1search~1emailActivities/get)                                                 |
| `get_endpoint_activity_data` `consume_endpoint_activity_data` | [Get endpoint activity data](https://automation.trendmicro.com/xdr/api-v3#tag/Search/paths/~1v3.0~1search~1endpointActivities/get)                                                 |
| `get_endpoint_activity_data_count`                            | [Get endpoint activity data count](https://automation.trendmicro.com/xdr/api-v3#tag/Search/paths/~1v3.0~1search~1endpointActivities/get)                                           |
| `get_endpoint_data` `consume_endpoint_data`                   | [Get endpoint data](https://automation.trendmicro.com/xdr/api-v3#tag/Search/paths/~1v3.0~1eiqs~1endpoints/get)                                                                     |
| **Suspicious Objects**                                        |                                                                                                                                                                                    |
| `add_to_block_list`                                           | [Add to block list](https://automation.trendmicro.com/xdr/api-v3#tag/Suspicious-Objects/paths/~1v3.0~1response~1suspiciousObjects/post)                                            | 
| `remove_from_block_list`                                      | [Remove from block list](https://automation.trendmicro.com/xdr/api-v3#tag/Suspicious-Objects/paths/~1v3.0~1response~1suspiciousObjects~1delete/post)                               |
| **Suspicious Object Exception List**                          |                                                                                                                                                                                    |
| `add_to_exception_list`                                       | [Add to exception list](https://automation.trendmicro.com/xdr/api-v3#tag/Suspicious-Object-Exception-List/paths/~1v3.0~1threatintel~1suspiciousObjectExceptions/post)              |
| `get_exception_list` `consume_exception_list`                 | [Get exception list](https://automation.trendmicro.com/xdr/api-v3#tag/Suspicious-Object-Exception-List/paths/~1v3.0~1threatintel~1suspiciousObjectExceptions/get)                  |
| `remove_from_exception_list`                                  | [Remove from exception list](https://automation.trendmicro.com/xdr/api-v3#tag/Suspicious-Object-Exception-List/paths/~1v3.0~1threatintel~1suspiciousObjectExceptions~1delete/post) |
| **Suspicious Object List**                                    |                                                                                                                                                                                    |
| `add_to_suspicious_list`                                      | [Add to suspicious object list](https://automation.trendmicro.com/xdr/api-v3#tag/Suspicious-Object-List/paths/~1v3.0~1threatintel~1suspiciousObjects/post)                         |
| `get_suspicious_list` `consume_suspicious_list`               | [List suspicious objects](https://automation.trendmicro.com/xdr/api-v3#tag/Suspicious-Object-List/paths/~1v3.0~1threatintel~1suspiciousObjects/get)                                |
| `remove_from_suspicious_list`                                 | [Remove from suspicious object list](https://automation.trendmicro.com/xdr/api-v3#tag/Suspicious-Object-List/paths/~1v3.0~1threatintel~1suspiciousObjects~1delete/post)            |
| **Workbench**                                                 |                                                                                                                                                                                    |
| `add_alert_note`                                              | [Add alert note](https://automation.trendmicro.com/xdr/api-v3#tag/Workbench-notes/paths/~1v3.0~1workbench~1alerts~1{alertId}~1notes/post)                                          |
| `edit_alert_status`                                           | [Modify alert status](https://automation.trendmicro.com/xdr/api-v3#tag/Workbench/paths/~1v3.0~1workbench~1alerts~1{id}/patch)                                                      |
| `get_alert_details`                                           | [Get alert details](https://automation.trendmicro.com/xdr/api-v3#tag/Workbench/paths/~1v3.0~1workbench~1alerts/get)                                                                |
| `get_alert_list` `consume_alert_list`                         | [Get alerts list](https://automation.trendmicro.com/xdr/api-v3#tag/Workbench/paths/~1v3.0~1workbench~1alerts/get)                                                                  |
| **Workbench Notes**                                           |                                                                                                                                                                                    |
| `add_alert_note`                                              | [Add alert note](https://automation.trendmicro.com/xdr/api-v3#tag/Workbench-notes/paths/~1v3.0~1workbench~1alerts~1{alertId}~1notes/post)                                          |
| `update_alert_note_status`                                    | [Edit alert note](https://automation.trendmicro.com/xdr/api-v3#tag/Workbench-notes/paths/~1v3.0~1workbench~1alerts~1%7BalertId%7D~1notes~1%7Bid%7D/patch)                          |
| `delete_alert_note_status`                                    | [Delete alert notes](https://automation.trendmicro.com/xdr/api-v3#tag/Workbench-notes/paths/~1v3.0~1workbench~1alerts~1%7BalertId%7D~1notes~1delete/post)                          |
| `get_alert_note_details`                                      | [Get alert note](https://automation.trendmicro.com/xdr/api-v3#tag/Workbench-notes/paths/~1v3.0~1workbench~1alerts~1%7BalertId%7D~1notes~1%7Bid%7D/get)                             |
| `get_alert_note_list` `consume_alert_note_list`               | [Get alerts notes](https://automation.trendmicro.com/xdr/api-v3#tag/Workbench-notes/paths/~1v3.0~1workbench~1alerts~1%7BalertId%7D~1notes/get)                                                                 |

Contributing
------------
Read our [contributing guide](https://github.com/trendmicro/tm-v1/blob/main/CONTRIBUTING.md) to learn about our development process, how to propose bug fixes and improvements, and how to build and test your changes to Trend Vision One.

Code of conduct
---------------
Trend Micro has adopted a [Code of Conduct](https://github.com/trendmicro/tm-v1/blob/main/CODE_OF_CONDUCT.md) that we expect project participants to adhere to. Please read the [full text](https://github.com/trendmicro/tm-v1/blob/main/CODE_OF_CONDUCT.md) to understand what actions will and will not be tolerated.

License
-------
Project distributed under the [Apache 2.0](https://spdx.org/licenses/Apache-2.0.html) license.
