from pathlib import Path
import sys
from tempfile import mkdtemp


class _EPlusImporter:
    """
    This class provides a simple context manager for importing EnergyPlus.
    EnergyPlus comes with its own API code that lives with EnergyPlus, not in the Python install environment.
    Because of this, Python cannot by default find the EnergyPlus API.
    Using this class, the client code can easily pass the desired EnergyPlus install directory and import the API.
    This class should be used as::

        from pathlib import Path
        from energyplus_api_helpers import EPlusImporter
        p = Path('/path/to/energyplus/install')
        with _EplusImporter() as eplus_helper:
            from pyenergyplus.api import EnergyPlusAPI
            api = EnergyPlusAPI()

    """
    def __init__(self, eplus_install_path: Path):
        self.eplus_install_path = eplus_install_path

    def __enter__(self):
        sys.path.insert(0, str(self.eplus_install_path))

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            sys.path.remove(str(self.eplus_install_path))
        except ValueError:
            pass


class EPlusAPIHelper:
    """
    This is the primary helper class for providing usability to E+ API clients
    This class intentionally provides strings as path outputs to keep the conversion to strings reduced in the client
    """
    def __init__(self, eplus_install_path: Path):
        self.eplus_install_path = eplus_install_path

    def get_api_instance(self):
        with _EPlusImporter(self.eplus_install_path):
            from pyenergyplus.api import EnergyPlusAPI
            return EnergyPlusAPI()

    def is_an_install_folder(self) -> bool:
        if (self.eplus_install_path / 'ExampleFiles').exists():
            return True
        return False

    def find_source_dir_from_cmake_cache(self) -> Path:
        cmake_cache_file = self.eplus_install_path.parent / 'CMakeCache.txt'
        lines = cmake_cache_file.read_text().split('\n')
        for line in lines:
            line_trimmed = line.strip()
            if line_trimmed.startswith('EnergyPlus_SOURCE_DIR:STATIC='):
                found_dir = line_trimmed.split('=')[1]
                return Path(found_dir)

    def path_to_test_file(self, test_file_name: str) -> str:
        """Returns the path to an example/test file, trying to figure out if it is a build dir or install."""
        if self.is_an_install_folder():
            return str(self.eplus_install_path / 'ExampleFiles' / test_file_name)
        else:
            source_dir = self.find_source_dir_from_cmake_cache()
            return str(source_dir / 'testfiles' / test_file_name)

    def weather_file_path(self, weather_file_name: str = 'USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw') -> str:
        """Gets a path to a default weather file"""
        if self.is_an_install_folder():
            return str(self.eplus_install_path / 'WeatherData' / weather_file_name)
        else:
            source_dir = self.find_source_dir_from_cmake_cache()
            return str(source_dir / 'weather' / weather_file_name)

    @staticmethod
    def get_temp_run_dir() -> str:
        di = mkdtemp()
        print(f"Generated temporary working directory at: {di}")
        return di
