import pytest
from lxml import etree
from datetime import date
from nfdinspector.ead_inspector import EADInspector


def xml(xml_string):
    return etree.fromstring(xml_string)


class Test_EADInspector:

    def test_configure(self):
        ei = EADInspector()
        default_config = ei.configuration.copy()
        ei.configure(
            {
                "unittitle": {
                    "collection": {"min_word_num": 5},
                    "class": {"inspect": False, "min_word_num": 0},
                }
            }
        )
        assert ei.configuration["unittitle"]["collection"]["min_word_num"] == 5
        assert (
            ei.configuration["unittitle"]["collection"]["inspect"]
            == default_config["unittitle"]["collection"]["inspect"]
        )
        assert ei.configuration["unittitle"]["class"] == {
            "inspect": False,
            "min_word_num": 0,
        }
        assert (
            ei.configuration["unittitle"]["file"] == default_config["unittitle"]["file"]
        )
        assert ei.configuration["abstract"] == default_config["abstract"]
        ei.configuration = default_config.copy()
        ei.configure(
            {
                "unknown": {
                    "collection": {"min_word_num": 5},
                    "class": {"inspect": False, "min_word_num": 0},
                }
            }
        )
        assert ei.configuration == default_config
        ei.configuration = default_config.copy()
        ei.configure(
            {
                "unittitle": {
                    "collection": {"min_word_num": 5},
                    "unknown": {"inspect": False, "min_word_num": 0},
                }
            }
        )
        assert ei.configuration["unittitle"]["collection"]["min_word_num"] == 5
        assert (
            ei.configuration["unittitle"]["class"]
            == default_config["unittitle"]["class"]
        )

    def test_configure_level(self):
        ei = EADInspector()
        default_config = ei.configuration.copy()
        ei.configure_level(
            "unittitle",
            {
                "collection": {"min_word_num": 5},
                "class": {"inspect": 0, "min_word_num": "0"},
            },
        )
        assert ei.configuration["unittitle"]["collection"]["min_word_num"] == 5
        assert (
            ei.configuration["unittitle"]["collection"]["inspect"]
            == default_config["unittitle"]["collection"]["inspect"]
        )
        assert ei.configuration["unittitle"]["class"] == {
            "inspect": False,
            "min_word_num": 0,
        }
        assert (
            ei.configuration["unittitle"]["file"] == default_config["unittitle"]["file"]
        )
        assert ei.configuration["abstract"] == default_config["abstract"]
        ei.configuration = default_config.copy()
        ei.configure_level(
            "unittitle",
            {
                "collection": {"min_word_num": 5},
                "unknown": {"inspect": False, "min_word_num": 0},
            },
        )
        assert ei.configuration["unittitle"]["collection"]["min_word_num"] == 5
        assert (
            ei.configuration["unittitle"]["class"]
            == default_config["unittitle"]["class"]
        )

    def test_configure_setting(self):
        ei = EADInspector()
        default_config = ei.configuration.copy()
        ei.configure_setting("unittitle", "file", {"inspect": False})
        assert ei.configuration["unittitle"]["file"]["inspect"] == False
        ei.configure_setting("unittitle", "file", {"inspect": 0})
        assert ei.configuration["unittitle"]["file"]["inspect"] == False
        assert (
            ei.configuration["unittitle"]["file"]["min_word_num"]
            == default_config["unittitle"]["file"]["min_word_num"]
        )
        ei.configuration = default_config.copy()
        ei.configure_setting("unittitle", "file", {"unknown": 5})
        assert ei.configuration == default_config
        ei.configure_setting("genreform", "normal", ["Akten"])
        assert ei.configuration["genreform"]["normal"] == ["Akten"]
        assert (
            ei.configuration["genreform"]["class"]
            == default_config["genreform"]["class"]
        )

    def test_inspect_id(self):
        ei = EADInspector()
        assert ei.inspect_id(xml("<c id='test'></c>")) == "test"
        assert ei.inspect_id(xml("<c id='test'/>")) == "test"
        assert ei.inspect_id(xml("<c otherid='test'></c>")) == ei.error.miss_info()
        assert ei.inspect_id(xml("<c id=''></c>")) == ei.error.miss_info()
        assert ei.inspect_id(xml("<c></c>")) == ei.error.miss_info()
        assert ei.inspect_id(xml("<c/>")) == ei.error.miss_info()

    def test_inspect_unitid(self):
        ei = EADInspector()
        assert (
            ei.inspect_unitid(xml("<c><did><unitid>test</unitid></did></c>")) == "test"
        )
        assert (
            ei.inspect_unitid(xml("<c><did><unitid></unitid></did></c>"))
            == ei.error.miss_info()
        )
        assert (
            ei.inspect_unitid(xml("<c><did><unitid/></did></c>"))
            == ei.error.miss_info()
        )
        assert ei.inspect_unitid(xml("<c><did></did></c>")) == ei.error.miss_info()
        ei.configuration["unitid"]["pattern"] = r"^BBB \d{1,5}$"
        assert (
            ei.inspect_unitid(xml("<c><did><unitid>BBB 1</unitid></did></c>"))
            == "BBB 1"
        )
        assert (
            ei.inspect_unitid(xml("<c><did><unitid>BBB 12345</unitid></did></c>"))
            == "BBB 12345"
        )
        assert ei.inspect_unitid(
            xml("<c><did><unitid>BBB Z</unitid></did></c>")
        ) == ei.error.pattern("BBB Z")
        assert ei.inspect_unitid(
            xml("<c><did><unitid>BBB 123456</unitid></did></c>")
        ) == ei.error.pattern("BBB 123456")

    def test_inspect_text(self):
        ei = EADInspector()
        config = {"inspect": True, "min_word_num": 2}
        assert ei.inspect_text(xml("<elem>test test</elem>"), config) == None
        assert ei.error.miss_info() in ei.inspect_text(xml("<elem></elem>"), config)
        assert ei.error.miss_info() in ei.inspect_text(xml("<elem/>"), config)
        assert ei.error.short() in ei.inspect_text(xml("<elem>test</elem>"), config)
        assert ei.error.dupl_blanks() in ei.inspect_text(
            xml("<elem>test  test</elem>"), config
        )

    def test_inspect_unittitle(self):
        ei = EADInspector()
        ei.configuration["unittitle"]["_"] = {"inspect": True, "min_word_num": 2}
        assert (
            ei.inspect_unittitle(
                xml("<c><did><unittitle>test test</unittitle></did></c>"),
                "_",
            )
            == None
        )
        assert ei.error.miss_info() in ei.inspect_unittitle(
            xml("<c><did><unittitle></unittitle></did></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_unittitle(
            xml("<c><did><unittitle/></did></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_unittitle(
            xml("<c><did></did></c>"),
            "_",
        )
        assert ei.error.short() in ei.inspect_unittitle(
            xml("<c><did><unittitle>test</unittitle></did></c>"),
            "_",
        )
        assert ei.error.dupl_blanks() in ei.inspect_unittitle(
            xml("<c><did><unittitle>test  test</unittitle></did></c>"),
            "_",
        )

    def test_subordinate_unitdates(self):
        ei = EADInspector()
        assert ei.subordinate_unitdates(xml("<c></c>")) == {}
        assert ei.subordinate_unitdates(
            xml("<c><c><did><unitid>1</unitid></did></c></c>")
        ) == {"1": []}
        assert ei.subordinate_unitdates(
            xml(
                "<c><c><did><unitid>1</unitid><unitdate normal='2015-01-01'/></did></c></c>"
            )
        ) == {
            "1": [
                {
                    "earliest_date": date(2015, 1, 1),
                    "latest_date": date(2015, 1, 1),
                }
            ]
        }
        assert ei.subordinate_unitdates(
            xml(
                "<c><c><did><unitid>1</unitid><unitdate normal='2015-01-01'/><unitdate normal='2016-01-01'/></did></c></c>"
            )
        ) == {
            "1": [
                {
                    "earliest_date": date(2015, 1, 1),
                    "latest_date": date(2015, 1, 1),
                },
                {
                    "earliest_date": date(2016, 1, 1),
                    "latest_date": date(2016, 1, 1),
                },
            ]
        }
        assert ei.subordinate_unitdates(
            xml(
                "<c><c><did><unitid>1</unitid><unitdate normal='2015-01-01'/></did></c><c><did><unitid>2</unitid><unitdate normal='2016-01-01'/></did></c></c>"
            )
        ) == {
            "1": [
                {
                    "earliest_date": date(2015, 1, 1),
                    "latest_date": date(2015, 1, 1),
                }
            ],
            "2": [
                {
                    "earliest_date": date(2016, 1, 1),
                    "latest_date": date(2016, 1, 1),
                }
            ],
        }

    def test_normalized_unitdates(self):
        ei = EADInspector()
        assert ei.normalized_unitdates([xml("<unitdate normal='2015-01-01'/>")]) == [
            {
                "earliest_date": date(2015, 1, 1),
                "latest_date": date(2015, 1, 1),
            }
        ]
        assert ei.normalized_unitdates(
            [xml("<unitdate normal='2015-01-01/2015-01-15'/>")]
        ) == [
            {
                "earliest_date": date(2015, 1, 1),
                "latest_date": date(2015, 1, 15),
            }
        ]
        assert ei.normalized_unitdates(
            [
                xml("<unitdate normal='2015-01-01/2015-01-15'/>"),
                xml("<unitdate normal='2016-01-01/2016-01-15'/>"),
            ]
        ) == [
            {
                "earliest_date": date(2015, 1, 1),
                "latest_date": date(2015, 1, 15),
            },
            {
                "earliest_date": date(2016, 1, 1),
                "latest_date": date(2016, 1, 15),
            },
        ]

    def test_is_consistent_latest_date(self):
        ei = EADInspector()
        assert (
            ei.is_consistent_latest_date(
                {"earliest_date": date(2015, 1, 5), "latest_date": None},
                {"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 15)},
            )
            == True
        )
        assert (
            ei.is_consistent_latest_date(
                {"earliest_date": date(2015, 1, 5), "latest_date": date(2015, 1, 13)},
                {"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 15)},
            )
            == True
        )
        assert (
            ei.is_consistent_latest_date(
                {"earliest_date": date(2014, 1, 5), "latest_date": date(2015, 1, 15)},
                {"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 15)},
            )
            == True
        )
        assert (
            ei.is_consistent_latest_date(
                {"earliest_date": date(2015, 1, 5), "latest_date": date(2015, 1, 16)},
                {"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 15)},
            )
            == False
        )
        assert (
            ei.is_consistent_latest_date(
                {"earliest_date": date(2010, 1, 5), "latest_date": date(2016, 1, 16)},
                {"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 15)},
            )
            == False
        )

    def test_is_consistent_earliest_date(self):
        ei = EADInspector()
        assert (
            ei.is_consistent_earliest_date(
                {"earliest_date": None, "latest_date": date(2015, 1, 10)},
                {"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 15)},
            )
            == True
        )
        assert (
            ei.is_consistent_earliest_date(
                {"earliest_date": date(2015, 1, 5), "latest_date": date(2015, 1, 10)},
                {"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 15)},
            )
            == True
        )
        assert (
            ei.is_consistent_earliest_date(
                {"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 20)},
                {"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 15)},
            )
            == True
        )
        assert (
            ei.is_consistent_earliest_date(
                {"earliest_date": date(2014, 12, 31), "latest_date": date(2015, 1, 10)},
                {"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 15)},
            )
            == False
        )
        assert (
            ei.is_consistent_earliest_date(
                {"earliest_date": date(2010, 12, 16), "latest_date": date(2018, 1, 10)},
                {"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 15)},
            )
            == False
        )

    def test_is_consistent_date(self):
        ei = EADInspector()
        assert (
            ei.is_consistent_date(
                {"earliest_date": date(2015, 1, 5), "latest_date": date(2015, 1, 13)},
                [{"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 15)}],
            )
            == True
        )
        assert (
            ei.is_consistent_date(
                {"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 15)},
                [{"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 15)}],
            )
            == True
        )
        assert (
            ei.is_consistent_date(
                {"earliest_date": date(2015, 2, 2), "latest_date": date(2015, 2, 2)},
                [
                    {
                        "earliest_date": date(2015, 1, 1),
                        "latest_date": date(2015, 1, 15),
                    },
                    {
                        "earliest_date": date(2015, 2, 1),
                        "latest_date": date(2015, 2, 15),
                    },
                ],
            )
            == True
        )
        assert (
            ei.is_consistent_date(
                {"earliest_date": date(2014, 12, 15), "latest_date": date(2015, 1, 13)},
                [{"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 15)}],
            )
            == False
        )
        assert (
            ei.is_consistent_date(
                {"earliest_date": date(2015, 1, 13), "latest_date": date(2015, 1, 22)},
                [
                    {
                        "earliest_date": date(2015, 1, 1),
                        "latest_date": date(2015, 1, 15),
                    },
                    {
                        "earliest_date": date(2015, 1, 20),
                        "latest_date": date(2015, 2, 15),
                    },
                ],
            )
            == False
        )

    def test_inspect_sub_dating(self):
        ei = EADInspector()
        assert (
            ei.inspect_sub_dating(
                [{"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 15)}],
                "id",
                [{"earliest_date": date(2015, 1, 5), "latest_date": date(2015, 1, 13)}],
            )
            == []
        )
        assert (
            ei.inspect_sub_dating(
                [{"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 15)}],
                "id",
                [
                    {
                        "earliest_date": date(2015, 1, 1),
                        "latest_date": date(2015, 1, 1),
                    },
                    {
                        "earliest_date": date(2015, 1, 2),
                        "latest_date": date(2015, 1, 2),
                    },
                ],
            )
            == []
        )
        assert (
            ei.inspect_sub_dating(
                [
                    {
                        "earliest_date": date(2015, 1, 1),
                        "latest_date": date(2015, 1, 15),
                    },
                    {
                        "earliest_date": date(2016, 1, 1),
                        "latest_date": date(2016, 1, 15),
                    },
                ],
                "id",
                [
                    {
                        "earliest_date": date(2015, 1, 1),
                        "latest_date": date(2015, 1, 1),
                    },
                    {
                        "earliest_date": date(2015, 1, 2),
                        "latest_date": date(2015, 1, 2),
                    },
                    {
                        "earliest_date": date(2016, 1, 2),
                        "latest_date": date(2016, 1, 2),
                    },
                ],
            )
            == []
        )
        assert (
            ei.inspect_sub_dating(
                [{"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 15)}],
                "id",
                [{"earliest_date": date(2015, 1, 5), "latest_date": date(2015, 1, 17)}],
            )
            != []
        )
        assert (
            ei.inspect_sub_dating(
                [{"earliest_date": date(2015, 1, 1), "latest_date": date(2015, 1, 15)}],
                "id",
                [
                    {
                        "earliest_date": date(2015, 1, 1),
                        "latest_date": date(2015, 1, 1),
                    },
                    {
                        "earliest_date": date(2015, 1, 2),
                        "latest_date": date(2015, 2, 2),
                    },
                ],
            )
            != []
        )
        assert (
            ei.inspect_sub_dating(
                [
                    {
                        "earliest_date": date(2015, 1, 1),
                        "latest_date": date(2015, 1, 15),
                    },
                    {
                        "earliest_date": date(2016, 1, 1),
                        "latest_date": date(2016, 1, 15),
                    },
                ],
                "id",
                [
                    {
                        "earliest_date": date(2015, 1, 1),
                        "latest_date": date(2015, 1, 1),
                    },
                    {
                        "earliest_date": date(2015, 1, 2),
                        "latest_date": date(2015, 1, 2),
                    },
                    {
                        "earliest_date": date(2015, 1, 2),
                        "latest_date": date(2016, 1, 2),
                    },
                ],
            )
            != []
        )

    def test_inspect_unitdates_consistency(self):
        ei = EADInspector()
        assert (
            ei.inspect_unitdates_consistency(
                [
                    xml("<unitdate normal='2015-01-01'/>"),
                ],
                xml(
                    "<c><c><did><unitid>1</unitid><unitdate normal='2015-01-01'/></did></c></c>"
                ),
            )
            == []
        )
        assert (
            ei.inspect_unitdates_consistency(
                [
                    xml("<unitdate normal='2015-01-01/2015-01-15'/>"),
                ],
                xml(
                    "<c><c><did><unitid>1</unitid><unitdate normal='2015-01-01'/></did></c><c><did><unitid>2</unitid><unitdate normal='2015-01-15'/></did></c></c>"
                ),
            )
            == []
        )
        assert (
            ei.inspect_unitdates_consistency(
                [
                    xml("<unitdate normal='2015-01-01/2015-01-15'/>"),
                    xml("<unitdate normal='2016-01-01/2016-01-15'/>"),
                ],
                xml(
                    "<c><c><did><unitid>1</unitid><unitdate normal='2015-01-01'/></did></c><c><did><unitid>2</unitid><unitdate normal='2016-01-15'/></did></c></c>"
                ),
            )
            == []
        )
        assert (
            ei.inspect_unitdates_consistency(
                [
                    xml("<unitdate normal='2015-01-01'/>"),
                ],
                xml(
                    "<c><c><did><unitid>1</unitid><unitdate normal='2015-01-02'/></did></c></c>"
                ),
            )
            != []
        )
        assert (
            ei.inspect_unitdates_consistency(
                [
                    xml("<unitdate normal='2015-01-01/2015-01-15'/>"),
                ],
                xml(
                    "<c><c><did><unitid>1</unitid><unitdate normal='2015-01-01'/></did></c><c><did><unitid>2</unitid><unitdate normal='2016-01-15'/></did></c></c>"
                ),
            )
            != []
        )
        assert (
            ei.inspect_unitdates_consistency(
                [
                    xml("<unitdate normal='2015-01-01/2015-01-15'/>"),
                ],
                xml(
                    "<c><c><did><unitid>1</unitid><unitdate normal='2015-01-01/2015-01-30'/></did></c></c>"
                ),
            )
            != []
        )
        assert (
            ei.inspect_unitdates_consistency(
                [
                    xml("<unitdate normal='2015-01-01/2015-01-15'/>"),
                    xml("<unitdate normal='2016-01-01/2016-01-15'/>"),
                ],
                xml(
                    "<c><c><did><unitid>1</unitid><unitdate normal='2015-01-01/2016-01-10'/></did></c></c>"
                ),
            )
            != []
        )

    def test_normal_date_range(self):
        ei = EADInspector()
        assert ei.normal_date_range(xml("<elem normal='2015-01-01/2015-01-15'/>")) == {
            "earliest_date": date(2015, 1, 1),
            "latest_date": date(2015, 1, 15),
        }
        assert ei.normal_date_range(xml("<elem normal='2015-01-01/2015-01-01'/>")) == {
            "earliest_date": date(2015, 1, 1),
            "latest_date": date(2015, 1, 1),
        }
        assert ei.normal_date_range(xml("<elem/>")) == {
            "earliest_date": None,
            "latest_date": None,
        }
        assert ei.normal_date_range(xml("<elem normal='2015-01-01'/>")) == {
            "earliest_date": date(2015, 1, 1),
            "latest_date": date(2015, 1, 1),
        }
        assert ei.normal_date_range(xml("<elem normal='2015-01-01'/>")) != {
            "earliest_date": date(2015, 1, 1),
            "latest_date": None,
        }
        assert ei.normal_date_range(xml("<elem normal='2015-01-01'/>")) != {
            "earliest_date": None,
            "latest_date": date(2015, 1, 1),
        }

    def test_is_future(self):
        ei = EADInspector()
        assert (
            ei.is_future(
                {"earliest_date": date(3000, 1, 1), "latest_date": date(3000, 12, 31)}
            )
            == True
        )
        assert (
            ei.is_future(
                {"earliest_date": date(2000, 1, 1), "latest_date": date(3000, 12, 31)}
            )
            == True
        )
        assert (
            ei.is_future(
                {"earliest_date": date(2000, 1, 1), "latest_date": date(2000, 12, 31)}
            )
            == False
        )

    def test_inspect_date(self):
        ei = EADInspector()
        assert ei.inspect_date(xml("<elem normal='2015-01-01'/>")) == []
        assert ei.inspect_date(xml("<elem normal='2015-01-01/2015-01-15'/>")) == []
        assert ei.error.miss_norm_date("01.01.2015") in ei.inspect_date(
            xml("<elem>01.01.2015</elem>")
        )
        assert ei.error.miss_norm_date("01.01.2015") in ei.inspect_date(
            xml("<elem normal='01.01.2015'>01.01.2015</elem>")
        )
        assert ei.error.miss_norm_date("") in ei.inspect_date(
            xml("<elem normal='01.01.2015'/>")
        )
        assert ei.error.future("3000-01-01/3000-12-31") in ei.inspect_date(
            xml("<elem normal='3000-01-01/3000-12-31'/>")
        )
        assert ei.error.future("3000-01-01") in ei.inspect_date(
            xml("<elem normal='3000-01-01'/>")
        )

    def test_inspect_dates(self):
        ei = EADInspector()
        assert ei.inspect_dates([xml("<elem normal='2015-01-01'/>")]) == []
        assert ei.inspect_dates([xml("<elem normal='2015-01-01/2015-01-15'/>")]) == []
        assert (
            ei.inspect_dates(
                [
                    xml("<elem normal='2015-01-01/2015-01-15'/>"),
                    xml("<elem normal='2016-01-01/2016-01-15'/>"),
                ]
            )
            == []
        )
        assert ei.error.miss_norm_date("01.01.2015") in ei.inspect_dates(
            [xml("<elem>01.01.2015</elem>")]
        )
        assert ei.error.miss_norm_date("01.01.2015") in ei.inspect_dates(
            [xml("<elem normal='01.01.2015'>01.01.2015</elem>")]
        )
        assert ei.error.miss_norm_date("") in ei.inspect_dates(
            [xml("<elem normal='01.01.2015'/>")]
        )
        assert ei.error.miss_norm_date("01.01.2015") in ei.inspect_dates(
            [
                xml("<elem>01.01.2015</elem>"),
                xml("<elem>01.01.2016</elem>"),
            ]
        )
        assert ei.error.miss_norm_date("01.01.2016") not in ei.inspect_dates(
            [
                xml("<elem>01.01.2015</elem>"),
                xml("<elem normal='2016-01-01'>01.01.2016</elem>"),
            ]
        )

    def test_inspect_unitdates(self):
        ei = EADInspector()
        ei.configuration["unitdate"]["_"] = {"inspect": True}
        assert (
            ei.inspect_unitdates(
                xml(
                    "<c><did><unitdate normal='2015-01-01'/></did><c><did><unitid>1</unitid><unitdate normal='2015-01-01'/></did></c></c>"
                ),
                "_",
            )
            == None
        )
        assert (
            ei.inspect_unitdates(
                xml(
                    "<c><did><unitdate normal='2015-01-01/2015-01-15'/></did><c><did><unitid>1</unitid><unitdate normal='2015-01-01'/></did></c><c><did><unitid>2</unitid><unitdate normal='2015-01-15'/></did></c></c>"
                ),
                "_",
            )
            == None
        )
        assert ei.error.miss_info() in (
            ei.inspect_unitdates(
                xml("<c><did></did></c>"),
                "_",
            )
        )
        assert ei.error.miss_norm_date("01.01.2015") in (
            ei.inspect_unitdates(
                xml("<c><did><unitdate>01.01.2015</unitdate></did></c>"),
                "_",
            )
        )
        assert ei.error.inconsistent_date("2", "2016-01-15/2016-01-15") in (
            ei.inspect_unitdates(
                xml(
                    "<c><did><unitdate normal='2015-01-01/2015-01-15'/></did><c><did><unitid>1</unitid><unitdate normal='2015-01-01'/></did></c><c><did><unitid>2</unitid><unitdate normal='2016-01-15'/></did></c></c>"
                ),
                "_",
            )
        )
        assert ei.error.inconsistent_date("1", "2015-01-01/2016-01-15") in (
            ei.inspect_unitdates(
                xml(
                    "<c><did><unitdate normal='2015-01-01/2015-01-15'/></did><c><did><unitid>1</unitid><unitdate normal='2015-01-01/2016-01-15'/></did></c></c>"
                ),
                "_",
            )
        )

    def test_inspect_abstract(self):
        ei = EADInspector()
        ei.configuration["abstract"]["_"] = {"inspect": True, "min_word_num": 2}
        assert (
            ei.inspect_abstract(
                xml("<c><did><abstract>test test</abstract></did></c>"),
                "_",
            )
            == None
        )
        assert ei.error.miss_info() in ei.inspect_abstract(
            xml("<c><did><abstract></abstract></did></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_abstract(
            xml("<c><did><abstract/></did></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_abstract(
            xml("<c><did></did></c>"),
            "_",
        )
        assert ei.error.short() in ei.inspect_abstract(
            xml("<c><did><abstract>test</abstract></did></c>"),
            "_",
        )
        assert ei.error.dupl_blanks() in ei.inspect_abstract(
            xml("<c><did><abstract>test  test</abstract></did></c>"),
            "_",
        )

    def inspect_genreform(self):
        ei = EADInspector()
        ei.configuration["genreform"]["_"] = {"inspect": True}
        ei.configuration["genreform"]["normal"] = ["test"]
        assert (
            ei.inspect_genreform(
                xml(
                    "<c><did><physdesc><genreform normal='test'>test</genreform></physdesc></did></c>"
                ),
                "_",
            )
            == None
        )
        assert (
            ei.inspect_genreform(
                xml(
                    "<c><did><physdesc><genreform normal='test'/></physdesc></did></c>"
                ),
                "_",
            )
            == None
        )
        assert ei.error.miss_info() in ei.inspect_genreform(
            xml("<c><did><physdesc><genreform></genreform></physdesc></did></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_genreform(
            xml("<c><did><physdesc><genreform/></physdesc></did></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_genreform(
            xml("<c><did><physdesc></physdesc></did></c>"),
            "_",
        )
        assert ei.error.miss_norm_term() in ei.inspect_genreform(
            xml("<c><did><physdesc><genreform>test</genreform></physdesc></did></c>"),
            "_",
        )
        assert ei.error.miss_norm_term() in ei.inspect_genreform(
            xml(
                "<c><did><physdesc><genreform normal=''>test</genreform></physdesc></did></c>"
            ),
            "_",
        )
        assert ei.error.miss_norm_term() in ei.inspect_genreform(
            xml(
                "<c><did><physdesc><genreform normal='not normal'>test</genreform></physdesc></did></c>"
            ),
            "_",
        )

    def test_inspect_dimensions(self):
        ei = EADInspector()
        ei.configuration["dimensions"]["_"] = {"inspect": True}
        assert (
            ei.inspect_dimensions(
                xml(
                    "<c><did><physdesc><dimensions>test</dimensions></physdesc></did></c>"
                ),
                "_",
            )
            == None
        )
        assert ei.error.miss_info() in ei.inspect_dimensions(
            xml("<c><did><physdesc><dimensions></dimensions></physdesc></did></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_dimensions(
            xml("<c><did><physdesc><dimensions/></physdesc></did></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_dimensions(
            xml("<c><did><physdesc></physdesc></did></c>"),
            "_",
        )

    def test_inspect_extent(self):
        ei = EADInspector()
        ei.configuration["extent"]["_"] = {"inspect": True}
        assert (
            ei.inspect_extent(
                xml("<c><did><physdesc><extent>test</extent></physdesc></did></c>"),
                "_",
            )
            == None
        )
        assert ei.error.miss_info() in ei.inspect_extent(
            xml("<c><did><physdesc><extent></extent></physdesc></did></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_extent(
            xml("<c><did><physdesc><extent/></physdesc></did></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_extent(
            xml("<c><did><physdesc></physdesc></did></c>"),
            "_",
        )

    def test_inspect_scopecontent(self):
        ei = EADInspector()
        ei.configuration["scopecontent"]["_"] = {"inspect": True, "min_word_num": 4}
        assert (
            ei.inspect_scopecontent(
                xml(
                    "<c><scopecontent><head>test test</head><p>test test</p></scopecontent></c>"
                ),
                "_",
            )
            == None
        )
        assert ei.error.miss_info() in ei.inspect_scopecontent(
            xml("<c><scopecontent></scopecontent></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_scopecontent(
            xml("<c><scopecontent/></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_scopecontent(
            xml("<c></c>"),
            "_",
        )
        assert ei.error.short() in ei.inspect_scopecontent(
            xml(
                "<c><scopecontent><head>test test</head><p>test</p></scopecontent></c>"
            ),
            "_",
        )
        assert ei.error.dupl_blanks() in ei.inspect_scopecontent(
            xml(
                "<c><scopecontent><head>test  test</head><p>test test</p></scopecontent></c>"
            ),
            "_",
        )

    def test_inspect_origination(self):
        ei = EADInspector()
        ei.configuration["origination"]["_"] = {"inspect": True, "ref": True}
        assert (
            ei.inspect_origination(
                xml("<origination authfilenumber='1'>test</origination>"),
                "_",
            )
            == []
        )
        assert ei.error.empty_elem("origination") in ei.inspect_origination(
            xml("<origination></origination>"),
            "_",
        )
        assert ei.error.empty_elem("origination") in ei.inspect_origination(
            xml("<origination/>"),
            "_",
        )
        assert ei.error.miss_ref("test") in ei.inspect_origination(
            xml("<origination>test</origination>"),
            "_",
        )
        assert ei.error.miss_ref("test") in ei.inspect_origination(
            xml("<origination authfilenumber=''>test</origination>"),
            "_",
        )

    def test_inspect_originations(self):
        ei = EADInspector()
        ei.configuration["origination"]["_"] = {"inspect": True, "ref": True}
        assert (
            ei.inspect_originations(
                xml(
                    "<c><did><origination authfilenumber='1'>test</origination></did></c>"
                ),
                "_",
            )
            == None
        )
        assert ei.error.empty_elem("origination") in ei.inspect_originations(
            xml("<c><did><origination></origination></did></c>"),
            "_",
        )
        assert ei.error.empty_elem("origination") in ei.inspect_originations(
            xml("<c><did><origination/></did></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_originations(
            xml("<c><did></did></c>"),
            "_",
        )
        assert ei.error.miss_ref("test") in ei.inspect_originations(
            xml("<c><did><origination authfilenumber=''>test</origination></did></c>"),
            "_",
        )
        assert ei.error.miss_ref("test") in ei.inspect_originations(
            xml("<c><did><origination>test</origination></did></c>"),
            "_",
        )
        assert ei.error.miss_ref("test2") in ei.inspect_originations(
            xml(
                "<c><did><origination>test</origination><origination>test2</origination></did></c>"
            ),
            "_",
        )

    def test_inspect_materialspec(self):
        ei = EADInspector()
        ei.configuration["materialspec"]["_"] = {"inspect": True}
        assert (
            ei.inspect_materialspec(
                xml("<c><did><materialspec>test</materialspec></did></c>"),
                "_",
            )
            == None
        )
        assert ei.error.miss_info() in ei.inspect_materialspec(
            xml("<c><did><materialspec></materialspec></did></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_materialspec(
            xml("<c><did><materialspec/></did></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_extent(
            xml("<c><did></did></c>"),
            "_",
        )

    def test_inspect_language(self):
        ei = EADInspector()
        ei.configuration["language"]["_"] = {"inspect": True}
        assert (
            ei.inspect_language(
                xml(
                    "<c><did><langmaterial><language langcode='ger'>test</language></langmaterial></did></c>"
                ),
                "_",
            )
            == None
        )
        assert ei.error.miss_info() in ei.inspect_language(
            xml("<c><did><langmaterial><language></language></langmaterial></did></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_language(
            xml("<c><did><langmaterial><language/></langmaterial></did></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_extent(
            xml("<c><did><langmaterial></langmaterial></did></c>"),
            "_",
        )
        assert ei.error.miss_lang_code() in ei.inspect_language(
            xml(
                "<c><did><langmaterial><language langcode=''>test</language></langmaterial></did></c>"
            ),
            "_",
        )
        assert ei.error.miss_lang_code() in ei.inspect_language(
            xml(
                "<c><did><langmaterial><language>test</language></langmaterial></did></c>"
            ),
            "_",
        )

    def test_inspect_daogrp(self):
        ei = EADInspector()
        wrap = ["<daogrp xmlns:xlink='http://www.w3.org/1999/xlink'>", "</daogrp>"]
        assert (
            ei.inspect_daogrp(xml(f"{wrap[0]}<daoloc xlink:href='url'/>{wrap[1]}"))
            == []
        )
        assert ei.error.empty_elem("daogrp") in (
            ei.inspect_daogrp(xml(f"{wrap[0]}{wrap[1]}"))
        )
        assert ei.error.miss_link() in (
            ei.inspect_daogrp(xml(f"{wrap[0]}<daoloc xlink:href=''/>{wrap[1]}"))
        )
        assert ei.error.miss_link() in (
            ei.inspect_daogrp(xml(f"{wrap[0]}<daoloc/>{wrap[1]}"))
        )

    def test_inspect_daos(self):
        ei = EADInspector()
        wrap = ["<c xmlns:xlink='http://www.w3.org/1999/xlink'>", "</c>"]
        ei.configuration["digital_archival_object"]["_"] = {"inspect": True}
        assert (
            ei.inspect_daos(
                xml(f"{wrap[0]}<daogrp><daoloc xlink:href='url'/></daogrp>{wrap[1]}"),
                "_",
            )
            == None
        )
        assert ei.error.miss_info() in (
            ei.inspect_daos(xml(f"{wrap[0]}{wrap[1]}"), "_")
        )
        assert ei.error.empty_elem("daogrp") in (
            ei.inspect_daos(xml(f"{wrap[0]}<daogrp></daogrp>{wrap[1]}"), "_")
        )
        assert ei.error.empty_elem("daogrp") in (
            ei.inspect_daos(xml(f"{wrap[0]}<daogrp/>{wrap[1]}"), "_")
        )
        assert ei.error.miss_link() in (
            ei.inspect_daos(
                xml(f"{wrap[0]}<daogrp><daoloc xlink:href=''/></daogrp>{wrap[1]}"), "_"
            )
        )
        assert ei.error.miss_link() in (
            ei.inspect_daos(xml(f"{wrap[0]}<daogrp><daoloc/></daogrp>{wrap[1]}"), "_")
        )

    def test_inspect_indexentry(self):
        ei = EADInspector()
        ei.configuration["index"]["_"] = {"inspect": True, "ref": True, "min_num": 2}
        assert (
            ei.inspect_indexentry(
                xml(
                    "<indexentry><subject authfilenumber='1'>test</subject></indexentry>"
                ),
                "_",
            )
            == []
        )
        assert (
            ei.inspect_indexentry(
                xml(
                    "<indexentry><persname authfilenumber='1'>test</persname></indexentry>"
                ),
                "_",
            )
            == []
        )
        assert (
            ei.inspect_indexentry(
                xml(
                    "<indexentry><corpname authfilenumber='1'>test</corpname></indexentry>"
                ),
                "_",
            )
            == []
        )
        assert ei.error.empty_elem("subject") in ei.inspect_indexentry(
            xml("<indexentry><subject></subject></indexentry>"),
            "_",
        )
        assert ei.error.empty_elem("subject") in ei.inspect_indexentry(
            xml("<indexentry><subject/></indexentry>"),
            "_",
        )
        assert ei.error.miss_ref("test") in ei.inspect_indexentry(
            xml("<indexentry><subject>test</subject></indexentry>"),
            "_",
        )
        assert ei.error.miss_ref("test") in ei.inspect_indexentry(
            xml("<indexentry><subject authfilenumber=''>test</subject></indexentry>"),
            "_",
        )

    def test_inspect_index(self):
        ei = EADInspector()
        ei.configuration["index"]["_"] = {"inspect": True, "ref": True, "min_num": 2}
        assert (
            ei.inspect_index(
                xml(
                    "<c><index><indexentry><subject authfilenumber='1'>test</subject></indexentry><indexentry><subject authfilenumber='2'>test2</subject></indexentry></index></c>"
                ),
                "_",
            )
            == None
        )
        assert ei.error.empty_elem("subject") in ei.inspect_index(
            xml("<c><index><indexentry><subject/></indexentry></index></c>"),
            "_",
        )
        assert ei.error.empty_elem("subject") in ei.inspect_index(
            xml("<c><index><indexentry><subject></subject></indexentry></index></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_index(
            xml("<c><index></index></c>"),
            "_",
        )
        assert ei.error.miss_info() in ei.inspect_index(
            xml("<c><index/></c>"),
            "_",
        )
        assert ei.error.empty_elem("indexentry") in ei.inspect_index(
            xml("<c><index><indexentry/></index></c>"),
            "_",
        )
        assert ei.error.empty_elem("indexentry") in ei.inspect_index(
            xml("<c><index><indexentry></indexentry></index></c>"),
            "_",
        )
        assert ei.error.miss_ref("test") in ei.inspect_index(
            xml(
                "<c><index><indexentry><subject authfilenumber=''>test</subject></indexentry></index></c>"
            ),
            "_",
        )
        assert ei.error.miss_ref("test") in ei.inspect_index(
            xml(
                "<c><index><indexentry><subject>test</subject></indexentry></index></c>"
            ),
            "_",
        )
        assert ei.error.miss_ref("test2") in ei.inspect_index(
            xml(
                "<c><index><indexentry><subject>test</subject></indexentry><indexentry><subject>test2</subject></indexentry></index></c>"
            ),
            "_",
        )
        assert ei.error.few() in ei.inspect_index(
            xml(
                "<c><index><indexentry><subject>test</subject></indexentry></index></c>"
            ),
            "_",
        )

    def test_inspect_userestrict(self):
        ei = EADInspector()
        ei.configuration["userestrict"]["_"] = {"inspect": True, "ref": True}
        ei.rights_ead = None
        assert (
            ei.inspect_userestrict(
                xml(
                    "<c xmlns:xlink='http://www.w3.org/1999/xlink'><userestrict type='ead'><p><extref xlink:href='1'>test</extref></p></userestrict></c>"
                ),
                "_",
            )
            == None
        )
        assert (
            ei.inspect_userestrict(
                xml(
                    "<c><userestrict type='ead'><p><extref>test</extref></p></userestrict></c>"
                ),
                "_",
            )
            == None
        )
        assert (
            ei.inspect_userestrict(
                xml(
                    "<c xmlns:xlink='http://www.w3.org/1999/xlink'><userestrict type='ead'><p><extref xlink:href='1'/></p></userestrict></c>"
                ),
                "_",
            )
            == None
        )
        assert ei.error.miss_rights("EAD") in ei.inspect_userestrict(
            xml(
                "<c xmlns:xlink='http://www.w3.org/1999/xlink'><userestrict type='ead'><p><extref xlink:href=''></extref></p></userestrict></c>"
            ),
            "_",
        )
        assert ei.error.miss_rights("EAD") in ei.inspect_userestrict(
            xml(
                "<c xmlns:xlink='http://www.w3.org/1999/xlink'><userestrict type='ead'></userestrict></c>"
            ),
            "_",
        )
        assert ei.error.miss_rights("EAD") in ei.inspect_userestrict(
            xml(
                "<c xmlns:xlink='http://www.w3.org/1999/xlink'><userestrict><p><extref xlink:href='1'>test</extref></p></userestrict></c>"
            ),
            "_",
        )
        ei.rights_ead = xml("<extref>test</extref>")
        assert (
            ei.inspect_userestrict(
                xml("<c></c>"),
                "_",
            )
            == None
        )


if __name__ == "__main__":
    pytest.main()
