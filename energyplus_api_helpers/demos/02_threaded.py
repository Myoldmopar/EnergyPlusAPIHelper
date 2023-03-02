from pathlib import Path
from sys import argv
from threading import Thread
from energyplus_api_helpers.import_helper import EPlusAPIHelper


eplus_path = '/eplus/installs/EnergyPlus-22-2-0'
if len(argv) > 1:
    eplus_path = argv[1]


def thread_function(_working_dir: str):
    print(f"Thread: Running at working dir: {_working_dir}")
    state = api.state_manager.new_state()
    api.runtime.run_energyplus(
        state, [
            '-d',
            _working_dir,
            '-a',
            '-w',
            e.weather_file_path(),
            e.path_to_test_file('5ZoneAirCooled.idf')
        ]
    )


e = EPlusAPIHelper(Path(eplus_path))
api = e.get_api_instance()
for index in range(3):
    working_dir = e.get_temp_run_dir()
    print(f"Main    : create and start thread at working directory: {working_dir}.")
    x = Thread(target=thread_function, args=(working_dir,))
    x.start()
