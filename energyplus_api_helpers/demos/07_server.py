from flask import Flask, request
from pathlib import Path
from threading import Thread
from time import sleep
from energyplus_api_helpers.import_helper import EPlusAPIHelper

app = Flask("EnergyPlus API Server Demo")
e = EPlusAPIHelper(Path('/eplus/installs/EnergyPlus-22-2-0'))
api = e.get_api_instance()

eplus_outdoor_temp = 23.3
eplus_output = b"HERE IA M"
eplus_progress = 0
got_handles = False
oa_temp_actuator = -1
oa_temp_handle = -1
zone_temp_handle = -1
count = 0
outdoor_data = []
zone_temp_data = []


@app.route("/", methods=['GET'])
def hello():
    html_file = Path(__file__).resolve().parent / '07_server_index.html'
    return html_file.read_text()


@app.route('/api/data/', methods=['GET'])
def get_api_data():
    return {
        "output": eplus_output.decode('utf-8'),
        "progress": eplus_progress + 1,
        "outdoor_data": outdoor_data,
        "zone_temp_data": zone_temp_data
    }


@app.route('/api/start/', methods=['POST'])
def post_api_start():
    Thread(target=thread_function).start()
    return {}


@app.route('/api/outdoor_temp/', methods=['POST'])
def get_outdoor_temp():
    global eplus_outdoor_temp
    data = request.json
    print(data)
    if 'temperature' not in data:
        return {"message": "Need to supply 'temperature' in POST data as a float"}
    temp = float(data['temperature'])
    eplus_outdoor_temp = temp
    return {"outdoor_temp": eplus_outdoor_temp}


def eplus_output_handler(msg):
    global eplus_output
    eplus_output += msg + b'\n'


def eplus_progress_handler(p):
    global eplus_progress
    eplus_progress = p


def callback_function(s):
    global count, got_handles, oa_temp_actuator, oa_temp_handle, zone_temp_handle, zone_temp_data
    if not got_handles:
        if not api.exchange.api_data_fully_ready(s):
            return
        oa_temp_actuator = api.exchange.get_actuator_handle(s, "Weather Data", "Outdoor Dry Bulb", "Environment")
        oa_temp_handle = api.exchange.get_variable_handle(s, "Site Outdoor Air DryBulb Temperature", "Environment")
        zone_temp_handle = api.exchange.get_variable_handle(s, "Zone Mean Air Temperature", 'Zone One')
        if -1 in [oa_temp_actuator, oa_temp_handle, zone_temp_handle]:
            print("***Invalid handles, check spelling and sensor/actuator availability")
            # TODO: Ask E+ to fatal error
        got_handles = True
    if api.exchange.warmup_flag(s):
        return
    count += 1
    sleep(0.0002)
    if count % 200 != 0:
        return
    api.exchange.set_actuator_value(s, oa_temp_actuator, eplus_outdoor_temp)
    oa_temp = api.exchange.get_variable_value(s, oa_temp_handle)
    outdoor_data.append({'x': count, 'y': oa_temp})
    zone_temp = api.exchange.get_variable_value(s, zone_temp_handle)
    zone_temp_data.append({'x': count, 'y': zone_temp})


def thread_function():
    global api, eplus_output, eplus_progress, count, outdoor_data, zone_temp_data
    eplus_output = b""
    eplus_progress = 0
    count = 0
    outdoor_data = []
    zone_temp_data = []
    state = api.state_manager.new_state()
    api.exchange.request_variable(state, "Site Outdoor Air DryBulb Temperature", "Environment")
    api.exchange.request_variable(state, "Zone Mean Air Temperature", 'Zone One')
    api.runtime.callback_begin_zone_timestep_after_init_heat_balance(state, callback_function)
    api.runtime.callback_message(state, eplus_output_handler)
    api.runtime.callback_progress(state, eplus_progress_handler)
    api.runtime.run_energyplus(
        state, [
            '-d',
            e.get_temp_run_dir(),
            '-a',
            '-w',
            e.weather_file_path(),
            e.path_to_test_file('1ZoneUncontrolled.idf')
        ]
    )


if __name__ == "__main__":
    app.run()
