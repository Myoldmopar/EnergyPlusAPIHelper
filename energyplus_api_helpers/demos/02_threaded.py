from threading import Thread

from energyplus_api_helpers.demos.helper import get_eplus_path_from_argv1
from energyplus_api_helpers.import_helper import EPlusAPIHelper


def thread_function(_working_dir: str):
    print(f"Thread: Running at working dir: {_working_dir}")
    state = api.state_manager.new_state()
    api.runtime.run_energyplus(
        state, ["-d", _working_dir, "-a", "-w", e.weather_file_path(), e.path_to_test_file("5ZoneAirCooled.idf")]
    )


e = EPlusAPIHelper(get_eplus_path_from_argv1())
api = e.get_api_instance()
for index in range(3):
    working_dir = e.get_temp_run_dir()
    print(f"Main    : create and start thread at working directory: {working_dir}.")
    x = Thread(target=thread_function, args=(working_dir,))
    x.start()
