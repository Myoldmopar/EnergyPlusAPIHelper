import argparse
import os
import sys
import shutil

# need to check for diffs between the two versions...
#  should be able to binary compare most, just filter timestamp and runtime

# set up command line arguments and parse them
parser = argparse.ArgumentParser(
    description='This script will run EnergyPlus by API twice, clearing the state in between, and return the number '
                'of failed runs (0, 1, or 2) '
)
parser.add_argument(
    'folder_with_pyenergyplus', help='This is the path to a folder, which itself contains a pyenergyplus folder'
)
parser.add_argument(
    'path_to_idf', help='This is the absolute path to the IDF to run twice'
)
args = parser.parse_args()

# insert the repo build tree or install path into the search Path, then import the EnergyPlus API
sys.path.insert(0, args.folder_with_pyenergyplus)
from pyenergyplus.api import EnergyPlusAPI

# clean out an existing run directory and remake it, moving into that directory as needed
temp_run_dir = '/tmp/blah'
if os.path.exists(temp_run_dir):
    shutil.rmtree(temp_run_dir)
os.makedirs(temp_run_dir)
weather_file_to_use = '/eplus/epw/miami.epw'

# output_dir_1 = os.path.join(temp_run_dir, 'case1')
# output_dir_2 = os.path.join(temp_run_dir, 'case2')
# os.makedirs(output_dir_1)
# os.makedirs(output_dir_2)

# call EnergyPlus twice, report out the status and return the number of failures
a = EnergyPlusAPI()
state = a.state_manager.new_state()
ret1 = a.runtime.run_energyplus(state, ['-d', temp_run_dir, '-w', weather_file_to_use, args.path_to_idf])
a.state_manager.reset_state(state)
ret2 = a.runtime.run_energyplus(state, ['-d', temp_run_dir, '-w', weather_file_to_use, args.path_to_idf])
sys.exit(ret1 + ret2)
