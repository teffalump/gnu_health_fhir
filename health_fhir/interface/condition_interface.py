from fhirclient.models.condition import Condition as Con
from fhirclient.models.fhirreference import FHIRReference as FR
from fhirclient.models.fhirdate import FHIRDate as FD
from fhirclient.models.codeableconcept import CodeableConcept as CC
from fhirclient.models.coding import Coding as C
from operator import attrgetter
from .common import Resource

class Condition(Resource):
    """Wrapper for adapter using fhirclient models.

    FHIR Condition resource
    """

    def _import_data(self):
        con = Con()

        # patient
        con.subject = FR({'display': self.adapter.subject.display,
                        'reference': self.adapter.subject.reference})

        # asserter
        if self.adapter.asserter:
            con.asserter = FR({'display': self.adapter.asserter.display,
                            'reference': self.adapter.asserter.reference})

        # dateRecorded
        con.dateRecorded = FD(self.adapter.dateRecorded)

        # notes
        con.notes = self.adapter.notes

        # abatementDateTime
        con.abatementDateTime = FD(self.adapter.abatementDateTime)

        # verificationStatus
        con.verificationStatus = self.adapter.verificationStatus

        # severity
        if self.adapter.severity:
            d, c, s = attrgetter('display', 'code', 'system')(self.adapter.severity.coding[0])
            con.severity = CC({'text': d,
                        'coding':
                            [{'display': d, 'code': c, 'system': s}]})

        # code
        if self.adapter.code:
            d, c, s = attrgetter('display', 'code', 'system')(self.adapter.code.coding[0])
            con.code = CC({'text': d,
                        'coding':
                            [{'display': d, 'code': c, 'system': s}]})

        self.resource = con

__all__ = ['Condition']
