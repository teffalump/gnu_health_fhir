from fhirclient.models.immunization import Immunization as fhir_immunization
from pendulum import instance
from .base import BaseAdapter
from .utils import safe_attrgetter
from ..converters import immunizationRoute, immunizationSite
from .patient_adapter import Patient
from .practitioner_adapter import Practitioner

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
        jsondict["patient"] = cls.build_fhir_patient(vaccination)
        jsondict["practitioner"] = cls.build_fhir_practitioner(vaccination)
        jsondict["lotNumber"] = cls.build_fhir_lot_number(vaccination)
        jsondict["expirationDate"] = cls.build_fhir_expiration_date(vaccination)
        jsondict["doseQuantity"] = cls.build_fhir_dose_quantity(vaccination)
        jsondict["note"] = cls.build_fhir_note(vaccination)
        jsondict["route"] = cls.build_fhir_route(vaccination)
        jsondict["site"] = cls.build_fhir_site(vaccination)
        jsondict["vaccineCode"] = cls.build_fhir_vaccine_code(vaccination)
        jsondict["primarySource"] = cls.build_fhir_primary_source(vaccination)
        jsondict["vaccinationProtocol"] = cls.build_fhir_vaccination_protocol(
            vaccination
        )
        return fhir_immunization(jsondict=jsondict)

    @classmethod
    def get_fhir_resource_type(cls):
        return "Immunization"

    @classmethod
    def get_fhir_object_id_from_gh_object(cls, vaccination):
        return vaccination.id

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
        return cls.build_fhir_reference_from_adapter_and_object(
            Patient, vaccination.name
        )

    @classmethod
    def build_fhir_practitioner(cls, vaccination):
        return [
            {
                "actor": cls.build_fhir_reference_from_adapter_and_object(
                    Practitioner, vaccination.healthprof
                )
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

    @classmethod
    def build_fhir_primary_source(cls, vaccination):
        # DEBUG If there is no attached administered healthprof,
        #   AND no reasonable documents then self-reported (?)
        administer = vaccination.healthprof
        asserter = vaccination.signed_by
        if administer is None and asserter is None:
            # return {"text": "Self-reported"}, False
            # jsondict["reportOrigin"] = {"text": "Self-reported"}
            # jsondict["primarySource"] = False
            return False
        else:
            # don't need to populate if primary source per standard
            return True

    @classmethod
    def build_fhir_route(cls, vaccination):
        route = vaccination.admin_route

        if route:
            ir = [i for i in immunizationRoute.contents if i["code"] == route.upper()]
            if ir:
                return cls.build_codeable_concept(
                    code=ir[0]["code"], text=ir[0]["display"]
                )

    @classmethod
    def build_fhir_site(cls, vaccination):
        site = vaccination.admin_site
        if site:
            m = [i for i in immunizationSite.contents if i["code"] == site.upper()]
            if m:
                return cls.build_codeable_concept(
                    code=m[0]["code"], text=m[0]["display"]
                )

    @classmethod
    def build_fhir_vaccine_code(cls, vaccination):
        # TODO Better coding information
        type_ = vaccination.vaccine
        if type_:
            return cls.build_codeable_concept(code=type_.name.code, text=type_.rec_name)

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
