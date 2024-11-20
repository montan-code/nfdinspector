# NFDInspector


NFDInspector is designed to facilitate the inspection of formal quality issues pertaining to research data. 
It is currently compatible with the LIDO and EAD metadata standards. 
The project has been funded by the "4Memory Incubator Funds" of the NFDI4Memory consortium and is being developed and maintained by the Montanhistorisches Dokumentationszentrum (montan.dok) of the Deutsches Bergbau-Museum Bochum.

* [Documentation](https://montan-code.github.io/nfdinspector/)
* [GitHub](https://github.com/montan-code/nfdinspector)
* [PyPI](https://pypi.org/project/NFDInspector/)
* [License](https://pypi.org/project/NFDInspector/)

## Installation

To install with pip on macOS or Linux, run:

    python3 -m pip install nfdinspector

To install with pip on Windows, run:

    py -m pip install nfdinspector

## Quickstart Guide

### LIDO inspection

Import LIDOInspector:

    from nfdinspector.lido_inspector import LIDOInspector

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

Import EADInspector:

    from nfdinspector.ead_inspector import EADInspector

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
