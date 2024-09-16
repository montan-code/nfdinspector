# NFDInspector


A Python package to inspect formal quality problems in research data (currently compatible metadata standards: LIDO and EAD). Funded by the "4Memory Incubator Funds" of the consortium NFDI4Memory, developed and maintained by the Montanhistorisches Dokumentationszentrum (montan.dok) of the Deutsches Bergbau-Museum Bochum.

## Installation

To install with pip on macOS or Linux, run:

    python3 -m pip install nfdinspector

To install with pip on Windows, run:

    py -m pip install nfdinspector

## Quickstart Guide

### LIDO inspection

Initialize a LIDOInspector. You can specify a language (currently available: "en" or "de") for the error messages:

    lido_inspector = LIDOInspector(error_lang="de")

Read LIDO files you want to inspect:

    lido_inspector.read_lido_files("files_path")

Refer to a configuration file (optional). Without this step the inspections are executed with a default configuration:

    lido_inspector.config_file("file_path")

Execute the inspections:

    lido_inspector.inspect()

Save the inspections as a JSON file. You can specify the indention (default: None):

    lido_inspector.to_json("file_path", indent=4)

Save the inspections as a CSV file. You can specify a field separator/delimiter (default: ","):

    lido_inspector.to_csv("file_path", delimiter=";")


### EAD inspection

Initialize an EADInspector. You can specify a language (currently available: "en" or "de") for the error messages:

    ead_inspector = EADInspector(error_lang="en")

Read EAD file you want to inspect:

    ead_inspector.read_ead_file("file_path")

Refer to a configuration file (optional). Without this step the inspections are executed with a default configuration. It is highly recommended to use different configuration files for archive tectonics and finding aids:

    ead_inspector.config_file("file_path")

Execute the inspections:

    ead_inspector.inspect()

Save the inspections as a JSON file. You can specify the indention (default: None):
    
    ead_inspector.to_json("file_path", indent=4)

Save the inspections as a CSV file. You can specify a field separator/delimiter (default: ","):

    ead_inspector.to_csv("file_path", delimiter=";")   

## Contribute

If you'd like to contribute to NFDInspector, check out https://github.com/montan-code/nfdinspector
