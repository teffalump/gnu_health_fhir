from pendulum import instance, parse
from fhirclient.models.condition import Condition as fhir_condition
from .base import BaseAdapter

__all__ = ["Condition"]


class Condition(BaseAdapter):
    @classmethod
    def to_fhir_object(cls, condition):
        # TODO verificationStatus No corresponding Health equivalent (I think?)
        jsondict = {}
        jsondict["subject"] = cls.build_fhir_subject(condition)
        jsondict["asserter"] = cls.build_fhir_asserter(condition)
        jsondict["assertedDate"] = cls.build_fhir_asserted_date(condition)
        jsondict["note"] = cls.build_fhir_note(condition)
        jsondict["code"] = cls.build_fhir_code(condition)
        jsondict["severity"] = cls.build_fhir_severity(condition)
        # jsondict["verificationStatus"] = cls.build_fhir_verificationStatus(condition)
        jsondict["abatementDateTime"] = cls.build_fhir_abatement_datetime(condition)
        return fhir_condition(jsondict=jsondict)

    @classmethod
    def get_fhir_resource_type(cls):
        return "Condition"

    @classmethod
    def get_fhir_object_id_from_gh_object(cls, condition):
        return condition.id

    @classmethod
    def build_fhir_subject(cls, condition):
        patient = condition.name
        if patient:
            return {
                "display": patient.rec_name,
                "reference": "".join(["Patient/", str(patient.id)]),
            }

    @classmethod
    def build_fhir_asserter(cls, condition):
        asserter = condition.healthprof
        if asserter:
            return {
                "display": asserter.rec_name,
                "reference": "".join(["Practitioner/", str(asserter.id)]),
            }

    @classmethod
    def build_fhir_asserted_date(cls, condition):
        if condition.diagnosed_date:
            return parse(str(condition.diagnosed_date)).to_iso8601_string()

    @classmethod
    def build_fhir_note(cls, condition):
        # Add comments about specific food allergy here, too
        allergies = {
            "da": "Drug Allergy",
            "fa": "Food Allergy",
            "ma": "Misc Allergy",
            "mc": "Misc Contraindication",
        }
        notes = []
        if condition.allergy_type:
            notes.append({"text": allergies.get(condition.allergy_type)})
        if condition.short_comment:
            notes.append({"text": condition.short_comment})
        if condition.extra_info:
            notes.append({"text": condition.extra_info})
        if notes:
            return notes

    @classmethod
    def build_fhir_abatement_datetime(cls, condition):
        if condition.healed_date:
            return instance(condition.healed_date).to_iso8601_string()

    @classmethod
    def build_fhir_severity(cls, condition):
        # TODO Make config / helper
        severity = condition.disease_severity
        if severity:
            # These are the snomed codes
            sev = {
                "1_mi": ("Mild", "255604002"),
                "2_mo": ("Moderate", "6736007"),
                "3_sv": ("Severe", "24484000"),
            }
            t = sev.get(severity)
            if t:
                return cls.build_codeable_concept(t[1], "http://snomed.info/sct", t[0])

    @classmethod
    def build_fhir_code(cls, condition):
        code = condition.pathology
        if code:
            return cls.build_codeable_concept(
                code.code, "urn:oid:2.16.840.1.113883.6.90", code.name  # ICD-10-CM
            )
