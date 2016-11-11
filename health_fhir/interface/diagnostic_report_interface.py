from fhirclient.models.diagnosticreport import DiagnosticReport as DR
from fhirclient.models.fhirreference import FHIRReference as FR
from fhirclient.models.fhirdate import FHIRDate as FD
from fhirclient.models.identifier import Identifier as ID
from fhirclient.models.codeableconcept import CodeableConcept as CC
from fhirclient.models.coding import Coding as C
from fhirclient.models.fhirreference import Patient as FR
from health_fhir.adapters import diagnosticReportAdapter
from operator import attrgetter
from .common import Resource

class DiagnosticReport(Resource):
    """Provides FHIR interface for the DiagnosticReport resource"""

    def __init__(self, model):
        adapter = diagnosticReportAdapter(model)
        super().__init__(adapter)

    def _import_data(self):

        dr = DR()

        # status
        dr.status = self.adapter.status

        # effectiveDateTime
        dr.effectiveDateTime = FD({'date': self.adapter.effectiveDateTime})

        # issued
        dr.issued = FD({'date': self.adapter.issued})

        # conclusion
        dr.conclusion = self.adapter.conclusion

        # identifer
        dr.identifier = [ ID({'use': ident.use, 'value': ident.value})
                            for ident in self.adapter.identifier ]

        # result(s)
        dr.result = [ FR({'display': res.display, 'reference': res.reference})
                        for res in self.adapter.result ]

        # performer
        dr.performer = FR({'display': self.adapter.performer.display,
                            'reference': self.adapter.performer.reference})

        # subject
        dr.subject = FR({'display': self.adapter.subject.display,
                            'reference': self.adapter.subject.reference})

        # code
        dr.code = CC({ 'text': self.adapter.code.text,
                        'coding':
                            [ C(
                                {'code': self.adapter.code.coding[0].code,
                                'display': self.adapter.code.coding[0].display
                                }
                            ) ]
                    })

        self.resource = dr

