import pytest
from lxml import etree
from nfdinspector.lido_inspector import LIDOInspector


def xml(xml_string):
    return etree.fromstring(xml_string)


class Test_LIDOInspector:

    def test_configure(self):
        li = LIDOInspector()
        default_config = li.configuration.copy()
        li.configure(
            {
                "title": {
                    "inspect": True,
                    "unique": False,
                    "distinct_from_type": True,
                    "min_word_num": 3,
                    "max_word_num": "5",
                },
                "object_description": {"distinct_from_type": True},
                "category": {"ref": True, "min_num": 2},
                "subject_concept": {"inspect": True, "min_num": 5.0},
                "record_info": {"inspect": 0},
                "unknown": {"inspect": True},
            }
        )
        assert li.configuration["title"] == {
            "inspect": True,
            "unique": False,
            "distinct_from_type": True,
            "min_word_num": 3,
            "max_word_num": 5,
        }
        assert li.configuration["category"] == {
            "inspect": True,
            "ref": True,
            "patterns": {"label": "", "ref": ""},
        }
        assert li.configuration["subject_concept"] == {
            "inspect": True,
            "ref": True,
            "min_num": 5,
        }
        assert li.configuration["record_info"] == {"inspect": False}
        assert "unknown" not in li.configuration
        assert (
            li.configuration["object_work_type"] == default_config["object_work_type"]
        )
        assert (
            li.configuration["object_description"]
            == default_config["object_description"]
        )

    def test_configure_setting(self):
        li = LIDOInspector()
        default_config = li.configuration.copy()
        li.configure_setting(
            "title", {"inspect": True, "unique": False, "min_word_num": "2"}
        )
        assert li.configuration["title"] == {
            "inspect": True,
            "unique": False,
            "distinct_from_type": default_config["title"]["distinct_from_type"],
            "min_word_num": 2,
            "max_word_num": default_config["title"]["max_word_num"],
        }
        li.configure_setting("category", {"ref": 0, "min_num": 2})
        assert li.configuration["category"] == {
            "inspect": default_config["category"]["inspect"],
            "ref": False,
            "patterns": {"label": "", "ref": ""},
        }
        li.configure_setting("classification", {})
        assert li.configuration["classification"] == default_config["classification"]

    def test_find_duplicates(self):
        li = LIDOInspector()
        wrap = [
            "<lido><descriptiveMetadata><objectIdentificationWrap>",
            "</objectIdentificationWrap></descriptiveMetadata></lido>",
        ]
        li.lido_objects = [
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue>test test</appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue>test</appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue></appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue>Duplicate</appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue>Duplicate</appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue>test test test</appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue>Duplicate2</appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue>test test test test</appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue>Duplicate2</appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue></appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue>Duplicate2</appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
        ]
        assert "Duplicate" in li.find_duplicates(
            "{*}descriptiveMetadata/{*}objectIdentificationWrap/{*}titleWrap/{*}titleSet/{*}appellationValue"
        )
        assert "Duplicate2" in li.find_duplicates(
            "{*}descriptiveMetadata/{*}objectIdentificationWrap/{*}titleWrap/{*}titleSet/{*}appellationValue"
        )
        assert "" not in li.find_duplicates(
            "{*}descriptiveMetadata/{*}objectIdentificationWrap/{*}titleWrap/{*}titleSet/{*}appellationValue"
        )
        assert "test test" not in li.find_duplicates(
            "{*}descriptiveMetadata/{*}objectIdentificationWrap/{*}titleWrap/{*}titleSet/{*}appellationValue"
        )
        assert "test test test test" not in li.find_duplicates(
            "{*}descriptiveMetadata/{*}objectIdentificationWrap/{*}titleWrap/{*}titleSet/{*}appellationValue"
        )

    def test_find_duplicate_titles(self):
        li = LIDOInspector()
        wrap = [
            "<lido><descriptiveMetadata><objectIdentificationWrap>",
            "</objectIdentificationWrap></descriptiveMetadata></lido>",
        ]
        li.lido_objects = [
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue>test test</appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue>test</appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue></appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue>Duplicate</appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue>Duplicate</appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue>test test test</appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue>Duplicate2</appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue>test test test test</appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue>Duplicate2</appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue></appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<titleWrap><titleSet><appellationValue>Duplicate2</appellationValue></titleSet></titleWrap>{wrap[1]}"
            ),
        ]
        assert "Duplicate" in li.find_duplicate_titles()
        assert "Duplicate2" in li.find_duplicate_titles()
        assert "" not in li.find_duplicate_titles()
        assert "test test" not in li.find_duplicate_titles()
        assert "test test test test" not in li.find_duplicate_titles()

    def test_find_duplicate_descriptions(self):
        li = LIDOInspector()
        wrap = [
            "<lido><descriptiveMetadata><objectIdentificationWrap>",
            "</objectIdentificationWrap></descriptiveMetadata></lido>",
        ]
        li.lido_objects = [
            xml(
                f"{wrap[0]}<objectDescriptionWrap><objectDescriptionSet><descriptiveNoteValue>test test</descriptiveNoteValue></objectDescriptionSet></objectDescriptionWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<objectDescriptionWrap><objectDescriptionSet><descriptiveNoteValue>test</descriptiveNoteValue></objectDescriptionSet></objectDescriptionWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<objectDescriptionWrap><objectDescriptionSet><descriptiveNoteValue></descriptiveNoteValue></objectDescriptionSet></objectDescriptionWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<objectDescriptionWrap><objectDescriptionSet><descriptiveNoteValue>Duplicate</descriptiveNoteValue></objectDescriptionSet></objectDescriptionWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<objectDescriptionWrap><objectDescriptionSet><descriptiveNoteValue>Duplicate</descriptiveNoteValue></objectDescriptionSet></objectDescriptionWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<objectDescriptionWrap><objectDescriptionSet><descriptiveNoteValue>test test test</descriptiveNoteValue></objectDescriptionSet></objectDescriptionWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<objectDescriptionWrap><objectDescriptionSet><descriptiveNoteValue>Duplicate2</descriptiveNoteValue></objectDescriptionSet></objectDescriptionWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<objectDescriptionWrap><objectDescriptionSet><descriptiveNoteValue>test test test test</descriptiveNoteValue></objectDescriptionSet></objectDescriptionWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<objectDescriptionWrap><objectDescriptionSet><descriptiveNoteValue>Duplicate2</descriptiveNoteValue></objectDescriptionSet></objectDescriptionWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<objectDescriptionWrap><objectDescriptionSet><descriptiveNoteValue></descriptiveNoteValue></objectDescriptionSet></objectDescriptionWrap>{wrap[1]}"
            ),
            xml(
                f"{wrap[0]}<objectDescriptionWrap><objectDescriptionSet><descriptiveNoteValue>Duplicate2</descriptiveNoteValue></objectDescriptionSet></objectDescriptionWrap>{wrap[1]}"
            ),
        ]
        assert "Duplicate" in li.find_duplicate_descriptions()
        assert "Duplicate2" in li.find_duplicate_descriptions()
        assert "" not in li.find_duplicate_descriptions()
        assert "test test" not in li.find_duplicate_descriptions()
        assert "test test test test" not in li.find_duplicate_descriptions()

    def test_inspect_lido_rec_id(self):
        li = LIDOInspector()
        assert (
            li.inspect_lido_rec_id(xml("<lido><lidoRecID>test</lidoRecID></lido>"))
            == "test"
        )
        assert (
            li.inspect_lido_rec_id(xml("<lido><lidoRecID></lidoRecID></lido>"))
            == li.error.miss_info()
        )
        assert (
            li.inspect_lido_rec_id(xml("<lido><lidoRecID/></lido>"))
            == li.error.miss_info()
        )
        assert li.inspect_lido_rec_id(xml("<lido></lido>")) == li.error.miss_info()

    def test_inspect_work_id(self):
        li = LIDOInspector()
        wrap = [
            "<lido><descriptiveMetadata><objectIdentificationWrap><repositoryWrap><repositorySet>",
            "</repositorySet></repositoryWrap></objectIdentificationWrap></descriptiveMetadata></lido>",
        ]
        assert (
            li.inspect_work_id(xml(f"{wrap[0]}<workID>test</workID>{wrap[1]}"))
            == "test"
        )
        assert (
            li.inspect_work_id(xml(f"{wrap[0]}<workID></workID>{wrap[1]}"))
            == li.error.miss_info()
        )
        assert (
            li.inspect_work_id(xml(f"{wrap[0]}<workID/>{wrap[1]}"))
            == li.error.miss_info()
        )
        assert li.inspect_work_id(xml(f"{wrap[0]}{wrap[1]}")) == li.error.miss_info()
        li.configuration["work_id"]["pattern"] = r"^\d{12}$"
        assert (
            li.inspect_work_id(xml(f"{wrap[0]}<workID>123456789000</workID>{wrap[1]}"))
            == "123456789000"
        )
        assert li.inspect_work_id(
            xml(f"{wrap[0]}<workID>123456789</workID>{wrap[1]}")
        ) == li.error.pattern("123456789")
        assert li.inspect_work_id(
            xml(f"{wrap[0]}<workID>123456789000000</workID>{wrap[1]}")
        ) == li.error.pattern("123456789000000")
        assert li.inspect_work_id(
            xml(f"{wrap[0]}<workID>12A456789000</workID>{wrap[1]}")
        ) == li.error.pattern("12A456789000")

    def test_is_distinct_from_type(self):
        li = LIDOInspector()
        wrap = [
            "<lido><descriptiveMetadata><objectClassificationWrap><objectWorkTypeWrap>",
            "</objectWorkTypeWrap></objectClassificationWrap></descriptiveMetadata></lido>",
        ]
        assert (
            li.is_distinct_from_type(
                xml(
                    f"{wrap[0]}<objectWorkType><term>test</term></objectWorkType>{wrap[1]}"
                ),
                "test",
            )
            == False
        )
        assert (
            li.is_distinct_from_type(
                xml(
                    f"{wrap[0]}<objectWorkType><Concept><prefLabel>test</prefLabel></Concept></objectWorkType>{wrap[1]}"
                ),
                "test",
            )
            == False
        )
        assert (
            li.is_distinct_from_type(
                xml(
                    f"{wrap[0]}<objectWorkType><term>other</term></objectWorkType>{wrap[1]}"
                ),
                "test",
            )
            == True
        )
        assert (
            li.is_distinct_from_type(
                xml(
                    f"{wrap[0]}<objectWorkType><Concept><prefLabel>other</prefLabel></Concept></objectWorkType>{wrap[1]}"
                ),
                "test",
            )
            == True
        )
        assert (
            li.is_distinct_from_type(
                xml(
                    f"{wrap[0]}<objectWorkType><term></term></objectWorkType>{wrap[1]}"
                ),
                "test",
            )
            == True
        )
        assert (
            li.is_distinct_from_type(
                xml(f"{wrap[0]}{wrap[1]}"),
                "test",
            )
            == True
        )

    def test_inspect_title(self):
        li = LIDOInspector()
        li.configuration["title"] = {
            "inspect": True,
            "unique": True,
            "distinct_from_type": True,
            "min_word_num": 2,
            "max_word_num": 3,
        }
        li.duplicate_titles = ["Duplicate"]
        object_work_type = "<objectClassificationWrap><objectWorkTypeWrap><objectWorkType><term>Type</term></objectWorkType></objectWorkTypeWrap></objectClassificationWrap>"
        wrap = [
            "<lido><descriptiveMetadata><objectIdentificationWrap><titleWrap>",
            f"</titleWrap></objectIdentificationWrap>{object_work_type}</descriptiveMetadata></lido>",
        ]
        assert (
            li.inspect_title(
                xml(
                    f"{wrap[0]}<titleSet><appellationValue>test test</appellationValue></titleSet>{wrap[1]}"
                )
            )
            == None
        )
        assert (
            li.inspect_title(
                xml(
                    f"{wrap[0]}<titleSet><appellationValue>test test test</appellationValue></titleSet>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.miss_info() in (
            li.inspect_title(
                xml(
                    f"{wrap[0]}<titleSet><appellationValue></appellationValue></titleSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_info() in (
            li.inspect_title(
                xml(f"{wrap[0]}<titleSet><appellationValue/></titleSet>{wrap[1]}")
            )
        )
        assert li.error.miss_info() in (
            li.inspect_title(xml(f"{wrap[0]}<titleSet></titleSet>{wrap[1]}"))
        )
        assert li.error.miss_info() in (
            li.inspect_title(xml(f"{wrap[0]}<titleSet/>{wrap[1]}"))
        )
        assert li.error.miss_info() in (li.inspect_title(xml(f"{wrap[0]}{wrap[1]}")))
        assert li.error.dupl_blanks() in (
            li.inspect_title(
                xml(
                    f"{wrap[0]}<titleSet><appellationValue>test  test</appellationValue></titleSet>{wrap[1]}"
                )
            )
        )
        assert li.error.dupl_blanks() in (
            li.inspect_title(
                xml(
                    f"{wrap[0]}<titleSet><appellationValue>  test test</appellationValue></titleSet>{wrap[1]}"
                )
            )
        )
        assert li.error.not_uniq() in (
            li.inspect_title(
                xml(
                    f"{wrap[0]}<titleSet><appellationValue>Duplicate</appellationValue></titleSet>{wrap[1]}"
                )
            )
        )
        assert li.error.dist("objectWorkType") in (
            li.inspect_title(
                xml(
                    f"{wrap[0]}<titleSet><appellationValue>Type</appellationValue></titleSet>{wrap[1]}"
                )
            )
        )
        assert li.error.short() in (
            li.inspect_title(
                xml(
                    f"{wrap[0]}<titleSet><appellationValue>test</appellationValue></titleSet>{wrap[1]}"
                )
            )
        )
        assert li.error.short() in (
            li.inspect_title(
                xml(
                    f"{wrap[0]}<titleSet><appellationValue>test  </appellationValue></titleSet>{wrap[1]}"
                )
            )
        )
        assert li.error.long() in (
            li.inspect_title(
                xml(
                    f"{wrap[0]}<titleSet><appellationValue>test test test test</appellationValue></titleSet>{wrap[1]}"
                )
            )
        )

    def test_value(self):
        li = LIDOInspector()
        assert (
            li.value(xml("<elem><appellationValue>test</appellationValue></elem>"))
            == "test"
        )
        assert (
            li.value(
                xml(
                    "<elem><legalBodyName><appellationValue>test</appellationValue></legalBodyName></elem>"
                )
            )
            == "test"
        )
        assert (
            li.value(
                xml("<elem><descriptiveNoteValue>test</descriptiveNoteValue></elem>")
            )
            == "test"
        )
        assert li.value(xml("<elem><appellationValue></appellationValue></elem>")) == ""
        assert (
            li.value(
                xml("<elem><legalBodyName><appellationValue/></legalBodyName></elem>")
            )
            == ""
        )
        assert li.value(xml("<elem><legalBodyName></legalBodyName></elem>")) == ""
        assert li.value(xml("<elem><legalBodyName/></elem>")) == ""
        assert (
            li.value(xml("<elem><descriptiveNoteValue></descriptiveNoteValue></elem>"))
            == ""
        )
        assert li.value(xml("<elem><appellationValue/></elem>")) == ""
        assert li.value(xml("<elem><descriptiveNoteValue/></elem>")) == ""
        assert li.value(xml("<elem></elem>")) == ""

    def test_term(self):
        li = LIDOInspector()
        assert li.term(xml("<elem><term>test</term></elem>")) == "test"
        assert (
            li.term(xml("<elem><Concept><prefLabel>test</prefLabel></Concept></elem>"))
            == "test"
        )
        assert li.term(xml("<elem><term></term></elem>")) == ""
        assert (
            li.term(xml("<elem><Concept><prefLabel></prefLabel></Concept></elem>"))
            == ""
        )
        assert li.term(xml("<elem><term/></elem>")) == ""
        assert li.term(xml("<elem><Concept><prefLabel/></Concept></elem>")) == ""
        assert li.term(xml("<elem><Concept/></elem>")) == ""
        assert li.term(xml("<elem></elem>")) == ""

    def test_is_uniq(self):
        li = LIDOInspector()
        li.duplicate_titles = ["title"]
        li.duplicate_descriptions = ["description"]
        assert (
            li.is_uniq(
                "unique",
                xml("<titleSet/>"),
            )
            == True
        )
        assert (
            li.is_uniq(
                "unique",
                xml("<lido:titleSet xmlns:lido='http://www.lido-schema.org'/>"),
            )
            == True
        )
        assert (
            li.is_uniq(
                "title",
                xml("<titleSet/>"),
            )
            == False
        )
        assert (
            li.is_uniq(
                "title",
                xml("<lido:titleSet xmlns:lido='http://www.lido-schema.org'/>"),
            )
            == False
        )
        assert (
            li.is_uniq(
                "unique",
                xml("<objectDescriptionSet/>"),
            )
            == True
        )
        assert (
            li.is_uniq(
                "unique",
                xml(
                    "<lido:objectDescriptionSet xmlns:lido='http://www.lido-schema.org'/>"
                ),
            )
            == True
        )
        assert (
            li.is_uniq(
                "description",
                xml("<objectDescriptionSet/>"),
            )
            == False
        )
        assert (
            li.is_uniq(
                "description",
                xml(
                    "<lido:objectDescriptionSet xmlns:lido='http://www.lido-schema.org'/>"
                ),
            )
            == False
        )

    def test_inspect_text(self):
        li = LIDOInspector()
        li.duplicate_titles = ["not unique"]
        wrap = [
            "<lido><descriptiveMetadata><objectClassificationWrap><objectWorkTypeWrap>",
            "</objectWorkTypeWrap></objectClassificationWrap></descriptiveMetadata></lido>",
        ]
        assert (
            li.inspect_text(
                xml("<elem><appellationValue>test test</appellationValue></elem>"),
                xml(
                    f"{wrap[0]}<objectWorkType><term>test</term></objectWorkType>{wrap[1]}"
                ),
                {
                    "inspect": True,
                    "unique": True,
                    "distinct_from_type": True,
                    "min_word_num": 2,
                    "max_word_num": 3,
                },
            )
            == None
        )
        assert (
            li.inspect_text(
                xml(
                    "<elem><descriptiveNoteValue>test test test</descriptiveNoteValue></elem>"
                ),
                xml(
                    f"{wrap[0]}<objectWorkType><term>test</term></objectWorkType>{wrap[1]}"
                ),
                {
                    "inspect": True,
                    "unique": True,
                    "distinct_from_type": True,
                    "min_word_num": 2,
                    "max_word_num": 3,
                },
            )
            == None
        )
        assert li.error.miss_info() in (
            li.inspect_text(
                xml("<elem><appellationValue></appellationValue></elem>"),
                xml(
                    f"{wrap[0]}<objectWorkType><term>test</term></objectWorkType>{wrap[1]}"
                ),
                {
                    "inspect": True,
                    "unique": True,
                    "distinct_from_type": True,
                    "min_word_num": 2,
                    "max_word_num": 3,
                },
            )
        )
        assert li.error.miss_info() in (
            li.inspect_text(
                xml("<elem><descriptiveNoteValue/></elem>"),
                xml(
                    f"{wrap[0]}<objectWorkType><term>test</term></objectWorkType>{wrap[1]}"
                ),
                {
                    "inspect": True,
                    "unique": True,
                    "distinct_from_type": True,
                    "min_word_num": 2,
                    "max_word_num": 3,
                },
            )
        )
        assert li.error.miss_info() in (
            li.inspect_text(
                xml("<elem></elem>"),
                xml(
                    f"{wrap[0]}<objectWorkType><term>test</term></objectWorkType>{wrap[1]}"
                ),
                {
                    "inspect": True,
                    "unique": True,
                    "distinct_from_type": True,
                    "min_word_num": 2,
                    "max_word_num": 3,
                },
            )
        )
        assert li.error.dupl_blanks() in (
            li.inspect_text(
                xml("<elem><appellationValue>test  test</appellationValue></elem>"),
                xml(
                    f"{wrap[0]}<objectWorkType><term>test</term></objectWorkType>{wrap[1]}"
                ),
                {
                    "inspect": True,
                    "unique": True,
                    "distinct_from_type": True,
                    "min_word_num": 2,
                    "max_word_num": 3,
                },
            )
        )
        assert li.error.dupl_blanks() in (
            li.inspect_text(
                xml("<elem><appellationValue>test  </appellationValue></elem>"),
                xml(
                    f"{wrap[0]}<objectWorkType><term>test</term></objectWorkType>{wrap[1]}"
                ),
                {
                    "inspect": True,
                    "unique": True,
                    "distinct_from_type": True,
                    "min_word_num": 2,
                    "max_word_num": 3,
                },
            )
        )
        assert li.error.not_uniq() in (
            li.inspect_text(
                xml(
                    "<titleSet><appellationValue>not unique</appellationValue></titleSet>"
                ),
                xml(
                    f"{wrap[0]}<objectWorkType><term>test</term></objectWorkType>{wrap[1]}"
                ),
                {
                    "inspect": True,
                    "unique": True,
                    "distinct_from_type": True,
                    "min_word_num": 2,
                    "max_word_num": 3,
                },
            )
        )
        assert li.error.dist("objectWorkType") in (
            li.inspect_text(
                xml("<elem><appellationValue>test</appellationValue></elem>"),
                xml(
                    f"{wrap[0]}<objectWorkType><term>test</term></objectWorkType>{wrap[1]}"
                ),
                {
                    "inspect": True,
                    "unique": True,
                    "distinct_from_type": True,
                    "min_word_num": 2,
                    "max_word_num": 3,
                },
            )
        )
        assert li.error.short() in (
            li.inspect_text(
                xml("<elem><appellationValue>test</appellationValue></elem>"),
                xml(
                    f"{wrap[0]}<objectWorkType><term>test</term></objectWorkType>{wrap[1]}"
                ),
                {
                    "inspect": True,
                    "unique": True,
                    "distinct_from_type": True,
                    "min_word_num": 2,
                    "max_word_num": 3,
                },
            )
        )
        assert li.error.short() in (
            li.inspect_text(
                xml("<elem><appellationValue>test </appellationValue></elem>"),
                xml(
                    f"{wrap[0]}<objectWorkType><term>test</term></objectWorkType>{wrap[1]}"
                ),
                {
                    "inspect": True,
                    "unique": True,
                    "distinct_from_type": True,
                    "min_word_num": 2,
                    "max_word_num": 3,
                },
            )
        )
        assert li.error.long() in (
            li.inspect_text(
                xml("<elem><appellationValue>test test test</appellationValue></elem>"),
                xml(
                    f"{wrap[0]}<objectWorkType><term>test</term></objectWorkType>{wrap[1]}"
                ),
                {
                    "inspect": True,
                    "unique": True,
                    "distinct_from_type": True,
                    "min_word_num": 2,
                    "max_word_num": 2,
                },
            )
        )

    def test_about(self):
        li = LIDOInspector()
        assert (
            li.about(
                xml(
                    "<elem xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' rdf:about='test'></elem>"
                )
            )
            == "test"
        )
        assert (
            li.about(
                xml(
                    "<elem xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' rdf:about='test'/>"
                )
            )
            == "test"
        )
        assert (
            li.about(
                xml(
                    "<elem xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' rdf:about=''></elem>"
                )
            )
            == ""
        )
        assert (
            li.about(
                xml(
                    "<elem xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'></elem>"
                )
            )
            == ""
        )

    def test_concept_id(self):
        li = LIDOInspector()
        assert li.concept_id(xml("<lido><conceptID>test</conceptID></lido>")) == "test"
        assert li.concept_id(xml("<lido><conceptID></conceptID></lido>")) == ""
        assert li.concept_id(xml("<lido><conceptID/></lido>")) == ""
        assert li.concept_id(xml("<lido></lido>")) == ""
        assert (
            li.concept_id(
                xml(
                    "<lido><Concept xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' rdf:about='test'/></lido>"
                )
            )
            == "test"
        )
        assert (
            li.concept_id(
                xml(
                    "<lido><Concept xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' rdf:about=''/></lido>"
                )
            )
            == ""
        )
        assert (
            li.concept_id(
                xml(
                    "<lido><Concept xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'/></lido>"
                )
            )
            == ""
        )

    def test_inspect_concept(self):
        li = LIDOInspector()
        assert (
            li.inspect_concept(
                xml("<elem><conceptID>1</conceptID><term>test</term></elem>"),
                {"ref": True},
            )
            == []
        )
        assert (
            li.inspect_concept(
                xml("<elem><term>test</term></elem>"),
                {"ref": False},
            )
            == []
        )
        assert (
            li.inspect_concept(
                xml(
                    "<elem><Concept xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' rdf:about='1'><prefLabel>test</prefLabel></Concept></elem>"
                ),
                {"ref": True},
            )
            == []
        )
        assert li.error.miss_info() in (
            li.inspect_concept(
                xml("<elem></elem>"),
                {"ref": True},
            )
        )
        assert li.error.miss_info() in (
            li.inspect_concept(
                xml("<elem/>"),
                {"ref": True},
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_concept(
                xml("<elem><conceptID>1</conceptID></elem>"),
                {"ref": True},
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_concept(
                xml(
                    "<elem><Concept xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' rdf:about='1'/></elem>"
                ),
                {"ref": True},
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_concept(
                xml("<elem><term>test</term></elem>"),
                {"ref": True},
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_concept(
                xml(
                    "<elem><Concept xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' rdf:about=''><prefLabel>test</prefLabel></Concept></elem>"
                ),
                {"ref": True},
            )
        )
        assert (
            li.inspect_concept(
                xml("<elem><conceptID>1</conceptID><term>test</term></elem>"),
                {"ref": True, "patterns": {"label": "test", "ref": "1"}},
            )
        ) == []
        assert (
            li.inspect_concept(
                xml(
                    "<elem><conceptID>https://www.test.de/</conceptID><term>test</term></elem>"
                ),
                {
                    "ref": True,
                    "patterns": {
                        "label": rf"^[a-zA-ZäöüÄÖÜß0-9'-]+$",
                        "ref": rf"^https:\/\/.+$",
                    },
                },
            )
        ) == []
        assert li.error.pattern("tst") in (
            li.inspect_concept(
                xml("<elem><conceptID>1</conceptID><term>tst</term></elem>"),
                {"ref": True, "patterns": {"label": "test", "ref": "1"}},
            )
        )
        assert li.error.pattern("2") in (
            li.inspect_concept(
                xml("<elem><conceptID>2</conceptID><term>tst</term></elem>"),
                {"ref": True, "patterns": {"label": "test", "ref": "1"}},
            )
        )
        assert li.error.pattern("1") in (
            li.inspect_concept(
                xml(
                    "<elem><Concept xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' rdf:about='1'><prefLabel>test</prefLabel></Concept></elem>"
                ),
                {
                    "ref": True,
                    "patterns": {
                        "label": rf"^[a-zA-ZäöüÄÖÜß0-9'-]+$",
                        "ref": rf"^https:\/\/.+$",
                    },
                },
            )
        )

    def test_inspect_concepts(self):
        li = LIDOInspector()
        assert (
            li.inspect_concepts(
                [
                    xml("<elem><conceptID>1</conceptID><term>test</term></elem>"),
                    xml("<elem><conceptID>2</conceptID><term>test</term></elem>"),
                ],
                {"ref": True, "min_num": 2},
            )
            == None
        )
        assert (
            li.inspect_concepts(
                [
                    xml("<elem><conceptID>1</conceptID><term>test</term></elem>"),
                    xml(
                        "<elem><Concept xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' rdf:about='2'><prefLabel>test</prefLabel></Concept></elem>"
                    ),
                ],
                {"ref": True, "min_num": 2},
            )
            == None
        )
        assert (
            li.inspect_concepts(
                [
                    xml("<elem><term>test</term></elem>"),
                ],
                {"ref": False, "min_num": 1},
            )
            == None
        )
        assert li.error.miss_info() in (
            li.inspect_concepts(
                [xml("<elem></elem>")],
                {"ref": True, "min_num": 2},
            )
        )
        assert li.error.miss_info() in (
            li.inspect_concepts(
                [xml("<elem/>")],
                {"ref": True, "min_num": 2},
            )
        )
        assert li.error.miss_info() in (
            li.inspect_concepts(
                [],
                {"ref": True, "min_num": 2},
            )
        )
        assert li.error.miss_label("2") in (
            li.inspect_concepts(
                [
                    xml("<elem><conceptID>1</conceptID><term>test</term></elem>"),
                    xml(
                        "<elem><Concept xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' rdf:about='2'/></elem>"
                    ),
                ],
                {"ref": True, "min_num": 2},
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_concepts(
                [
                    xml("<elem><conceptID>1</conceptID></elem>"),
                    xml(
                        "<elem><Concept xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' rdf:about='2'/></elem>"
                    ),
                ],
                {"ref": True, "min_num": 2},
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_concepts(
                [
                    xml("<elem><term>test</term></elem>"),
                    xml(
                        "<elem><Concept xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' rdf:about='2'/></elem>"
                    ),
                ],
                {"ref": True, "min_num": 2},
            )
        )
        assert li.error.miss_ref("") in (
            li.inspect_concepts(
                [
                    xml("<elem><conceptID>1</conceptID></elem>"),
                    xml(
                        "<elem><Concept xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' rdf:about=''/></elem>"
                    ),
                ],
                {"ref": True, "min_num": 2},
            )
        )
        assert li.error.few() in (
            li.inspect_concepts(
                [xml("<elem><term>test</term></elem>")],
                {"ref": True, "min_num": 2},
            )
        )
        assert (
            li.inspect_concepts(
                [
                    xml("<elem><conceptID>1</conceptID><term>test</term></elem>"),
                    xml("<elem><conceptID>2</conceptID><term>test</term></elem>"),
                ],
                {
                    "ref": True,
                    "min_num": 2,
                    "patterns": {"label": "test", "ref": rf"^[12]$"},
                },
            )
            == None
        )
        assert (
            li.inspect_concepts(
                [
                    xml("<elem><conceptID>1</conceptID><term>test</term></elem>"),
                    xml("<elem><conceptID>2</conceptID><term>alt</term></elem>"),
                ],
                {
                    "ref": True,
                    "min_num": 2,
                    "patterns": {"label": "^(test|alt)$", "ref": ""},
                },
            )
            == None
        )
        assert li.error.pattern("3") in (
            li.inspect_concepts(
                [
                    xml("<elem><conceptID>1</conceptID><term>test</term></elem>"),
                    xml("<elem><conceptID>3</conceptID><term>test</term></elem>"),
                ],
                {
                    "ref": True,
                    "min_num": 2,
                    "patterns": {"label": "test", "ref": rf"^[12]$"},
                },
            )
        )
        assert li.error.pattern("test test") in (
            li.inspect_concepts(
                [
                    xml("<elem><conceptID>1</conceptID><term>test</term></elem>"),
                    xml("<elem><conceptID>2</conceptID><term>test test</term></elem>"),
                ],
                {
                    "ref": True,
                    "min_num": 2,
                    "patterns": {"label": "^(test|alt)$", "ref": rf"^[12]$"},
                },
            )
        )

    def test_inspect_category(self):
        li = LIDOInspector()
        li.configuration["category"] = {
            "inspect": True,
            "ref": True,
            "patterns": {"label": "", "ref": ""},
        }
        wrap = [
            "<lido xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>",
            "</lido>",
        ]
        assert (
            li.inspect_category(
                xml(
                    f"{wrap[0]}<category><conceptID>1</conceptID><term>test</term></category>{wrap[1]}"
                )
            )
            == None
        )
        assert (
            li.inspect_category(
                xml(
                    f"{wrap[0]}<category><Concept rdf:about='2'><prefLabel>test</prefLabel></Concept></category>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.miss_info() in (
            li.inspect_category(xml(f"{wrap[0]}<category></category>{wrap[1]}"))
        )
        assert li.error.miss_info() in (
            li.inspect_category(xml(f"{wrap[0]}<category/>{wrap[1]}"))
        )
        assert li.error.miss_info() in (li.inspect_category(xml(f"{wrap[0]}{wrap[1]}")))
        assert li.error.miss_label("1") in (
            li.inspect_category(
                xml(
                    f"{wrap[0]}<category><conceptID>1</conceptID><term/></category>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_category(
                xml(f"{wrap[0]}<category><conceptID>1</conceptID></category>{wrap[1]}")
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_category(
                xml(f"{wrap[0]}<category><Concept rdf:about='1'/></category>{wrap[1]}")
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_category(
                xml(
                    f"{wrap[0]}<category><conceptID/><term>test</term></category>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_category(
                xml(f"{wrap[0]}<category><term>test</term></category>{wrap[1]}")
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_category(
                xml(
                    f"{wrap[0]}<category><Concept rdf:about=''><prefLabel>test</prefLabel></Concept></category>{wrap[1]}"
                )
            )
        )
        li.configuration["category"]["patterns"] = {"label": "test", "ref": "1"}
        assert (
            li.inspect_category(
                xml(
                    f"{wrap[0]}<category><conceptID>1</conceptID><term>test</term></category>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.pattern("2") in (
            li.inspect_category(
                xml(
                    f"{wrap[0]}<category><conceptID>2</conceptID><term>test</term></category>{wrap[1]}"
                )
            )
        )
        assert li.error.pattern("tst") in (
            li.inspect_category(
                xml(
                    f"{wrap[0]}<category><conceptID>2</conceptID><term>tst</term></category>{wrap[1]}"
                )
            )
        )
        li.configuration["category"]["patterns"] = {
            "label": rf"^[a-zA-ZäöüÄÖÜß0-9'-]+$",
            "ref": rf"^https:\/\/.+$",
        }
        assert (
            li.inspect_category(
                xml(
                    f"{wrap[0]}<category><conceptID>https://www.test.com/</conceptID><term>test</term></category>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.pattern("2") in (
            li.inspect_category(
                xml(
                    f"{wrap[0]}<category><conceptID>2</conceptID><term>test</term></category>{wrap[1]}"
                )
            )
        )
        assert li.error.pattern("test test") in (
            li.inspect_category(
                xml(
                    f"{wrap[0]}<category><conceptID>2</conceptID><term>test test</term></category>{wrap[1]}"
                )
            )
        )

    def test_inspect_object_work_types(self):
        li = LIDOInspector()
        li.configuration["object_work_type"] = {"inspect": True, "ref": True}
        wrap = [
            "<lido xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'><descriptiveMetadata><objectClassificationWrap><objectWorkTypeWrap>",
            "</objectWorkTypeWrap></objectClassificationWrap></descriptiveMetadata></lido>",
        ]
        assert (
            li.inspect_object_work_types(
                xml(
                    f"{wrap[0]}<objectWorkType><conceptID>1</conceptID><term>test</term></objectWorkType>{wrap[1]}"
                )
            )
            == None
        )
        assert (
            li.inspect_object_work_types(
                xml(
                    f"{wrap[0]}<objectWorkType><Concept rdf:about='2'><prefLabel>test</prefLabel></Concept></objectWorkType>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.miss_info() in (
            li.inspect_object_work_types(
                xml(f"{wrap[0]}<objectWorkType></objectWorkType>{wrap[1]}")
            )
        )
        assert li.error.miss_info() in (
            li.inspect_object_work_types(xml(f"{wrap[0]}<objectWorkType/>{wrap[1]}"))
        )
        assert li.error.miss_info() in (
            li.inspect_object_work_types(xml(f"{wrap[0]}{wrap[1]}"))
        )
        assert li.error.miss_label("1") in (
            li.inspect_object_work_types(
                xml(
                    f"{wrap[0]}<objectWorkType><conceptID>1</conceptID><term/></objectWorkType>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_object_work_types(
                xml(
                    f"{wrap[0]}<objectWorkType><conceptID>1</conceptID></objectWorkType>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_object_work_types(
                xml(
                    f"{wrap[0]}<objectWorkType><Concept rdf:about='1'/></objectWorkType>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_object_work_types(
                xml(
                    f"{wrap[0]}<objectWorkType><conceptID/><term>test</term></objectWorkType>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_object_work_types(
                xml(
                    f"{wrap[0]}<objectWorkType><term>test</term></objectWorkType>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_object_work_types(
                xml(
                    f"{wrap[0]}<objectWorkType><Concept rdf:about=''><prefLabel>test</prefLabel></Concept></objectWorkType>{wrap[1]}"
                )
            )
        )
        li.configuration["object_work_type"]["patterns"] = {"label": "test", "ref": "1"}
        assert (
            li.inspect_object_work_types(
                xml(
                    f"{wrap[0]}<objectWorkType><conceptID>1</conceptID><term>test</term></objectWorkType>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.pattern("2") in (
            li.inspect_object_work_types(
                xml(
                    f"{wrap[0]}<objectWorkType><conceptID>2</conceptID><term>test</term></objectWorkType>{wrap[1]}"
                )
            )
        )
        assert li.error.pattern("tst") in (
            li.inspect_object_work_types(
                xml(
                    f"{wrap[0]}<objectWorkType><conceptID>2</conceptID><term>tst</term></objectWorkType>{wrap[1]}"
                )
            )
        )
        li.configuration["object_work_type"]["patterns"] = {
            "label": rf"^[a-zA-ZäöüÄÖÜß0-9'-]+$",
            "ref": rf"^https:\/\/.+$",
        }
        assert (
            li.inspect_object_work_types(
                xml(
                    f"{wrap[0]}<objectWorkType><conceptID>https://www.test.com/</conceptID><term>test</term></objectWorkType>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.pattern("2") in (
            li.inspect_object_work_types(
                xml(
                    f"{wrap[0]}<objectWorkType><conceptID>2</conceptID><term>test</term></objectWorkType>{wrap[1]}"
                )
            )
        )
        assert li.error.pattern("test test") in (
            li.inspect_object_work_types(
                xml(
                    f"{wrap[0]}<objectWorkType><conceptID>2</conceptID><term>test test</term></objectWorkType>{wrap[1]}"
                )
            )
        )

    def test_inspect_classifications(self):
        li = LIDOInspector()
        li.configuration["classification"] = {"inspect": True, "ref": True}
        wrap = [
            "<lido xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'><descriptiveMetadata><objectClassificationWrap><classificationWrap>",
            "</classificationWrap></objectClassificationWrap></descriptiveMetadata></lido>",
        ]
        assert (
            li.inspect_classifications(
                xml(
                    f"{wrap[0]}<classification><conceptID>1</conceptID><term>test</term></classification>{wrap[1]}"
                )
            )
            == None
        )
        assert (
            li.inspect_classifications(
                xml(
                    f"{wrap[0]}<classification><Concept rdf:about='2'><prefLabel>test</prefLabel></Concept></classification>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.miss_info() in (
            li.inspect_classifications(
                xml(f"{wrap[0]}<classification></classification>{wrap[1]}")
            )
        )
        assert li.error.miss_info() in (
            li.inspect_classifications(xml(f"{wrap[0]}<classification/>{wrap[1]}"))
        )
        assert li.error.miss_info() in (
            li.inspect_classifications(xml(f"{wrap[0]}{wrap[1]}"))
        )
        assert li.error.miss_label("1") in (
            li.inspect_classifications(
                xml(
                    f"{wrap[0]}<classification><conceptID>1</conceptID><term/></classification>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_classifications(
                xml(
                    f"{wrap[0]}<classification><conceptID>1</conceptID></classification>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_classifications(
                xml(
                    f"{wrap[0]}<classification><Concept rdf:about='1'/></classification>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_classifications(
                xml(
                    f"{wrap[0]}<classification><conceptID/><term>test</term></classification>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_classifications(
                xml(
                    f"{wrap[0]}<classification><term>test</term></classification>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_classifications(
                xml(
                    f"{wrap[0]}<classification><Concept rdf:about=''><prefLabel>test</prefLabel></Concept></classification>{wrap[1]}"
                )
            )
        )
        li.configuration["classification"]["patterns"] = {"label": "test", "ref": "1"}
        assert (
            li.inspect_classifications(
                xml(
                    f"{wrap[0]}<classification><conceptID>1</conceptID><term>test</term></classification>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.pattern("2") in (
            li.inspect_classifications(
                xml(
                    f"{wrap[0]}<classification><conceptID>2</conceptID><term>test</term></classification>{wrap[1]}"
                )
            )
        )
        assert li.error.pattern("tst") in (
            li.inspect_classifications(
                xml(
                    f"{wrap[0]}<classification><conceptID>2</conceptID><term>tst</term></classification>{wrap[1]}"
                )
            )
        )
        li.configuration["classification"]["patterns"] = {
            "label": rf"^[a-zA-ZäöüÄÖÜß0-9'-]+$",
            "ref": rf"^https:\/\/.+$",
        }
        assert (
            li.inspect_classifications(
                xml(
                    f"{wrap[0]}<classification><conceptID>https://www.test.com/</conceptID><term>test</term></classification>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.pattern("2") in (
            li.inspect_classifications(
                xml(
                    f"{wrap[0]}<classification><conceptID>2</conceptID><term>test</term></classification>{wrap[1]}"
                )
            )
        )
        assert li.error.pattern("test test") in (
            li.inspect_classifications(
                xml(
                    f"{wrap[0]}<classification><conceptID>2</conceptID><term>test test</term></classification>{wrap[1]}"
                )
            )
        )

    def test_inspect_object_description(self):
        li = LIDOInspector()
        li.configuration["object_description"] = {
            "inspect": True,
            "unique": True,
            "min_word_num": 2,
            "max_word_num": 3,
        }
        li.duplicate_descriptions = ["Duplicate"]
        wrap = [
            "<lido><descriptiveMetadata><objectIdentificationWrap><objectDescriptionWrap>",
            "</objectDescriptionWrap></objectIdentificationWrap></descriptiveMetadata></lido>",
        ]
        assert (
            li.inspect_object_description(
                xml(
                    f"{wrap[0]}<objectDescriptionSet><descriptiveNoteValue>test test</descriptiveNoteValue></objectDescriptionSet>{wrap[1]}"
                )
            )
            == None
        )
        assert (
            li.inspect_object_description(
                xml(
                    f"{wrap[0]}<objectDescriptionSet><descriptiveNoteValue>test test test</descriptiveNoteValue></objectDescriptionSet>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.miss_info() in (
            li.inspect_object_description(
                xml(
                    f"{wrap[0]}<objectDescriptionSet><descriptiveNoteValue></descriptiveNoteValue></objectDescriptionSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_info() in (
            li.inspect_object_description(
                xml(
                    f"{wrap[0]}<objectDescriptionSet><descriptiveNoteValue/></objectDescriptionSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_info() in (
            li.inspect_object_description(
                xml(f"{wrap[0]}<objectDescriptionSet></objectDescriptionSet>{wrap[1]}")
            )
        )
        assert li.error.miss_info() in (
            li.inspect_object_description(
                xml(f"{wrap[0]}<objectDescriptionSet/>{wrap[1]}")
            )
        )
        assert li.error.miss_info() in (
            li.inspect_object_description(xml(f"{wrap[0]}{wrap[1]}"))
        )
        assert li.error.dupl_blanks() in (
            li.inspect_object_description(
                xml(
                    f"{wrap[0]}<objectDescriptionSet><descriptiveNoteValue>test  test</descriptiveNoteValue></objectDescriptionSet>{wrap[1]}"
                )
            )
        )
        assert li.error.dupl_blanks() in (
            li.inspect_object_description(
                xml(
                    f"{wrap[0]}<objectDescriptionSet><descriptiveNoteValue>  test test</descriptiveNoteValue></objectDescriptionSet>{wrap[1]}"
                )
            )
        )
        assert li.error.not_uniq() in (
            li.inspect_object_description(
                xml(
                    f"{wrap[0]}<objectDescriptionSet><descriptiveNoteValue>Duplicate</descriptiveNoteValue></objectDescriptionSet>{wrap[1]}"
                )
            )
        )
        assert li.error.short() in (
            li.inspect_object_description(
                xml(
                    f"{wrap[0]}<objectDescriptionSet><descriptiveNoteValue>test</descriptiveNoteValue></objectDescriptionSet>{wrap[1]}"
                )
            )
        )
        assert li.error.short() in (
            li.inspect_object_description(
                xml(
                    f"{wrap[0]}<objectDescriptionSet><descriptiveNoteValue>test  </descriptiveNoteValue></objectDescriptionSet>{wrap[1]}"
                )
            )
        )
        assert li.error.long() in (
            li.inspect_object_description(
                xml(
                    f"{wrap[0]}<objectDescriptionSet><descriptiveNoteValue>test test test test</descriptiveNoteValue></objectDescriptionSet>{wrap[1]}"
                )
            )
        )

    def test_lido_type(self):
        li = LIDOInspector()
        assert (
            li.lido_type(
                xml("<elem xmlns:lido='http://www.lido-schema.org' lido:type='test'/>")
            )
            == "test"
        )
        assert (
            li.lido_type(
                xml("<elem xmlns:lido='http://www.lido-schema.org' lido:type=''/>")
            )
            == ""
        )
        assert (
            li.lido_type(xml("<elem xmlns:lido='http://www.lido-schema.org'/>")) == ""
        )

    def test_has_valid_type(self):
        li = LIDOInspector()
        assert (
            li.has_valid_type(
                [
                    xml(
                        "<elem xmlns:lido='http://www.lido-schema.org' lido:type='test'/>"
                    )
                ],
                ["test"],
            )
            == True
        )
        assert (
            li.has_valid_type(
                [
                    xml(
                        "<elem xmlns:lido='http://www.lido-schema.org' lido:type='invalid'/>"
                    ),
                    xml(
                        "<elem xmlns:lido='http://www.lido-schema.org' lido:type='test'/>"
                    ),
                ],
                ["test"],
            )
            == True
        )
        assert (
            li.has_valid_type(
                [
                    xml(
                        "<elem xmlns:lido='http://www.lido-schema.org' lido:type='invalid'/>"
                    ),
                    xml(
                        "<elem xmlns:lido='http://www.lido-schema.org' lido:type='test2'/>"
                    ),
                ],
                ["test", "test2"],
            )
            == True
        )
        assert (
            li.has_valid_type(
                [
                    xml(
                        "<elem xmlns:lido='http://www.lido-schema.org' lido:type='invalid'/>"
                    )
                ],
                ["test"],
            )
            == False
        )
        assert (
            li.has_valid_type(
                [
                    xml(
                        "<elem xmlns:lido='http://www.lido-schema.org' lido:type='invalid'/>"
                    )
                ],
                ["test", "test2"],
            )
            == False
        )
        assert (
            li.has_valid_type(
                [xml("<elem xmlns:lido='http://www.lido-schema.org' lido:type=''/>")],
                ["test", "test2"],
            )
            == False
        )
        assert (
            li.has_valid_type(
                [xml("<elem xmlns:lido='http://www.lido-schema.org'/>")],
                ["test"],
            )
            == False
        )

    def test_has_material(self):
        li = LIDOInspector()
        assert (
            li.has_material(
                [
                    xml(
                        "<termMaterialsTech xmlns:lido='http://www.lido-schema.org' lido:type='technique'/>"
                    ),
                    xml(
                        "<termMaterialsTech xmlns:lido='http://www.lido-schema.org' lido:type='material'/>"
                    ),
                ]
            )
            == True
        )
        assert (
            li.has_material(
                [
                    xml(
                        "<termMaterialsTech xmlns:lido='http://www.lido-schema.org' lido:type='http://terminology.lido-schema.org/lido00131'/>"
                    ),
                    xml(
                        "<termMaterialsTech xmlns:lido='http://www.lido-schema.org' lido:type='http://terminology.lido-schema.org/lido00132'/>"
                    ),
                ]
            )
            == True
        )
        assert (
            li.has_material(
                [
                    xml(
                        "<termMaterialsTech xmlns:lido='http://www.lido-schema.org' lido:type='http://terminology.lido-schema.org/lido00131'/>"
                    ),
                    xml("<termMaterialsTech xmlns:lido='http://www.lido-schema.org'/>"),
                ]
            )
            == False
        )
        assert (
            li.has_material(
                [
                    xml("<termMaterialsTech xmlns:lido='http://www.lido-schema.org'/>"),
                ]
            )
            == False
        )

    def test_has_tech(self):
        li = LIDOInspector()
        assert (
            li.has_tech(
                [
                    xml(
                        "<termMaterialsTech xmlns:lido='http://www.lido-schema.org' lido:type='technique'/>"
                    ),
                    xml(
                        "<termMaterialsTech xmlns:lido='http://www.lido-schema.org' lido:type='material'/>"
                    ),
                ]
            )
            == True
        )
        assert (
            li.has_tech(
                [
                    xml(
                        "<termMaterialsTech xmlns:lido='http://www.lido-schema.org' lido:type='http://terminology.lido-schema.org/lido00131'/>"
                    ),
                    xml(
                        "<termMaterialsTech xmlns:lido='http://www.lido-schema.org' lido:type='http://terminology.lido-schema.org/lido00132'/>"
                    ),
                ]
            )
            == True
        )
        assert (
            li.has_tech(
                [
                    xml(
                        "<termMaterialsTech xmlns:lido='http://www.lido-schema.org' lido:type='http://terminology.lido-schema.org/lido00132'/>"
                    ),
                    xml("<termMaterialsTech xmlns:lido='http://www.lido-schema.org'/>"),
                ]
            )
            == False
        )
        assert (
            li.has_tech(
                [
                    xml("<termMaterialsTech xmlns:lido='http://www.lido-schema.org'/>"),
                ]
            )
            == False
        )

    def test_inspect_materials_tech(self):
        li = LIDOInspector()
        li.configuration["materials_tech"] = {
            "inspect": True,
            "ref": True,
            "differentiated": True,
        }
        wrap = [
            "<lido xmlns:lido='http://www.lido-schema.org' xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'><descriptiveMetadata><objectIdentificationWrap><objectMaterialsTechWrap><objectMaterialsTechSet><materialsTech>",
            "</materialsTech></objectMaterialsTechSet></objectMaterialsTechWrap></objectIdentificationWrap></descriptiveMetadata></lido>",
        ]
        assert (
            li.inspect_materials_tech(
                xml(
                    f"{wrap[0]}<termMaterialsTech lido:type='technique'><term>test</term><conceptID>1</conceptID></termMaterialsTech><termMaterialsTech lido:type='material'><term>test</term><conceptID>2</conceptID></termMaterialsTech>{wrap[1]}"
                )
            )
            == None
        )
        assert (
            li.inspect_materials_tech(
                xml(
                    f"{wrap[0]}<termMaterialsTech lido:type='technique'><term>test</term><conceptID>1</conceptID></termMaterialsTech><termMaterialsTech lido:type='material'><Concept rdf:about='2'><prefLabel>test</prefLabel></Concept></termMaterialsTech>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.miss_info() in (
            li.inspect_materials_tech(
                xml(f"{wrap[0]}<termMaterialsTech></termMaterialsTech>{wrap[1]}")
            )
        )
        assert li.error.miss_info() in (
            li.inspect_materials_tech(xml(f"{wrap[0]}<termMaterialsTech/>{wrap[1]}"))
        )
        assert li.error.miss_info() in (
            li.inspect_materials_tech(xml(f"{wrap[0]}{wrap[1]}"))
        )
        assert li.error.miss_ref("test2") in (
            li.inspect_materials_tech(
                xml(
                    f"{wrap[0]}<termMaterialsTech lido:type='technique'><term>test</term><conceptID>1</conceptID></termMaterialsTech><termMaterialsTech lido:type='material'><term>test2</term><conceptID></conceptID></termMaterialsTech>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test2") in (
            li.inspect_materials_tech(
                xml(
                    f"{wrap[0]}<termMaterialsTech lido:type='technique'><term>test</term><conceptID>1</conceptID></termMaterialsTech><termMaterialsTech lido:type='material'><term>test2</term></termMaterialsTech>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_materials_tech(
                xml(
                    f"{wrap[0]}<termMaterialsTech lido:type='material'><Concept rdf:about=''><prefLabel>test</prefLabel></Concept></termMaterialsTech>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_materials_tech(
                xml(
                    f"{wrap[0]}<termMaterialsTech lido:type='material'><Concept rdf:about='1'/></termMaterialsTech>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_materials_tech(
                xml(
                    f"{wrap[0]}<termMaterialsTech lido:type='technique'><term/><conceptID>1</conceptID></termMaterialsTech>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_mat() in (
            li.inspect_materials_tech(
                xml(
                    f"{wrap[0]}<termMaterialsTech lido:type='technique'><term/><conceptID>1</conceptID></termMaterialsTech>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_tech() in (
            li.inspect_materials_tech(
                xml(
                    f"{wrap[0]}<termMaterialsTech lido:type='material'><term/><conceptID>1</conceptID></termMaterialsTech>{wrap[1]}"
                )
            )
        )

    def test_meas_type(self):
        li = LIDOInspector()
        assert li.meas_type(xml("<measurementType>h</measurementType>")) == "h"
        assert li.meas_type(xml("<measurementType></measurementType>")) == ""
        assert (
            li.meas_type(
                xml(
                    "<measurementType xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'><Concept rdf:about='1'/></measurementType>"
                )
            )
            == "1"
        )

    def test_inspect_measurements_set(self):
        li = LIDOInspector()
        assert (
            li.inspect_measurements_set(
                xml(
                    "<measurementsSet><measurementType>h</measurementType><measurementUnit>m</measurementUnit><measurementValue>1</measurementValue></measurementsSet>"
                )
            )
            == []
        )
        assert li.error.miss_meas_type() in (
            li.inspect_measurements_set(
                xml(
                    "<measurementsSet><measurementType></measurementType><measurementUnit>m</measurementUnit><measurementValue>1</measurementValue></measurementsSet>"
                )
            )
        )
        assert li.error.miss_meas_type() in (
            li.inspect_measurements_set(
                xml(
                    "<measurementsSet><measurementType/><measurementUnit>m</measurementUnit><measurementValue>1</measurementValue></measurementsSet>"
                )
            )
        )
        assert li.error.miss_meas_type() in (
            li.inspect_measurements_set(
                xml(
                    "<measurementsSet><measurementUnit>m</measurementUnit><measurementValue>1</measurementValue></measurementsSet>"
                )
            )
        )
        assert li.error.miss_meas_unit("h") in (
            li.inspect_measurements_set(
                xml(
                    "<measurementsSet><measurementType>h</measurementType><measurementUnit></measurementUnit><measurementValue>1</measurementValue></measurementsSet>"
                )
            )
        )
        assert li.error.miss_meas_unit("h") in (
            li.inspect_measurements_set(
                xml(
                    "<measurementsSet><measurementType>h</measurementType><measurementUnit/><measurementValue>1</measurementValue></measurementsSet>"
                )
            )
        )
        assert li.error.miss_meas_unit("h") in (
            li.inspect_measurements_set(
                xml(
                    "<measurementsSet><measurementType>h</measurementType><measurementValue>1</measurementValue></measurementsSet>"
                )
            )
        )
        assert li.error.miss_meas_value("h") in (
            li.inspect_measurements_set(
                xml(
                    "<measurementsSet><measurementType>h</measurementType><measurementValue></measurementValue></measurementsSet>"
                )
            )
        )
        assert li.error.miss_meas_value("h") in (
            li.inspect_measurements_set(
                xml(
                    "<measurementsSet><measurementType>h</measurementType><measurementValue/></measurementsSet>"
                )
            )
        )
        assert li.error.miss_meas_value("h") in (
            li.inspect_measurements_set(
                xml(
                    "<measurementsSet><measurementType>h</measurementType></measurementsSet>"
                )
            )
        )

    def test_inspect_object_measurements(self):
        li = LIDOInspector()
        li.configuration["object_measurements"] = {"inspect": True}
        wrap = [
            "<lido><descriptiveMetadata><objectIdentificationWrap><objectMeasurementsWrap><objectMeasurementsSet><objectMeasurements>",
            "</objectMeasurements></objectMeasurementsSet></objectMeasurementsWrap></objectIdentificationWrap></descriptiveMetadata></lido>",
        ]
        assert (
            li.inspect_object_measurements(
                xml(
                    f"{wrap[0]}<measurementsSet><measurementType>h</measurementType><measurementUnit>m</measurementUnit><measurementValue>1</measurementValue></measurementsSet>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.miss_info() in (
            li.inspect_object_measurements(xml(f"{wrap[0]}{wrap[1]}"))
        )
        assert li.error.miss_meas_type() in (
            li.inspect_object_measurements(
                xml(
                    f"{wrap[0]}<measurementsSet><measurementType></measurementType><measurementUnit>m</measurementUnit><measurementValue>1</measurementValue></measurementsSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_meas_type() in (
            li.inspect_object_measurements(
                xml(
                    f"{wrap[0]}<measurementsSet><measurementType/><measurementUnit>m</measurementUnit><measurementValue>1</measurementValue></measurementsSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_meas_type() in (
            li.inspect_object_measurements(
                xml(
                    f"{wrap[0]}<measurementsSet><measurementUnit>m</measurementUnit><measurementValue>1</measurementValue></measurementsSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_meas_unit("h") in (
            li.inspect_object_measurements(
                xml(
                    f"{wrap[0]}<measurementsSet><measurementType>h</measurementType><measurementUnit></measurementUnit><measurementValue>1</measurementValue></measurementsSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_meas_unit("h") in (
            li.inspect_object_measurements(
                xml(
                    f"{wrap[0]}<measurementsSet><measurementType>h</measurementType><measurementUnit/><measurementValue>1</measurementValue></measurementsSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_meas_unit("h") in (
            li.inspect_object_measurements(
                xml(
                    f"{wrap[0]}<measurementsSet><measurementType>h</measurementType><measurementValue>1</measurementValue></measurementsSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_meas_value("h") in (
            li.inspect_object_measurements(
                xml(
                    f"{wrap[0]}<measurementsSet><measurementType>h</measurementType><measurementValue></measurementValue></measurementsSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_meas_value("h") in (
            li.inspect_object_measurements(
                xml(
                    f"{wrap[0]}<measurementsSet><measurementType>h</measurementType><measurementValue/></measurementsSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_meas_value("h") in (
            li.inspect_object_measurements(
                xml(
                    f"{wrap[0]}<measurementsSet><measurementType>h</measurementType></measurementsSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_meas_type() in (
            li.inspect_object_measurements(
                xml(
                    f"{wrap[0]}<measurementsSet><measurementType>h</measurementType></measurementsSet><measurementsSet><measurementType/></measurementsSet>{wrap[1]}"
                )
            )
        )

    def test_inspect_subject_concepts(self):
        li = LIDOInspector()
        li.configuration["subject_concept"] = {
            "inspect": True,
            "ref": True,
            "min_num": 2,
        }
        wrap = [
            "<lido xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'><descriptiveMetadata><objectRelationWrap><subjectWrap><subjectSet><subject>",
            "</subject></subjectSet></subjectWrap></objectRelationWrap></descriptiveMetadata></lido>",
        ]
        assert (
            li.inspect_subject_concepts(
                xml(
                    f"{wrap[0]}<subjectConcept><conceptID>1</conceptID><term>test</term></subjectConcept><subjectConcept><conceptID>2</conceptID><term>test</term></subjectConcept>{wrap[1]}"
                )
            )
            == None
        )
        assert (
            li.inspect_subject_concepts(
                xml(
                    f"{wrap[0]}<subjectConcept><Concept rdf:about='2'><prefLabel>test</prefLabel></Concept></subjectConcept><subjectConcept><Concept rdf:about='3'><prefLabel>test</prefLabel></Concept></subjectConcept>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.few() in (
            li.inspect_subject_concepts(
                xml(
                    f"{wrap[0]}<subjectConcept><conceptID>1</conceptID><term>test</term></subjectConcept>{wrap[1]}"
                )
            )
        )
        assert li.error.few() in (
            li.inspect_subject_concepts(
                xml(
                    f"{wrap[0]}<subjectConcept><Concept rdf:about='2'><prefLabel>test</prefLabel></Concept></subjectConcept>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_info() in (
            li.inspect_subject_concepts(
                xml(f"{wrap[0]}<subjectConcept></subjectConcept>{wrap[1]}")
            )
        )
        assert li.error.miss_info() in (
            li.inspect_subject_concepts(xml(f"{wrap[0]}<subjectConcept/>{wrap[1]}"))
        )
        assert li.error.miss_info() in (
            li.inspect_subject_concepts(xml(f"{wrap[0]}{wrap[1]}"))
        )
        assert li.error.miss_label("1") in (
            li.inspect_subject_concepts(
                xml(
                    f"{wrap[0]}<subjectConcept><conceptID>1</conceptID><term/></subjectConcept>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_subject_concepts(
                xml(
                    f"{wrap[0]}<subjectConcept><conceptID>1</conceptID></subjectConcept>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_subject_concepts(
                xml(
                    f"{wrap[0]}<subjectConcept><Concept rdf:about='1'/></subjectConcept>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_subject_concepts(
                xml(
                    f"{wrap[0]}<subjectConcept><conceptID/><term>test</term></subjectConcept>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_subject_concepts(
                xml(
                    f"{wrap[0]}<subjectConcept><term>test</term></subjectConcept>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_subject_concepts(
                xml(
                    f"{wrap[0]}<subjectConcept><Concept rdf:about=''><prefLabel>test</prefLabel></Concept></subjectConcept>{wrap[1]}"
                )
            )
        )

    def test_inspect_resource_set(self):
        li = LIDOInspector()
        assert (
            li.inspect_resource_set(
                xml(
                    "<resourceSet><resourceRepresentation><linkResource>url</linkResource></resourceRepresentation><resourceType><term>test</term></resourceType><rightsResource><rightsType><term>test</term></rightsType></rightsResource></resourceSet>"
                )
            )
            == []
        )
        assert li.error.empty_elem("resourceSet") in (
            li.inspect_resource_set(xml("<resourceSet></resourceSet>"))
        )
        assert li.error.empty_elem("resourceSet") in (
            li.inspect_resource_set(xml("<resourceSet/>"))
        )
        assert li.error.miss_link() in (
            li.inspect_resource_set(
                xml(
                    "<resourceSet><resourceRepresentation><linkResource></linkResource></resourceRepresentation><resourceType><term>test</term></resourceType><rightsResource><rightsType><term>test</term></rightsType></rightsResource></resourceSet>"
                )
            )
        )
        assert li.error.miss_link() in (
            li.inspect_resource_set(
                xml(
                    "<resourceSet><resourceRepresentation><linkResource/></resourceRepresentation><resourceType><term>test</term></resourceType><rightsResource><rightsType><term>test</term></rightsType></rightsResource></resourceSet>"
                )
            )
        )
        assert li.error.miss_link() in (
            li.inspect_resource_set(
                xml(
                    "<resourceSet><resourceRepresentation></resourceRepresentation><resourceType><term>test</term></resourceType><rightsResource><rightsType><term>test</term></rightsType></rightsResource></resourceSet>"
                )
            )
        )
        assert li.error.miss_rights("url") in (
            li.inspect_resource_set(
                xml(
                    "<resourceSet><resourceRepresentation><linkResource>url</linkResource></resourceRepresentation><resourceType><term>test</term></resourceType><rightsResource><rightsType><term/></rightsType></rightsResource></resourceSet>"
                )
            )
        )
        assert li.error.miss_rights("url") in (
            li.inspect_resource_set(
                xml(
                    "<resourceSet><resourceRepresentation><linkResource>url</linkResource></resourceRepresentation><resourceType><term>test</term></resourceType><rightsResource><rightsType/></rightsResource></resourceSet>"
                )
            )
        )
        assert li.error.miss_rights("url") in (
            li.inspect_resource_set(
                xml(
                    "<resourceSet><resourceRepresentation><linkResource>url</linkResource></resourceRepresentation><resourceType><term>test</term></resourceType><rightsResource/></resourceSet>"
                )
            )
        )
        assert li.error.miss_res_type("url") in (
            li.inspect_resource_set(
                xml(
                    "<resourceSet><resourceRepresentation><linkResource>url</linkResource></resourceRepresentation><resourceType><term/></resourceType><rightsResource><rightsType><term/></rightsType></rightsResource></resourceSet>"
                )
            )
        )
        assert li.error.miss_res_type("url") in (
            li.inspect_resource_set(
                xml(
                    "<resourceSet><resourceRepresentation><linkResource>url</linkResource></resourceRepresentation><resourceType/><rightsResource><rightsType><term/></rightsType></rightsResource></resourceSet>"
                )
            )
        )

    def test_inspect_resource_sets(self):
        li = LIDOInspector()
        li.configuration["resourceSet"] = {"inspect": True}
        wrap = [
            "<lido><administrativeMetadata><resourceWrap>",
            "</resourceWrap></administrativeMetadata></lido>",
        ]
        assert (
            li.inspect_resource_sets(
                xml(
                    f"{wrap[0]}<resourceSet><resourceRepresentation><linkResource>url</linkResource></resourceRepresentation><resourceType><term>test</term></resourceType><rightsResource><rightsType><term>test</term></rightsType></rightsResource></resourceSet>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.miss_info() in (
            li.inspect_resource_sets(xml(f"{wrap[0]}{wrap[1]}"))
        )
        assert li.error.empty_elem("resourceSet") in (
            li.inspect_resource_sets(
                xml(f"{wrap[0]}<resourceSet></resourceSet>{wrap[1]}")
            )
        )
        assert li.error.empty_elem("resourceSet") in (
            li.inspect_resource_sets(xml(f"{wrap[0]}<resourceSet/>{wrap[1]}"))
        )
        assert li.error.miss_link() in (
            li.inspect_resource_sets(
                xml(
                    f"{wrap[0]}<resourceSet><resourceRepresentation><linkResource></linkResource></resourceRepresentation><resourceType><term>test</term></resourceType><rightsResource><rightsType><term>test</term></rightsType></rightsResource></resourceSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_link() in (
            li.inspect_resource_sets(
                xml(
                    f"{wrap[0]}<resourceSet><resourceRepresentation><linkResource/></resourceRepresentation><resourceType><term>test</term></resourceType><rightsResource><rightsType><term>test</term></rightsType></rightsResource></resourceSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_link() in (
            li.inspect_resource_sets(
                xml(
                    f"{wrap[0]}<resourceSet><resourceRepresentation></resourceRepresentation><resourceType><term>test</term></resourceType><rightsResource><rightsType><term>test</term></rightsType></rightsResource></resourceSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_rights("url") in (
            li.inspect_resource_sets(
                xml(
                    f"{wrap[0]}<resourceSet><resourceRepresentation><linkResource>url</linkResource></resourceRepresentation><resourceType><term>test</term></resourceType><rightsResource><rightsType><term/></rightsType></rightsResource></resourceSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_rights("url") in (
            li.inspect_resource_sets(
                xml(
                    f"{wrap[0]}<resourceSet><resourceRepresentation><linkResource>url</linkResource></resourceRepresentation><resourceType><term>test</term></resourceType><rightsResource><rightsType/></rightsResource></resourceSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_rights("url") in (
            li.inspect_resource_sets(
                xml(
                    f"{wrap[0]}<resourceSet><resourceRepresentation><linkResource>url</linkResource></resourceRepresentation><resourceType><term>test</term></resourceType><rightsResource/></resourceSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_res_type("url") in (
            li.inspect_resource_sets(
                xml(
                    f"{wrap[0]}<resourceSet><resourceRepresentation><linkResource>url</linkResource></resourceRepresentation><resourceType><term/></resourceType><rightsResource><rightsType><term/></rightsType></rightsResource></resourceSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_res_type("url") in (
            li.inspect_resource_sets(
                xml(
                    f"{wrap[0]}<resourceSet><resourceRepresentation><linkResource>url</linkResource></resourceRepresentation><resourceType/><rightsResource><rightsType><term/></rightsType></rightsResource></resourceSet>{wrap[1]}"
                )
            )
        )

    def test_inspect_event_type(self):
        li = LIDOInspector()
        li.configuration["event"] = {"inspect": True, "ref": True}
        assert (
            li.inspect_event_type(
                xml("<eventType><conceptID>1</conceptID><term>test</term></eventType>")
            )
            == []
        )
        assert (
            li.inspect_event_type(
                xml(
                    "<eventType xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'><Concept rdf:about='2'><prefLabel>test</prefLabel></Concept></eventType>"
                )
            )
            == []
        )
        assert li.error.miss_event_type() in (
            li.inspect_event_type(xml("<eventType></eventType>"))
        )
        assert li.error.miss_event_type() in (
            li.inspect_event_type(xml("<eventType/>"))
        )
        assert li.error.miss_label("1") in (
            li.inspect_event_type(
                xml("<eventType><conceptID>1</conceptID><term/></eventType>")
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_event_type(
                xml("<eventType><conceptID>1</conceptID></eventType>")
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_event_type(
                xml(
                    "<eventType xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'><Concept rdf:about='1'/></eventType>"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_event_type(
                xml("<eventType><conceptID/><term>test</term></eventType>")
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_event_type(xml("<eventType><term>test</term></eventType>"))
        )
        assert li.error.miss_ref("test") in (
            li.inspect_event_type(
                xml(
                    "<eventType xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'><Concept rdf:about=''><prefLabel>test</prefLabel></Concept></eventType>"
                )
            )
        )

    def test_place_id(self):
        li = LIDOInspector()
        assert li.place_id(xml("<elem><placeID>1</placeID></elem>")) == "1"
        assert li.place_id(xml("<elem><placeID></placeID></elem>")) == ""
        assert li.place_id(xml("<elem><placeID/></elem>")) == ""
        assert li.place_id(xml("<elem></elem>")) == ""

    def test_inspect_place(self):
        li = LIDOInspector()
        assert (
            li.inspect_place(
                xml(
                    "<place><placeID>1</placeID><namePlaceSet><appellationValue>test</appellationValue></namePlaceSet></place>"
                ),
                xml("<eventType><term>test</term></eventType>"),
                {"ref": True},
            )
            == []
        )
        assert li.error.miss_place("test") in li.inspect_place(
            xml("<place></place>"),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_place("test") in li.inspect_place(
            xml("<place/>"),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_ref("test") in li.inspect_place(
            xml(
                "<place><placeID></placeID><namePlaceSet><appellationValue>test</appellationValue></namePlaceSet></place>"
            ),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_ref("test") in li.inspect_place(
            xml(
                "<place><placeID/><namePlaceSet><appellationValue>test</appellationValue></namePlaceSet></place>"
            ),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_ref("test") in li.inspect_place(
            xml(
                "<place><namePlaceSet><appellationValue>test</appellationValue></namePlaceSet></place>"
            ),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_place(
            xml(
                "<place><placeID>1</placeID><namePlaceSet><appellationValue></appellationValue></namePlaceSet></place>"
            ),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_place(
            xml(
                "<place><placeID>1</placeID><namePlaceSet><appellationValue/></namePlaceSet></place>"
            ),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_place(
            xml("<place><placeID>1</placeID><namePlaceSet></namePlaceSet></place>"),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_place(
            xml("<place><placeID>1</placeID><namePlaceSet/></place>"),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_place(
            xml("<place><placeID>1</placeID></place>"),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )

    def test_inspect_places(self):
        li = LIDOInspector()
        assert (
            li.inspect_places(
                [
                    xml(
                        "<place><placeID>1</placeID><namePlaceSet><appellationValue>test</appellationValue></namePlaceSet></place>"
                    )
                ],
                xml("<eventType><term>test</term></eventType>"),
                {"ref": True},
            )
            == []
        )
        assert (
            li.inspect_places(
                [],
                xml("<eventType><term>Event (non-specified)</term></eventType>"),
                {"ref": True},
            )
            == []
        )
        assert li.error.miss_place("test") in li.inspect_places(
            [],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_place("test") in li.inspect_places(
            [xml("<place></place>")],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_place("test") in li.inspect_places(
            [xml("<place/>")],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_ref("test") in li.inspect_places(
            [
                xml(
                    "<place><placeID></placeID><namePlaceSet><appellationValue>test</appellationValue></namePlaceSet></place>"
                )
            ],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_ref("test") in li.inspect_places(
            [
                xml(
                    "<place><placeID/><namePlaceSet><appellationValue>test</appellationValue></namePlaceSet></place>"
                )
            ],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_ref("test") in li.inspect_places(
            [
                xml(
                    "<place><namePlaceSet><appellationValue>test</appellationValue></namePlaceSet></place>"
                )
            ],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_places(
            [
                xml(
                    "<place><placeID>1</placeID><namePlaceSet><appellationValue></appellationValue></namePlaceSet></place>"
                )
            ],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_places(
            [
                xml(
                    "<place><placeID>1</placeID><namePlaceSet><appellationValue/></namePlaceSet></place>"
                )
            ],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_places(
            [xml("<place><placeID>1</placeID><namePlaceSet></namePlaceSet></place>")],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_places(
            [xml("<place><placeID>1</placeID><namePlaceSet/></place>")],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_places(
            [xml("<place><placeID>1</placeID></place>")],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )

    def test_actor_id(self):
        li = LIDOInspector()
        assert li.actor_id(xml("<elem><actorID>1</actorID></elem>")) == "1"
        assert li.actor_id(xml("<elem><actorID></actorID></elem>")) == ""
        assert li.actor_id(xml("<elem><actorID/></elem>")) == ""
        assert li.actor_id(xml("<elem></elem>")) == ""

    def test_inspect_actor(self):
        li = LIDOInspector()
        assert (
            li.inspect_actor(
                xml(
                    "<actor><actorID>1</actorID><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor>"
                ),
                xml("<eventType><term>test</term></eventType>"),
                {"ref": True},
            )
            == []
        )
        assert li.error.miss_actor("test") in li.inspect_actor(
            xml("<actor></actor>"),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_actor("test") in li.inspect_actor(
            xml("<actor/>"),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_ref("test") in li.inspect_actor(
            xml(
                "<actor><actorID></actorID><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor>"
            ),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_ref("test") in li.inspect_actor(
            xml(
                "<actor><actorID/><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor>"
            ),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_ref("test") in li.inspect_actor(
            xml(
                "<actor><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor>"
            ),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_actor(
            xml(
                "<actor><actorID>1</actorID><nameActorSet><appellationValue></appellationValue></nameActorSet></actor>"
            ),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_actor(
            xml(
                "<actor><actorID>1</actorID><nameActorSet><appellationValue/></nameActorSet></actor>"
            ),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_actor(
            xml("<actor><actorID>1</actorID><nameActorSet></nameActorSet></actor>"),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_actor(
            xml("<actor><actorID>1</actorID><nameActorSet/></actor>"),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_actor(
            xml("<actor><actorID>1</actorID></actor>"),
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )

    def test_inspect_actors(self):
        li = LIDOInspector()
        assert (
            li.inspect_actors(
                [
                    xml(
                        "<actor><actorID>1</actorID><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor>"
                    )
                ],
                xml("<eventType><term>test</term></eventType>"),
                {"ref": True},
            )
            == []
        )
        assert (
            li.inspect_actors(
                [],
                xml("<eventType><term>Event (non-specified)</term></eventType>"),
                {"ref": True},
            )
            == []
        )
        assert li.error.miss_actor("test") in li.inspect_actors(
            [],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_actor("test") in li.inspect_actors(
            [xml("<actor></actor>")],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_actor("test") in li.inspect_actors(
            [xml("<actor/>")],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_ref("test") in li.inspect_actors(
            [
                xml(
                    "<actor><actorID></actorID><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor>"
                )
            ],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_ref("test") in li.inspect_actors(
            [
                xml(
                    "<actor><actorID/><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor>"
                )
            ],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_ref("test") in li.inspect_actors(
            [
                xml(
                    "<actor><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor>"
                )
            ],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_actors(
            [
                xml(
                    "<actor><actorID>1</actorID><nameActorSet><appellationValue></appellationValue></nameActorSet></actor>"
                )
            ],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_actors(
            [
                xml(
                    "<actor><actorID>1</actorID><nameActorSet><appellationValue/></nameActorSet></actor>"
                )
            ],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_actors(
            [xml("<actor><actorID>1</actorID><nameActorSet></nameActorSet></actor>")],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_actors(
            [xml("<actor><actorID>1</actorID><nameActorSet/></actor>")],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )
        assert li.error.miss_label("1") in li.inspect_actors(
            [xml("<actor><actorID>1</actorID></actor>")],
            xml("<eventType><term>test</term></eventType>"),
            {"ref": True},
        )

    def test_inspect_date(self):
        li = LIDOInspector()
        assert (
            li.inspect_date(
                xml(
                    "<date><earliestDate>2000</earliestDate><latestDate>2001</latestDate></date>"
                ),
                xml("<eventType><term>test</term></eventType>"),
            )
            == []
        )
        assert (
            li.inspect_date(
                xml("<date/>"),
                xml("<eventType><term>Event (non-specified)</term></eventType>"),
            )
            == []
        )
        assert li.error.miss_date("test") in (
            li.inspect_date(
                xml("<date></date>"),
                xml("<eventType><term>test</term></eventType>"),
            )
        )
        assert li.error.miss_date("test") in (
            li.inspect_date(
                xml("<date/>"),
                xml("<eventType><term>test</term></eventType>"),
            )
        )
        assert li.error.miss_earl_date("test") in (
            li.inspect_date(
                xml(
                    "<date><earliestDate></earliestDate><latestDate>2001</latestDate></date>"
                ),
                xml("<eventType><term>test</term></eventType>"),
            )
        )
        assert li.error.miss_earl_date("test") in (
            li.inspect_date(
                xml("<date><earliestDate/><latestDate>2001</latestDate></date>"),
                xml("<eventType><term>test</term></eventType>"),
            )
        )
        assert li.error.miss_earl_date("test") in (
            li.inspect_date(
                xml("<date><latestDate>2001</latestDate></date>"),
                xml("<eventType><term>test</term></eventType>"),
            )
        )
        assert li.error.miss_lat_date("test") in (
            li.inspect_date(
                xml(
                    "<date><earliestDate>2000</earliestDate><latestDate></latestDate></date>"
                ),
                xml("<eventType><term>test</term></eventType>"),
            )
        )
        assert li.error.miss_lat_date("test") in (
            li.inspect_date(
                xml("<date><earliestDate>2000</earliestDate><latestDate/></date>"),
                xml("<eventType><term>test</term></eventType>"),
            )
        )
        assert li.error.miss_lat_date("test") in (
            li.inspect_date(
                xml("<date><earliestDate>2000</earliestDate></date>"),
                xml("<eventType><term>test</term></eventType>"),
            )
        )

    def test_summarize_event_messages(self):
        li = LIDOInspector()
        assert li.summarize_event_messages(
            [
                li.error.miss_actor("t"),
                li.error.miss_place("t"),
                li.error.miss_date("t"),
            ],
            "t",
        ) == [li.error.miss_event_info("t")]
        assert (
            li.summarize_event_messages(
                [
                    li.error.miss_actor("t"),
                    li.error.miss_place("t"),
                ],
                "t",
            )
            == []
        )
        assert (
            li.summarize_event_messages(
                [
                    li.error.miss_actor("t"),
                    li.error.miss_date("t"),
                ],
                "t",
            )
            == []
        )
        assert (
            li.summarize_event_messages(
                [
                    li.error.miss_place("t"),
                    li.error.miss_date("t"),
                ],
                "t",
            )
            == []
        )
        assert (
            li.summarize_event_messages(
                [li.error.miss_place("t")],
                "t",
            )
            == []
        )
        assert (
            li.summarize_event_messages(
                [li.error.miss_actor("t")],
                "t",
            )
            == []
        )
        assert (
            li.summarize_event_messages(
                [],
                "t",
            )
            == []
        )

    def test_inspect_event(self):
        li = LIDOInspector()
        li.configuration["event"] = {"inspect": True, "ref": True}
        assert (
            li.inspect_event(
                xml(
                    "<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventActor><actorInRole><actor><actorID>1</actorID><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor></actorInRole></eventActor></event>"
                )
            )
            == []
        )
        assert (
            li.inspect_event(
                xml(
                    "<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventDate><date><earliestDate>2000</earliestDate><latestDate>2001</latestDate></date></eventDate></event>"
                )
            )
            == []
        )
        assert (
            li.inspect_event(
                xml(
                    "<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventPlace><place><placeID>1</placeID><namePlaceSet><appellationValue>test</appellationValue></namePlaceSet></place></eventPlace></event>"
                )
            )
            == []
        )
        assert li.error.empty_elem("event") in (
            li.inspect_event(xml("<event></event>"))
        )
        assert li.error.empty_elem("event") in (li.inspect_event(xml("<event/>")))
        assert li.error.miss_event_type() in (
            li.inspect_event(
                xml(
                    "<event><eventType></eventType><eventActor><actorInRole><actor><actorID>1</actorID><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor></actorInRole></eventActor></event>"
                )
            )
        )
        assert li.error.miss_event_type() in (
            li.inspect_event(
                xml(
                    "<event><eventActor><actorInRole><actor><actorID>1</actorID><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor></actorInRole></eventActor></event>"
                )
            )
        )
        assert li.error.miss_event_info("test") in (
            li.inspect_event(
                xml(
                    "<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventActor><actorInRole><actor></actor></actorInRole></eventActor></event>"
                )
            )
        )
        assert li.error.miss_event_info("test") in (
            li.inspect_event(
                xml(
                    "<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventActor></eventActor></event>"
                )
            )
        )
        assert li.error.miss_event_info("test") in (
            li.inspect_event(
                xml(
                    "<event><eventType><conceptID>1</conceptID><term>test</term></eventType></event>"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_event(
                xml(
                    "<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventActor><actorInRole><actor><actorID></actorID><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor></actorInRole></eventActor></event>"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_event(
                xml(
                    "<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventActor><actorInRole><actor><actorID/><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor></actorInRole></eventActor></event>"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_event(
                xml(
                    "<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventActor><actorInRole><actor><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor></actorInRole></eventActor></event>"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_event(
                xml(
                    "<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventActor><actorInRole><actor><actorID>1</actorID><nameActorSet><appellationValue></appellationValue></nameActorSet></actor></actorInRole></eventActor></event>"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_event(
                xml(
                    "<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventActor><actorInRole><actor><actorID>1</actorID><nameActorSet></nameActorSet></actor></actorInRole></eventActor></event>"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_event(
                xml(
                    "<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventActor><actorInRole><actor><actorID>1</actorID></actor></actorInRole></eventActor></event>"
                )
            )
        )
        assert li.error.miss_earl_date("test") in (
            li.inspect_event(
                xml(
                    "<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventDate><date><earliestDate></earliestDate><latestDate>2000</latestDate></date></eventDate></event>"
                )
            )
        )
        assert li.error.miss_earl_date("test") in (
            li.inspect_event(
                xml(
                    "<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventDate><date><earliestDate/><latestDate>2000</latestDate></date></eventDate></event>"
                )
            )
        )
        assert li.error.miss_earl_date("test") in (
            li.inspect_event(
                xml(
                    "<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventDate><date><latestDate>2000</latestDate></date></eventDate></event>"
                )
            )
        )
        assert li.error.miss_lat_date("test") in (
            li.inspect_event(
                xml(
                    "<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventDate><date><earliestDate>2000</earliestDate><latestDate></latestDate></date></eventDate></event>"
                )
            )
        )
        assert li.error.miss_lat_date("test") in (
            li.inspect_event(
                xml(
                    "<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventDate><date><earliestDate>2000</earliestDate><latestDate/></date></eventDate></event>"
                )
            )
        )
        assert li.error.miss_lat_date("test") in (
            li.inspect_event(
                xml(
                    "<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventDate><date><earliestDate>2000</earliestDate></date></eventDate></event>"
                )
            )
        )

    def test_inspect_events(self):
        li = LIDOInspector()
        li.configuration["event"] = {"inspect": True, "ref": True}
        wrap = [
            "<lido><descriptiveMetadata><eventWrap><eventSet>",
            "</eventSet></eventWrap></descriptiveMetadata></lido>",
        ]
        assert (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventActor><actorInRole><actor><actorID>1</actorID><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor></actorInRole></eventActor></event>{wrap[1]}"
                )
            )
            == None
        )
        assert (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventDate><date><earliestDate>2000</earliestDate><latestDate>2001</latestDate></date></eventDate></event>{wrap[1]}"
                )
            )
            == None
        )
        assert (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventPlace><place><placeID>1</placeID><namePlaceSet><appellationValue>test</appellationValue></namePlaceSet></place></eventPlace></event>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.miss_info() in (li.inspect_events(xml(f"{wrap[0]}{wrap[1]}")))
        assert li.error.empty_elem("event") in (
            li.inspect_events(xml(f"{wrap[0]}<event></event>{wrap[1]}"))
        )
        assert li.error.empty_elem("event") in (
            li.inspect_events(xml(f"{wrap[0]}<event/>{wrap[1]}"))
        )
        assert li.error.miss_event_type() in (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType></eventType><eventActor><actorInRole><actor><actorID>1</actorID><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor></actorInRole></eventActor></event>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_event_type() in (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventActor><actorInRole><actor><actorID>1</actorID><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor></actorInRole></eventActor></event>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_event_info("test") in (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventActor><actorInRole><actor></actor></actorInRole></eventActor></event>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_event_info("test") in (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventActor></eventActor></event>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_event_info("test") in (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType><conceptID>1</conceptID><term>test</term></eventType></event>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventActor><actorInRole><actor><actorID></actorID><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor></actorInRole></eventActor></event>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventActor><actorInRole><actor><actorID/><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor></actorInRole></eventActor></event>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventActor><actorInRole><actor><nameActorSet><appellationValue>test</appellationValue></nameActorSet></actor></actorInRole></eventActor></event>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventActor><actorInRole><actor><actorID>1</actorID><nameActorSet><appellationValue></appellationValue></nameActorSet></actor></actorInRole></eventActor></event>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventActor><actorInRole><actor><actorID>1</actorID><nameActorSet></nameActorSet></actor></actorInRole></eventActor></event>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventActor><actorInRole><actor><actorID>1</actorID></actor></actorInRole></eventActor></event>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_earl_date("test") in (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventDate><date><earliestDate></earliestDate><latestDate>2000</latestDate></date></eventDate></event>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_earl_date("test") in (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventDate><date><earliestDate/><latestDate>2000</latestDate></date></eventDate></event>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_earl_date("test") in (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventDate><date><latestDate>2000</latestDate></date></eventDate></event>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_lat_date("test") in (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventDate><date><earliestDate>2000</earliestDate><latestDate></latestDate></date></eventDate></event>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_lat_date("test") in (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventDate><date><earliestDate>2000</earliestDate><latestDate/></date></eventDate></event>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_lat_date("test") in (
            li.inspect_events(
                xml(
                    f"{wrap[0]}<event><eventType><conceptID>1</conceptID><term>test</term></eventType><eventDate><date><earliestDate>2000</earliestDate></date></eventDate></event>{wrap[1]}"
                )
            )
        )

    def test_inspect_record_type(self):
        li = LIDOInspector()
        li.configuration["record_type"] = {"inspect": True, "ref": True}
        wrap = [
            "<lido xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'><administrativeMetadata><recordWrap>",
            "</recordWrap></administrativeMetadata></lido>",
        ]
        assert (
            li.inspect_record_type(
                xml(
                    f"{wrap[0]}<recordType><conceptID>1</conceptID><term>test</term></recordType>{wrap[1]}"
                )
            )
            == None
        )
        assert (
            li.inspect_record_type(
                xml(
                    f"{wrap[0]}<recordType><Concept rdf:about='2'><prefLabel>test</prefLabel></Concept></recordType>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.miss_info() in (
            li.inspect_record_type(xml(f"{wrap[0]}<recordType></recordType>{wrap[1]}"))
        )
        assert li.error.miss_info() in (
            li.inspect_record_type(xml(f"{wrap[0]}<recordType/>{wrap[1]}"))
        )
        assert li.error.miss_info() in (
            li.inspect_record_type(xml(f"{wrap[0]}{wrap[1]}"))
        )
        assert li.error.miss_label("1") in (
            li.inspect_record_type(
                xml(
                    f"{wrap[0]}<recordType><conceptID>1</conceptID><term/></recordType>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_record_type(
                xml(
                    f"{wrap[0]}<recordType><conceptID>1</conceptID></recordType>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_record_type(
                xml(
                    f"{wrap[0]}<recordType><Concept rdf:about='1'/></recordType>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_record_type(
                xml(
                    f"{wrap[0]}<recordType><conceptID/><term>test</term></recordType>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_record_type(
                xml(f"{wrap[0]}<recordType><term>test</term></recordType>{wrap[1]}")
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_record_type(
                xml(
                    f"{wrap[0]}<recordType><Concept rdf:about=''><prefLabel>test</prefLabel></Concept></recordType>{wrap[1]}"
                )
            )
        )
        li.configuration["record_type"]["patterns"] = {"label": "test", "ref": "1"}
        assert (
            li.inspect_record_type(
                xml(
                    f"{wrap[0]}<recordType><conceptID>1</conceptID><term>test</term></recordType>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.pattern("2") in (
            li.inspect_record_type(
                xml(
                    f"{wrap[0]}<recordType><conceptID>2</conceptID><term>test</term></recordType>{wrap[1]}"
                )
            )
        )
        assert li.error.pattern("tst") in (
            li.inspect_record_type(
                xml(
                    f"{wrap[0]}<recordType><conceptID>2</conceptID><term>tst</term></recordType>{wrap[1]}"
                )
            )
        )
        li.configuration["record_type"]["patterns"] = {
            "label": rf"^[a-zA-ZäöüÄÖÜß0-9'-]+$",
            "ref": rf"^https:\/\/.+$",
        }
        assert (
            li.inspect_record_type(
                xml(
                    f"{wrap[0]}<recordType><conceptID>https://www.test.com/</conceptID><term>test</term></recordType>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.pattern("2") in (
            li.inspect_record_type(
                xml(
                    f"{wrap[0]}<recordType><conceptID>2</conceptID><term>test</term></recordType>{wrap[1]}"
                )
            )
        )
        assert li.error.pattern("test test") in (
            li.inspect_record_type(
                xml(
                    f"{wrap[0]}<recordType><conceptID>2</conceptID><term>test test</term></recordType>{wrap[1]}"
                )
            )
        )

    def test_legal_body_id(self):
        li = LIDOInspector()
        assert li.legal_body_id(xml("<elem><legalBodyID>1</legalBodyID></elem>")) == "1"
        assert li.legal_body_id(xml("<elem><legalBodyID></legalBodyID></elem>")) == ""
        assert li.legal_body_id(xml("<elem><legalBodyID/></elem>")) == ""
        assert li.legal_body_id(xml("<elem></elem>")) == ""

    def test_inspect_repository_name(self):
        li = LIDOInspector()
        li.configuration["repository_name"] = {"inspect": True, "ref": True}
        wrap = [
            "<lido><descriptiveMetadata><objectIdentificationWrap><repositoryWrap><repositorySet>",
            "</repositorySet></repositoryWrap></objectIdentificationWrap></descriptiveMetadata></lido>",
        ]
        assert (
            li.inspect_repository_name(
                xml(
                    f"{wrap[0]}<repositoryName><legalBodyID>1</legalBodyID><legalBodyName><appellationValue>test</appellationValue></legalBodyName></repositoryName>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.miss_info() in (
            li.inspect_repository_name(
                xml(f"{wrap[0]}<repositoryName></repositoryName>{wrap[1]}")
            )
        )
        assert li.error.miss_info() in (
            li.inspect_repository_name(xml(f"{wrap[0]}<repositoryName/>{wrap[1]}"))
        )
        assert li.error.miss_label("1") in (
            li.inspect_repository_name(
                xml(
                    f"{wrap[0]}<repositoryName><legalBodyID>1</legalBodyID><legalBodyName><appellationValue></appellationValue></legalBodyName></repositoryName>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_repository_name(
                xml(
                    f"{wrap[0]}<repositoryName><legalBodyID>1</legalBodyID><legalBodyName><appellationValue/></legalBodyName></repositoryName>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_repository_name(
                xml(
                    f"{wrap[0]}<repositoryName><legalBodyID>1</legalBodyID><legalBodyName></legalBodyName></repositoryName>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_repository_name(
                xml(
                    f"{wrap[0]}<repositoryName><legalBodyID>1</legalBodyID><legalBodyName/></repositoryName>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_repository_name(
                xml(
                    f"{wrap[0]}<repositoryName><legalBodyID>1</legalBodyID></repositoryName>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_repository_name(
                xml(
                    f"{wrap[0]}<repositoryName><legalBodyID></legalBodyID><legalBodyName><appellationValue>test</appellationValue></legalBodyName></repositoryName>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_repository_name(
                xml(
                    f"{wrap[0]}<repositoryName><legalBodyID/><legalBodyName><appellationValue>test</appellationValue></legalBodyName></repositoryName>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_repository_name(
                xml(
                    f"{wrap[0]}<repositoryName><legalBodyName><appellationValue>test</appellationValue></legalBodyName></repositoryName>{wrap[1]}"
                )
            )
        )
        li.configuration["repository_name"]["patterns"] = {
            "label": rf"Testmuseum",
            "ref": rf"^DE-MUS-\d+",
        }
        assert (
            li.inspect_repository_name(
                xml(
                    f"{wrap[0]}<repositoryName><legalBodyID>DE-MUS-1234</legalBodyID><legalBodyName><appellationValue>Testmuseum</appellationValue></legalBodyName></repositoryName>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.pattern("www.testmuseum.de") in (
            li.inspect_repository_name(
                xml(
                    f"{wrap[0]}<repositoryName><legalBodyID>www.testmuseum.de</legalBodyID><legalBodyName><appellationValue>Testmuseum</appellationValue></legalBodyName></repositoryName>{wrap[1]}"
                )
            )
        )
        assert li.error.pattern("Test-Museum") in (
            li.inspect_repository_name(
                xml(
                    f"{wrap[0]}<repositoryName><legalBodyID>DE-MUS-1234</legalBodyID><legalBodyName><appellationValue>Test-Museum</appellationValue></legalBodyName></repositoryName>{wrap[1]}"
                )
            )
        )

    def test_inspect_record_source(self):
        li = LIDOInspector()
        li.configuration["record_source"] = {"inspect": True, "ref": True}
        assert (
            li.inspect_record_source(
                xml(
                    "<recordSource><legalBodyID>1</legalBodyID><legalBodyName><appellationValue>test</appellationValue></legalBodyName></recordSource>"
                )
            )
            == []
        )
        assert li.error.empty_elem("recordSource") in (
            li.inspect_record_source(xml("<recordSource></recordSource>"))
        )
        assert li.error.empty_elem("recordSource") in (
            li.inspect_record_source(xml("<recordSource/>"))
        )
        assert li.error.miss_label("1") in (
            li.inspect_record_source(
                xml(
                    "<recordSource><legalBodyID>1</legalBodyID><legalBodyName><appellationValue></appellationValue></legalBodyName></recordSource>"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_record_source(
                xml(
                    "<recordSource><legalBodyID>1</legalBodyID><legalBodyName><appellationValue/></legalBodyName></recordSource>"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_record_source(
                xml(
                    "<recordSource><legalBodyID>1</legalBodyID><legalBodyName></legalBodyName></recordSource>"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_record_source(
                xml(
                    "<recordSource><legalBodyID>1</legalBodyID><legalBodyName/></recordSource>"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_record_source(
                xml("<recordSource><legalBodyID>1</legalBodyID></recordSource>")
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_record_source(
                xml(
                    "<recordSource><legalBodyID></legalBodyID><legalBodyName><appellationValue>test</appellationValue></legalBodyName></recordSource>"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_record_source(
                xml(
                    "<recordSource><legalBodyID/><legalBodyName><appellationValue>test</appellationValue></legalBodyName></recordSource>"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_record_source(
                xml(
                    "<recordSource><legalBodyName><appellationValue>test</appellationValue></legalBodyName></recordSource>"
                )
            )
        )

    def test_inspect_record_sources(self):
        li = LIDOInspector()
        li.configuration["record_source"] = {"inspect": True, "ref": True}
        wrap = [
            "<lido><administrativeMetadata><recordWrap>",
            "</recordWrap></administrativeMetadata></lido>",
        ]
        assert (
            li.inspect_record_sources(
                xml(
                    f"{wrap[0]}<recordSource><legalBodyID>1</legalBodyID><legalBodyName><appellationValue>test</appellationValue></legalBodyName></recordSource>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.empty_elem("recordSource") in (
            li.inspect_record_sources(
                xml(f"{wrap[0]}<recordSource></recordSource>{wrap[1]}")
            )
        )
        assert li.error.miss_info() in (
            li.inspect_record_sources(xml(f"{wrap[0]}{wrap[1]}"))
        )
        assert li.error.empty_elem("recordSource") in (
            li.inspect_record_sources(xml(f"{wrap[0]}<recordSource/>{wrap[1]}"))
        )
        assert li.error.miss_label("1") in (
            li.inspect_record_sources(
                xml(
                    f"{wrap[0]}<recordSource><legalBodyID>1</legalBodyID><legalBodyName><appellationValue></appellationValue></legalBodyName></recordSource>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_record_sources(
                xml(
                    f"{wrap[0]}<recordSource><legalBodyID>1</legalBodyID><legalBodyName><appellationValue/></legalBodyName></recordSource>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_record_sources(
                xml(
                    f"{wrap[0]}<recordSource><legalBodyID>1</legalBodyID><legalBodyName></legalBodyName></recordSource>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_record_sources(
                xml(
                    f"{wrap[0]}<recordSource><legalBodyID>1</legalBodyID><legalBodyName/></recordSource>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_record_sources(
                xml(
                    f"{wrap[0]}<recordSource><legalBodyID>1</legalBodyID></recordSource>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_record_sources(
                xml(
                    f"{wrap[0]}<recordSource><legalBodyID></legalBodyID><legalBodyName><appellationValue>test</appellationValue></legalBodyName></recordSource>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_record_sources(
                xml(
                    f"{wrap[0]}<recordSource><legalBodyID/><legalBodyName><appellationValue>test</appellationValue></legalBodyName></recordSource>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_record_sources(
                xml(
                    f"{wrap[0]}<recordSource><legalBodyName><appellationValue>test</appellationValue></legalBodyName></recordSource>{wrap[1]}"
                )
            )
        )

    def test_inspect_record_rights(self):
        li = LIDOInspector()
        li.configuration["record_rights"] = {"inspect": True, "ref": True}
        wrap = [
            "<lido xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'><administrativeMetadata><recordWrap><recordRights>",
            "</recordRights></recordWrap></administrativeMetadata></lido>",
        ]
        assert (
            li.inspect_record_rights(
                xml(
                    f"{wrap[0]}<rightsType><conceptID>1</conceptID><term>test</term></rightsType>{wrap[1]}"
                )
            )
            == None
        )
        assert (
            li.inspect_record_rights(
                xml(
                    f"{wrap[0]}<rightsType><Concept rdf:about='2'><prefLabel>test</prefLabel></Concept></rightsType>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.miss_info() in (
            li.inspect_record_rights(
                xml(f"{wrap[0]}<rightsType></rightsType>{wrap[1]}")
            )
        )
        assert li.error.miss_info() in (
            li.inspect_record_rights(xml(f"{wrap[0]}<rightsType/>{wrap[1]}"))
        )
        assert li.error.miss_info() in (
            li.inspect_record_rights(xml(f"{wrap[0]}{wrap[1]}"))
        )
        assert li.error.miss_label("1") in (
            li.inspect_record_rights(
                xml(
                    f"{wrap[0]}<rightsType><conceptID>1</conceptID><term/></rightsType>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_record_rights(
                xml(
                    f"{wrap[0]}<rightsType><conceptID>1</conceptID></rightsType>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_label("1") in (
            li.inspect_record_rights(
                xml(
                    f"{wrap[0]}<rightsType><Concept rdf:about='1'/></rightsType>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_record_rights(
                xml(
                    f"{wrap[0]}<rightsType><conceptID/><term>test</term></rightsType>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_record_rights(
                xml(f"{wrap[0]}<rightsType><term>test</term></rightsType>{wrap[1]}")
            )
        )
        assert li.error.miss_ref("test") in (
            li.inspect_record_rights(
                xml(
                    f"{wrap[0]}<rightsType><Concept rdf:about=''><prefLabel>test</prefLabel></Concept></rightsType>{wrap[1]}"
                )
            )
        )
        li.configuration["record_rights"]["patterns"] = {"label": "test", "ref": "1"}
        assert (
            li.inspect_record_rights(
                xml(
                    f"{wrap[0]}<rightsType><conceptID>1</conceptID><term>test</term></rightsType>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.pattern("2") in (
            li.inspect_record_rights(
                xml(
                    f"{wrap[0]}<rightsType><conceptID>2</conceptID><term>test</term></rightsType>{wrap[1]}"
                )
            )
        )
        assert li.error.pattern("tst") in (
            li.inspect_record_rights(
                xml(
                    f"{wrap[0]}<rightsType><conceptID>2</conceptID><term>tst</term></rightsType>{wrap[1]}"
                )
            )
        )
        li.configuration["record_rights"]["patterns"] = {
            "label": rf"^[a-zA-ZäöüÄÖÜß0-9'-]+$",
            "ref": rf"^https:\/\/.+$",
        }
        assert (
            li.inspect_record_rights(
                xml(
                    f"{wrap[0]}<rightsType><conceptID>https://www.test.com/</conceptID><term>test</term></rightsType>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.pattern("2") in (
            li.inspect_record_rights(
                xml(
                    f"{wrap[0]}<rightsType><conceptID>2</conceptID><term>test</term></rightsType>{wrap[1]}"
                )
            )
        )
        assert li.error.pattern("test test") in (
            li.inspect_record_rights(
                xml(
                    f"{wrap[0]}<rightsType><conceptID>2</conceptID><term>test test</term></rightsType>{wrap[1]}"
                )
            )
        )

    def test_inspect_record_info_set(self):
        li = LIDOInspector()
        li.configuration["record_info"] = {"inspect": True}
        wrap = [
            "<lido><administrativeMetadata><recordWrap>",
            "</recordWrap></administrativeMetadata></lido>",
        ]
        assert (
            li.inspect_record_info_set(
                xml(
                    f"{wrap[0]}<recordInfoSet><recordInfoLink>url</recordInfoLink><recordMetadataDate>date</recordMetadataDate></recordInfoSet>{wrap[1]}"
                )
            )
            == None
        )
        assert li.error.miss_info() in (
            li.inspect_record_info_set(
                xml(f"{wrap[0]}<recordInfoSet></recordInfoSet>{wrap[1]}")
            )
        )
        assert li.error.miss_info() in (
            li.inspect_record_info_set(xml(f"{wrap[0]}<recordInfoSet/>{wrap[1]}"))
        )
        assert li.error.miss_info() in (
            li.inspect_record_info_set(xml(f"{wrap[0]}<recordInfoSet/>{wrap[1]}"))
        )
        assert li.error.miss_link() in (
            li.inspect_record_info_set(
                xml(
                    f"{wrap[0]}<recordInfoSet><recordInfoLink></recordInfoLink><recordMetadataDate>date</recordMetadataDate></recordInfoSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_link() in (
            li.inspect_record_info_set(
                xml(
                    f"{wrap[0]}<recordInfoSet><recordInfoLink/><recordMetadataDate>date</recordMetadataDate></recordInfoSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_link() in (
            li.inspect_record_info_set(
                xml(
                    f"{wrap[0]}<recordInfoSet><recordMetadataDate>date</recordMetadataDate></recordInfoSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_date("http://terminology.lido-schema.org/lido00472") in (
            li.inspect_record_info_set(
                xml(
                    f"{wrap[0]}<recordInfoSet><recordInfoLink>url</recordInfoLink><recordMetadataDate></recordMetadataDate></recordInfoSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_date("http://terminology.lido-schema.org/lido00472") in (
            li.inspect_record_info_set(
                xml(
                    f"{wrap[0]}<recordInfoSet><recordInfoLink>url</recordInfoLink><recordMetadataDate/></recordInfoSet>{wrap[1]}"
                )
            )
        )
        assert li.error.miss_date("http://terminology.lido-schema.org/lido00472") in (
            li.inspect_record_info_set(
                xml(
                    f"{wrap[0]}<recordInfoSet><recordInfoLink>url</recordInfoLink></recordInfoSet>{wrap[1]}"
                )
            )
        )


if __name__ == "__main__":
    pytest.main()
