import sys
from pathlib import Path
from sys import argv
import sparkline
from energyplus_api_helpers.import_helper import EPlusAPIHelper

outdoor_db_handle = None
plot_data = []
counter = 0

eplus_path = '/eplus/installs/EnergyPlus-22-2-0'
if len(argv) > 1:
    eplus_path = argv[1]


def callback_function(s):
    global outdoor_db_handle, counter
    if not outdoor_db_handle:
        outdoor_db_handle = api.exchange.get_variable_handle(
            s, "Site Outdoor Air Drybulb Temperature", "Environment"
        )
        # data = api.exchange.list_available_api_data_csv(s)
        # with open('/tmp/data.csv', 'wb') as f:
        #     f.write(data)
    if api.exchange.warmup_flag(s) or api.exchange.current_environment_num(s) < 3:
        sys.stdout.write('\r')
        sys.stdout.write('Simulation Starting...')
        sys.stdout.flush()
        return
    counter += 1
    if counter % 600 == 0:
        plot_data.append(api.exchange.get_variable_value(s, outdoor_db_handle))
        sys.stdout.write('\r')
        sys.stdout.flush()
        sys.stdout.write("Outdoor Temperature: " + sparkline.sparkify(plot_data))
        sys.stdout.flush()


e = EPlusAPIHelper(Path(eplus_path))
api = e.get_api_instance()
state = api.state_manager.new_state()
api.runtime.set_console_output_status(state, False)
api.runtime.callback_begin_zone_timestep_before_init_heat_balance(state, callback_function)
api.exchange.request_variable(state, "Site Outdoor Air Drybulb Temperature", "Environment")
api.runtime.run_energyplus(
    state, [
        '-d',
        e.get_temp_run_dir(),
        '-w',
        e.weather_file_path(),
        "-a",
        e.path_to_test_file('5ZoneAirCooled.idf'),
    ]
)
