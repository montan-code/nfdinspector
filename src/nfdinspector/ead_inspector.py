from .metadata_inspector import MetadataInspector
import json
from datetime import date


class EADInspector(MetadataInspector):
    """Class for inspectors that examine records in EAD-XML."""

    def __init__(self, error_lang="en") -> None:
        """
        Construct EADInspector with specific error language.

        :param error_lang: Error language for the inspections.
        :type error_lang: str, default 'en'
        """
        super().__init__(error_lang)
        self._ead_namespace: str = "urn:isbn:1-931666-22-9"
        self._cs: list = []
        self._rights_ead: list = []
        self.configuration: dict = {
            "unittitle": {
                "collection": {"inspect": True, "min_word_num": 2},
                "class": {"inspect": True, "min_word_num": 1},
                "series": {"inspect": True, "min_word_num": 1},
                "file": {"inspect": True, "min_word_num": 2},
                "item": {"inspect": True, "min_word_num": 2},
                "_": {"inspect": True, "min_word_num": 2},
            },
            "unitdate": {
                "collection": {"inspect": True},
                "class": {"inspect": False},
                "series": {"inspect": False},
                "file": {"inspect": True},
                "item": {"inspect": True},
                "_": {"inspect": True},
            },
            "abstract": {
                "collection": {"inspect": True, "min_word_num": 10},
                "class": {"inspect": False, "min_word_num": 10},
                "series": {"inspect": False, "min_word_num": 10},
                "file": {"inspect": True, "min_word_num": 10},
                "item": {"inspect": True, "min_word_num": 10},
                "_": {"inspect": True, "min_word_num": 10},
            },
            "genreform": {
                "normal": [
                    "Urkunden",
                    "Siegel",
                    "Amtsbücher, Register und Grundbücher",
                    "Akten",
                    "Karten und Pläne",
                    "Plakate und Flugblätter",
                    "Drucksachen",
                    "Bilder",
                    "Handschriften",
                    "Audio-Visuelle Medien",
                    "Datenbanken",
                    "Sonstiges",
                ],
                "collection": {"inspect": True},
                "class": {"inspect": False},
                "series": {"inspect": False},
                "file": {"inspect": True},
                "item": {"inspect": True},
                "_": {"inspect": True},
            },
            "dimensions": {
                "collection": {"inspect": True},
                "class": {"inspect": False},
                "series": {"inspect": False},
                "file": {"inspect": True},
                "item": {"inspect": True},
                "_": {"inspect": True},
            },
            "extent": {
                "collection": {"inspect": True},
                "class": {"inspect": False},
                "series": {"inspect": False},
                "file": {"inspect": True},
                "item": {"inspect": True},
                "_": {"inspect": True},
            },
            "scopecontent": {
                "collection": {"inspect": True, "min_word_num": 100},
                "class": {"inspect": False, "min_word_num": 10},
                "series": {"inspect": False, "min_word_num": 10},
                "file": {"inspect": True, "min_word_num": 10},
                "item": {"inspect": False, "min_word_num": 10},
                "_": {"inspect": True, "min_word_num": 10},
            },
            "origination": {
                "collection": {"inspect": True, "ref": True},
                "class": {"inspect": False, "ref": True},
                "series": {"inspect": False, "ref": True},
                "file": {"inspect": True, "ref": True},
                "item": {"inspect": True, "ref": True},
                "_": {"inspect": True, "ref": True},
            },
            "materialspec": {
                "collection": {"inspect": True},
                "class": {"inspect": False},
                "series": {"inspect": False},
                "file": {"inspect": True},
                "item": {"inspect": True},
                "_": {"inspect": True},
            },
            "language": {
                "collection": {"inspect": True},
                "class": {"inspect": False},
                "series": {"inspect": False},
                "file": {"inspect": True},
                "item": {"inspect": True},
                "_": {"inspect": True},
            },
            "digital_archival_object": {
                "collection": {"inspect": False},
                "class": {"inspect": False},
                "series": {"inspect": False},
                "file": {"inspect": False},
                "item": {"inspect": True},
                "_": {"inspect": True},
            },
            "index": {
                "collection": {"inspect": True, "ref": True, "min_num": 5},
                "class": {"inspect": False, "ref": True, "min_num": 3},
                "series": {"inspect": False, "ref": True, "min_num": 3},
                "file": {"inspect": True, "ref": True, "min_num": 3},
                "item": {"inspect": True, "ref": True, "min_num": 3},
                "_": {"inspect": True, "ref": True, "min_num": 3},
            },
            "userestrict": {
                "collection": {"inspect": True, "ref": True},
                "class": {"inspect": False, "ref": True},
                "series": {"inspect": False, "ref": True},
                "file": {"inspect": True, "ref": True},
                "item": {"inspect": True, "ref": True},
                "_": {"inspect": True, "ref": True},
            },
        }

    @property
    def ead_namespace(self) -> str:
        """Get the EAD namespace when needed for reading attributes."""
        return self._ead_namespace

    @property
    def cs(self) -> list[object]:
        """Get or set the list of EAD components. These components are examined during the inspection."""
        return self._cs

    @cs.setter
    def cs(self, cs: list) -> None:
        self._cs = cs

    @property
    def rights_ead(self) -> list:
        """Get or set the EAD metadata rights."""
        return self._rights_ead

    @rights_ead.setter
    def rights_ead(self, rights_ead: list) -> None:
        self._rights_ead = rights_ead

    @property
    def configuration(self) -> dict:
        """Get or set the configuration. The inspection is carried out based on the configuration."""
        return self._configuration

    @configuration.setter
    def configuration(self, configuration: dict) -> None:
        self._configuration = configuration

    def read_ead(self, xml_str: str) -> None:
        """
        Parse EAD-XML from a string and assign EAD components to the inspector.

        :param xml_str: String with EAD-XML syntax
        :type xml_str: str
        """
        xml_root = MetadataInspector.read_xml(xml_str)
        self.cs = [comp for comp in xml_root.iter("{*}c")]
        self.rights_ead = xml_root.find(
            ".//{*}archdesc/{*}userestrict[@type='ead']//{*}extref"
        )

    def read_ead_file(self, file_path: str) -> None:
        """
        Parse EAD-XML from a file and assign EAD components to the inspector.

        :param file_path: File path to a XML file
        :type file_path: str
        """
        xml_root = MetadataInspector.read_xml_file(file_path)
        self.cs = [comp for comp in xml_root.iter("{*}c")]
        self.rights_ead = xml_root.find(
            ".//{*}archdesc/{*}userestrict[@type='ead']//{*}extref"
        )

    def configure(self, config: dict) -> None:
        """
        Alter the default configurations of an inspector.

        :param config: Dict of configurations with the syntax of the default configurations
        :type config: dict
        """
        for key in self.configuration.keys():
            if key in config:
                self.configure_level(key, config[key])

    def configure_level(self, setting: str, change: dict | list) -> None:
        """
        Alter a specific level in the configurations of an inspector.

        :param setting: Name of the setting which should be altered
        :type setting: str
        :param change: New configuartions for the specific setting
        :type change: dict | list
        """
        for key in self.configuration[setting].keys():
            if key in change:
                self.configure_setting(setting, key, change[key])

    def configure_setting(self, setting: str, level: str, change: list | dict) -> None:
        """
        Alter a specific setting in the configurations of an inspector.

        :param setting: Name of the setting which should be altered
        :type setting: str
        :param level: Name of the level which should be altered
        :type level: str
        :param change: New configuartions for the specific setting
        :type change: dict | list
        """
        if level in ["normal"]:
            self.configuration[setting][level] = change
            return
        if isinstance(change, dict):
            for key, value in change.items():
                if key not in self.configuration[setting][level]:
                    continue
                if key in ["inspect", "ref"]:
                    self.configuration[setting][level][key] = bool(value)
                elif key in ["min_word_num", "min_num"]:
                    self.configuration[setting][level][key] = int(value)

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
        """Carry out an inspection based on the read-in EAD components."""
        self.inspections = []
        for c in self.cs:
            level: str = self.attr(c, "level")
            if level not in ["collection", "class", "series", "file", "item"]:
                level = "_"
            inspection: dict = {}
            inspection["id"] = self.inspect_id(c)
            inspection["unitid"] = self.inspect_unitid(c)
            inspection["unittitle"] = self.inspect_unittitle(c, level)
            inspection["unitdate"] = self.inspect_unitdates(c, level)
            inspection["abstract"] = self.inspect_abstract(c, level)
            inspection["genreform"] = self.inspect_genreform(c, level)
            inspection["dimensions"] = self.inspect_dimensions(c, level)
            inspection["extent"] = self.inspect_extent(c, level)
            inspection["scopecontent"] = self.inspect_scopecontent(c, level)
            inspection["origination"] = self.inspect_originations(c, level)
            inspection["materialspec"] = self.inspect_materialspec(c, level)
            inspection["language"] = self.inspect_language(c, level)
            inspection["digital_archival_object"] = self.inspect_daos(c, level)
            inspection["index"] = self.inspect_index(c, level)
            inspection["userestrict"] = self.inspect_userestrict(c, level)
            self.inspections.append(inspection)

    def inspect_id(self, c) -> str:
        """
        Inspect component ID.

        :param c: Component of an EAD record
        :type c: etree._Element
        :return: Component ID or error message if missing
        :rtype: str
        """
        return (
            self.attr(c, "id")
            if self.has_attribute(c, "id")
            else self.error.miss_info()
        )

    def inspect_unitid(self, c) -> str:
        """
        Inspect unit ID.

        :param c: Component of an EAD record
        :type c: etree._Element
        :return: Unit ID or error message if missing
        :rtype: str
        """
        unitid = c.find("{*}did/{*}unitid")
        return unitid.text if self.text(unitid) else self.error.miss_info()

    def inspect_text(self, element, config: dict) -> list | None:
        """
        Inspect a text element.

        :param element: XML element with supposed text
        :type element: etree._Element
        :param config: Configuration of the specific inspection.
        :type config: dict
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.text(element):
            return [self.error.miss_info()]
        messages: list = []
        if self.has_duplicate_blanks(self.text(element)):
            messages.append(self.error.dupl_blanks())
        if not len(self.text(element).split()) >= config["min_word_num"]:
            messages.append(self.error.short())
        return messages if messages else None

    def inspect_unittitle(self, c, level: str) -> list | None:
        """
        Inspect unit title.

        :param c: Component of an EAD record
        :type c: etree._Element
        :param level: Level of the inspected EAD component
        :type level: str
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["unittitle"][level]["inspect"]:
            return None
        return self.inspect_text(
            c.find("{*}did/{*}unittitle"), self.configuration["unittitle"][level]
        )

    def subordinate_unitdates(self, c) -> dict:
        """
        Get all subordinate unit dates of an component.

        :param c: Component of an EAD record
        :type c: etree._Element
        :return: Dict of unit dates
        :rtype: dict
        """
        dates: dict = {}
        sub_cs: list = c.findall(".//{*}c")
        for sub_c in sub_cs:
            unitid: str = self.text(sub_c.find("{*}did/{*}unitid"))
            if unitid:
                unitdates: list = sub_c.findall("{*}did/{*}unitdate")
                dates[unitid] = self.normalized_unitdates(unitdates)
        return dates

    def normalized_unitdates(self, unitdates: list) -> list:
        """
        Normalize unit dates.

        :param unitdates: List of unit dates
        :type unitdates: list
        :return: List of normalized dates
        :rtype: list
        """
        return [self.normal_date_range(unitdate) for unitdate in unitdates]

    def is_consistent_latest_date(self, sub_date: dict, date: dict) -> bool:
        """
        Check if sub date (latest) is consistent.

        :param sub_date: Sub date of a subordinate component
        :type sub_date: dict
        :param date: Date of the superordinate component
        :type date: dict
        :return: True if date is consistent, False if not
        :rtype: bool
        """
        if sub_date["latest_date"] is None:
            return True
        if (
            date["latest_date"] is not None
            and sub_date["latest_date"] <= date["latest_date"]
        ):
            return True
        return False

    def is_consistent_earliest_date(self, sub_date: dict, date: dict) -> bool:
        """
        Check if sub date (earliest) is consistent.

        :param sub_date: Sub date of a subordinate component
        :type sub_date: dict
        :param date: Date of the superordinate component
        :type date: dict
        :return: True if date is consistent, False if not
        :rtype: bool
        """
        if sub_date["earliest_date"] is None:
            return True
        if (
            date["earliest_date"] is not None
            and sub_date["earliest_date"] >= date["earliest_date"]
        ):
            return True
        return False

    def is_consistent_date(self, sub_date: dict, dates: list) -> bool:
        """
        Check if sub date (earliest and latest) is consistent.

        :param sub_date: Sub date of a subordinate component
        :type sub_date: dict
        :param dates: Dates of the superordinate component
        :type dates: list
        :return: True if date is consistent, False if not
        :rtype: bool
        """
        if sub_date["earliest_date"] is None and sub_date["latest_date"] is None:
            return True
        for date in dates:
            if self.is_consistent_earliest_date(
                sub_date, date
            ) and self.is_consistent_latest_date(sub_date, date):
                return True
        return False

    def inspect_sub_dating(
        self, dates: list, sub_unitid: str, sub_dating: dict
    ) -> list:
        """
        Inspect dates in comparison to sub dates.

        :param dates: Dates of the inspected component
        :type dates: list
        :param sub_unitid: Unit id of subordinate component
        :type sub_unitid: str
        :param sub_dating: Dating of subordinate component
        :type sub_dating: str
        :return: List of error messages
        :rtype: list
        """
        messages: list = []
        for sub_date in sub_dating:
            if not self.is_consistent_date(sub_date, dates):
                messages.append(
                    self.error.inconsistent_date(
                        sub_unitid,
                        f"{sub_date['earliest_date']}/{sub_date['latest_date']}",
                    )
                )
        return messages

    def inspect_unitdates_consistency(self, unitdates: list, c) -> list:
        """
        Inspect consistency of unit dates.

        :param unitdates: Unit dates of the inspected component
        :type unitdates: list
        :param c: Component of an EAD record
        :type c: etree._Element
        :return: List of error messages
        :rtype: list
        """
        messages: list = []
        dates: list = self.normalized_unitdates(unitdates)
        sub_dates: dict = self.subordinate_unitdates(c)
        for unitid, sub_dating in sub_dates.items():
            messages.extend(self.inspect_sub_dating(dates, unitid, sub_dating))
        return messages

    def normal_date_range(self, date) -> dict:
        """
        Get normalized date range.

        :param date: Date to normalize
        :type date: etree._Element
        :return: Normalized date range
        :rtype: dict
        """
        return self.date_range(self.attr(date, "normal"))

    def is_future(self, norm_date: dict) -> bool:
        """
        Check if a date is in the future.

        :param norm_date: Normalized form of the inspected date
        :type norm_date: dict
        :return: True if date is in the future, False if not
        :rtype: bool
        """
        today: date = date.today()
        if (
            norm_date["earliest_date"] is not None
            and norm_date["earliest_date"] > today
        ):
            return True
        if norm_date["latest_date"] is not None and norm_date["latest_date"] > today:
            return True
        return False

    def inspect_date(self, date) -> list:
        """
        Inspect date.

        :param date: Date to inspect
        :type date: etree._Element
        :return: List of error messages
        :rtype: list
        """
        messages: list = []
        norm_date: dict = self.normal_date_range(date)
        if norm_date["earliest_date"] is None or norm_date["latest_date"] is None:
            messages.append(self.error.miss_norm_date(self.text(date)))
        if self.is_future(norm_date):
            messages.append(self.error.future(f"{self.attr(date, 'normal')}"))
        return messages

    def inspect_dates(self, dates: list) -> list:
        """
        Inspect multiple dates.

        :param dates: Dates to inspect
        :type dates: list
        :return: List of error messages
        :rtype: list
        """
        messages: list = []
        for date in dates:
            messages.extend(self.inspect_date(date))
        return messages

    def inspect_unitdates(self, c, level: str) -> list | None:
        """
        Inspect unit dates.

        :param c: Component of an EAD record
        :type c: etree._Element
        :param level: Level of the inspected EAD component
        :type level: str
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["unitdate"][level]["inspect"]:
            return None
        unitdates: list = c.findall("{*}did/{*}unitdate")
        if not unitdates:
            return [self.error.miss_info()]
        messages: list = []
        messages.extend(self.inspect_dates(unitdates))
        messages.extend(self.inspect_unitdates_consistency(unitdates, c))
        return messages if messages else None

    def inspect_abstract(self, c, level: str) -> list | None:
        """
        Inspect abstract.

        :param c: Component of an EAD record
        :type c: etree._Element
        :param level: Level of the inspected EAD component
        :type level: str
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["abstract"][level]["inspect"]:
            return None
        return self.inspect_text(
            c.find("{*}did/{*}abstract"), self.configuration["abstract"][level]
        )

    def inspect_genreform(self, c, level: str) -> list | None:
        """
        Inspect genreform.

        :param c: Component of an EAD record
        :type c: etree._Element
        :param level: Level of the inspected EAD component
        :type level: str
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["genreform"][level]["inspect"]:
            return None
        genreform = c.find("{*}did/{*}physdesc/{*}genreform")
        normal: str = self.attr(genreform, "normal")
        if not normal and not self.text(genreform):
            return [self.error.miss_info()]
        if not normal or normal not in self.configuration["genreform"]["normal"]:
            return [
                self.error.miss_norm_term(normal if normal else self.text(genreform))
            ]
        return None

    def inspect_dimensions(self, c, level: str) -> list | None:
        """
        Inspect dimensions.

        :param c: Component of an EAD record
        :type c: etree._Element
        :param level: Level of the inspected EAD component
        :type level: str
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["dimensions"][level]["inspect"]:
            return None
        if not self.text(c.find("{*}did/{*}physdesc/{*}dimensions")):
            return [self.error.miss_info()]
        return None

    def inspect_extent(self, c, level: str) -> list | None:
        """
        Inspect extent.

        :param c: Component of an EAD record
        :type c: etree._Element
        :param level: Level of the inspected EAD component
        :type level: str
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["extent"][level]["inspect"]:
            return None
        if not self.text(c.find("{*}did/{*}physdesc/{*}extent")):
            return [self.error.miss_info()]
        return None

    def inspect_scopecontent(self, c, level: str) -> list | None:
        """
        Inspect scope content.

        :param c: Component of an EAD record
        :type c: etree._Element
        :param level: Level of the inspected EAD component
        :type level: str
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["scopecontent"][level]["inspect"]:
            return None
        scopecontent_subelems = c.findall("{*}scopecontent/{*}*")
        text: str = " ".join(
            [elem.text.strip() for elem in scopecontent_subelems if self.has_text(elem)]
        )
        return self.inspect_text(
            self.create_element("scopecontent", text),
            self.configuration["scopecontent"][level],
        )

    def inspect_origination(self, origination, level: str) -> list:
        """
        Inspect origination.

        :param origination: XML element of origination
        :type origination: etree._Element
        :param level: Level of the inspected EAD component
        :type level: str
        :return: List of error messages
        :rtype: list
        """
        if not self.has_text(origination) and not self.has_subelems(origination):
            return [self.error.empty_elem(origination.tag)]
        if self.has_subelems(origination):
            origination = origination.find("{*}name")
            if not self.has_text(origination):
                return [self.error.empty_elem(origination.tag)]
        return self.inspect_entity(
            self.text(origination),
            self.attr(origination, "authfilenumber"),
            self.configuration["origination"][level],
        )

    def inspect_originations(self, c, level: str) -> list | None:
        """
        Inspect originations.

        :param c: Component of an EAD record
        :type c: etree._Element
        :param level: Level of the inspected EAD component
        :type level: str
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["origination"][level]["inspect"]:
            return None
        originations = c.findall("{*}did/{*}origination")
        if not originations:
            return [self.error.miss_info()]
        messages: list = []
        for origination in originations:
            messages.extend(self.inspect_origination(origination, level))
        return messages if messages else None

    def inspect_materialspec(self, c, level: str) -> list | None:
        """
        Inspect materialspec.

        :param c: Component of an EAD record
        :type c: etree._Element
        :param level: Level of the inspected EAD component
        :type level: str
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["materialspec"][level]["inspect"]:
            return None
        if not self.text(c.find("{*}did/{*}materialspec")):
            return [self.error.miss_info()]
        return None

    def inspect_language(self, c, level: str) -> list | None:
        """
        Inspect language.

        :param c: Component of an EAD record
        :type c: etree._Element
        :param level: Level of the inspected EAD component
        :type level: str
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["language"][level]["inspect"]:
            return None
        language = c.find("{*}did/{*}langmaterial/{*}language")
        if not self.text(language):
            return [self.error.miss_info()]
        if not self.attr(language, "langcode"):
            return [self.error.miss_lang_code()]
        return None

    def inspect_daogrp(self, daogrp) -> list:
        """
        Inspect a digital archival object.

        :param c: Component of an EAD record
        :type c: etree._Element
        :return: List of error messages, None if there are no errors
        :rtype: list
        """
        if not self.has_subelems(daogrp):
            return [self.error.empty_elem("daogrp")]
        messages: list = []
        if not self.attr(daogrp.find("{*}daoloc"), f"{{{self.xlink_namespace}}}href"):
            messages.append(self.error.miss_link())
        return messages

    def inspect_daos(self, c, level: str) -> list | None:
        """
        Inspect digital archival objects.

        :param c: Component of an EAD record
        :type c: etree._Element
        :param level: Level of the inspected EAD component
        :type level: str
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["digital_archival_object"][level]["inspect"]:
            return None
        daogrps = c.findall("{*}daogrp")
        if not daogrps:
            return [self.error.miss_info()]
        messages: list = []
        for daogrp in daogrps:
            messages.extend(self.inspect_daogrp(daogrp))
        return messages if messages else None

    def inspect_indexentry(self, indexentry, level: str) -> list:
        """
        Inspect an index entry.

        :param indexentry: XML element of an index entry
        :type indexentry: etree._Element
        :param level: Level of the inspected EAD component
        :type level: str
        :return: List of error messages
        :rtype: list
        """
        if not self.has_subelems(indexentry):
            return [self.error.empty_elem(indexentry.tag)]
        name_subject = indexentry.find("{*}*")
        if not self.has_text(name_subject):
            return [self.error.empty_elem(name_subject.tag)]
        return self.inspect_entity(
            self.text(name_subject),
            self.attr(name_subject, "authfilenumber"),
            self.configuration["index"][level],
        )

    def inspect_index(self, c, level: str) -> list | None:
        """
        Inspect index.

        :param c: Component of an EAD record
        :type c: etree._Element
        :param level: Level of the inspected EAD component
        :type level: str
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["index"][level]["inspect"]:
            return None
        indexentries: list = c.findall("{*}index/{*}indexentry")
        if not indexentries:
            return [self.error.miss_info()]
        messages: list = []
        for indexentry in indexentries:
            messages.extend(self.inspect_indexentry(indexentry, level))
        if len(indexentries) < self.configuration["index"][level]["min_num"]:
            messages.append(self.error.few())
        return messages if messages else None

    def inspect_userestrict(self, c, level: str) -> list | None:
        """
        Inspect use restrict.

        :param c: Component of an EAD record
        :type c: etree._Element
        :param level: Level of the inspected EAD component
        :type level: str
        :return: List of error messages, None if there are no errors
        :rtype: list | None
        """
        if not self.configuration["userestrict"][level]["inspect"]:
            return None
        extref = c.find("{*}userestrict[@type='ead']//{*}extref")
        if (
            not self.has_text(extref)
            and not self.has_text(self.rights_ead)
            and not self.attr(extref, f"{{{self.xlink_namespace}}}href")
            and not self.attr(self.rights_ead, f"{{{self.xlink_namespace}}}href")
        ):
            return [self.error.miss_rights("EAD")]
        return None
