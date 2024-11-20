LIDOInspector Guide
===================

Quick Start
-----------

Import LIDOInspector::

    from nfdinspector.lido_inspector import LIDOInspector

Initialize a LIDOInspector. You can specify a language (currently available: "en" or "de") for the error messages::

    lido_inspector = LIDOInspector(error_lang="de")

Read LIDO files you want to inspect::

    lido_inspector.read_lido_files("files_path")

Refer to a configuration file (optional). Without this step the inspections are executed with a default configuration::

    lido_inspector.config_file("file_path")

Execute the inspections::

    lido_inspector.inspect()

Save the inspections as a JSON file. You can specify the indention (default: None)::

    lido_inspector.to_json("file_path", indent=4)

Save the inspections as a CSV file. You can specify a field separator/delimiter (default: ",")::

    lido_inspector.to_csv("file_path", delimiter=";")