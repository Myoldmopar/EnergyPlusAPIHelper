import platform
import shutil
import sys
from pathlib import Path
from tempfile import mkdtemp
from typing import Optional


def _infer_energyplus_install_dir():
    """Try to locate the EnergyPlus installation path.

    Starts by looking at `which energyplus` first then tries the default installation paths.
    Returns the most recent version found"""
    if ep := shutil.which("energyplus"):
        return Path(ep).resolve().parent
    ext = ""
    if platform.system() == 'Linux':
        base_dir = Path('/usr/local')
    elif platform.system() == 'Darwin':
        base_dir = Path('Applications')
    else:
        base_dir = Path('C:/')
        ext = ".exe"
    if not base_dir.is_dir():
        raise ValueError(f"{base_dir=} is not a directory")
    candidates = [p.parent for p in base_dir.glob(f"EnergyPlus*/energyplus{ext}")]
    if not candidates:
        raise ValueError(f"Found zero EnergyPlus installation directories")
    candidates = [c for c in candidates if (c / 'pyenergyplus').is_dir()]
    if not candidates:
        raise ValueError(f"Found zero EnergyPlus installation directories that have the pyenergyplus directory")
    # Sort by version
    candidates.sort(key=lambda c: [int(x) for x in c.name.split('-')[1:]])
    return candidates[-1]


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

    def __init__(self, eplus_install_path: Optional[Path] = None):
        if eplus_install_path is None:
            self.eplus_install_path = _infer_energyplus_install_dir()
            print(f"Infered Location of EnergyPlus installation at {self.eplus_install_path}")
        else:
            if not (self.eplus_install_path / 'pyenergyplus').is_dir():
                raise ValueError(f"Wrong eplus_install_path, '{eplus_install_path}/pyenergyplus' does not exist")
            self.eplus_install_path = eplus_install_path

    def get_api_instance(self):
        with _EPlusImporter(self.eplus_install_path):
            from pyenergyplus.api import EnergyPlusAPI

            return EnergyPlusAPI()

    def is_an_install_folder(self) -> bool:
        if (self.eplus_install_path / "ExampleFiles").exists():
            return True
        return False

    def find_source_dir_from_cmake_cache(self) -> Path:
        cmake_cache_file = self.eplus_install_path.parent / "CMakeCache.txt"
        if not cmake_cache_file.is_file():
            raise ValueError("Cannot locate the CMakeCache.txt")
        lines = cmake_cache_file.read_text().split("\n")
        for line in lines:
            line_trimmed = line.strip()
            if line_trimmed.startswith("EnergyPlus_SOURCE_DIR:STATIC="):
                found_dir = line_trimmed.split("=")[1]
                return Path(found_dir)
        raise ValueError(f"Could not locate the source directory in {cmake_cache_file}")

    def path_to_test_file(self, test_file_name: str) -> str:
        """Returns the path to an example/test file, trying to figure out if it is a build dir or install."""
        if self.is_an_install_folder():
            return str(self.eplus_install_path / "ExampleFiles" / test_file_name)
        else:
            source_dir = self.find_source_dir_from_cmake_cache()
            return str(source_dir / "testfiles" / test_file_name)

    def weather_file_path(self, weather_file_name: str = "USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw") -> str:
        """Gets a path to a default weather file"""
        if self.is_an_install_folder():
            return str(self.eplus_install_path / "WeatherData" / weather_file_name)
        else:
            source_dir = self.find_source_dir_from_cmake_cache()
            return str(source_dir / "weather" / weather_file_name)

    @staticmethod
    def get_temp_run_dir() -> str:
        di = mkdtemp()
        print(f"Generated temporary working directory at: {di}")
        return di
