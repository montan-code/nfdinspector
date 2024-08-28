class Error:
    """Class with various error messages for the metadata inspections"""

    def __init__(self, language: str) -> None:
        """
        Construct Error with specific language.

        :param language: Error language for the inspections.
        :type language: str
        """
        self._language: str = language

    @property
    def language(self) -> str:
        """Get and set the language for the error messages."""
        return self._language

    @language.setter
    def language(self, language) -> None:
        self._language = language

    def miss_info(self) -> str:
        """
        Get error message for missing information.

        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return "missing information"
            case "de":
                return "Angabe fehlt"
            case _:
                return "missing information"

    def empty_elem(self, tag: str) -> str:
        """
        Get error message for empty XML element.

        :param tag: Tag of the concerned element
        :type tag: str
        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"empty element ({tag})"
            case "de":
                return f"leeres Element ({tag})"
            case _:
                return f"empty element ({tag})"

    def miss_label(self, id: str) -> str:
        """
        Get error message for missing label.

        :param id: ID of the concerned entity
        :type id: str
        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"missing label ({id})"
            case "de":
                return f"Bezeichnung fehlt ({id})"
            case _:
                return f"missing label ({id})"

    def miss_ref(self, label: str) -> str:
        """
        Get error message for missing reference/ID.

        :param label: Label of the concerned entity
        :type label: str
        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"missing reference/ID ({label})"
            case "de":
                return f"Verweis/ID fehlt ({label})"
            case _:
                return f"missing reference/ID ({label})"

    def not_uniq(self) -> str:
        """
        Get error message for text that is not unique.

        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"not unique"
            case "de":
                return f"nicht einzigartig"
            case _:
                return f"not unique"

    def dupl_text(self) -> str:
        """
        Get error message for duplicate text.

        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"duplicate text"
            case "de":
                return f"duplizierter Text"
            case _:
                return f"duplicate text"

    def dist(self, compare: str) -> str:
        """
        Get error message for missing distinction.

        :param compare: Comparison
        :type compare: str
        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"not distinct from {compare}"
            case "de":
                return f"kein Unterschied zu {compare}"
            case _:
                return f"not distinct from {compare}"

    def short(self) -> str:
        """
        Get error message for shortness.

        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return "too short"
            case "de":
                return "zu kurz"
            case _:
                return "too short"

    def long(self) -> str:
        """
        Get error message for length.

        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return "too long"
            case "de":
                return "zu lang"
            case _:
                return "too long"

    def miss_mat(self) -> str:
        """
        Get error message for missing explicit material.

        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return "missing explicit material"
            case "de":
                return "explizites Material fehlt"
            case _:
                return "missing explicit material"

    def miss_tech(self) -> str:
        """
        Get error message for missing explicit technique.

        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return "missing explicit technique"
            case "de":
                return "explizite Technik fehlt"
            case _:
                return "missing explicit technique"

    def miss_meas_type(self) -> str:
        """
        Get error message for missing measurement type.

        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return "missing measurement type"
            case "de":
                return "Messgröße fehlt"
            case _:
                return "missing measurement type"

    def miss_meas_unit(self, meas_type: str) -> str:
        """
        Get error message for missing measurement unit.

        :param meas_type: Measurement type
        :type meas_type: str
        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"missing measurement unit ({meas_type})"
            case "de":
                return f"Maßeinheit fehlt ({meas_type})"
            case _:
                return f"missing measurement unit ({meas_type})"

    def miss_meas_value(self, meas_type: str) -> str:
        """
        Get error message for missing measurement value.

        :param meas_type: Measurement type
        :type meas_type: str
        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"missing measurement value ({meas_type})"
            case "de":
                return f"Messwert fehlt ({meas_type})"
            case _:
                return f"missing measurement value ({meas_type})"

    def miss_event_type(self) -> str:
        """
        Get error message for missing event type.

        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return "missing event type"
            case "de":
                return "Eventtyp fehlt"
            case _:
                return "missing event type"

    def miss_event_info(self, event_type: str) -> str:
        """
        Get error message for missing event info.

        :param event_type: Event type
        :type event_type: str
        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"missing actor, place or date ({event_type})"
            case "de":
                return f"Akteur:in, Ort oder Datierung fehlen ({event_type})"
            case _:
                return f"missing actor, place or date ({event_type})"

    def miss_actor(self, event_type: str) -> str:
        """
        Get error message for missing actor.

        :param event_type: Event type
        :type event_type: str
        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"missing actor ({event_type})"
            case "de":
                return f"Akteur:in fehlt ({event_type})"
            case _:
                return f"missing actor ({event_type})"

    def miss_place(self, event_type: str) -> str:
        """
        Get error message for missing place.

        :param event_type: Event type
        :type event_type: str
        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"missing place ({event_type})"
            case "de":
                return f"Ort fehlt ({event_type})"
            case _:
                return f"missing place ({event_type})"

    def future(self, date: str) -> str:
        """
        Get error message for date in future.

        :param date: Date string
        :type date: str
        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"date in future ({date})"
            case "de":
                return f"Datum liegt in der Zukunft ({date})"
            case _:
                return f"date in future ({date})"

    def miss_date(self, event_type: str) -> str:
        """
        Get error message for missing date.

        :param event_type: Event type
        :type event_type: str
        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"missing date ({event_type})"
            case "de":
                return f"Datierung fehlt ({event_type})"
            case _:
                return f"missing date ({event_type})"

    def miss_norm_date(self, text_date: str) -> str:
        """
        Get error message for missing normalized date.

        :param text_date: Date as text
        :type text_date: str
        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"missing normalized (ISO-8601) date ({text_date})"
            case "de":
                return f"normalisierte (ISO-8601) Datierung fehlt ({text_date})"
            case _:
                return f"missing normalized (ISO-8601) date ({text_date})"

    def miss_earl_date(self, event_type: str) -> str:
        """
        Get error message for missing earliest date.

        :param event_type: Event type
        :type event_type: str
        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"missing earliest date ({event_type})"
            case "de":
                return f"Anfangsdatum fehlt ({event_type})"
            case _:
                return f"missing earliest date ({event_type})"

    def miss_lat_date(self, event_type: str) -> str:
        """
        Get error message for missing latest date.

        :param event_type: Event type
        :type event_type: str
        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"missing latest date ({event_type})"
            case "de":
                return f"Enddatum fehlt ({event_type})"
            case _:
                return f"missing latest date ({event_type})"

    def miss_norm_term(self, term: str) -> str:
        """
        Get error message for missing normalized term.

        :param term: Term that is not normalized
        :type term: str
        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"missing normalized term ({term})"
            case "de":
                return f"normalisierter Begriff fehlt ({term})"
            case _:
                return f"missing normalized term ({term})"

    def few(self) -> str:
        """
        Get error message for too few entries.

        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return "too few entries"
            case "de":
                return "zu wenige Einträge"
            case _:
                return "too few entries"

    def miss_link(self) -> str:
        """
        Get error message for missing link.

        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return "missing link"
            case "de":
                return "Link fehlt"
            case _:
                return "missing link"

    def miss_lang_code(self) -> str:
        """
        Get error message for missing language code.

        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return "missing language code"
            case "de":
                return "Sprachcode fehlt"
            case _:
                return "missing language code"

    def miss_rights(self, add: str) -> str:
        """
        Get error message for missing rights statement.

        :param add: Additional information
        :type add: str
        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"missing rights statement ({add})"
            case "de":
                return f"Rechteangabe fehlt ({add})"
            case _:
                return f"missing rights statement ({add})"

    def miss_res_type(self, add: str) -> str:
        """
        Get error message for missing resource type.

        :param add: Additional information
        :type add: str
        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"missing resource type ({add})"
            case "de":
                return f"Ressourcentyp fehlt ({add})"
            case _:
                return f"missing resource type ({add})"

    def dupl_blanks(self) -> str:
        """
        Get error message for duplicate blanks.

        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return "duplicate blanks"
            case "de":
                return "doppelte Leerzeichen"
            case _:
                return "duplicate blanks"

    def inconsistent_date(self, id: str, inconsistency: str) -> str:
        """
        Get error message for missing inconsistent date.

        :param id: ID of concerned file
        :type id: str
        :param inconsistency: Inconsistent date
        :type inconsistency: str
        :return: Error message
        :rtype: str
        """
        match self.language:
            case "en":
                return f"inconsistent date ({id}: {inconsistency})"
            case "de":
                return f"inkonsistente Datierung ({id}: {inconsistency})"
            case _:
                return f"inconsistent date ({id}: {inconsistency})"
