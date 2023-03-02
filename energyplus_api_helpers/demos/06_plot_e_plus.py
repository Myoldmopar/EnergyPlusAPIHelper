import matplotlib.pyplot as plt
from pathlib import Path
from energyplus_api_helpers.import_helper import EPlusAPIHelper


class PlotManager:
    def __init__(self):
        self.hl, = plt.plot([], [], label="Outdoor Air Temp")
        self.h2, = plt.plot([], [], label="Zone Temperature")
        self.ax = plt.gca()
        plt.title('Outdoor Temperature')
        plt.xlabel('Zone time step index')
        plt.ylabel('Temperature [C]')
        plt.legend(loc='lower right')
        self.x = []
        self.y_outdoor = []
        self.y_zone = []
        self.update_interval = 250  # effectively number of E+ time steps

    def update_line(self):
        self.hl.set_xdata(self.x)
        self.hl.set_ydata(self.y_outdoor)
        self.h2.set_xdata(self.x)
        self.h2.set_ydata(self.y_zone)
        self.ax.relim()
        self.ax.autoscale_view()
        plt.draw()
        plt.pause(0.00001)


class EnergyPlusManager:
    def __init__(self):
        self.e = EPlusAPIHelper(Path('/eplus/installs/EnergyPlus-22-2-0'))
        self.api = self.e.get_api_instance()
        self.got_handles = False
        self.oa_temp_handle = -1
        self.zone_temp_handle = -1
        self.count = 0
        self.p = PlotManager()

    def callback_function(self, state):
        if not self.got_handles:
            if not self.api.exchange.api_data_fully_ready(state):
                return
            self.oa_temp_handle = self.api.exchange.get_variable_handle(
                state, u"SITE OUTDOOR AIR DRYBULB TEMPERATURE", u"ENVIRONMENT"
            )
            self.zone_temp_handle = self.api.exchange.get_variable_handle(
                state, "Zone Mean Air Temperature", 'Main Zone'
            )
            if -1 in [self.oa_temp_handle, self.zone_temp_handle]:
                print("***Invalid handles, check spelling and sensor/actuator availability")
                return  # TODO: Request fatal error
            self.got_handles = True
        if self.api.exchange.warmup_flag(state):
            return
        self.count += 1
        self.p.x.append(self.count)
        oa_temp = self.api.exchange.get_variable_value(state, self.oa_temp_handle)
        self.p.y_outdoor.append(oa_temp)
        zone_temp = self.api.exchange.get_variable_value(state, self.zone_temp_handle)
        self.p.y_zone.append(zone_temp)
        if self.count % self.p.update_interval == 0:
            self.p.update_line()

    def run(self):
        state = self.api.state_manager.new_state()
        self.api.runtime.callback_begin_zone_timestep_after_init_heat_balance(state, self.callback_function)
        self.api.runtime.run_energyplus(state, [
                '-a',
                '-w', self.e.weather_file_path(),
                '-d', self.e.get_temp_run_dir(),
                self.e.path_to_test_file('1ZoneEvapCooler.idf')
            ]
        )


if __name__ == "__main__":
    EnergyPlusManager().run()
    plt.show()
