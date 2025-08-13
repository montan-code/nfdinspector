LIDOInspector guide
===================
 
The basic functionality of LIDOInspector is to analyse metadata records for objects and works based on the LIDO metadata standard for formal data quality aspects.
Inspections are performed in the following steps:

1. Read metadata records for objects and works
2. Customise inspection settings
3. Carry out inspections
4. Further process or output the results

The inspection process is mainly determined by the settings made. 
It makes sense to use different configuration files for different purposes.

In addition, LIDOInspector provides numerous methods for advanced users to design their own inspection processes.


Quick start
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


Reading metadata records
------------------------

LIDO metadata records can be read either as files or as XML strings. 
The data must be valid LIDO XML in order for subsequent inspections to work correctly.

:py:meth:`nfdinspector.lido_inspector.LIDOInspector.read_lido_files` can be used to read multiple LIDO files at once and :py:meth:`nfdinspector.lido_inspector.LIDOInspector.read_lido_file` to read a single LIDO file.
:py:meth:`nfdinspector.lido_inspector.LIDOInspector.read_lido` again reads an XML string.

The data is stored in :py:attr:`nfdinspector.lido_inspector.LIDOInspector.lido_objects`.
Note that the data read will always overwrite itself.

Examples::
    
    from nfdinspector.lido_inspector import LIDOInspector

    lido_inspector = LIDOInspector()

    # Read multiple LIDO files
    lido_inspector.read_lido_files("files_path")
    # Read single LIDO file
    lido_inspector.read_lido_file("file_path")
    # Read LIDO as an XML string
    lido_inspector.read_lido("xml_string")


Configuration
-------------

The configuration of LIDOInspector is stored in the file :py:attr:`nfdinspector.lido_inspector.LIDOInspector.configuration`. 
This is a :py:type:`dict` that lists data fields for which specific settings can be made. 
For example, for the data field 'title' the settings 'inspect', 'unique', 'distinct_from_type', 'min_word_num' and 'max_word_num' can be specified.

===================  ===============  ========================================================================
setting              dtype            description
===================  ===============  ========================================================================
inspect              :py:type:`bool`  specifies if a data field should be inspected
ref                  :py:type:`bool`  specifies if a reference to a vocabulary or similar should be given   
unique               :py:type:`bool`  specifies if an appellation should be unique in the records
distinct_from_type   :py:type:`bool`  specifies if an appellation should be differnt from the object-/worktype
min_word_num         :py:type:`int`   specifies the minimum word number of a text
max_word_num         :py:type:`int`   specifies the maximum word number of a text
min_num              :py:type:`int`   specifies the minimum number of terms
pattern              :py:type:`str`   specifies a valid pattern based on regular expressions
patterns             :py:type:`dict`  specifies valid patterns based on regular expressions
===================  ===============  ========================================================================

The settings available depend on the data field.

====================  ===============================================================
data field            settings
====================  ===============================================================
work_id               pattern
title                 inspect, unique, distinct_from_type, min_word_num, max_word_num
category              inspect, ref, patterns
object_work_type      inspect, ref, patterns
classification        inspect, ref, patterns
object_description    inspect, unique, min_word_num, max_word_num
materials_tech        inspect, ref
object_measurements   inspect
event                 inspect, ref
subject_concept       inspect, ref, min_num
resource              inspect
record_type           inspect, ref, patterns
repository_name       inspect, ref, patterns
record_source         inspect, ref
record_rights         inspect, ref, patterns
record_info           inspect
====================  ===============================================================

It is recommended that you output the :py:attr:`nfdinspector.lido_inspector.LIDOInspector.configuration` as a JSON file to familiarise yourself with the structure. 
This JSON file can also be used as the basis for a new configuration file::
    
    from nfdinspector.lido_inspector import LIDOInspector

    lido_inspector = LIDOInspector()
    with open("default_config.json", "w") as outfile:
        json.dump(lido_inspector.configuration, outfile, indent=4)

The easiest way to configure LIDOInspector is to read a JSON configuration file with :py:meth:`nfdinspector.lido_inspector.LIDOInspector.config_file`. 
The structure of the JSON file must match :py:attr:`nfdinspector.lido_inspector.LIDOInspector.configuration`. 

Changes to :py:attr:`nfdinspector.lido_inspector.LIDOInspector.configuration` can also be made using :py:meth:`nfdinspector.lido_inspector.LIDOInspector.configure`.

Examples::

    from nfdinspector.lido_inspector import LIDOInspector

    lido_inspector = LIDOInspector()
    # Read a configuration file
    lido_inspector.config_file("file_path")
    # Change specific configurations
    lido_inspector.configure({
        "title": {
            "inspect": True,
            "unique": False,
            "distinct_from_type": True,
            "min_word_num": 3,
            "max_word_num": 12,
        }
    })

Patterns
^^^^^^^^

Since version 0.2 it is possible to specify patterns based on regular expressions for some fields.
If they do not match, an error message is returned.

For example, you can specify a pattern for the "workID" field. In this case, the pattern must be a sequence of digits with a length of 12::
    
    from nfdinspector.lido_inspector import LIDOInspector

    lido_inspector = LIDOInspector()
    lido_inspector.configure({
        "work_id": {
            "pattern": "^\d{12}$",
        }
    })

For fields that refer to concepts/entities, patterns can be specified for both the label and the reference. 
In the following example, the label in the "category" field must be "Human-made object" and the reference must be "http://terminology.lido-schema.org/lido00096"::
    
    from nfdinspector.lido_inspector import LIDOInspector

    lido_inspector = LIDOInspector()
    lido_inspector.configure({
        "category": {
            "patterns": {
                "label": "Human-made object"
                "ref": "http://terminology.lido-schema.org/lido00096",
            }
        }
    })

Inspections
-----------

Inspections are performed using :py:meth:`nfdinspector.lido_inspector.LIDOInspector.inspect` based on the data read in and the configurations made. 
The results are stored in :py:attr:`nfdinspector.metadata_inspector.MetadataInspector.inspections` and can be processed further.

Example::
    
    from nfdinspector.lido_inspector import LIDOInspector

    lido_inspector = LIDOInspector()

    # Read multiple LIDO files
    lido_inspector.read_lido_files("files_path")
    # Read a configuration file
    lido_inspector.config_file("file_path")
    # Perform inspections
    lido_inspector.inspect()

:py:meth:`nfdinspector.lido_inspector.LIDOInspector.inspect` performs collective inspections of all configured data fields. 
In principle, methods like :py:meth:`nfdinspector.lido_inspector.LIDOInspector.inspect_title` can be used to inspect a specific field directly. 
The results are returned and not stored in :py:attr:`nfdinspector.metadata_inspector.MetadataInspector.inspections`.

File output
-----------

The results of the inspections can be output as a JSON file using :py:meth:`nfdinspector.metadata_inspector.MetadataInspector.to_json`. 
The indentation level can be determined. 
They can also be output as a CSV file using :py:meth:`nfdinspector.metadata_inspector.MetadataInspector.to_csv`. 
The delimiter can be specified here.

Examples::

    from nfdinspector.lido_inspector import LIDOInspector

    lido_inspector = LIDOInspector()

    # Read multiple LIDO files
    lido_inspector.read_lido_files("files_path")
    # Read a configuration file
    lido_inspector.config_file("file_path")
    # Perform inspections
    lido_inspector.inspect()
    # Output as JSON file
    lido_inspector.to_json("file_path", indent=4)
    # Output as CSV file
    lido_inspector.to_csv("file_path", delimiter=";")