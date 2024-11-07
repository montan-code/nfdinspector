import pytest
from lxml import etree
from datetime import date
from nfdinspector.metadata_inspector import MetadataInspector


def xml(xml_string):
    return etree.fromstring(xml_string)


class Test_MetadataInspector:

    def test_read_xml(self):
        mi = MetadataInspector()
        assert mi.read_xml("<root><elem></elem></root>").tag == "root"
        assert mi.read_xml("<root><elem></elem></root>").tag != "elem"
        assert mi.read_xml("<root><elem></elem></root>").find("elem") != None
        assert mi.read_xml("<root><elem></elem></root>").find("nonelem") == None
        assert mi.read_xml("<root></root>").find("elem") == None
        assert mi.read_xml("<root></root>").text == None
        assert mi.read_xml("<root>text</root>").text == "text"

    def test_exists(self):
        mi = MetadataInspector()
        assert mi.exists(xml("<elem>test</elem>")) == True
        assert mi.exists(xml("<elem></elem>")) == True
        assert mi.exists(xml("<elem/>")) == True
        assert mi.exists(None) == False

    def test_has_subelems(self):
        mi = MetadataInspector()
        assert mi.has_subelems(xml("<elem>test</elem>")) == False
        assert mi.has_subelems(xml("<elem></elem>")) == False
        assert mi.has_subelems(xml("<elem/>")) == False
        assert mi.has_subelems(None) == False
        assert mi.has_subelems(xml("<elem><elem/></elem>")) == True
        assert mi.has_subelems(xml("<elem><elem></elem></elem>")) == True
        assert mi.has_subelems(xml("<elem><elem>test</elem></elem>")) == True

    def test_text(self):
        mi = MetadataInspector()
        assert mi.text(xml("<elem>test</elem>")) == "test"
        assert mi.text(xml("<elem></elem>")) == ""
        assert mi.text(xml("<elem/>")) == ""
        assert mi.text(None) == ""

    def test_has_text(self):
        mi = MetadataInspector()
        assert mi.has_text(xml("<elem>test</elem>")) == True
        assert mi.has_text(xml("<elem></elem>")) == False
        assert mi.has_text(xml("<elem/>")) == False
        assert mi.has_text(None) == False

    def test_has_attribute(self):
        mi = MetadataInspector()
        assert mi.has_attribute(xml("<elem>test</elem>"), "attrib") == False
        assert mi.has_attribute(xml("<elem></elem>"), "attrib") == False
        assert mi.has_attribute(xml("<elem/>"), "attrib") == False
        assert mi.has_attribute(None, "attrib") == False
        assert mi.has_attribute(xml("<elem attrib=''/>"), "attrib") == False
        assert mi.has_attribute(xml("<elem attrib='test'/>"), "attrib") == True
        assert (
            mi.has_attribute(xml("<elem attrib='test'>test</elem>"), "attrib") == True
        )
        assert mi.has_attribute(xml("<elem otherattrib='test'/>"), "attrib") == False
        assert mi.has_attribute(xml("<elem attrib='test'/>"), "otherattrib") == False
        assert (
            mi.has_attribute(
                xml(
                    "<elem xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' rdf:about='test'></elem>"
                ),
                f"{{{mi.rdf_namespace}}}about",
            )
            == True
        )

    def test_attr(self):
        mi = MetadataInspector()
        assert mi.attr(xml("<elem>test</elem>"), "attrib") == ""
        assert mi.attr(xml("<elem></elem>"), "attrib") == ""
        assert mi.attr(xml("<elem/>"), "attrib") == ""
        assert mi.attr(None, "attrib") == ""
        assert mi.attr(xml("<elem attrib=''/>"), "attrib") == ""
        assert mi.attr(xml("<elem attrib='test'/>"), "attrib") == "test"
        assert mi.attr(xml("<elem attrib='test'>test</elem>"), "attrib") == "test"
        assert mi.attr(xml("<elem otherattrib='test'/>"), "attrib") == ""
        assert mi.attr(xml("<elem attrib='test'/>"), "otherattrib") == ""
        assert (
            mi.attr(
                xml(
                    "<elem xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' rdf:about='test'></elem>"
                ),
                f"{{{mi.rdf_namespace}}}about",
            )
            == "test"
        )

    def test_has_duplicate_blanks(self):
        mi = MetadataInspector()
        assert mi.has_duplicate_blanks("hello world") == False
        assert mi.has_duplicate_blanks("hello world ") == False
        assert mi.has_duplicate_blanks("hello  world") == True
        assert mi.has_duplicate_blanks("hello world  ") == True
        assert mi.has_duplicate_blanks("  hello world") == True

    def test_inspect_entity(self):
        mi = MetadataInspector()
        assert mi.inspect_entity("test", "test_id", {"ref": True}) == []
        assert mi.error.miss_ref("test") in mi.inspect_entity("test", "", {"ref": True})
        assert mi.error.miss_ref("") in mi.inspect_entity("", "", {"ref": True})
        assert mi.error.miss_label("") in mi.inspect_entity("", "", {"ref": True})
        assert mi.error.miss_label("") in mi.inspect_entity("", "", {"ref": False})
        assert mi.inspect_entity("test", "", {"ref": False}) == []
        assert (
            mi.inspect_entity(
                "test",
                "test_id",
                {"ref": True, "patterns": {"label": "", "ref": ""}},
            )
            == []
        )
        assert (
            mi.inspect_entity(
                "test",
                "test_id",
                {"ref": True, "patterns": {"label": "test", "ref": "test_id"}},
            )
            == []
        )
        assert (
            mi.inspect_entity(
                "Änderung",
                "test_id",
                {
                    "ref": True,
                    "patterns": {"label": rf"^[a-zA-ZäöüÄÖÜß0-9'-]+$", "ref": ""},
                },
            )
            == []
        )
        assert (
            mi.inspect_entity(
                "test",
                "https://www.test.de/",
                {"ref": True, "patterns": {"label": "", "ref": rf"^https:\/\/.+$"}},
            )
            == []
        )
        assert mi.error.pattern("tst") in (
            mi.inspect_entity(
                "tst",
                "test_id",
                {"ref": True, "patterns": {"label": "test", "ref": "test_id"}},
            )
        )
        assert mi.error.pattern("test_ident") in (
            mi.inspect_entity(
                "tst",
                "test_ident",
                {"ref": True, "patterns": {"label": "test", "ref": "test_id"}},
            )
        )
        assert mi.error.pattern("test test") in (
            mi.inspect_entity(
                "test test",
                "test_id",
                {
                    "ref": True,
                    "patterns": {"label": rf"^[a-zA-ZäöüÄÖÜß0-9'-]+$", "ref": ""},
                },
            )
        )
        assert mi.error.pattern("www.test.de/") in (
            mi.inspect_entity(
                "test",
                "www.test.de/",
                {"ref": True, "patterns": {"label": "", "ref": rf"^https:\/\/.+$"}},
            )
        )

    def test_date_object(self):
        mi = MetadataInspector()
        assert mi.date_object("2000-01-01") != None
        assert mi.date_object("2000:01:01") == None
        assert mi.date_object("2000-01-00") == None
        assert mi.date_object("2000-02-30") == None
        assert mi.date_object("2004-02-29") != None
        assert mi.date_object("2000-01-01/2000-12-31") == None

    def test_date_range(self):
        mi = MetadataInspector()
        assert mi.date_range("2015-01-01/2015-03-31") == {
            "earliest_date": date(2015, 1, 1),
            "latest_date": date(2015, 3, 31),
        }
        assert mi.date_range("2015-01-01/2015-03-31") != {
            "earliest_date": date(2015, 1, 1),
            "latest_date": date(2015, 3, 30),
        }
        assert mi.date_range("2015-01-01") == {
            "earliest_date": date(2015, 1, 1),
            "latest_date": date(2015, 1, 1),
        }
        assert mi.date_range("1.1.2015") == {
            "earliest_date": None,
            "latest_date": None,
        }
        assert mi.date_range("1.1.2015-31.3.2015") == {
            "earliest_date": None,
            "latest_date": None,
        }

    def test_create_element(self):
        mi = MetadataInspector()
        assert mi.create_element("elem", "text").tag == "elem"
        assert mi.create_element("elem", "text").text == "text"
        assert mi.create_element("elem", "").text == ""
        assert mi.create_element(text="text").text == "text"
        assert mi.create_element(text="text").tag == "element"
        assert mi.create_element("elem").text == ""


if __name__ == "__main__":
    pytest.main()
