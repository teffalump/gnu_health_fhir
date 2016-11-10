from proteus import config, Model
from practitioner_adapter import practitionerAdapter

config = config.set_xmlrpc('http://admin:admin@teffalump.com:8001/demo')

HP = Model.get('gnuhealth.healthprofessional')

for hp in HP.find():
    dr = practitionerAdapter(hp)
    print(dr.active)
    print(dr.telecom)
    print(dr.identifier)
    print(dr.name)
    print(dr.gender)
    print(dr.communication)
    print(dr.practitionerRole)
    print(dr.qualification)
