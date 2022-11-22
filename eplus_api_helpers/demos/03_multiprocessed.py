from pathlib import Path
import multiprocessing as mp
from eplus_api_helpers.import_helper import EPlusAPIHelper


e = EPlusAPIHelper(Path('/eplus/installs/EnergyPlus-22-2-0'))
api = e.get_api_instance()


def subprocess_function():
    working_dir = e.get_temp_run_dir()
    print(f"Thread: Running at working dir: {working_dir}")
    state = api.state_manager.new_state()
    api.runtime.run_energyplus(
        state, [
            '-d',
            working_dir,
            '-a',
            '-w',
            e.weather_file_path(),
            e.path_to_test_file('1ZoneUncontrolled.idf')
        ]
    )


processes = [mp.Process(target=subprocess_function) for x in range(7)]

for p in processes:
    print("Main    : create and start process.")
    p.start()

for p in processes:
    p.join()
