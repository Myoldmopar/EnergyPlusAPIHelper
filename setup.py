import pathlib
from setuptools import setup

readme_file = pathlib.Path(__file__).parent.resolve() / 'README.md'
readme_contents = readme_file.read_text()

setup(
    name="energyplus_api_helpers",
    version="0.1",
    packages=['eplus_api_helpers', 'eplus_api_helpers.demos'],
    description="A set of helper classes, functions and demos, for interacting with the EnergyPlus Python API",
    package_data={"eplus_api_helpers.demos": ["*.html"]},
    include_package_data=True,
    long_description=readme_contents,
    long_description_content_type='text/markdown',
    author='Edwin Lee',
    author_email='a@a.a',
    url='https://github.com/Myoldmopar/EnergyPlusAPIDemos',
    license='UnlicensedForNow',
    install_requires=['matplotlib', 'flask', 'pysparklines', 'asciichartpy'],
    entry_points={
        'console_scripts': ['energyplus_pet_gui=energyplus_pet.runner:main_gui']
    }
)
