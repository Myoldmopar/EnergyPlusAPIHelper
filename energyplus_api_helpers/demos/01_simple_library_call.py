from energyplus_api_helpers.demos.helper import get_eplus_path_from_argv1
from energyplus_api_helpers.import_helper import EPlusAPIHelper

e = EPlusAPIHelper(get_eplus_path_from_argv1())
api = e.get_api_instance()
state = api.state_manager.new_state()
return_value = api.runtime.run_energyplus(
    state, ["-d", e.get_temp_run_dir(), "-a", "-w", e.weather_file_path(), e.path_to_test_file("5ZoneAirCooled.idf")]
)
