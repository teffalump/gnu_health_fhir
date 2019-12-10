from .utils import safe_attrgetter
from pendulum import instance
from fhirclient.models.diagnosticreport import DiagnosticReport as fhir_report
from .base import BaseAdapter

__all__ = ["DiagnosticReport"]


class DiagnosticReport(BaseAdapter):

    @classmethod
    def to_fhir_object(cls, report):
        jsondict = {}
        jsondict["status"] = cls.build_fhir_status(report)
        jsondict["effectiveDateTime"] = cls.build_fhir_effective_datetime(report)
        jsondict["identifier"] = cls.build_fhir_identifier(report)
        jsondict["code"] = cls.build_fhir_code(report)
        jsondict["issued"] = cls.build_fhir_issued(report)
        jsondict["result"] = cls.build_fhir_result(report)
        jsondict["performer"] = cls.build_fhir_performer(report)
        jsondict["subject"] = cls.build_fhir_subject(report)
        jsondict["conclusion"] = cls.build_fhir_conclusion(report)
        return fhir_report(jsondict=jsondict)
        
    @classmethod
    def build_fhir_status(cls, report):
        # TODO No clear correlate in Health (?)
        return "final"

    @classmethod
    def build_fhir_effective_datetime(cls, report):
        try:
            return instance(report.date_analysis).to_is8601_string()
        except:
            return None

    @classmethod
    def build_fhir_identifier(cls, report):
        # identifier
        # TODO Return more information
        # patient = self.report.patient
        # date = self.report.date_analysis
        # report = self.report.test

        # if report and patient and date:
        # label = '{0}: {1} on {2}'.format(report.name, patient.rec_name or '<unknown>', date.strftime('%Y-%m-%d'))
        return [{"value": str(report.id), "use": "official"}]

    @classmethod
    def build_fhir_code(cls, report):
        # TODO Use LOINC coding
        try:
            return {"coding": [{"display": report.test.name, "code": report.test.code}]}
        except:
            return None

    @classmethod
    def build_fhir_issued(cls, report):
        try:
            return instance(report.write_date).to_is8601_string()
        except:
            return None

    @classmethod
    def build_fhir_result(cls, report):
        # TODO output actual observations, not links
        references = []
        for test in result.report.critearea:
            r = {
                "display": test.rec_name,
                "reference": "".join(["Observation/", str(test.id)]),
            }
            references.append(r)
        return references

    @classmethod
    def build_fhir_performer(cls, report):
        performers = []
        path = report.pathologist
        tech = report.done_by
        if path:
            r = {
                "display": path.name.rec_name,
                "reference": "".join(["Practitioner/", str(path.id)]),
            }
            performers.append({"actor": r, "role": {"text": "Pathologist"}})
        if tech:
            r = {
                "display": tech.name.rec_name,
                "reference": "".join(["Practitioner/", str(tech.id)]),
            }
            performers.append({"actor": r, "role": {"text": "Technician"}})
        return performers

    @classmethod
    def build_fhir_subject(cls, report):
        try:
            return {
                    "display": report.patient.rec_name,
                    "reference": "".join(["Patient/", str(report.patient.id)]),
                }
        except:
            return None

    @classmethod
    def build_fhir_conclusion(cls, report):
        return report.results or report.diagnosis
