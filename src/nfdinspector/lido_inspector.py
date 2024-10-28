from .metadata_inspector import MetadataInspector
import json


class LIDOInspector(MetadataInspector):
    """Class for inspectors that examine records in LIDO-XML."""

    def __init__(self, error_lang: str = "en") -> None:
        """
        Construct LIDOInspector with specific error language.

        :param error_lang: Error language for the inspections.
        :type error_lang: str, default 'en'
        """
        super().__init__(error_lang)
        self._lido_namespace: str = "http://www.lido-schema.org"
        self._lido_objects: list = []
        self._configuration: dict = {
            "title": {
                "inspect": True,
                "unique": True,
                "distinct_from_type": True,
                "min_word_num": 2,
                "max_word_num": 20,
            },
            "category": {"inspect": True, "ref": True},
            "object_work_type": {"inspect": True, "ref": True},
            "classification": {"inspect": True, "ref": True},
            "object_description": {
                "inspect": True,
                "unique": True,
                "min_word_num": 20,
                "max_word_num": 500,
            },
            "materials_tech": {
                "inspect": True,
                "ref": True,
                "differentiated": False,
            },
            "object_measurements": {"inspect": True},
            "event": {"inspect": True, "ref": True},
            "subject_concept": {
                "inspect": True,
                "ref": True,
                "min_num": 3,
            },
            "resource": {"inspect": True},
            "record_type": {"inspect": True, "ref": True},
            "repository_name": {"inspect": True, "ref": True},
            "record_source": {"inspect": True, "ref": True},
            "record_rights": {"inspect": True, "ref": True},
            "record_info": {"inspect": True},
        }
        self._duplicate_titles: set = set()
        self._duplicate_descriptions: set = set()

    @property
    def lido_namespace(self) -> str:
        """Get the LIDO namespace when needed for reading attributes."""
        return self._lido_namespace

    @property
    def lido_objects(self) -> list:
        """Get or set the list of LIDO records. These records are examined during the inspection."""
        return self._lido_objects

    @lido_objects.setter
    def lido_objects(self, lido_objects: list) -> None:
        self._lido_objects = lido_objects

    @property
    def configuration(self) -> dict:
        """Get or set the configuration. The inspection is carried out based on the configuration."""
        return self._configuration

    @configuration.setter
    def configuration(self, configuration: dict) -> None:
        self._configuration = configuration

    @property
    def duplicate_titles(self) -> set:
        """Get or set the set of duplicate titles."""
        return self._duplicate_titles

    @duplicate_titles.setter
    def duplicate_titles(self, duplicate_titles: set) -> None:
        self._duplicate_titles = duplicate_titles

    @property
    def duplicate_descriptions(self) -> set:
        """Get or set the set of duplicate descriptions."""
        return self._duplicate_descriptions

    @duplicate_descriptions.setter
    def duplicate_descriptions(self, duplicate_descriptions: set) -> None:
        self._duplicate_descriptions = duplicate_descriptions

    def read_lido(self, xml_str: str) -> None:
        """
        Parse LIDO-XML from a string and assign LIDO records to the inspector.

        :param xml_str: String with LIDO-XML syntax
        :type xml_str: str
        """
        xml_root = MetadataInspector.read_xml(xml_str)
        self.lido_objects = [obj for obj in xml_root.iter("{*}lido")]

    def read_lido_file(self, file_path: str) -> None:
        """
        Parse LIDO-XML from a file and assign LIDO records to the inspector.

        :param file_path: File path to a XML file
        :type file_path: str
        """
        xml_root = MetadataInspector.read_xml_file(file_path)
        self.lido_objects = [obj for obj in xml_root.iter("{*}lido")]

    def read_lido_files(self, files_path: str) -> None:
        """
        Parse LIDO-XML from multiple files in a folder and assign LIDO records to the inspector.

        :param file_path: File path to a XML file
        :type file_path: str
        """
        xml_roots: list = MetadataInspector.read_xml_files(files_path)
        self.lido_objects = [obj for root in xml_roots for obj in root.iter("{*}lido")]

    def configure(self, config: dict) -> None:
        """
        Alter the default configurations of an inspector.

        :param config: Dict of configurations with the syntax of the default configurations
        :type config: dict
        """
        for key in self.configuration.keys():
            if key in config:
                self.configure_setting(key, config[key])

    def configure_setting(self, setting: str, change: dict) -> None:
        """
        Alter a specific setting in the configurations of an inspector.

        :param setting: Name of the setting to change
        :type setting: str
        :param change: Desired change for the specific setting
        :type change: dict
        """
        for key, value in change.items():
            if key not in self.configuration[setting]:
                continue
            if key in [
                "inspect",
                "unique",
                "distinct_from_type",
                "ref",
                "differentiated",
            ]:
                self.configuration[setting][key] = bool(value)
            elif key in ["min_word_num", "max_word_num", "min_num"]:
                self.configuration[setting][key] = int(value)

    def config_file(self, file_path: str) -> None:
        """
        Read a configuration file and alter the default configurations of an inspector.

        :param file_path: File path to a JSON file with configurations in the required syntax
        :type file_path: str
        """
        with open(file_path, "r") as f:
            config = json.load(f)
        self.configure(config)

    def inspect(self) -> None:
        """Carry out an inspection based on the read-in LIDO records."""
        self.inspections = []
        if self.configuration["title"]["unique"]:
            self.duplicate_titles = self.find_duplicate_titles()
        if self.configuration["object_description"]["unique"]:
            self.duplicate_descriptions = self.find_duplicate_descriptions()
        for lido_object in self.lido_objects:
            inspection: dict = {}
            inspection["lidoRecID"] = self.inspect_lido_rec_id(lido_object)
            inspection["workID"] = self.inspect_work_id(lido_object)
            inspection["title"] = self.inspect_title(lido_object)
            inspection["category"] = self.inspect_category(lido_object)
            inspection["objectWorkType"] = self.inspect_object_work_types(lido_object)
            inspection["classification"] = self.inspect_classifications(lido_object)
            inspection["objectDescription"] = self.inspect_object_description(
                lido_object
            )
            inspection["materialsTech"] = self.inspect_materials_tech(lido_object)
            inspection["objectMeasurements"] = self.inspect_object_measurements(
                lido_object
            )
            inspection["event"] = self.inspect_events(lido_object)
            inspection["subjectConcept"] = self.inspect_subject_concepts(lido_object)
            inspection["resourceSet"] = self.inspect_resource_sets(lido_object)
            inspection["recordType"] = self.inspect_record_type(lido_object)
            inspection["repositoryName"] = self.inspect_repository_name(lido_object)
            inspection["recordSource"] = self.inspect_record_sources(lido_object)
            inspection["recordRights"] = self.inspect_record_rights(lido_object)
            inspection["recordInfoSet"] = self.inspect_record_info_set(lido_object)
            self.inspections.append(inspection)

    def find_duplicates(self, xpath: str) -> set:
        """
        Find duplicates based on an XPATH expression.

        :param xpath: XPATH expression
        :type xpath: str
        :return: All duplicate titles in lido_objects
        :rtype: set
        """
        texts: list = [
            self.text(lido_object.find(xpath)) for lido_object in self.lido_objects
        ]
        seen: set = set()
        return set(
            text for text in texts if text != "" and text in seen or seen.add(text)
        )

    def find_duplicate_titles(self) -> set:
        """
        Find duplicate titles.

        :return: All duplicate titles in lido_objects
        :rtype: set
        """
        return self.find_duplicates(
            "{*}descriptiveMetadata/{*}objectIdentificationWrap/{*}titleWrap/{*}titleSet/{*}appellationValue"
        )

    def find_duplicate_descriptions(self) -> set:
        """
        Find duplicate descriptions.

        :return: All duplicate descriptions in lido_objects
        :rtype: set
        """
        return self.find_duplicates(
            "{*}descriptiveMetadata/{*}objectIdentificationWrap/{*}objectDescriptionWrap/{*}objectDescriptionSet/{*}descriptiveNoteValue"
        )

    def inspect_lido_rec_id(self, lido_object) -> str:
        """
        Inspect record ID.

        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :return: Record ID or error message if missing
        :rtype: str
        """
        lido_rec_id = lido_object.find("{*}lidoRecID")
        return lido_rec_id.text if self.text(lido_rec_id) else self.error.miss_info()

    def inspect_work_id(self, lido_object) -> str:
        """
        Inspect work ID.

        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :return: Work ID or error message if missing
        :rtype: str
        """
        work_id = lido_object.find(
            "{*}descriptiveMetadata/{*}objectIdentificationWrap/{*}repositoryWrap/{*}repositorySet/{*}workID"
        )
        return work_id.text if self.text(work_id) else self.error.miss_info()

    def is_distinct_from_type(self, lido_object, value: str) -> bool:
        """
        Check if title is distinct from object/work type.

        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :param value: Text value of the inspected record and element
        :type value: str
        :return: True if title is distinct from object/work type, False if not
        :rtype: bool
        """
        object_work_type = lido_object.find(
            "{*}descriptiveMetadata/{*}objectClassificationWrap/{*}objectWorkTypeWrap/{*}objectWorkType"
        )
        if self.has_subelems(object_work_type):
            return False if value == self.term(object_work_type) else True
        return True

    def inspect_title(self, lido_object) -> list | None:
        """
        Inspect title.

        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["title"]["inspect"]:
            return None
        return self.inspect_text(
            lido_object.find(
                "{*}descriptiveMetadata/{*}objectIdentificationWrap/{*}titleWrap/{*}titleSet"
            ),
            lido_object,
            self.configuration["title"],
        )

    def value(self, parent) -> str:
        """
        Get value (appellation or descriptiveNote) of a text field.

        :param parent: Parent element of the supposed value element.
        :type parent: etree._Element
        :return: Text value
        :rtype: str
        """
        if not self.has_subelems(parent):
            return ""
        value = parent.find(".//{*}appellationValue")
        return (
            value.text
            if self.text(value)
            else self.text(parent.find("{*}descriptiveNoteValue"))
        )

    def term(self, parent) -> str:
        """
        Get term or prefLabel of a concept.

        :param parent: Parent element of the supposed term or prefLabel element.
        :type parent: etree._Element
        :return: Term or label
        :rtype: str
        """
        if not self.has_subelems(parent):
            return ""
        term = parent.find("{*}term")
        return (
            term.text if self.text(term) else self.text(parent.find(".//{*}prefLabel"))
        )

    def is_uniq(self, text: str, element) -> bool:
        """
        Check if title or object description is unique.

        :param text: Text that is checked
        :type text: str
        :param element: XML element with supposed text
        :type element: etree._Element
        :return: True if title/description is unique, False if not
        :rtype: bool
        """
        if (
            (
                element.tag == f"{{{self.lido_namespace}}}titleSet"
                or element.tag == "titleSet"
            )
            and text in self.duplicate_titles
        ) or (
            (
                element.tag == f"{{{self.lido_namespace}}}objectDescriptionSet"
                or element.tag == "objectDescriptionSet"
            )
            and text in self.duplicate_descriptions
        ):
            return False
        return True

    def inspect_text(self, element, lido_object, config: dict) -> list | None:
        """
        Inspect a text element.

        :param element: XML element with supposed text
        :type element: etree._Element
        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :param config: Configuration of the specific inspection.
        :type config: dict
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.has_subelems(element):
            return [self.error.miss_info()]
        value: str = self.value(element)
        if not value:
            return [self.error.miss_info()]
        messages: list = []
        if self.has_duplicate_blanks(value):
            messages.append(self.error.dupl_blanks())
        if config["unique"]:
            if not self.is_uniq(value, element):
                messages.append(self.error.not_uniq())
        if config.get("distinct_from_type", False):
            if not self.is_distinct_from_type(lido_object, value):
                messages.append(self.error.dist("objectWorkType"))
        if not len(value.split()) >= config["min_word_num"]:
            messages.append(self.error.short())
        if not len(value.split()) <= config["max_word_num"]:
            messages.append(self.error.long())
        return messages if messages else None

    def about(self, element) -> str:
        """
        Get value from about attribute.

        :param element: XML element with supposed about attribute
        :type element: etree._Element
        :return: Value of about
        :rtype: str
        """
        return self.attr(element, f"{{{self.rdf_namespace}}}about")

    def concept_id(self, parent) -> str:
        """
        Get ID of a concept.

        :param parent: Parent element of the supposed conceptID or Concept element.
        :type parent: etree._Element
        :return: conceptID or Concept
        :rtype: str
        """
        if not self.has_subelems(parent):
            return ""
        concept_id = parent.find("{*}conceptID")
        return (
            concept_id.text
            if self.text(concept_id)
            else self.about(parent.find("{*}Concept"))
        )

    def inspect_concept(self, concept, config: dict) -> list:
        """
        Inspect concept.

        :param concept: XML element of the concept
        :type concept: etree._Element
        :param config: Configuration of the specific inspection.
        :type config: dict
        :return: List of error messages
        :rtype: list
        """
        if not self.has_subelems(concept):
            return [self.error.miss_info()]
        return self.inspect_entity(self.term(concept), self.concept_id(concept), config)

    def inspect_concepts(self, concept_list: list, config: dict) -> list | None:
        """
        Inspect multiple concepts.

        :param concept_list: List of XML elements of concepts
        :type concept_list: list
        :param config: Configuration of the specific inspection.
        :type config: dict
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not concept_list:
            return [self.error.miss_info()]
        messages: list = []
        for element in concept_list:
            messages.extend(self.inspect_concept(element, config))
        if "min_num" in config:
            if len(concept_list) < config["min_num"]:
                messages.append(self.error.few())
        return messages if messages else None

    def inspect_category(self, lido_object) -> list | None:
        """
        Inspect category.

        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["category"]["inspect"]:
            return None
        return self.inspect_concepts(
            lido_object.findall("{*}category"), self.configuration["category"]
        )

    def inspect_object_work_types(self, lido_object) -> list | None:
        """
        Inspect object/work types.

        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["object_work_type"]["inspect"]:
            return None
        return self.inspect_concepts(
            lido_object.findall(
                "{*}descriptiveMetadata/{*}objectClassificationWrap/{*}objectWorkTypeWrap/{*}objectWorkType"
            ),
            self.configuration["object_work_type"],
        )

    def inspect_classifications(self, lido_object) -> list | None:
        """
        Inspect classifications.

        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["classification"]["inspect"]:
            return None
        return self.inspect_concepts(
            lido_object.findall(
                "{*}descriptiveMetadata/{*}objectClassificationWrap/{*}classificationWrap/{*}classification"
            ),
            self.configuration["classification"],
        )

    def inspect_object_description(self, lido_object) -> list | None:
        """
        Inspect object description.

        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["object_description"]["inspect"]:
            return None
        return self.inspect_text(
            lido_object.find(
                "{*}descriptiveMetadata/{*}objectIdentificationWrap/{*}objectDescriptionWrap/{*}objectDescriptionSet"
            ),
            lido_object,
            self.configuration["object_description"],
        )

    def lido_type(self, element) -> str:
        """
        Get value from type attribute.

        :param element: XML element with supposed type attribute
        :type element: etree._Element
        :return: Value of type
        :rtype: str
        """
        return self.attr(element, f"{{{self.lido_namespace}}}type")

    def has_valid_type(self, elements: list, valid_types: list) -> bool:
        """
        Check if elements have valid types.

        :param elements: Elements with supposed type attributes
        :type elements: list
        :return: True if type is valid, False if not
        :rtype: bool
        """
        for element in elements:
            if self.lido_type(element).lower() in valid_types:
                return True
        return False

    def has_material(self, materials_tech: list) -> bool:
        """
        Check if record contains information about material.

        :param materials_tech: XML elements of materials/techniques
        :type materials_tech: list
        :return: True if record contains information about material, False if not
        :rtype: bool
        """
        return self.has_valid_type(
            materials_tech,
            [
                "http://terminology.lido-schema.org/lido00132",
                "material",
                "materials",
                "substances",
            ],
        )

    def has_tech(self, materials_tech: list) -> bool:
        """
        Check if record contains information about technique.

        :param materials_tech: XML elements of materials/techniques
        :type materials_tech: list
        :return: True if record contains information about technique, False if not
        :rtype: bool
        """
        return self.has_valid_type(
            materials_tech,
            [
                "http://terminology.lido-schema.org/lido00131",
                "technique",
                "methods",
                "technique",
                "technik",
                "entstehungsmethode",
            ],
        )

    def inspect_materials_tech(self, lido_object) -> list | None:
        """
        Inspect materials and techniques.

        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["materials_tech"]["inspect"]:
            return None
        materials_tech = lido_object.findall(".//{*}materialsTech/{*}termMaterialsTech")
        concepts_inspection = self.inspect_concepts(
            materials_tech, self.configuration["materials_tech"]
        )
        messages: list = []
        if concepts_inspection is not None:
            messages.extend(concepts_inspection)
        if (
            not self.configuration["materials_tech"]["differentiated"]
            or self.error.miss_info() in messages
        ):
            return messages if messages else None
        if not self.has_material(materials_tech):
            messages.append(self.error.miss_mat())
        if not self.has_tech(materials_tech):
            messages.append(self.error.miss_tech())
        return messages if messages else None

    def meas_type(self, measurement_type) -> str:
        """
        Get text or ID of measurement type.

        :param measurement_type: XML element of measurement type.
        :type measurement_type: etree._Element
        :return: Text or ID
        :rtype: str
        """
        return (
            measurement_type.text
            if self.text(measurement_type)
            else self.concept_id(measurement_type)
        )

    def inspect_measurements_set(self, measurements_set) -> list:
        """
        Inspect a measurements set.

        :param measurements_set: XML element of supposed measurements set
        :type measurements_set: etree._Element
        :return: List of error messages
        :rtype: list
        """
        if not self.has_subelems(measurements_set):
            return [self.error.empty_elem("measurementsSet")]
        measurement_type: str = self.meas_type(
            measurements_set.find("{*}measurementType")
        )
        measurement_unit = measurements_set.find("{*}measurementUnit")
        measurement_value = measurements_set.find("{*}measurementValue")
        messages: list = []
        if not measurement_type:
            messages.append(self.error.miss_meas_type())
        if not self.text(measurement_unit) and not self.has_subelems(measurement_unit):
            messages.append(self.error.miss_meas_unit(measurement_type))
        if not self.text(measurement_value):
            messages.append(self.error.miss_meas_value(measurement_type))
        return messages

    def inspect_object_measurements(self, lido_object) -> list | None:
        """
        Inspect objects measurements.

        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["object_measurements"]["inspect"]:
            return None
        measurements_sets = lido_object.findall(
            "{*}descriptiveMetadata/{*}objectIdentificationWrap/{*}objectMeasurementsWrap/{*}objectMeasurementsSet/{*}objectMeasurements/{*}measurementsSet"
        )
        if not measurements_sets:
            return [self.error.miss_info()]
        messages: list = []
        for measurements_set in measurements_sets:
            messages.extend(self.inspect_measurements_set(measurements_set))
        return messages if messages else None

    def inspect_event_type(self, event_type) -> list:
        """
        Inspect event type.

        :param event_type: XML element of supposed event type
        :type event_type: etree._Element
        :return: List of error messages
        :rtype: list
        """
        if not self.has_subelems(event_type):
            return [self.error.miss_event_type()]
        return self.inspect_concept(event_type, self.configuration["event"])

    def place_id(self, parent) -> str:
        """
        Get ID of a place.

        :param parent: Parent element of the supposed place element.
        :type parent: etree._Element
        :return: placeID
        :rtype: str
        """
        return self.text(parent.find("{*}placeID")) if self.has_subelems(parent) else ""

    def inspect_place(self, place, event_type, config: dict) -> list:
        """
        Inspect place.

        :param place: XML element of supposed place
        :type place: etree._Element
        :param event_type: XML element of corresponding event type
        :type event_type: etree._Element
        :param config: Configuration of the specific inspection.
        :type config: dict
        :return: List of error messages
        :rtype: list
        """
        if not self.has_subelems(place):
            return [self.error.miss_place(self.term(event_type))]
        return self.inspect_entity(self.value(place), self.place_id(place), config)

    def inspect_places(self, places: list, event_type, config: dict) -> list:
        """
        Inspect multiple places.

        :param places: XML elements of supposed places
        :type places: etree._Element
        :param event_type: XML element of corresponding event type
        :type event_type: etree._Element
        :param config: Configuration of the specific inspection.
        :type config: dict
        :return: List of error messages
        :rtype: list
        """
        if self.term(event_type) in ["Event (non-specified)"]:
            return []
        if not places:
            return [self.error.miss_place(self.term(event_type))]
        messages: list = []
        for place in places:
            messages.extend(self.inspect_place(place, event_type, config))
        return messages

    def actor_id(self, parent) -> str:
        """
        Get ID of an actor.

        :param parent: Parent element of the supposed actor element.
        :type parent: etree._Element
        :return: actorID
        :rtype: str
        """
        return self.text(parent.find("{*}actorID")) if self.has_subelems(parent) else ""

    def inspect_actor(self, actor, event_type, config: dict) -> list:
        """
        Inspect actor.

        :param actor: XML element of supposed actor
        :type actor: etree._Element
        :param event_type: XML element of corresponding event type
        :type event_type: etree._Element
        :param config: Configuration of the specific inspection.
        :type config: dict
        :return: List of error messages
        :rtype: list
        """
        if not self.has_subelems(actor):
            return [self.error.miss_actor(self.term(event_type))]
        return self.inspect_entity(self.value(actor), self.actor_id(actor), config)

    def inspect_actors(self, actors: list, event_type, config: dict) -> list:
        """
        Inspect multiple actors.

        :param actors: XML elements of supposed actors
        :type actors: etree._Element
        :param event_type: XML element of corresponding event type
        :type event_type: etree._Element
        :param config: Configuration of the specific inspection.
        :type config: dict
        :return: List of error messages
        :rtype: list
        """
        if self.term(event_type) in ["Event (non-specified)"]:
            return []
        if not actors:
            return [self.error.miss_actor(self.term(event_type))]
        messages: list = []
        for actor in actors:
            messages.extend(self.inspect_actor(actor, event_type, config))
        return messages

    def inspect_date(self, date, event_type) -> list:
        """
        Inspect date.

        :param date: XML element of supposed date
        :type date: etree._Element
        :param event_type: XML element of corresponding event type
        :type event_type: etree._Element
        :return: List of error messages
        :rtype: list
        """
        if self.term(event_type) in ["Event (non-specified)"]:
            return []
        if not self.has_subelems(date):
            return [self.error.miss_date(self.term(event_type))]
        messages: list = []
        if not self.text(date.find("{*}earliestDate")):
            messages.append(self.error.miss_earl_date(self.term(event_type)))
        if not self.text(date.find("{*}latestDate")):
            messages.append(self.error.miss_lat_date(self.term(event_type)))
        return messages

    def summarize_event_messages(self, messages: list, event_type: str) -> list:
        """
        Summarize several event-specific error messages (missing actor, place and date).

        :param messages: Error messages of an event
        :type messages: list
        :param event_type: XML element of corresponding event type
        :type event_type: etree._Element
        :return: List of error messages
        :rtype: list
        """
        if (
            self.error.miss_actor(event_type) in messages
            and self.error.miss_place(event_type) in messages
            and self.error.miss_date(event_type) in messages
        ):
            messages.append(self.error.miss_event_info(event_type))
        return [
            message
            for message in messages
            if message != self.error.miss_actor(event_type)
            and message != self.error.miss_place(event_type)
            and message != self.error.miss_date(event_type)
        ]

    def inspect_event(self, event) -> list:
        """
        Inspect event.

        :param event: XML element of supposed event
        :type event: etree._Element
        :return: List of error messages
        :rtype: list
        """
        if not self.has_subelems(event):
            return [self.error.empty_elem("event")]
        messages: list = []
        event_type = event.find("{*}eventType")
        messages.extend(self.inspect_event_type(event_type))
        messages.extend(
            self.inspect_actors(
                event.findall("{*}eventActor/{*}actorInRole/{*}actor"),
                event_type,
                self.configuration["event"],
            )
        )
        messages.extend(
            self.inspect_places(
                event.findall("{*}eventPlace/{*}place"),
                event_type,
                self.configuration["event"],
            )
        )
        messages.extend(
            self.inspect_date(event.find("{*}eventDate/{*}date"), event_type)
        )
        return self.summarize_event_messages(messages, self.term(event_type))

    def inspect_events(self, lido_object) -> list | None:
        """
        Inspect events.

        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["event"]["inspect"]:
            return None
        events: list = lido_object.findall(
            "{*}descriptiveMetadata/{*}eventWrap/{*}eventSet/{*}event"
        )
        if not events:
            return [self.error.miss_info()]
        messages: list = []
        for event in events:
            messages.extend(self.inspect_event(event))
        return messages if messages else None

    def inspect_subject_concepts(self, lido_object) -> list | None:
        """
        Inspect subject concepts.

        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["subject_concept"]["inspect"]:
            return None
        return self.inspect_concepts(
            lido_object.findall(
                "{*}descriptiveMetadata/{*}objectRelationWrap/{*}subjectWrap/{*}subjectSet/{*}subject/{*}subjectConcept"
            ),
            self.configuration["subject_concept"],
        )

    def inspect_resource_set(self, resource_set) -> list:
        """
        Inspect resource set.

        :param resource_set: XML element of supposed resource set
        :type resource_set: etree._Element
        :return: List of error messages
        :rtype: list
        """
        if not self.has_subelems(resource_set):
            return [self.error.empty_elem("resourceSet")]
        messages: list = []
        link_resource: str = self.text(
            resource_set.find("{*}resourceRepresentation/{*}linkResource")
        )
        if not link_resource:
            messages.append(self.error.miss_link())
        if not self.text(resource_set.find("{*}rightsResource/{*}rightsType/{*}term")):
            messages.append(self.error.miss_rights(link_resource))
        if not self.text(resource_set.find("{*}resourceType/{*}term")):
            messages.append(self.error.miss_res_type(link_resource))
        return messages

    def inspect_resource_sets(self, lido_object) -> list | None:
        """
        Inspect resource sets.

        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["resource"]["inspect"]:
            return None
        resource_sets = lido_object.findall(
            "{*}administrativeMetadata/{*}resourceWrap/{*}resourceSet"
        )
        if not resource_sets:
            return [self.error.miss_info()]
        messages: list = []
        for resource_set in resource_sets:
            messages.extend(self.inspect_resource_set(resource_set))
        return messages if messages else None

    def inspect_record_type(self, lido_object) -> list | None:
        """
        Inspect record type.

        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["record_type"]["inspect"]:
            return None
        messages: list = self.inspect_concept(
            lido_object.find("{*}administrativeMetadata/{*}recordWrap/{*}recordType"),
            self.configuration["record_type"],
        )
        return messages if messages else None

    def legal_body_id(self, parent) -> str:
        """
        Get ID of a legal body.

        :param parent: Parent element of the supposed legal body element.
        :type parent: etree._Element
        :return: legalBodyID
        :rtype: str
        """
        return (
            self.text(parent.find("{*}legalBodyID"))
            if self.has_subelems(parent)
            else ""
        )

    def inspect_repository_name(self, lido_object) -> list | None:
        """
        Inspect repository name.

        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["repository_name"]["inspect"]:
            return None
        repository_name = lido_object.find(
            "{*}descriptiveMetadata/{*}objectIdentificationWrap/{*}repositoryWrap/{*}repositorySet/{*}repositoryName"
        )
        if not self.has_subelems(repository_name):
            return [self.error.miss_info()]
        messages: list = []
        messages.extend(
            self.inspect_entity(
                self.value(repository_name),
                self.legal_body_id(repository_name),
                self.configuration["repository_name"],
            )
        )
        return messages if messages else None

    def inspect_record_source(self, record_source) -> list:
        """
        Inspect record source.

        :param record_source: XML element of supposed record source
        :type record_source: etree._Element
        :return: List of error messages
        :rtype: list
        """
        if not self.has_subelems(record_source):
            return [self.error.empty_elem("recordSource")]
        return self.inspect_entity(
            self.value(record_source),
            self.legal_body_id(record_source),
            self.configuration["record_source"],
        )

    def inspect_record_sources(self, lido_object) -> list | None:
        """
        Inspect record sources.

        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["record_source"]["inspect"]:
            return None
        record_sources = lido_object.findall(
            "{*}administrativeMetadata/{*}recordWrap/{*}recordSource"
        )
        if not record_sources:
            return [self.error.miss_info()]
        messages: list = []
        for record_source in record_sources:
            messages.extend(self.inspect_record_source(record_source))
        return messages if messages else None

    def inspect_record_rights(self, lido_object) -> list | None:
        """
        Inspect record rights.

        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["record_rights"]["inspect"]:
            return None
        return self.inspect_concepts(
            lido_object.findall(
                "{*}administrativeMetadata/{*}recordWrap/{*}recordRights/{*}rightsType"
            ),
            self.configuration["record_rights"],
        )

    def inspect_record_info_set(self, lido_object) -> list | None:
        """
        Inspect record information.

        :param lido_object: Record of an object in LIDO-XML
        :type lido_object: etree._Element
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["record_info"]["inspect"]:
            return None
        record_info_set = lido_object.find(
            "{*}administrativeMetadata/{*}recordWrap/{*}recordInfoSet"
        )
        if not self.has_subelems(record_info_set):
            return [self.error.miss_info()]
        messages: list = []
        if not self.has_text(record_info_set.find("{*}recordInfoLink")):
            messages.append(self.error.miss_link())
        if not self.has_text(record_info_set.find("{*}recordMetadataDate")):
            messages.append(
                self.error.miss_date("http://terminology.lido-schema.org/lido00472")
            )
        return messages if messages else None
