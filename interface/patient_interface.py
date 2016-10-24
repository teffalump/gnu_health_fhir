from fhirclient.models.patient import Patient as P, PatientCommunication as PC
from fhirclient.models.codeableconcept import CodeableConcept as CC
from fhirclient.models.identifier import Identifier as ID
from fhirclient.models.attachment import Attachment as AT
from fhirclient.models.coding import Coding as C
from fhirclient.models.fhirreference import Patient as FR
from fhirclient.models.address import Address as AD
from fhirclient.models.fhirdate import FHIRDate as FD
from fhirclient.models.contactpoint import ContactPoint as CP
from fhirclient.models.humanname import HumanName as HN
from fhirclient.models.period import Period as Per

class Patient:
    """Takes a patient adapter instance and provides valid FHIR data.

        Basically a wrapper for the adapter using the fhirclient models.

           E.g., p = Patient(adapter) --> p.fhir_json #valid FHIR json
    """

    def __init__(self, adapter):
        self.adapter = adapter
        self._import_data()

    def _import_data(self):
        patient = P()

        # identifier
        for ident in self.adapter.identifier:
            id_ = ID({'use': ident.use,
                'value': ident.value,
                'type': CC({'text': ident.type.text})})
            patient.identifier.append(id_)


        # active
        patient.active = self.adapter.active

        # name
        patient.name = []
        for name in self.adapter.name:
            hn = HN({'given': name.given,
                        'family': name.family,
                        'prefix': name.prefix,
                        'use': name.use})
            hn.period = Per({'start': FD(name.period.start),
                                'end': FD(name.period.end)})
            patient.name.append(hn)

        #telecom
        patient.telecom = []
        for telecom in self.adapter.telecom:
            cp = CP({'system': telecom.system,
                        'use': telecom.use,
                        'value': telecom.value
                        })
            patient.telecom.append(cp)

        #gender
        patient.gender = self.adapter.gender

        #date of birth
        patient.birthDate = FD(self.adapter.birthDate)

        #deceased
        patient.deceasedBoolean = self.adapter.deceasedBoolean
        patient.deceasedDateTime = FD(self.adapter.deceasedDateTime)

        #address
        for address in self.adapter.address:
            ad = AD({'city': address.city,
                    'country': address.country,
                    'line': address.line,
                    'type': address.type,
                    'use': address.use,
                    'state': address.state,
                    'postalCode': address.postalCode})

        #careProvider
        for provider in self.adapter.careProvider:
            fr = FR({'display': provider.display,
                        'reference': provider.reference})
            patient.careProvider.append(fr)

        #communication
        for lang in self.adapter.communication:
            cc = CC({'coding':
                        C(
                            {'code': lang.language.coding.code,
                            'display': lang.language.coding.display,
                            'system': lang.language.coding.system
                        })})

            pc = PC({'preferred': lang.preferred,
                        'language': cc})
            patient.communication.append(pc)

        #photo
        for i in self.adapter.photo:
            a = A({'data': i.data})
            patient.photo.append(a)

        #marital status
        patient.maritalStatus = CC(
                {'coding': C({
                    'system': self.adapter.maritalStatus.coding.system,
                    'code': self.adapter.maritalStatus.coding.code,
                    'display': self.adapter.maritalStatus.coding.display
                    })})

        self.patient = patient

    @property
    def fhir_json(self):
        return self.patient.as_json()

__all__ = ['Patient']
