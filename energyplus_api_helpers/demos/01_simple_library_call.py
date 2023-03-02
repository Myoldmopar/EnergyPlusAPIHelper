from pathlib import Path
from sys import argv
from energyplus_api_helpers.import_helper import EPlusAPIHelper


eplus_path = '/eplus/installs/EnergyPlus-22-2-0'
if len(argv) > 1:
    eplus_path = argv[1]

e = EPlusAPIHelper(Path(eplus_path))
api = e.get_api_instance()
state = api.state_manager.new_state()
return_value = api.runtime.run_energyplus(
    state, [
        '-d',
        e.get_temp_run_dir(),
        '-a',
        '-w',
        e.weather_file_path(),
        e.path_to_test_file('5ZoneAirCooled.idf')
    ]
)
