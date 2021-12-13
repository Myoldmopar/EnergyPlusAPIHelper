import matplotlib.pyplot as plt
import os
import requests
import sys


hl, = plt.plot([], [], label="Outdoor Air Temp")
h2, = plt.plot([], [], label="Zone Temperature")
ax = plt.gca()
plt.title('Outdoor Temperature')
plt.xlabel('Zone time step index')
plt.ylabel('Temperature [C]')
plt.legend(loc='lower right')
x = []
y_outdoor = []
y_zone = []

got_handles = False
oa_temp_actuator = -1
oa_temp_handle = -1
zone_temp_handle = -1
count = 0
plot_update_interval = 250  # time steps
case_index_to_run = 1
if len(sys.argv) > 1:
    case_index_to_run = int(sys.argv[1])
filename_to_run = ''
zone_name = ''
if case_index_to_run == 1:
    filename_to_run = '1ZoneEvapCooler.idf'
    zone_name = 'Main Zone'
elif case_index_to_run == 2:
    filename_to_run = '1ZoneUncontrolled.idf'
    zone_name = 'Zone One'


def update_line():
    hl.set_xdata(x)
    hl.set_ydata(y_outdoor)
    h2.set_xdata(x)
    h2.set_ydata(y_zone)
    ax.relim()
    ax.autoscale_view()
    plt.draw()
    plt.pause(0.00001)


get_by_api = False


def get_new_outdoor_air_temp() -> float:
    response = requests.get('http://127.0.0.1:8000/api/outdoor_temp/')
    data = response.json()
    return data['outdoor_temp']


def callback_function(s):
    global count, got_handles, oa_temp_actuator, oa_temp_handle, zone_temp_handle
    if not got_handles:
        if not a.exchange.api_data_fully_ready(s):
            return
        oa_temp_actuator = a.exchange.get_actuator_handle(s, "Weather Data", "Outdoor Dry Bulb", "Environment")
        oa_temp_handle = a.exchange.get_variable_handle(s, u"SITE OUTDOOR AIR DRYBULB TEMPERATURE", u"ENVIRONMENT")
        zone_temp_handle = a.exchange.get_variable_handle(s, "Zone Mean Air Temperature", zone_name)
        if -1 in [oa_temp_actuator, oa_temp_handle, zone_temp_handle]:
            print("***Invalid handles, check spelling and sensor/actuator availability")
            sys.exit(1)
        got_handles = True
    if a.exchange.warmup_flag(s):
        return
    if get_by_api:
        a.exchange.set_actuator_value(s, oa_temp_actuator, get_new_outdoor_air_temp())
    count += 1
    x.append(count)
    oa_temp = a.exchange.get_variable_value(s, oa_temp_handle)
    y_outdoor.append(oa_temp)
    zone_temp = a.exchange.get_variable_value(s, zone_temp_handle)
    y_zone.append(zone_temp)
    if count % plot_update_interval == 0:
        update_line()


# insert the repo build tree or install path into the search Path, then import the EnergyPlus API
RepoDir = '/eplus/installs/EnergyPlus-9-6-0'
sys.path.insert(0, RepoDir)
from pyenergyplus.api import EnergyPlusAPI

a = EnergyPlusAPI()
state = a.state_manager.new_state()
a.runtime.callback_begin_zone_timestep_after_init_heat_balance(state, callback_function)
a.runtime.run_energyplus(
    state,
    [
        '-a',
        '-w', '/eplus/epw/chicago.epw',
        '-d', 'output',
        os.path.join(RepoDir, 'ExampleFiles', filename_to_run)
    ]
)

plt.show()
