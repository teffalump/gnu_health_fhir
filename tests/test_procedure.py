from proteus import config, Model

config = config.set_xmlrpc('http://admin:admin@teffalump.com:8001/demo')

OP = Model.get('gnuhealth.operation')

from procedure_adapter import procedureAdapter as adapter
for op in OP.find():
    info = adapter(op)
    print(info.identifier)
    print(info.subject)
    print(info.status)
    print(info.category)
    print(info.code)
    print(info.notPerformed)
    print(info.reasonNotePerformed)
    print(info.reasonCodeableConcept)
    print(info.performer)
    print(info.performedPeriod)
    print(info.encounter)
    print(info.location)
    print(info.outcome)
    print(info.complication)
    print(info.followUp)
    print(info.request)
    print(info.notes)
    print(info.used)
    print(info.request)
