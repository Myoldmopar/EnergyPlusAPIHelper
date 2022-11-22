from pathlib import Path
from eplus_api_helpers.import_helper import EPlusAPIHelper


e = EPlusAPIHelper(Path('/eplus/installs/EnergyPlus-22-2-0'))
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
