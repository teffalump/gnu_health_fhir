from pendulum import instance, now
from fhirclient.models.coverage import Coverage as fhir_coverage
from .base import import BaseAdapter

__all__ = ["Coverage"]


class Coverage(BaseAdapter):

    @classmethod
    def to_fhir_object(cls, coverage):
        jsondict = {}
        jsondict["identifier"] = cls.build_fhir_identifier(coverage)
        jsondict["status"] = cls.build_fhir_status(coverage)
        jsondict["type"] = cls.build_fhir_type(coverage)
        return fhir_coverage(jsondict=jsondict)

    @classmethod
    def build_fhir_identifier(cls, coverage):
        return [{"value": coverage.number}]


    @classmethod
    def build_fhir_status(cls, coverage):
        if coverage.member_exp:
            if now() < coverage.member_exp:
                return "active"
            else:
                return "cancelled"
        else:  # assume active
            return "active"

    @classmethod
    def build_fhir_type(cls, coverage):
        # TODO There are preferred codes in FHIR
        if coverage.insurance_type:
            return {"coding": [{"code": coverage.insurance_type}]}
