import argparse
import os
import sys
import shutil
import threading

# set up command line arguments and parse them
parser = argparse.ArgumentParser(
    description='This script will run EnergyPlus by API twice, in two different threads, clearing the state in between'
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


def thread_function(api_instance, tmp_run_dir, weather_file, idf_to_run):
    print("Thread %s: starting" % threading.get_ident())
    state = api_instance.state_manager.new_state()
    api_instance.runtime.run_energyplus(state, ['-d', tmp_run_dir, '-w', weather_file, idf_to_run])
    print("Thread %s: finishing" % threading.get_ident())


weather_file_to_use = '/eplus/epw/miami.epw'
a = EnergyPlusAPI()

for run_in_dir in ['/tmp/blah1', '/tmp/blah2']:
    # clean out an existing run directory and remake it, moving into that directory as needed
    temp_run_dir = '/tmp/blah1'
    if os.path.exists(run_in_dir):
        shutil.rmtree(run_in_dir)
    os.makedirs(run_in_dir)
    t = threading.Thread(target=thread_function, args=(a, temp_run_dir, weather_file_to_use, args.path_to_idf))
    t.start()
    t.join()
