from operator import attrgetter
from pendulum import instance
from fhirclient.models.practitioner import Practitioner as fhir_practitioner
from .base import BaseAdapter

__all__ = ["Practitioner"]


class Practitioner(BaseAdapter):
    @classmethod
    def to_fhir_object(cls, hp):
        jsondict = {}
        jsondict["active"] = cls.build_fhir_active(hp)
        jsondict["telecom"] = cls.build_fhir_telecom(hp)
        jsondict["name"] = cls.build_fhir_name(hp)
        jsondict["identifier"] = cls.build_fhir_identifier(hp)
        jsondict["gender"] = cls.build_fhir_gender(hp)
        jsondict["communication"] = cls.build_fhir_communication(hp)
        return fhir_practitioner(jsondict=jsondict)

    @classmethod
    def build_fhir_active(cls, hp):
        return hp.name.active

    @classmethod
    def build_fhir_telecom(cls, hp):
        telecom = []
        for contact in hp.name.contact_mechanisms:
            c = {"value": contact.value}
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
    def build_fhir_name(cls, hp):
        names = []
        for name in hp.name.person_names:
            n = {}
            n["given"] = [x for x in name.given.split()]
            n["family"] = name.family
            n["prefix"] = [name.prefix] if name.prefix else []
            n["suffix"] = [name.suffix] if name.suffix else []
            n["use"] = name.use
            if name.date_from:
                n["period"] = {"start": instance(name.date_from).to_iso8601_string()}
                if name.date_to:
                    n["period"]["end"] = instance(name.date_to).to_iso8601_string()
            names.append(n)
        if names:
            return names
        else:
            # try in default fields
            n = {}
            n["given"] = [x for x in hp.name.name.split()]
            n["family"] = hp.name.lastname
            n["use"] = "official"
            return [n]

    @classmethod
    def build_fhir_identifier(cls, hp):
        idents = []
        if hp.puid:
            i = {
                "use": "usual",
                "value": hp.puid or "<UNKNOWN>",
                "type": {"text": "PUID/MRN"},
            }
            idents.append(i)

        for alt in hp.name.alternative_ids:
            i = {
                "use": "official",
                "value": alt.code or "<UNKNOWN>",
                "type": {"text": alt.alternative_id_type},
            }
            idents.append(i)
        return idents

    @classmethod
    def build_fhir_gender(cls, hp):
        g = hp.name.gender
        if g:
            if g == "f":
                l = "female"
            elif g == "m":
                l = "male"
            else:
                l = "other"
        else:
            l = "unknown"
        return l

    @classmethod
    def build_fhir_communication(cls, hp):
        lang = hp.name.lang
        if lang:
            cc = {"text": lang.name}
            from re import sub

            c = {
                "code": sub("_", "-", lang.code),
                "display": lang.name,
                "system": "urn:ietf:bcp:47",
            }
            cc["coding"] = [c]
            return [cc]

        # TODO Handle the specialties and roles better
        #     Specifically, output better job titles -- e.g., radiology tech, etc.
        # inst = self.hp.institution
        # occ = self.hp.name.occupation.name #Is this the right place for employee job title?

        # role = CodeableConcept(text=occ, coding=[Coding(display=occ)])

        # organization = Reference(display=inst.rec_name,
        # reference='/'.join(['Organization', str(inst.id)]))

        # specialties = []
        # for spec in self.hp.specialties:
        # code, name = attrgetter('specialty.code', 'specialty.name')(spec)
        # cc = CodeableConcept(text=name)
        # cc.coding = [Coding(code=code,
        # display=name)]
        # specialties.append(cc)

        # pr = practitionerRole(role=role, specialty=specialties,
        # managingOrganization=organization)
