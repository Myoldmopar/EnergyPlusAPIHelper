import os
import sys

RepoDir = '/eplus/installs/EnergyPlus-9-6-0'
sys.path.insert(0, RepoDir)
from pyenergyplus.api import EnergyPlusAPI


def progress_update(percent):
    filled_length = int(80 * (percent/100.0))
    bar = "*" * filled_length + '-' * (80 - filled_length)
    print(f'\rProgress: |{bar}| {percent}%', end="\r")


api = EnergyPlusAPI()
state = api.state_manager.new_state()
api.runtime.set_console_output_status(state, False)
api.runtime.callback_progress(state, progress_update)
idf_path = os.path.join(RepoDir, 'ExampleFiles', '5ZoneAirCooled.idf')
result = api.runtime.run_energyplus(state, ['-d', 'output', '-w', '/eplus/epw/chicago.epw', "-a", idf_path])
if result == 0:
    print("Success, finished")
else:
    print("EnergyPlus ERROR")
