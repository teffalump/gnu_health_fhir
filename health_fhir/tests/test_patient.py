from proteus import config, Model

config = config.set_xmlrpc('http://admin:admin@teffalump.com:8001/demo')

Pat = Model.get('gnuhealth.patient')
pat = Pat.find()[0]

from patient_adapter import patientAdapter
patient = patientAdapter(pat)
print(patient.telecom)
print(patient.identifier)
print(patient.gender)
print(patient.birthDate)
print(patient.address)
print(patient.active)
print(patient.photo)
print(patient.maritalStatus)
print(patient.communication)
print(patient.link)
print(patient.deceasedDateTime)
print(patient.deceasedBoolean)

