import sys
import sparkline

ProductsDir = '/eplus/installs/EnergyPlus-9-6-0'
RepoRoot = '/eplus/installs/EnergyPlus-9-6-0'
outdoor_db_handle = None
plot_data = []
counter = 0

sys.path.insert(0, ProductsDir)
from pyenergyplus.api import EnergyPlusAPI


def callback_function(s):
    global outdoor_db_handle, counter
    if not outdoor_db_handle:
        outdoor_db_handle = api.exchange.get_variable_handle(
            s, "Site Outdoor Air Drybulb Temperature", "Environment"
        )
    if api.exchange.warmup_flag(s) or api.exchange.current_environment_num(s) < 3:
        sys.stdout.write('\r')
        sys.stdout.write('Simulation Starting...')
        sys.stdout.flush()
        return
    counter += 1
    if counter % 300 == 0:
        plot_data.append(api.exchange.get_variable_value(s, outdoor_db_handle))
        sys.stdout.write('\r')
        sys.stdout.flush()
        sys.stdout.write("Outdoor Temperature: " + sparkline.sparkify(plot_data))
        sys.stdout.flush()


api = EnergyPlusAPI()
state = api.state_manager.new_state()
api.runtime.set_console_output_status(state, False)
api.runtime.callback_begin_zone_timestep_before_init_heat_balance(state, callback_function)
api.exchange.request_variable(state, "Site Outdoor Air Drybulb Temperature", "Environment")
api.runtime.run_energyplus(
    state, [
        '-d',
        r'/tmp/abc',
        '-w',
        r"/eplus/epw/chicago.epw",
        "-a",
        r"/eplus/installs/EnergyPlus-9-6-0/ExampleFiles/5ZoneAirCooled.idf",
    ]
)
