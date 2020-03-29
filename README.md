# Purpose
Downloading and Manipulating Covid Case Data

# Requirements
 - Python3 (using Python 3.8.0)
 `$ python --version`
 - VirtualEnv (using 16.7.8)
 `$ virtualenv --version`
 - pip (using pip 20.0.2)
 `$ pip --version`
 - pipenv (using pipenv, version 2018.11.26)
 `$ pipenv --version`

# Installation

Note the installation is already performed in the code.

## virtualenv
Create a virtual environment with a clean copy of Python
```
virtualenv .
cd bin
source activate
```

## Modules
```
pip install requests
pip install matplotlib
```

# Running
Activate virtual environment
`source activate`

From the project root, run:
`$ pipenv run python fetch_data.py`


# Quitting
To exit your virtualenv
`deactivate`
