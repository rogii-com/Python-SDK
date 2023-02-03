# Rogii Solo

Rogii Solo is a Python SDK designed to make data scientists' work with Solo easier.

## Requirements
Python 3.10

## Installation
1. Install the package using `pip install rogii-solo` command.
2. Generate access credentials on the [landing page](https://solo.cloud/credentials/python-sdk) and copy the initialization string.
3. Initialize the client by pasting the initialization string in the constructor.
4. Set the project you wish to work with by name or UUID.

## Example
```python
from rogii_solo import SoloClient

solo_client = SoloClient(client_id='my-client-id', client_secret='my-client-secret')
project = solo_client.set_project_by_name('My project')

wells = project.wells

wells_data = wells.to_dict() # List of dicts
wells_df = wells.to_df() # DataFrame
```

## Usage
Please check the SDK documentation in our [Knowledge Base](https://kb.solo.cloud/Python+SDK).
