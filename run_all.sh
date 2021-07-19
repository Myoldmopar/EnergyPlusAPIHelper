#!/bin/bash

# define the location containing the pyenergyplus package
EPLUS_ROOT='/eplus/repos/energy-plus/builds/r/Products'

# define the folder containing IDF files
IDF_DIR='/eplus/repos/energy-plus/testfiles'

# full path to run script
PYTHON_EXE='/home/edwin/PycharmProjects/LinkToEnergyPlusAPI/venv/bin/python3'
SCRIPT='/home/edwin/PycharmProjects/LinkToEnergyPlusAPI/run_ep_on_file_using_api_twice.py'

echo "FileName,NumFailures" > /tmp/repeat_api.csv

for IDF in "${IDF_DIR}"/*.idf; do
  CASE_NAME=$(basename "${IDF}")
  #case $CASE_NAME in
  #  "5ZoneCoolBeam.idf")
    echo -n "Running ${CASE_NAME} ... "
    $PYTHON_EXE $SCRIPT $EPLUS_ROOT "$IDF" > /dev/null 2>&1
    echo "${CASE_NAME},$?" >> /tmp/repeat_api.csv
    echo "[DONE]"
  #  ;;
  #*)
  #  ;;
  #esac
done
