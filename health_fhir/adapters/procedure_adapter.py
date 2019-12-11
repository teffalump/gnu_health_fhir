from .utils import safe_attrgetter
from pendulum import instance
from fhirclient.models.procedure import Procedure as fhir_procedure
from .base import BaseAdapter

__all__ = ["Procedure"]


class Procedure(BaseAdapter):
    @classmethod
    def to_fhir_object(cls, procedure):
        # TODO category
        # TODO usedCode Use procedure.name.supplies
        # TODO location - room = procedure.name.operating_room
        jsondict = {}
        jsondict["identifier"] = cls.build_fhir_identifier(procedure)
        jsondict["subject"] = cls.build_fhir_subject(procedure)
        jsondict["status"] = cls.build_fhir_status(procedure)
        jsondict["code"] = cls.build_fhir_code(procedure)
        jsondict["notDone"] = cls.build_fhir_not_done(procedure)
        jsondict["reasonCode"] = cls.build_fhir_reason_code(procedure)
        jsondict["performer"] = cls.build_fhir_performer(procedure)
        jsondict["performedPeriod"] = cls.build_fhir_performed_period(procedure)
        jsondict["note"] = cls.build_fhir_note(procedure)
        return fhir_procedure(jsondict=jsondict)

    @classmethod
    def build_fhir_identifier(cls, procedure):
        return [
            {
                "use": "official",
                "value": "-".join([procedure.procedure.name, str(procedure.id)]),
            }
        ]

    @classmethod
    def build_fhir_subject(cls, procedure):
        try:
            subject = procedure.name.patient
            return {
                "display": subject.name.rec_name,
                "reference": "".join(["Patient/", str(subject.id)]),
            }
        except:
            return None

    @classmethod
    def build_fhir_status(cls, procedure):
        state = procedure.name.state
        s = None
        if state == "in_progress":
            s = "in-progress"
        elif state == "cancelled":
            s = "aborted"
        elif state in ["done", "signed"]:
            s = "completed"
        elif state in ["draft", "confirmed"]:  # NOT in standard
            s = "scheduled"
        else:
            s = "entered-in-error"
        return s

    @classmethod
    def build_fhir_code(cls, procedure):
        cc = {}
        c = {
            "userSelected": False,
            "system": "urn:oid:2.16.840.1.113883.6.4",
            "code": procedure.procedure.name,
        }  # ICD-10-PCS
        cc["text"] = c["display"] = procedure.procedure.description.capitalize()
        cc["coding"] = [c]
        return cc

    @classmethod
    def build_fhir_not_done(cls, procedure):
        # There is no Health equivalent (I think?)
        return False

    @classmethod
    def build_fhir_reason_code(cls, procedure):
        code = procedure.name.pathology
        if code:
            cc = {"text": code.name}
            coding = {
                "system": "urn:oid:2.16.840.1.113883.6.90",  # ICD-10-CM
                "code": code.code,
                "display": code.name,
            }
            cc["coding"] = [coding]
            return [cc]

    @classmethod
    def build_fhir_performer(cls, procedure):
        actors = []
        surgeon = procedure.name.surgeon
        if surgeon:
            ref = {
                "display": surgeon.name.rec_name,
                "reference": "/".join(["Practitioner", str(surgeon.id)]),
            }
            role = {
                "text": "Surgeon",
                "coding": [
                    {
                        "code": "304292004",
                        "display": "Surgeon",
                        "system": "urn:oid:2.16.840.1.113883.4.642.2.420",
                    }
                ],
            }  # Performer-Role
            actors.append({"actor": ref, "role": role})

        anesthetist = procedure.name.anesthetist
        if anesthetist:
            ref = {
                "display": anesthetist.name.rec_name,
                "reference": "".join(["Practitioner/", str(anesthetist.id)]),
            }
            role = {
                "text": "Anesthetist",
                "coding": [
                    {
                        "code": "158970007",
                        "display": "Anesthetist",
                        "system": "urn:oid:2.16.840.1.113883.4.642.2.420",
                    }
                ],
            }  # Performer-Role
            actors.append({"actor": ref, "role": role})

        for m in procedure.name.surgery_team:
            ref = {
                "display": m.team_member.name.rec_name,
                "reference": "".join(["Practitioner/", str(m.team_member.id)]),
            }
            role = {}
            if m.role:
                code, name = safe_attrgetter(
                    m, "role.specialty.code", "role.specialty.name"
                )
                role = {"text": name, "coding": [{"code": code, "display": name}]}
            actors.append({"actor": ref, "role": role or None})
        return actors

    @classmethod
    def build_fhir_performed_period(cls, procedure):
        start, end = safe_attrgetter(
            procedure, "name.surgery_date", "name.surgery_end_date"
        )
        if start is not None:
            period = {"start": instance(start).to_iso8601_string()}
            if end is not None:
                period["end"] = instance(end).to_iso8601_string()
            return period

    @classmethod
    def build_fhir_note(cls, procedure):
        if procedure.name.extra_info:
            return [{"text": procedure.name.extra_info}]
