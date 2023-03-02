from pathlib import Path
import multiprocessing as mp
from sys import argv
from energyplus_api_helpers.import_helper import EPlusAPIHelper

eplus_path = '/eplus/installs/EnergyPlus-22-2-0'
if len(argv) > 1:
    eplus_path = argv[1]


def subprocess_function():
    e = EPlusAPIHelper(Path(eplus_path))
    api = e.get_api_instance()
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


# for multiprocessing on Windows, need to protect the re-entrance to the file with a __name__ == "__main__" check
if __name__ == "__main__":
    processes = [mp.Process(target=subprocess_function) for x in range(7)]
    # create the processes
    for p in processes:
        print("Main    : create and start process.")
        p.start()
    # wait for them to finish
    for p in processes:
        p.join()
