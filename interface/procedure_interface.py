from fhirclient.models.procedure import Procedure as PR, ProcedurePerformer as PP
from fhirclient.models.annotation import Annotation as A
from fhirclient.models.identifier import Identifier as ID
from fhirclient.models.fhirreference import FHIRReference as FR
from fhirclient.models.coding import Coding as C
from fhirclient.models.fhirdate import FHIRDate as FD
from fhirclient.models.codeableconcept import CodeableConcept as CC
from fhirclient.models.performer import CodeableConcept as CC
from fhirclient.models.period import Period as Per

from operator import attrgetter

class Procedure:
    """Takes a procedure adapter instance and returns valid FHIR data.

    A wrapper, basically, for the adapter using fhirclient.
    """

    def __init__(self, adapter):
        self.adapter = adapter
        self._import_data()

    def _import_data(self):
        pr = PR()

        # identifier
        pr.identifier = [ID({'use': ident.use,
                            'value': ident.value})
                        for ident in self.adapter.identifier]

        # subject
        pr.subject = FR({'reference': self.adapter.subject.reference,
                            'display': self.adapter.subject.display})

        # status
        pr.status = self.adapter.status

        # code
        us, sys, code, display = attrgetter('userSelected', 'system', 'code', 'display')(self.adapter.code.coding[0])
        c = C({'userSelected': us,
                    'system': sys,
                    'code': code,
                    'display': display})

        pr.code = CC({'text': self.adapter.code.text,
                        'coding': [c]})

        # notPerformed
        pr.notPerformed = self.adapter.notPerformed

        # reason
        sys, code, display = attrgetter('system', 'code', 'display')(self.adapter.reasonCodeableConcept.coding[0])
        c = C({'system': sys,
                    'code': code,
                    'display': display})

        pr.reasonCodeableConcept = CC({'text': self.adapter.reasonCodeableConcept.text,
                                        'coding': [c]})

        # performer
        performers = []
        for p in self.adapter.performer:
            display, ref = attrgetter('display', 'reference')(p.actor)
            actor = FR({'display': display, 'reference': ref})

            role = CC({'text': p.role.text,
                        'coding': [C({'code': t.code,
                                        'display': t.display,
                                        'system': t.system})
                                    for t in p.role.coding]})

            performers.append(PP({'actor': actor, 'role': role}))
        pr.performer = performers

        # performedPeriod
        per = Per({'start': FD({'date': self.adapter.period.start}),
                    'end': FD({'date': self.adapter.period.end})})
        pr.performedPeriod = per

        # location
        pr.location = FR({'display': self.adapter.location.display,
                        'reference': self.adapter.location.reference})

        # notes
        pr.notes = A({'text': self.adapter.notes.text})

        self.procedure = pr

    @property
    def fhir_json(self):
        return self.procedure.as_json()
