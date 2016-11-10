from proteus import config, Model

config = config.set_xmlrpc('http://admin:admin@teffalump.com:8001/demo')

Pat = Model.get('gnuhealth.patient')
pats = Pat.find()

from medication_statement_adapter import medicationStatementAdapter as adapter
for pat in pats:
    for med in pat.medications:
        data = adapter(med)
        print(data.identifier)
        print(data.patient)
        print(data.informationSource)
        print(data.dateAsserted)
        print(data.status)
        print(data.dosage)
        print(data.wasNotTaken)
        print(data.reasonNotTaken)
        print(data.reasonForUseCodeableConcept)
        print(data.effectivePeriod)
        print(data.note)
        print(data.medicationReference)
