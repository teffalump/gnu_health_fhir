from fhirclient.models.familymemberhistory import FamilyMemberHistory as fhir_fmh
from pendulum import instance
from .base import BaseAdapter
from ..value_sets import familyMember

__all__ = ["FamilyMemberHistory"]


class FamilyMemberHistory(BaseAdapter):

    @classmethod
    def to_fhir_object(cls, member):
        # TODO Add more info to family history data model on Health side
        jsondict = {}
        jsondict["gender"] = cls.build_fhir_gender(member)
        jsondict["date"] = cls.build_fhir_date(member)
        jsondict["patient"] = cls.build_fhir_patient(member)
        jsondict["relationship"] = cls.build_fhir_relationship(member)
        jsondict["status"] = cls.build_fhir_status(member)
        jsondict["condition"] = cls.build_fhir_condition(member)
        return fhir_fmh(jsondict=jsondict)

    @classmethod
    def build_fhir_gender(cls, member):
        # TODO Turn into helper / config
        ### NOTE KEEP THIS UPDATED ###
        # Possible selections (currently)
        #
        # Female
        # 'mother'
        # 'sister'
        # 'aunt'
        # 'niece'
        # 'grandmother'
        #
        # Male
        # 'father'
        # 'brother'
        # 'uncle'
        # 'nephew'
        # 'grandfather'
        #
        # Unknown
        # 'cousin'

        females = ["mother", "sister", "aunt", "niece", "grandmother"]
        males = ["father", "brother", "uncle", "nephew", "grandfather"]
        rel = member.relative
        if rel in females:
            g = "female"
        elif rel in males:
            g = "male"
        else:
            g = "unknown"
        return g

    @classmethod
    def build_fhir_date(cls, member):
        date = member.write_date or member.create_date
        if date:
            return instance(date).to_iso8601_string()

    @classmethod
    def build_fhir_patient(cls, member):
        patient = member.patient
        if patient:
            return {
                "display": patient.rec_name,
                "reference": "".join(["Patient/", str(patient.id)]),
            }


    @classmethod
    def build_fhir_relationship(cls, member):
        if member:
            cc = {}
            c = {}

            t = {"m": "maternal", "f": "paternal"}  # ignore sibling code
            k = " ".join((t.get(member.xory, ""), member.relative)).strip()
            info = [d for d in familyMember.contents if d["display"] == k]

            if info:
                c["code"] = info[0]["code"]
                c["system"] = info[0]["system"]
            cc["text"] = c["display"] = k
            cc["coding"] = [c]
            return cc

    @classmethod
    def build_fhir_status(cls, member):
        # TODO Unknown equivalent in Health
        return "completed"

    @classmethod
    def build_fhir_condition(cls, member):
        path = member.name
        if path:
            code = {}
            coding = {
                "code": path.code,
                "system": "urn:oid:2.16.840.1.113883.6.90",
            }  # ICD-10-CM
            code["text"] = coding["display"] = path.name
            code["coding"] = [coding]
            return [{"code": code}]
