import os
import json
import csv
from datetime import date
from lxml import etree
from .error import Error


class MetadataInspector:
    """Super class for various metadata standard-specific inspectors."""

    def __init__(self, error_lang: str = "en") -> None:
        """
        Construct MetadataInspector with specific error language.

        :param error_lang: Error language for the inspections.
        :type error_lang: str, default 'en'
        """
        self._error = Error(error_lang)
        self._inspections: list = []
        self._rdf_namespace: str = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        self._xlink_namespace: str = "http://www.w3.org/1999/xlink"

    @property
    def error(self) -> Error:
        """Get or set an Error object. The Error object is needed for adding error messages to the inspections"""
        return self._error

    @error.setter
    def error(self, error) -> None:
        self._error = error

    @property
    def inspections(self) -> list:
        """Get or set the inspections list. The list is filled while inspecting a data set."""
        return self._inspections

    @inspections.setter
    def inspections(self, inspections: list) -> None:
        self._inspections = inspections

    @property
    def rdf_namespace(self) -> str:
        """Get the RDF namespace when needed for reading attributes."""
        return self._rdf_namespace

    @property
    def xlink_namespace(self) -> str:
        """Get the XLINK namespace when needed for reading attributes."""
        return self._xlink_namespace

    @staticmethod
    def read_xml(xml_str: str):
        """
        Parse XML from a string.

        :param xml_str: String with XML syntax
        :type xml_str: str
        :return: Root element of an ElementTree
        :rtype: etree._Element
        """
        parser = etree.XMLParser(remove_blank_text=True, ns_clean=True)
        return etree.fromstring(xml_str, parser)

    @staticmethod
    def read_xml_file(file_path: str):
        """
        Parse XML from a file.

        :param file_path: File path to a XML file
        :type file_path: str
        :return: Root element of an ElementTree
        :rtype: etree._Element
        """
        parser = etree.XMLParser(remove_blank_text=True, ns_clean=True)
        return etree.parse(file_path, parser).getroot()

    @staticmethod
    def read_xml_files(files_path: str) -> list:
        """
        Parse XML from multiple XML files in a folder.

        :param file_path: File path to a folder with XML files
        :type file_path: str
        :return: List of root elements of multiple ElementTrees
        :rtype: list
        """
        return [
            MetadataInspector.read_xml_file(f"{files_path}/{file_name}")
            for file_name in os.listdir(files_path)
            if file_name.endswith(".xml")
        ]

    def exists(self, element) -> bool:
        """
        Check if an XML element exists.

        :param element: Supposed XML element
        :type element: etree._Element
        :return: True if element exists, False if not
        :rtype: bool
        """
        return True if element is not None else False

    def has_subelems(self, element) -> bool:
        """
        Check if an XML element has subelements.

        :param element: XML element with supposed subelements
        :type element: etree._Element
        :return: True if element has subelements, False if not
        :rtype: bool
        """
        return True if self.exists(element) and len(element) else False

    def has_text(self, element) -> bool:
        """
        Check if an XML element has text.

        :param element: XML element with supposed text
        :type element: etree._Element
        :return: True if element has text, False if not
        :rtype: bool
        """
        return (
            True
            if self.exists(element) and element.text is not None and len(element.text)
            else False
        )

    def text(self, element) -> str:
        """
        Get text from an XML element.

        :param element: XML element with supposed text
        :type element: etree._Element
        :return: Text from an XML Element
        :rtype: str
        """
        return element.text if self.has_text(element) else ""

    def has_attribute(self, element, attribute_name: str) -> bool:
        """
        Check if an XML element has a specific attribute.

        :param element: XML element with supposed attribute
        :type element: etree._Element
        :param attribute_name: Supposed attribute name
        :type attribute_name: str
        :return: True if element has a specific attribute, False if not
        :rtype: bool
        """
        return (
            True
            if self.exists(element)
            and element.get(attribute_name) is not None
            and len(element.get(attribute_name))
            else False
        )

    def attr(self, element, attribute_name: str) -> str:
        """
        Get attribute text from an XML element.

        :param element: XML element with supposed attribute
        :type element: etree._Element
        :param attribute_name: Supposed attribute name
        :type attribute_name: str
        :return: Attribute text from an XML Element
        :rtype: str
        """
        return (
            element.get(attribute_name)
            if self.has_attribute(element, attribute_name)
            else ""
        )

    def has_duplicate_blanks(self, text: str) -> bool:
        """
        Check if a text has duplicate blanks.

        :param text: Text with possible duplicate blanks
        :type text: str
        :return: True if text has duplicate blanks, False if not
        :rtype: bool
        """
        return True if "  " in text else False

    def inspect_entity(self, label: str, entity_id: str, config: dict) -> list:
        """
        Inspect label and ID of an entity (person, organisation etc.).

        :param label: Label of an entity
        :type label: str
        :param entity_id: ID of an entity
        :type entity_id: str
        :param config: Configuration of the specific inspection.
        :type config: dict
        :return: List of error messages
        :rtype: list
        """
        messages: list = []
        if not label:
            messages.append(self.error.miss_label(entity_id))
        if not config["ref"]:
            return messages
        if not entity_id:
            messages.append(self.error.miss_ref(label))
        return messages

    def date_object(self, date_str: str):
        """
        Get a date object from a date string (ISO 8601).

        :param date_str: Date string (ISO 8601)
        :type date_str: str
        :return: Date object if valid ISO 8601 format, None if not valid
        :rtype: datetime.date | None
        """
        try:
            date_obj = date.fromisoformat(date_str)
        except:
            return None
        return date_obj

    def date_range(self, date_str: str) -> dict:
        """
        Split a date to earliest and latest date.

        :param date_str: Date string (ISO 8601)
        :type date_str: str
        :return: Dict with date objects where earliest and latest date are separated
        :rtype: dict
        """
        return {
            "earliest_date": self.date_object(date_str.split("/")[0]),
            "latest_date": self.date_object(date_str.split("/")[-1]),
        }

    def create_element(self, tag_name: str = "element", text: str = ""):
        """
        Create an XML element from a tag name and text.

        :param tag_name: Tag name for the XML element
        :type tag_name: str
        :param text: Text for the XML element
        :type text: str
        :return: XML element
        :rtype: etree._Element
        """
        element = etree.Element(tag_name)
        element.text = text
        return element

    def to_json(self, file_path: str, indent: int | str | None = None) -> None:
        """
        Generate a JSON file of the inspections.

        :param file_path: File path for the JSON file
        :type file_path: str
        :param indent: Indent level of the JSON file
        :type indent: int | str | None
        """
        with open(file_path, "w", encoding="utf-8") as outfile:
            json.dump(self.inspections, outfile, indent=indent, ensure_ascii=False)

    def to_csv(self, file_path: str, delimiter: str = ",") -> None:
        """
        Generate a CSV file of the inspections.

        :param file_path: File path for the CSV file
        :type file_path: str
        :param delimiter: Delimiter for the columns in the CSV file
        :type delimiter: str
        """
        with open(file_path, "w", newline="") as outfile:
            writer = csv.DictWriter(
                outfile, fieldnames=self.inspections[0].keys(), delimiter=delimiter
            )
            if writer.fieldnames:
                writer.writeheader()
            writer.writerows(self.inspections)
