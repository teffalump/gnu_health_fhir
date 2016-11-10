from proteus import config, Model
from observation_adapter import observationAdapter

config = config.set_xmlrpc('http://admin:admin@teffalump.com:8001/demo')

crit = Model.get('gnuhealth.lab.test.critearea')

for result in crit.find([('gnuhealth_lab_id', '!=', None)])[:1]:
    data = observationAdapter(result)
    print(data.comments)
    print(data.identifier)
    print(data.interpretation)
    print(data.issued)
    print(data.code)
    print(data.performer)
    print(data.referenceRange)
    print(data.status)
    print(data.valueQuantity)
    print(data.subject)
    print(data.effectiveDateTime)
    print(data.specimen)
    print(data.method)
    print(data.related)
