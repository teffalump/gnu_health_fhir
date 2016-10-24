from fhirclient.models.observation import Observation as O, ObservationReferenceRange as RR
from fhirclient.models.identifier import Identifier as ID
from fhirclient.models.coding import Coding as C
from fhirclient.models.codeableconcept import CodeableConcept as CC
from fhirclient.models.fhirreference import Patient as FR
from fhirclient.models.quantity import Quantity as Q
from operator import attrgetter

class Observation:
    def __init__(self, adapter):
        self.adapter = adapter
        self._import_data()

    def _import_data(self):
        getter = attrgetter('system', 'code', 'display')

        o = Observation()

        # comments
        o.comments = self.adapter.comments

        # identifier
        o.identifier = [ ID({'use': ident.use,
                            'value': ident.value})
                        for ident in self.adapter.identifier]

        # interpretation
        sys, code, display = getter(self.adapter.interpretation.coding[0])
        c = C({'system': sys,
                'code': code,
                'display': display
                })
        o.interpretation = CC({'text': self.adapter.observation.text,
                                'coding': [c]})



        # issued
        o.issued = self.adapter.issued

        # status
        o.status = self.adapter.status

        # effectiveDateTime
        o.effectiveDateTime = self.adapter.effectiveDateTime

        # code
        _, code, display = getter(self.adapter.code.coding[0])
        o.code = CC({'text': self.adapter.text,
                        'coding': [ C({'code': code,
                                        'display': display}) ]
                    })

        # performer
        o.performer = [ FR({'display': ref.display,
                            'reference': ref.reference})
                        for ref in self.adapter.performer ]

        # subject
        o.subject = FR({'display': self.adapter.subject.display,
                        'reference': self.adapter.subject.reference})

        # valueQuantity
        v, u, s, c = attrgetter('value', 'units', 'system', 'code')(self.adapter.valueQuantity)
        o.valueQuantity = Q({'value': v,
                                'units': u,
                                'system': s,
                                'code': c})

        # referenceRange
        s, c, d = getter(self.adapter.referenceRange.meaning.coding[0])
        cc = CC({'text': self.adapter.referenceRange.meaning.text,
                    'coding': [ C({'display': d,
                                    'system': s,
                                    'code': c}) ]})
        l, h = attrgetter('low', 'high')(self.adapter.referenceRange)
        o.ReferenceRange = RR({'low': Q({'value': l}),
                                    'high': Q({'value': h}),
                                    'meaning': cc})

        self.observation = o

    @property
    def fhir_json(self):
        self.observation.as_json()

__all__ = ['Observation']
