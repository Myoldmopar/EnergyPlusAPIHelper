from os import makedirs, path
from shutil import rmtree
import sys
import multiprocessing as mp

ProductsDir = '/eplus/installs/EnergyPlus-9-6-0'
RepoRoot = '/eplus/installs/EnergyPlus-9-6-0'
IDFDir = 'ExampleFiles'

sys.path.insert(0, str(ProductsDir))
from pyenergyplus.api import EnergyPlusAPI


def subprocess_function(_working_dir: str):
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
            path.join(RepoRoot, IDFDir, '1ZoneUncontrolled.idf')
        ]
    )


processes = [mp.Process(target=subprocess_function, args=(f"/tmp/test_thread_{x}",)) for x in range(7)]

for p in processes:
    print(f"Main    : create and start process.")
    p.start()

for p in processes:
    p.join()
