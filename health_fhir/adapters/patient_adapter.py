from .utils import safe_attrgetter
from pendulum import instance
from fhirclient.models import patient as fhir_patient
from .base import BaseAdapter
from .value_sets import maritalStatus as ms
from re import sub

__all__ = ["Patient"]


class Patient(BaseAdapter):

    @classmethod
    def toFhirObject(cls, patient):
        # TODO Add general_info field - where appropriate?
        # TODO Link - other links to same person
        # TODO Photo - Figure out contentType of photo
        # TODO managingOrganization
        jsondict = {}
        jsondict["identifier"] = cls.buildFhirIdentifier(patient)
        jsondict["name"] = cls.buildFhirName(patient)
        jsondict["telecom"] = cls.buildFhirTelecom(patient)
        jsondict["birthDate"] = cls.buildFhirBirthDate(patient)
        jsondict["deceasedBoolean"] = cls.buildFhirDeceasedBoolean(patient)
        jsondict["deceasedDateTime"] = cls.buildFhirDeceasedDateTime(patient)
        jsondict["address"] = cls.buildFhirAddress(patient)
        jsondict["gender"] = cls.buildFhirGender(patient)
        jsondict["generalPractitioner"] = cls.buildFhirGeneralPractitioner(patient)
        jsondict["active"] = cls.buildFhirActive(patient)
        jsondict["maritalStatus"] = cls.buildFhirMaritalStatus(patient)
        jsondict["communication"] = cls.buildFhirCommunication(patient)
        return fhir_patient.Patient(jsondict=jsondict)

    @classmethod
    def buildFhirIdentifier(cls, patient):
        idents = []
        if patient.puid:
            i = {}
            i["use"] = "usual"
            i["value"] = patient.puid or "<UNKNOWN>"
            i["type"] = {"text": "PUID/MRN"}
            idents.append(i)

        for alt in patient.name.alternative_ids:
            i = {}
            i["use"] = "official"
            i["value"] = alt.code or "<UNKNOWN>"
            i["type"] = {"text": alt.alternative_id_type}
            idents.append(i)

        return idents

    @classmethod
    def buildFhirName(cls, patient):
        # TODO Make helper function
        names = []
        for name in patient.name.person_names:
            n = {}
            n["given"] = [x for x in name.given.split()]
            n["family"] = name.family if name.family else "<unknown>"
            n["prefix"] = [name.prefix] if name.prefix else []
            n["suffix"] = [name.suffix] if name.suffix else []
            n["use"] = name.use if name.use else "<unknown>"
            if name.date_from:
                n["period"] = {"start": instance(name.date_from).to_iso8601_string()}
                if name.date_to:
                    n["period"]["end"] = instance(name.date_to).to_iso8601_string()
            names.append(n)
        return names

    @classmethod
    def buildFhirTelecom(cls, patient):
        # TODO Make helper function
        telecom = []
        for contact in patient.name.contact_mechanisms:
            c = {}
            c["value"] = contact.value
            if contact.type == "phone":
                c["system"] = "phone"
                c["use"] = "home"
            elif contact.type == "mobile":
                c["system"] = "phone"
                c["use"] = "mobile"
            else:
                c["use"] = c["system"] = contact.type
            telecom.append(c)

        return telecom

    @classmethod
    def buildFhirGender(cls, patient):
        # Gender
        # NOTE This is a difficult decision - what is gender for record-keeping
        # Currently, simply take biological sex and make further decisions later
        bs = patient.biological_sex
        g = None
        if bs:
            if bs == "f":
                g = "female"
            elif bs == "m":
                g = "male"
            else:
                g = "other"

        else:
            g = "unknown"
        return g

    @classmethod
    def buildFhirBirthDate(cls, patient):
        try:
            return instance(patient.name.dob).to_iso8601_string()
        except:
            return None

    @classmethod
    def buildFhirDeceasedBoolean(cls, patient):
        return patient.deceased

    @classmethod
    def buildFhirDeceasedDateTime(cls, patient):
        try:
            return instance(patient.dod).to_iso8601_string()
        except:
            return None

    @classmethod
    def buildFhirAddress(cls, patient):
        # Only one currently
        du = patient.name.du
        if du:
            ad = {}
            ad["use"] = "home"
            ad["type"] = "physical"  # TODO Check for this
            ad["text"] = patient.name.du_address
            line = []
            number, street, zip_, city, state, country = safe_attrgetter(
                du,
                "address_street_number",
                "address_street",
                "address_zip",
                "address_city",
                "address_subdivision.name",
                "address_country.name",
            )

            if number:
                line.append(str(number))

            if street:
                line.append(street)

            if line:
                ad["line"] = [" ".join(line)]

            if city:
                ad["city"] = city

            if state:
                ad["state"] = state

            if zip_:
                ad["postalCode"] = zip_

            if country:
                ad["country"] = country

            return [ad]


    @classmethod
    def buildFhirActive(cls, patient):
        return patient.name.active

    @classmethod
    def buildFhirGeneralPractitioner(cls, patient):
        # generalPractitioner
        pcp = patient.primary_care_doctor
        if pcp:
            r = {
                "display": pcp.rec_name,
                "reference": "".join(["Practitioner/", str(pcp.id)]),
            }
            return [r]


    @classmethod
    def buildFhirCommunication(cls, patient):
        lang = patient.name.lang
        if lang:
            cc = {}
            c = {}

            c["code"] = sub("_", "-", lang.code)  # Standard requires dashes
            c["display"] = lang.name
            c["system"] = "urn:ietf:bcp:47"
            cc["coding"] = [c]
            com = {"preferred": "true", "language": cc}
            return [com]


        # import base64
        # if patient.name.photo:
        # b64 = base64.encodestring(patient.name.photo.decode('utf-8')) #Standard requires base64
        # if b64:
        # jsondict['photo'] = {'data': b64}]

    @classmethod
    def buildFhirMaritalStatus(cls, patient):
        # Health has concubinage and separated, which aren't truly
        # matching FHIR defined statuses
        if patient.name.marital_status:
            us = patient.name.marital_status.upper()  # Codes are uppercase
            fhir_status = [x for x in ms.contents if x["code"] == us]
            marital_status = {}
            if fhir_status:
                code = fhir_status[0]["code"]
                display = fhir_status[0]["display"]
            else:
                code = "OTH"
                display = "other"
            marital_status["coding"] = [
                {
                    "system": "http://hl7.org/fhir/v3/MaritalStatus",
                    "code": code,
                    "display": display,
                }
            ]
            return marital_status
