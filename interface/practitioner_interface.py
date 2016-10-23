from fhirclient.models.practitioner import Practitioner as P, PractitionerPractitionerRole as PR
from fhirclient.models.fhirdate import FHIRDate as FD
from fhirclient.models.contactpoint import ContactPoint as CP
from fhirclient.models.humanname import HumanName as HN
from fhirclient.models.coding import Coding as C
from fhirclient.models.codeableconcept import CodeableConcept as CC
from fhirclient.models.identifier import Identifier as ID

class Practitioner:
    """Class representing FHIR Practitioner Resource

        Wrapper for adapter via fhirclient
    """

    def __init__(self, adapter):
        self.adapter = adapter
        self._import_data()

    def _import_data(self):
        p = P()


        #active
        p.active = self.practitioner.active

        # telecom
        p.telecom = [ CP({'system': telecom.system,
                        'use': telecom.use,
                        'value': telecom.value
                        }) for telecom in self.adapter.telecom]

        #name
        p.name = []
        for name in self.adapter.name:
            hn = HN({'given': name.given,
                        'family': name.family,
                        'prefix': name.prefix,
                        'use': name.use})
            hn.period = Per({'start': FD(name.period.start),
                                'end': FD(name.period.end)})
            p.name.append(hn)

        #identifier
        p.identifier = []
        for ident in self.p.identifier:
            id_ = ID({'use': ident.use,
                'value': ident.value,
                'type': CC({'text': ident.type.text})})
            p.identifier.append(id_)

        #gender
        p.gender = self.adapter.gender

        #communication
        p.communication = []
        for lang in self.adapter.communication:
            cc = CC({'coding':
                        C(
                            {'code': lang.language.coding.code,
                            'display': lang.language.coding.display,
                            'system': lang.language.coding.system
                        })})

            p.communication.append(cc)

        #roles
        p.practionerRole = []
        for data in self.adapter.practionerRole:
            pr = PR()
            pr.role = CC({'text': data.role.text, 'coding': C({'display': data.role.coding.display})})
            pr.specialty = [ CC({'text': spec.text,
                                'coding':
                                    C({'code': spec.coding.code,
                                        'name': spec.coding.name})})
                            for spec in data.specialty]
            p.practionerRole.append(pr)

        self.practitioner = p


    @property
    def fhir_json(self):
        self.practitioner.as_json()

__all__ = ['Practitioner']
