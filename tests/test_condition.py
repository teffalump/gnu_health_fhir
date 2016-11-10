from proteus import config, Model

config = config.set_xmlrpc('http://admin:admin@teffalump.com:8001/demo')

Pat = Model.get('gnuhealth.patient')
pats = Pat.find()

from condition_adapter import conditionAdapter
for pat in pats:
    for c in pat.diseases:
        c = conditionAdapter(c)
        print(c.patient)
        print(c.asserter)
        print(c.dateRecorded)
        print(c.notes)
        print(c.abatementDateTime)
        print(c.severity)
        print(c.code)
