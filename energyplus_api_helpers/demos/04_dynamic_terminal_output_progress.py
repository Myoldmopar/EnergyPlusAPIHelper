from energyplus_api_helpers.demos.helper import get_eplus_path_from_argv1
from energyplus_api_helpers.import_helper import EPlusAPIHelper


def progress_update(percent):
    filled_length = int(80 * (percent / 100.0))
    bar = "*" * filled_length + "-" * (80 - filled_length)
    print(f"\rProgress: |{bar}| {percent}%", end="\r")


e = EPlusAPIHelper(get_eplus_path_from_argv1())
api = e.get_api_instance()
state = api.state_manager.new_state()
api.runtime.set_console_output_status(state, False)
api.runtime.callback_progress(state, progress_update)
result = api.runtime.run_energyplus(
    state, ["-d", e.get_temp_run_dir(), "-w", e.weather_file_path(), "-a", e.path_to_test_file("5ZoneAirCooled.idf")]
)
if result == 0:
    print("Success, finished")
else:
    print("EnergyPlus ERROR")
