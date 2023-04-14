import pathlib
from setuptools import setup

readme_file = pathlib.Path(__file__).parent.resolve() / 'README.md'
readme_contents = readme_file.read_text()

setup(
    name="energyplus_api_helpers",
    version="0.4",
    packages=['energyplus_api_helpers', 'energyplus_api_helpers.demos'],
    description="A set of helper classes, functions and demos, for interacting with the EnergyPlus Python API",
    package_data={"energyplus_api_helpers.demos": ["*.html"]},
    include_package_data=True,
    long_description=readme_contents,
    long_description_content_type='text/markdown',
    author='Edwin Lee, for NREL, for the United States Department of Energy',
    url='https://github.com/Myoldmopar/EnergyPlusAPIHelper',
    license='ModifiedBSD',
    install_requires=['matplotlib', 'flask', 'pysparklines', 'asciichartpy'],
    # entry_points={
    #     'console_scripts': ['energyplus_api_helper=energyplus_api_helpers.runner:main_gui']
    # }
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Utilities',
    ],
    platforms=[
        'Linux (Tested on Ubuntu)', 'MacOSX', 'Windows'
    ],
    keywords=[
        'energyplus_launch', 'ep_launch',
        'EnergyPlus', 'eplus', 'Energy+',
        'Building Simulation', 'Whole Building Energy Simulation',
        'Heat Transfer', 'HVAC', 'Modeling',
    ]
)
