from os import makedirs, path
from shutil import rmtree
import sys
from threading import Thread
from time import sleep

ProductsDir = '/eplus/installs/EnergyPlus-9-5-0'
RepoRoot = '/eplus/installs/EnergyPlus-9-5-0'
IDFDir = 'ExampleFiles'
# ProductsDir = '/eplus/repos/2eplus/cmake-build-debug/Products'
# RepoRoot = '/eplus/repos/2eplus'
# IDFDir = 'testfiles'

sys.path.insert(0, str(ProductsDir))
from pyenergyplus.api import EnergyPlusAPI


def thread_function(_working_dir: str):
    print(f"Thread: Running at working dir: {_working_dir}")
    if path.exists(_working_dir):
        rmtree(_working_dir)
    makedirs(_working_dir)
    api = EnergyPlusAPI()
    state = api.state_manager.new_state()
    api.runtime.run_energyplus(
        state, [
            '-d',
            _working_dir,
            '-a',
            '-w',
            '/eplus/epw/chicago.epw',
            path.join(RepoRoot, IDFDir, '5ZoneAirCooled.idf')
        ]
    )


threads = list()
for index in range(7):
    working_dir = f"/tmp/test_thread_{index}"
    print(f"Main    : create and start thread at working directory: {working_dir}.")
    x = Thread(target=thread_function, args=(working_dir,))
    threads.append(x)
    x.start()
    sleep(0)
