EADInspector guide
===================

The basic functionality of EADInspector is to analyse metadata records for archive tectonics and finding aids based on the EAD metadata standard for formal data quality aspects.
Inspections are performed in the following steps:

1. Read metadata record for archive tectonic or finding aid
2. Customise inspection settings
3. Carry out inspections
4. Further process or output the results

The inspection process is mainly determined by the settings made. 
It makes sense to use different configuration files for different purposes.

In addition, EADInspector provides numerous methods for advanced users to design their own inspection processes.

Quick start
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
    

Reading metadata records
------------------------

EAD metadata records can be read either as files or as XML strings. 
The data must be valid EAD(DDB) XML in order for subsequent inspections to work correctly.

:py:meth:`nfdinspector.ead_inspector.EADInspector.read_ead_file` can be used to read an EAD file.
:py:meth:`nfdinspector.ead_inspector.EADInspector.read_ead` again reads an XML string.

The data is stored in :py:attr:`nfdinspector.ead_inspector.EADInspector.cs`.
Note that the data read will always overwrite itself.

Examples::
    
    from nfdinspector.ead_inspector import EADInspector

    ead_inspector = EADInspector()

    # Read EAD file
    ead_inspector.read_ead_file("file_path")
    # Read EAD as an XML string
    ead_inspector.read_ead("xml_string")


Configuration
-------------

The configuration of EADInspector is stored in the file :py:attr:`nfdinspector.ead_inspector.EADInspector.configuration`. 
This is a :py:type:`dict` that lists data fields for which specific settings can be made. 
Most of these settings can be specifically adapted to the different levels (collection, class, series, file, item) of the hierarchy of an EAD file.
Note that depending on whether it is an archive tectonics or a finding aid, these levels have different meanings.


===================  ===============  ========================================================================
setting              dtype            description
===================  ===============  ========================================================================
inspect              :py:type:`bool`  specifies if a data field should be inspected
ref                  :py:type:`bool`  specifies if a reference to a vocabulary or similar should be given   
min_word_num         :py:type:`int`   specifies the minimum word number of a text
min_num              :py:type:`int`   specifies the minimum number of terms
normal               :py:type:`list`  specifies normalized terms that are allowed 
pattern              :py:type:`str`   specifies a valid pattern based on regular expressions
patterns             :py:type:`dict`  specifies valid patterns based on regular expressions
===================  ===============  ========================================================================

The settings available depend on the data field.

=========================  ===============================================================
data field                 settings
=========================  ===============================================================
unitid                     pattern
unittitle                  inspect, min_word_num
unitdate                   inspect
abstract                   inspect, min_word_num
genreform                  inspect, normal
dimensions                 inspect
extent                     inspect
scopecontent               inspect, min_word_num
origination                inspect, ref
materialspec               inspect
language                   inspect
digital_archival_object    inspect
index                      inspect, ref, min_num
userestrict                inspect, ref
=========================  ===============================================================

It is recommended that you output the :py:attr:`nfdinspector.ead_inspector.EADInspector.configuration` as a JSON file to familiarise yourself with the structure. 
This JSON file can also be used as the basis for a new configuration file::
    
    from nfdinspector.ead_inspector import EADInspector

    ead_inspector = EADInspector()
    with open("default_config.json", "w") as outfile:
        json.dump(ead_inspector.configuration, outfile, indent=4)

The easiest way to configure EADInspector is to read a JSON configuration file with :py:meth:`nfdinspector.ead_inspector.EADInspector.config_file`. 
The structure of the JSON file must match :py:attr:`nfdinspector.ead_inspector.EADInspector.configuration`. 

Changes to :py:attr:`nfdinspector.ead_inspector.EADInspector.configuration` can also be made using :py:meth:`nfdinspector.ead_inspector.EADInspector.configure`.

Examples::

    from nfdinspector.ead_inspector import EADInspector

    ead_inspector = EADInspector()
    # Read a configuration file
    ead_inspector.config_file("file_path")
    # Change specific configurations
    ead_inspector.configure({
        "unittitle": {
            "collection": {"inspect": True, "min_word_num": 2},
            "class": {"inspect": True, "min_word_num": 1},
            "series": {"inspect": True, "min_word_num": 1},
            "file": {"inspect": True, "min_word_num": 2},
            "item": {"inspect": True, "min_word_num": 2},
            "_": {"inspect": True, "min_word_num": 2},
        }
    })


Inspections
-----------

Inspections are performed using :py:meth:`nfdinspector.ead_inspector.EADInspector.inspect` based on the data read in and the configurations made. 
The results are stored in :py:attr:`nfdinspector.metadata_inspector.MetadataInspector.inspections` and can be processed further.

Example::
    
    from nfdinspector.ead_inspector import EADInspector

    ead_inspector = EADInspector()

    # Read EAD file
    ead_inspector.read_ead_file("files_path")
    # Read a configuration file
    ead_inspector.config_file("file_path")
    # Perform inspections
    ead_inspector.inspect()

:py:meth:`nfdinspector.ead_inspector.EADInspector.inspect` performs collective inspections of all configured data fields. 
In principle, methods like :py:meth:`nfdinspector.ead_inspector.EADInspector.inspect_unittitle` can be used to inspect a specific field directly. 
The results are returned and not stored in :py:attr:`nfdinspector.metadata_inspector.MetadataInspector.inspections`.

File output
-----------

The results of the inspections can be output as a JSON file using :py:meth:`nfdinspector.metadata_inspector.MetadataInspector.to_json`. 
The indentation level can be determined. 
They can also be output as a CSV file using :py:meth:`nfdinspector.metadata_inspector.MetadataInspector.to_csv`. 
The delimiter can be specified here.

Examples::

    from nfdinspector.ead_inspector import EADInspector

    ead_inspector = EADInspector()

    # Read EAD file
    ead_inspector.read_ead_file("files_path")
    # Read a configuration file
    ead_inspector.config_file("file_path")
    # Perform inspections
    ead_inspector.inspect()
    # Output as JSON file
    ead_inspector.to_json("file_path", indent=4)
    # Output as CSV file
    ead_inspector.to_csv("file_path", delimiter=";")