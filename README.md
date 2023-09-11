# EnergyPlus API Helper Scripts

This project is a small library of helper functionality and, more importantly, demo scripts, for interacting with the EnergyPlus API.
The EnergyPlus Python API is not on PyPi (as of now), it simply comes with the EnergyPlus installation.
This library makes that process a bit easier, and also offers a set of demos in the `energyplus_api_helpers/demos` folder.

A super minimal example using the helper class here:

```python
from pathlib import Path
from energyplus_api_helpers.import_helper import EPlusAPIHelper

helper = EPlusAPIHelper(Path('/path/to/EnergyPlus-22-2-0'))
api = helper.get_api_instance()
state = api.state_manager.new_state()
return_value = api.runtime.run_energyplus(state, ['-D', helper.path_to_test_file('5ZoneAirCooled.idf')])
```

In this example, the helper class is constructed simply by pointing it to a valid EnergyPlus install path (or build/Products directory for developers).
The helper class is then used to get an EnergyPlus API instance, which is in turn used to create a new EnergyPlus "state".
Finally, EnergyPlus is executed with some basic command line arguments passed into the `run_energyplus` function of the main EnergyPlus API.

## Inferring EnergyPlus path

It is possible to call `helper = EnergyPlusHelper()` (without a path argument), in which case the helper tries to locate your E+ installation directory.

It does so checking, in order of preference:

* Any `energyplus` executable in your `PATH`
* By trying to locate the most recent EnergyPlus version installed in a default location

## Code Quality

[![Flake8](https://github.com/Myoldmopar/EnergyPlusAPIDemos/actions/workflows/flake8.yml/badge.svg)](https://github.com/Myoldmopar/EnergyPlusAPIDemos/actions/workflows/flake8.yml)

Code is checked for style using GitHub Actions.

## Releases

[![PyPIRelease](https://github.com/Myoldmopar/EnergyPlusAPIDemos/actions/workflows/release.yml/badge.svg)](https://github.com/Myoldmopar/EnergyPlusAPIDemos/actions/workflows/release.yml)

When a release is tagged, a GitHub Action workflow will create a Python wheel and upload it to the PyPi server.

To install into an existing Python environment, execute `pip install energyplus_api_helpers`
