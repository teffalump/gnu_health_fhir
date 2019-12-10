from fhirclient.models.immunization import Immunization as fhir_immunization
from pendulum import instance
from .base import BaseAdapter
from .utils import safe_attrgetter
from ..value_sets import immunizationRoute, immunizationSite

__all__ = ["Immunization"]


class Immunization(BaseAdapter):

    @classmethod
    def to_fhir_object(cls, vaccination):
        # TODO reaction - Must be reference in standard, but stored as text
        jsondict = {}
        jsondict["identifier"] = cls.build_fhir_identifier(vaccination)
        jsondict["date"] = cls.build_fhir_date(vaccination)
        jsondict["notGiven"] = cls.build_fhir_not_given(vaccination)
        jsondict["status"] = cls.build_fhir_status(vaccination)
        jsondict["patient"] = cls.build_fhir_status(vaccination)
        jsondict["practitioner"] = cls.build_fhir_practitioner(vaccination)
        jsondict["lotNumber"] = cls.build_fhir_lot_number(vaccination)
        jsondict["expirationDate"] = cls.build_fhir_expiration_date(vaccination)
        jsondict["doseQuantity"] = cls.build_fhir_dose_quantity(vaccination)
        jsondict["note"] = cls.build_fhir_note(vaccination)
        jsondict["route"] = cls.build_fhir_route(vaccination)
        jsondict["site"] = cls.build_fhir_site(vaccination)
        jsondict["vaccineCode"] = cls.build_fhir_vaccine_code(vaccination)
        jsondict["vaccinationProtocol"] = cls.build_fhir_vaccination_protocol(vaccination)
        return fhir_immunization(jsondict=jsondict)

    @classmethod
    def build_fhir_identifier(cls, vaccination):
       return [
            {
                "use": "official",
                "value": "-".join([vaccination.vaccine.rec_name, str(vaccination.id)]),
            }
        ]

    @classmethod
    def build_fhir_date(cls, vaccination):
        date = vaccination.date
        if date:
            return instance(date).to_iso8601_string()

    @classmethod
    def build_fhir_not_given(cls, vaccination):
        # TODO Is there a field for this in Health (?)
        return False

    @classmethod
    def build_fhir_status(cls, vaccination):
        status = vaccination.state
        if status == "in_progress":
            g = "in-progress"
        elif status == "done":
            g = "completed"
        else:
            g = None
        return g

    @classmethod
    def build_fhir_patient(cls, vaccination):
        patient = vaccination.name
        if patient:
            return {
                "display": patient.rec_name,
                "reference": "".join(["Patient/", str(patient.id)]),
            }

    @classmethod
    def build_fhir_practitioner(cls, vaccination):
        practitioner = vaccination.healthprof
        if practitioner:
            return [
                {
                    "actor": {
                        "display": practitioner.rec_name,
                        "reference": "".join(["Practitioner/", str(practitioner.id)]),
                    }
                }
            ]

    @classmethod
    def build_fhir_lot_number(cls, vaccination):
        number = safe_attrgetter(vaccination, "lot.number")
        if number:
            return str(number)

    @classmethod
    def build_fhir_expiration_date(cls, vaccination):
        date = safe_attrgetter(vaccination, "lot.expiration_date")
        if date:
            return instance(date).to_iso8601_string()

    @classmethod
    def build_fhir_dose_quantity(cls, vaccination):
        quantity = vaccination.amount
        if quantity is not None:
            return {
                "value": quantity,
                "unit": "mL",
                "system": "http://snomed.info/sct",
                "code": "258773002",
            }

    @classmethod
    def build_fhir_note(cls, vaccination):
        notes = vaccination.observations
        if notes:
            return {"text": notes}

        # reportOrigin and primarySource
        # DEBUG If there is no attached administered healthprof,
        #   AND no reasonable documents then self-reported (?)
        administer = vaccination.healthprof
        asserter = vaccination.signed_by
        if administer is None and asserter is None:
            jsondict["reportOrigin"] = {"text": "Self-reported"}
            jsondict["primarySource"] = False
        else:
            # don't need to populate if primary source per standard
            # cc = {'text': 'Health professional asserter'}
            jsondict["primarySource"] = True

    @classmethod
    def build_fhir_route(cls, vaccination):
        route = vaccination.admin_route

        if route:
            ir = [i for i in immunizationRoute.contents if i["code"] == route.upper()]
            if ir:
                cc = {}
                c = {}
                c["display"] = cc["text"] = ir[0]["display"]
                c["code"] = ir[0]["code"]
                cc["coding"] = [c]
                return cc

    @classmethod
    def build_fhir_site(cls, vaccination):
        site = vaccination.admin_site
        if site:
            m = [i for i in immunizationSite.contents if i["code"] == site.upper()]
            if m:
                cc = {}
                c = {}
                c["display"] = cc["text"] = m[0]["display"]
                c["code"] = m[0]["code"]
                cc["coding"] = [c]
                return cc

    @classmethod
    def build_fhir_vaccine_code(cls, vaccination):
        # TODO Need better coding, much better!
        type_ = vaccination.vaccine
        if type_:
            cc = {}
            c = {}
            c["display"] = cc["text"] = type_.rec_name
            if type_.name.code:
                c["code"] = type_.name.code
                cc["coding"] = [c]
            return cc


    @classmethod
    def build_fhir_vaccination_protocol(cls, vaccination):
        # TODO Better vaccine coding/info
        seq = vaccination.dose
        authority = vaccination.institution
        disease = safe_attrgetter(vaccination, "vaccine.indications")  # DEBUG
        description = vaccination.observations
        if seq:
            vp = {"doseSequence": seq, "description": description}

            ref = {
                "display": safe_attrgetter(authority, "name.rec_name"),
                "reference": "".join(["Institution/", str(authority.id)]),
            }

            target = {"text": disease}

            # Unclear if equivalent concept in Health
            status = {"text": "Counts"}
            # coding = Coding(code='count',
            # display='Counts')
            # status.coding = [coding]
            vp["doseStatus"] = status
            vp["authority"] = ref
            vp["targetDisease"] = [target]
            return [vp]
