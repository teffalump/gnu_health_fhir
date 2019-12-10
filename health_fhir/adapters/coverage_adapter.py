from pendulum import instance, now
from fhirclient.models import coverage

__all__ = ["Coverage"]


class Coverage(coverage.coverage):
    def __init__(self, coverage, **kwargs):
        kwargs["jsondict"] = self._get_jsondict(coverage)
        super(Coverage, self).__init__(**kwargs)

    def _get_jsondict(self, coverage):
        jsondict = {}

        # identifier
        json["identifier"] = [{"value": coverage.number}]

        # status
        if coverage.member_exp:
            if now() < coverage.member_exp:
                json["status"] = "active"
            else:
                json["status"] = "cancelled"
        else:  # assume active
            json["status"] = "active"

        # type
        # TODO There are preferred codes in FHIR
        if coverage.insurance_type:
            json["type"] = {"coding": [{"code": coverage.insurance_type}]}
