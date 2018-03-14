from .utils import safe_attrgetter, TIME_FORMAT
from fhirclient.models import diagnosticreport

class DiagnosticReport(diagnosticreport.DiagnosticReport):

    def __init__(self, report):
        jsondict = self._get_jsondict(report)
        super(DiagnosticReport, self).__init__(jsondict=jsondict)

    def _get_jsondict(self, report):
        jsondict = {}

        #status
        #TODO No clear correlate in Health (?)
        jsondict['status'] = 'final'

        #effectiveDateTime
        t = report.date_analysis
        if t: jsondict['effectiveDateTime'] = t.strftime(TIME_FORMAT)

        #identifier
        #TODO Return more information
        #patient = self.report.patient
        #date = self.report.date_analysis
        #report = self.report.test

        #if report and patient and date:
            #label = '{0}: {1} on {2}'.format(report.name, patient.rec_name or '<unknown>', date.strftime('%Y-%m-%d'))
        jsondict['identifier'] = [{'value': str(report.id),
                                    'use': 'official'}]

        #code
        #TODO Use LOINC coding
        test = report.test
        if test:
            jsondict['code'] = {'coding': [{'display': test.name,
                                            'code': test.code}]}
        #issued
        t = report.write_date
        if t: jsondict['issued'] = t.strftime(TIME_FORMAT)

        #result
        #TODO output actual observations, not links
        result = report.critearea
        references = []
        for test in result:
            r = {'display': test.rec_name,
                    'reference': ''.join(['Observation/', str(test.id)])}
            references.append(r)
        if references: jsondict['result'] = references

        #performer
        performers = []
        path = report.pathologist
        tech = report.done_by
        if path:
            r = {'display': path.name.rec_name,
                    'reference': ''.join(['Practitioner/', str(path.id)])}
            performers.append({'actor': r,
                                'role': {'text': 'Pathologist'}})
        if tech:
            r = {'display': tech.name.rec_name,
                    'reference': ''.join(['Practitioner/', str(tech.id)])}
            performers.append({'actor': r,
                                'role': {'text': 'Technician'}})
        if performers: jsondict['performer'] = performers

        #subject
        subject = report.patient
        if subject:
            r = {'display': subject.rec_name,
                    'reference': ''.join(['Patient/', str(subject.id)])}
            jsondict['subject'] = r

        #conclusion
        jsondict['conclusion'] = report.results or report.diagnosis

        return jsondict

__all__ = ['DiagnosticReport']
