from fhirclient.models.familymemberhistory import FamilyMemberHistory as FH, FamilyMemberHistoryCondition as FHC
from fhirclient.models.fhirreference import FHIRReference as FR
from fhirclient.models.codeableconcept import CodeableConcept as CC
from fhirclient.models.coding import Coding as C
from operator import attrgetter
from .common import Resource

class FamilyMemberHistory(Resource):
    """Interface to adapter for Family Member History resource"""

    def _import_data(self):
        fh = FH()

        # gender
        fh.gender = self.adapter.gender

        # date
        fh.date = self.adapter.date

        # patient
        fh.patient = FR({'display': self.adapter.patient.display,
                        'reference': self.adapter.patient.reference})

        # relationship
        d, c, s = attrgetter('display', 'code', 'system')(self.adapter.relationship.coding[0])
        fh.relationship = CC({'text': self.adapter.relationship.text,
                                'coding': [C({'display': d,
                                                'code': c,
                                                'system': s})]})


        # condition
        d, c, s = attrgetter('display', 'code', 'system')(self.adapter.condition.code.coding[0])
        cc = CC({'text': self.adapter.condition.code.text,
                'coding': [C({'display': d,
                                'code': c,
                                'system': s})]})
        fh.condition = [ FHC(code=cc) ]

        self.resource = fh

__all__ = ['FamilyMemberHistory']
