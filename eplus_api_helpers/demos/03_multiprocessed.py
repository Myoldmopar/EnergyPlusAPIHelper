from pathlib import Path
import multiprocessing as mp
from eplus_api_helpers.import_helper import EPlusAPIHelper


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


# for multiprocessing on Windows, need to protect the re-entrance to the file with a __name__ == "__main__" check
if __name__ == "__main__":
    e = EPlusAPIHelper(Path('/eplus/installs/EnergyPlus-22-2-0'))
    api = e.get_api_instance()
    processes = [mp.Process(target=subprocess_function) for x in range(7)]
    # create the processes
    for p in processes:
        print("Main    : create and start process.")
        p.start()
    # wait for them to finish
    for p in processes:
        p.join()
