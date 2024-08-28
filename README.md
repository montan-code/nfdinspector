# NFDInspector


A Python module to inspect formal quality problems in research data, funded by the "4Memory Incubator Funds" of the consortium NFDI4Memory.

## Installation

To install with pip on macOS or Linux, run:

    python3 -m pip install nfdinspector

To install with pip on Windows, run:

    py -m pip install nfdinspector

## Quickstart Guide

### LIDO inspection

Initialize a LIDOInspector and specify a language (currently available: "en" or "de"):

    lido_inspector = LIDOInspector(lang="de")

Read LIDO files you want to inspect:

    lido_inspector.read_lido_files("file_path")

Read a configuration file:

    lido_inspector.config_file("file_path")

Execute the inspection:

    lido_inspector.inspect()

Save the inspection as a JSON file:

    lido_inspector.to_json("file_path")

Save the inspection as a CSV file:

    lido_inspector.to_csv("file_path", delimiter=";")


### EAD inspection

Initialize an EADInspector and specify a language (currently available: "en" or "de"):

    ead_inspector = LIDOInspector(lang="en")

Read EAD file you want to inspect:

    ead_inspector.read_ead_file("file_path")

Read a configuration file:

    ead_inspector.config_file("file_path")

Execute the inspection:

    ead_inspector.inspect()

Save the inspection as a JSON file:
    
    ead_inspector.to_json("file_path")

Save the inspection as a CSV file:

    ead_inspector.to_csv("file_path", delimiter=";")   

## Contribute

If you'd like to contribute to NFDInspector, check out https://github.com/montan-code/nfdinspector
