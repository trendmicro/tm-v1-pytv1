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
Using this project requires at least [Python 3.8](https://www.python.org/downloads/).

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
>> > client = pytmv1.init("MyApplication", "Token", "https://api.xdr.trendmicro.com")
>> > result = client.object.list_exception()
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
| Python                                         | Vision One                                                                                                                                                                                         |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Connectivity**                               |                                                                                                                                                                                                    |
| `system.check_connectivity`                    | [Check availability of service](https://automation.trendmicro.com/xdr/api-v3#tag/Connectivity/paths/~1v3.0~1healthcheck~1connectivity/get)                                                         |
| **API Keys**                                   |                                                                                                                                                                                                    |
| `api_key.create`                               | [Create API Keys](https://automation.trendmicro.com/xdr/api-v3#tag/API-Keys/paths/~1v3.0~1iam~1apiKeys/post)                                                                                       |
| `api_key.get`                                  | [Get API key](https://automation.trendmicro.com/xdr/api-v3#tag/API-Keys/paths/~1v3.0~1iam~1apiKeys~1%7Bid%7D/get)                                                                                  |
| `api_key.update`                               | [Update API key](https://automation.trendmicro.com/xdr/api-v3#tag/API-Keys/paths/~1v3.0~1iam~1apiKeys~1%7Bid%7D/patch)                                                                             |
| `api_key.delete`                               | [Delete API keys](https://automation.trendmicro.com/xdr/api-v3#tag/API-Keys/paths/~1v3.0~1iam~1apiKeys~1delete/post)                                                                               |
| `api_key.[list, consume]`                      | [List API keys](https://automation.trendmicro.com/xdr/api-v3#tag/API-Keys/paths/~1v3.0~1iam~1apiKeys/get)                                                                                          |
| **Common**                                     |                                                                                                                                                                                                    |
| `task.get_result`                              | [Download response task results](https://automation.trendmicro.com/xdr/api-v3#tag/Common/paths/~1v3.0~1response~1tasks~1%7Bid%7D/get)                                                              |
| **Custom Scripts**                             |                                                                                                                                                                                                    |
| `script.create`                                | [Add custom script](https://automation.trendmicro.com/xdr/api-v3#tag/Custom-Script/paths/~1v3.0~1response~1customScripts/post)                                                                     |
| `script.download`                              | [Download custom script](https://automation.trendmicro.com/xdr/api-v3#tag/Custom-Script/paths/~1v3.0~1response~1customScripts~1%7Bid%7D/get)                                                       |
| `script.update`                                | [Update custom script](https://automation.trendmicro.com/xdr/api-v3#tag/Custom-Script/paths/~1v3.0~1response~1customScripts~1%7Bid%7D~1update/post)                                                |
| `script.delete`                                | [Delete custom script](https://automation.trendmicro.com/xdr/api-v3#tag/Custom-Script/paths/~1v3.0~1response~1customScripts~1%7Bid%7D/delete)                                                      |
| `script.run`                                   | [Run custom script](https://automation.trendmicro.com/xdr/api-v3#tag/Custom-Script/paths/~1v3.0~1response~1endpoints~1runScript/post)                                                              |
| `script.[list, consume]`                       | [List custom scripts](https://automation.trendmicro.com/xdr/api-v3#tag/Custom-Script/paths/~1v3.0~1response~1customScripts/get)                                                                    |
| **Domain Account**                             |                                                                                                                                                                                                    |
| `account.enable`                               | [Enable user account](https://automation.trendmicro.com/xdr/api-v3#tag/Domain-Account/paths/~1v3.0~1response~1domainAccounts~1enable/post)                                                         |
| `account.disable`                              | [Disable user account](https://automation.trendmicro.com/xdr/api-v3#tag/Domain-Account/paths/~1v3.0~1response~1domainAccounts~1disable/post)                                                       |
| `account.sign_out`                             | [Force sign out](https://automation.trendmicro.com/xdr/api-v3#tag/Domain-Account/paths/~1v3.0~1response~1domainAccounts~1signOut/post)                                                             |
| `account.reset`                                | [Force password reset](https://automation.trendmicro.com/xdr/api-v3#tag/Domain-Account/paths/~1v3.0~1response~1domainAccounts~1resetPassword/post)                                                 |
| **Email**                                      |                                                                                                                                                                                                    |
| `email.restore`                                | [Restore email message](https://automation.trendmicro.com/xdr/api-v3#tag/Email/paths/~1v3.0~1response~1emails~1restore/post)                                                                       |
| `email.quarantine`                             | [Quarantine email message](https://automation.trendmicro.com/xdr/api-v3#tag/Email/paths/~1v3.0~1response~1emails~1quarantine/post)                                                                 |
| `email.delete`                                 | [Delete email message](https://automation.trendmicro.com/xdr/api-v3#tag/Email/paths/~1v3.0~1response~1emails~1delete/post)                                                                         |
| **Endpoint**                                   |                                                                                                                                                                                                    |
| `endpoint.collect_file`                        | [Collect file](https://automation.trendmicro.com/xdr/api-v3#tag/Endpoint/paths/~1v3.0~1response~1endpoints~1collectFile/post)                                                                      |
| `endpoint.isolate`                             | [Isolate endpoint](https://automation.trendmicro.com/xdr/api-v3#tag/Endpoint/paths/~1v3.0~1response~1endpoints~1isolate/post)                                                                      |
| `endpoint.restore`                             | [Restore endpoint](https://automation.trendmicro.com/xdr/api-v3#tag/Endpoint/paths/~1v3.0~1response~1endpoints~1restore/post)                                                                      |
| `endpoint.terminate_process`                   | [Terminate process](https://automation.trendmicro.com/xdr/api-v3#tag/Endpoint/paths/~1v3.0~1response~1endpoints~1terminateProcess/post)                                                            |
| **Observed Attack Techniques**                 |                                                                                                                                                                                                    |
| `oat.[list, consume]`                          | [Get Observed Attack Techniques events](https://automation.trendmicro.com/xdr/api-v3#tag/Observed-Attack-Techniques/paths/~1v3.0~1oat~1detections/get)                                             |
| **Sandbox Analysis**                           |                                                                                                                                                                                                    |
| `sandbox.submit_file`                          | [Submit file to sandbox](https://automation.trendmicro.com/xdr/api-v3#tag/Sandbox-Analysis/paths/~1v3.0~1sandbox~1files~1analyze/post)                                                             |
| `sandbox.submit_url`                           | [Submit URLs to sandbox](https://automation.trendmicro.com/xdr/api-v3#tag/Sandbox-Analysis/paths/~1v3.0~1sandbox~1urls~1analyze/post)                                                              |
| `sandbox.get_analysis_result`                  | [Get analysis results](https://automation.trendmicro.com/xdr/api-v3#tag/Sandbox-Analysis/paths/~1v3.0~1sandbox~1analysisResults~1{id}/get)                                                         |
| `sandbox.get_submission_status`                | [Get submission status](https://automation.trendmicro.com/xdr/api-v3#tag/Sandbox-Analysis/paths/~1v3.0~1sandbox~1tasks~1{id}/get)                                                                  |
| `sandbox.download_analysis_result`             | [Download analysis results](https://automation.trendmicro.com/xdr/api-v3#tag/Sandbox-Analysis/paths/~1v3.0~1sandbox~1analysisResults~1{id}~1report/get)                                            |
| `sandbox.download_investigation_package`       | [Download investigation package](https://automation.trendmicro.com/xdr/api-v3#tag/Sandbox-Analysis/paths/~1v3.0~1sandbox~1analysisResults~1{id}~1investigationPackage/get)                         |
| `sandbox.list_suspicious`                      | [Download suspicious object list](https://automation.trendmicro.com/xdr/api-v3#tag/Sandbox-Analysis/paths/~1v3.0~1sandbox~1analysisResults~1{id}~1suspiciousObjects/get)                           |
| **Search**                                     |                                                                                                                                                                                                    |
| `email.get_activity_count`                     | [Get email activity data count](https://automation.trendmicro.com/xdr/api-v3#tag/Search/paths/~1v3.0~1search~1emailActivities/get)                                                                 |
| `email.[list_activity, consume_activity]`      | [Get email activity data](https://automation.trendmicro.com/xdr/api-v3#tag/Search/paths/~1v3.0~1search~1emailActivities/get)                                                                       |
| `endpoint.get_activity_count`                  | [Get endpoint activity data count](https://automation.trendmicro.com/xdr/api-v3#tag/Search/paths/~1v3.0~1search~1endpointActivities/get)                                                           |
| `endpoint.[list_data, consume_data]`           | [Get endpoint data](https://automation.trendmicro.com/xdr/api-v3#tag/Search/paths/~1v3.0~1eiqs~1endpoints/get)                                                                                     |
| `endpoint.[list_activity, consume_activity]`   | [Get endpoint activity data](https://automation.trendmicro.com/xdr/api-v3#tag/Search/paths/~1v3.0~1search~1endpointActivities/get)                                                                 |
| **Suspicious Objects**                         |                                                                                                                                                                                                    |
| `object.add_block`                             | [Add to block list](https://automation.trendmicro.com/xdr/api-v3#tag/Suspicious-Objects/paths/~1v3.0~1response~1suspiciousObjects/post)                                                            | 
| `object.delete_block`                          | [Remove from block list](https://automation.trendmicro.com/xdr/api-v3#tag/Suspicious-Objects/paths/~1v3.0~1response~1suspiciousObjects~1delete/post)                                               |
| **Suspicious Object Exception List**           |                                                                                                                                                                                                    |
| `object.add_exception`                         | [Add to exception list](https://automation.trendmicro.com/xdr/api-v3#tag/Suspicious-Object-Exception-List/paths/~1v3.0~1threatintel~1suspiciousObjectExceptions/post)                              |
| `object.delete_exception`                      | [Remove from exception list](https://automation.trendmicro.com/xdr/api-v3#tag/Suspicious-Object-Exception-List/paths/~1v3.0~1threatintel~1suspiciousObjectExceptions~1delete/post)                 |
| `object.[list_exception, consume_exception]`   | [Get exception list](https://automation.trendmicro.com/xdr/api-v3#tag/Suspicious-Object-Exception-List/paths/~1v3.0~1threatintel~1suspiciousObjectExceptions/get)                                  |
| **Suspicious Object List**                     |                                                                                                                                                                                                    |
| `object.add_suspicious`                        | [Add to suspicious object list](https://automation.trendmicro.com/xdr/api-v3#tag/Suspicious-Object-List/paths/~1v3.0~1threatintel~1suspiciousObjects/post)                                         |
| `object.delete_suspicious`                     | [Remove from suspicious object list](https://automation.trendmicro.com/xdr/api-v3#tag/Suspicious-Object-List/paths/~1v3.0~1threatintel~1suspiciousObjects~1delete/post)                            |
| `object.[list_suspicious, consume_suspicious]` | [List suspicious objects](https://automation.trendmicro.com/xdr/api-v3#tag/Suspicious-Object-List/paths/~1v3.0~1threatintel~1suspiciousObjects/get)                                                |
| **Workbench**                                  |                                                                                                                                                                                                    |
| `alert.get`                                    | [Get alert details](https://automation.trendmicro.com/xdr/api-v3#tag/Workbench/paths/~1v3.0~1workbench~1alerts/get)                                                                                |
| `alert.update_status`                          | [Modify alert status](https://automation.trendmicro.com/xdr/api-v3#tag/Workbench/paths/~1v3.0~1workbench~1alerts~1{id}/patch)                                                                      |
| `alert.[list, consume]`                        | [Get alerts list](https://automation.trendmicro.com/xdr/api-v3#tag/Workbench/paths/~1v3.0~1workbench~1alerts/get)                                                                                  |
| **Workbench Notes**                            |                                                                                                                                                                                                    |
| `note.create`                                  | [Add alert note](https://automation.trendmicro.com/xdr/api-v3#tag/Workbench-notes/paths/~1v3.0~1workbench~1alerts~1{alertId}~1notes/post)                                                          |
| `note.get`                                     | [Get alert note](https://automation.trendmicro.com/xdr/api-v3#tag/Workbench-notes/paths/~1v3.0~1workbench~1alerts~1%7BalertId%7D~1notes~1%7Bid%7D/get)                                             |
| `note.update`                                  | [Edit alert note](https://automation.trendmicro.com/xdr/api-v3#tag/Workbench-notes/paths/~1v3.0~1workbench~1alerts~1%7BalertId%7D~1notes~1%7Bid%7D/patch)                                          |
| `note.delete`                                  | [Delete alert notes](https://automation.trendmicro.com/xdr/api-v3#tag/Workbench-notes/paths/~1v3.0~1workbench~1alerts~1%7BalertId%7D~1notes~1delete/post)                                          |
| `note.[list, consume]`                         | [Get alerts notes](https://automation.trendmicro.com/xdr/api-v3#tag/Workbench-notes/paths/~1v3.0~1workbench~1alerts~1%7BalertId%7D~1notes/get)                                                     |

Contributing
------------
Read our [contributing guide](https://github.com/trendmicro/tm-v1/blob/main/CONTRIBUTING.md) to learn about our development process, how to propose bug fixes and improvements, and how to build and test your changes to Trend Vision One.

Code of conduct
---------------
Trend Micro has adopted a [Code of Conduct](https://github.com/trendmicro/tm-v1/blob/main/CODE_OF_CONDUCT.md) that we expect project participants to adhere to. Please read the [full text](https://github.com/trendmicro/tm-v1/blob/main/CODE_OF_CONDUCT.md) to understand what actions will and will not be tolerated.

License
-------
Project distributed under the [Apache 2.0](https://spdx.org/licenses/Apache-2.0.html) license.
