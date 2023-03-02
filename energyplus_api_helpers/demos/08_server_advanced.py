from flask import Flask
from pathlib import Path
from threading import Thread
from time import sleep
from energyplus_api_helpers.import_helper import EPlusAPIHelper


class RunConfig:
    def __init__(self):
        self.e = EPlusAPIHelper(Path('/eplus/installs/EnergyPlus-22-2-0'))
        self.idf_name = '5ZoneAirCooled.idf'
        self.api = self.e.get_api_instance()
        self.eplus_outdoor_temp = 23.3
        self.eplus_output = b"HERE IA M"
        self.eplus_progress = 0
        self.got_handles = False
        self.oa_temp_handle = -1
        self.zone_temp_handles = {}
        self.zone_temperatures = {}
        self.count = 0
        self.outdoor_data = []
        self.zone_names = {
            'south': 'SPACE1-1', 'west': 'SPACE2-1', 'east': 'SPACE3-1',
            'north': 'SPACE4-1', 'center': 'SPACE5-1'
        }


runner = RunConfig()
app = Flask("EnergyPlus API Server Demo")


@app.route("/", methods=['GET'])
def hello():
    html_file = Path(__file__).resolve().parent / '08_server_advanced_index.html'
    return html_file.read_text()


@app.route('/api/data/', methods=['GET'])
def get_api_data():
    global runner
    return {
        "output": runner.eplus_output.decode('utf-8'),
        "progress": runner.eplus_progress + 1,
        "outdoor_data": runner.outdoor_data,
        "zone_temp_data": runner.zone_temperatures
    }


@app.route('/api/start/', methods=['POST'])
def post_api_start():
    Thread(target=thread_function).start()
    return {}


def eplus_output_handler(msg):
    global runner
    runner.eplus_output += msg + b'\n'


def eplus_progress_handler(p):
    global runner
    runner.eplus_progress = p


def callback_function(s):
    global runner
    if not runner.got_handles:
        if not runner.api.exchange.api_data_fully_ready(s):
            return
        runner.oa_temp_handle = runner.api.exchange.get_variable_handle(
            s, "Site Outdoor Air DryBulb Temperature", "Environment"
        )
        for zone_nickname, zone_name in runner.zone_names.items():
            runner.zone_temp_handles[zone_nickname] = runner.api.exchange.get_variable_handle(
                s, u"ZONE AIR TEMPERATURE", zone_name
            )
        if -1 in [runner.oa_temp_handle] + list(runner.zone_temp_handles.values()):
            runner.api.runtime.issue_severe("Invalid Handle in API usage, need to fix!")
        runner.got_handles = True
    if runner.api.exchange.warmup_flag(s):
        return
    runner.count += 1
    sleep(0.0002)
    if runner.count % 200 != 0:
        return
    oa_temp = runner.api.exchange.get_variable_value(s, runner.oa_temp_handle)
    runner.outdoor_data.append({'x': runner.count, 'y': oa_temp})
    for zone_nickname in runner.zone_names:
        runner.zone_temperatures[zone_nickname] = runner.api.exchange.get_variable_value(
            s, runner.zone_temp_handles[zone_nickname]
        )


def thread_function():
    global runner
    runner = RunConfig()
    state = runner.api.state_manager.new_state()
    runner.api.exchange.request_variable(state, "Site Outdoor Air DryBulb Temperature", "Environment")
    for zone_name in runner.zone_names.values():
        runner.api.exchange.request_variable(state, "Zone Mean Air Temperature", zone_name)
    runner.api.runtime.callback_begin_zone_timestep_after_init_heat_balance(state, callback_function)
    runner.api.runtime.callback_message(state, eplus_output_handler)
    runner.api.runtime.callback_progress(state, eplus_progress_handler)
    runner.api.runtime.set_console_output_status(state, False)
    runner.api.runtime.run_energyplus(
        state, [
            '-d',
            runner.e.get_temp_run_dir(),
            '-a',
            '-w',
            runner.e.weather_file_path(),
            runner.e.path_to_test_file(runner.idf_name)
        ]
    )


if __name__ == "__main__":
    app.run()
