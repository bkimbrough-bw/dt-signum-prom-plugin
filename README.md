# Signum Prometheus Plugin

## Setup

1. Download the Dynatrace Plugin SDK using the instruction on their [webpage](https://www.dynatrace.com/support/help/extend-dynatrace/plugins/oneagent-plugins/how-to-create-a-python-custom-plugin/)
2. Extract the zip and add the `.whl` file in the base of the directory. Ensure it is the same version as what is in requirements.txt
3. Setup virtual environment
```shell script
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
## Json File
The plugin.json file is required, you must specify every metric that you wish to export in this file and what type the data is

## Coding
The `query` method is expected to be defined for all `BasePlugin` types and will be invoked by the agent once a minute