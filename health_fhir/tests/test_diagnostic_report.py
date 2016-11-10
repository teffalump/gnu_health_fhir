from diagnostic_report_adapter import diagnosticReportAdapter
from proteus import config, Model

config = config.set_xmlrpc('http://admin:admin@teffalump.com:8001/demo')

Lab = Model.get('gnuhealth.lab')

for l in Lab.find():
    lab = diagnosticReportAdapter(l)
    print(lab.conclusion)
    print(lab.subject)
    print(lab.performer)
    print(lab.result)
    print(lab.issued)
    print(lab.category)
    print(lab.code)
    print(lab.identifier)
    print(lab.status)
    print(lab.effectiveDateTime)
