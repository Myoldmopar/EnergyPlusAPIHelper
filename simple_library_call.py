import os
import shutil
import sys

ProductsDir = '/eplus/repos/8eplus/builds/r/Products'  # '/eplus/installs/EnergyPlus-9-5-0'
RepoRoot = '/eplus/repos/8eplus'  # '/eplus/installs/EnergyPlus-9-5-0'
IDFDir = 'testfiles'  # 'ExampleFiles'

sys.path.insert(0, str(ProductsDir))
from pyenergyplus.api import EnergyPlusAPI

working_dir = f"/tmp/test_simple_eplus"
if os.path.exists(working_dir):
    shutil.rmtree(working_dir)
os.makedirs(working_dir)
api = EnergyPlusAPI()
state = api.state_manager.new_state()
return_value = api.runtime.run_energyplus(
    state, [
        '-d',
        working_dir,
        '-a',
        '-w',
        '/eplus/epw/chicago.epw',
        os.path.join(RepoRoot, IDFDir, 'PythonPluginCustomSchedule.idf')  # '5ZoneAirCooled.idf')
    ]
)
sys.exit(return_value)
