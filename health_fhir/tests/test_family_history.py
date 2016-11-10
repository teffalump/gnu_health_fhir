from proteus import config, Model

config = config.set_xmlrpc('http://admin:admin@teffalump.com:8001/demo')

Pat = Model.get('gnuhealth.patient')
pats = Pat.find()

from family_history_adapter import familyMemberHistoryAdapter as adapter
for pat in pats:
    for c in pat.family_history:
        fh = adapter(c)
        print(fh.gender)
        print(fh.subject)
        print(fh.date)
        print(fh.relationship)
        print(fh.condition)
