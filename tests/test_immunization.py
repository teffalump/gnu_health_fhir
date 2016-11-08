from proteus import config, Model

config = config.set_xmlrpc('http://admin:admin@teffalump.com:8001/demo')

Pat = Model.get('gnuhealth.patient')
pats = Pat.find()

from immunization_adapter import immunizationAdapter as adapter
for pat in pats:
    for vacc in pat.vaccinations:
        info = adapter(vacc)
        print(info.identifier)
        print(info.wasNotGiven)
        print(info.date)
        print(info.status)
        print(info.subject)
        print(info.performer)
        print(info.lotNumber)
        print(info.expirationDate)
        print(info.doseQuantity)
        print(info.notes)
        print(info.reported)
        print(info.route)
        print(info.site)
        print(info.vaccineCode)
        print(info.reaction)
        print(info.vaccinationProtocol)
