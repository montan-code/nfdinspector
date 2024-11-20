EADInspector Guide
===================

Quick Start
-----------

Import EADInspector::

    from nfdinspector.ead_inspector import EADInspector

Initialize an EADInspector. You can specify a language (currently available: "en" or "de") for the error messages::

    ead_inspector = EADInspector(error_lang="en")

Read EAD file you want to inspect::

    ead_inspector.read_ead_file("file_path")

Refer to a configuration file (optional). Without this step the inspections are executed with a default configuration. It is highly recommended to use different configuration files for archive tectonics and finding aids::

    ead_inspector.config_file("file_path")

Execute the inspections::

    ead_inspector.inspect()

Save the inspections as a JSON file. You can specify the indention (default: None)::
    
    ead_inspector.to_json("file_path", indent=4)

Save the inspections as a CSV file. You can specify a field separator/delimiter (default: ",")::

    ead_inspector.to_csv("file_path", delimiter=";")