from fhirclient.models.condition import Condition as C
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
        con = C()

        # patient
        con.patient = FR({'display': self.adapter.patient.display,
                        'reference': self.adapter.patient.reference})

        # asserter
        con.asserter = FR({'display': self.adapter.asserter.display,
                        'reference': self.adapter.asserter.reference})

        # dateRecorded
        con.dateRecorded = FD({'date': self.adapter.dateRecorded})

        # notes
        con.notes = self.adapter.notes

        # abatementDateTime
        con.abatementDateTime = FD({'date': self.adapter.abatementDateTime})

        # verificationStatus
        con.verificationStatus = self.adapter.verificationStatus

        # severity
        d, c, s = attrgetter('display', 'code', 'system')(self.adapter.severity.coding[0])
        con.severity = CC({'text': self.adapter.severity.text,
                    'coding':
                        [C({'display': d, 'code': c, 'severity': s})]})

        # code
        d, c, s = attrgetter('display', 'code', 'system')(self.adapter.code.coding[0])
        con.code = CC({'text': self.adapter.code.text,
                    'coding':
                        [C({'display': d, 'code': c, 'severity': s})]})

        self.resource = con

__all__ = ['Condition']
