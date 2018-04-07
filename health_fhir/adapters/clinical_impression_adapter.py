from .utils import safe_attrgetter, TIME_FORMAT
from fhirclient.models import clinicalimpression 

__all__=['ClinicalImpression']

class ClinicalImpression(clinicalimpression.ClinicalImpression):
    """Immature resource somewhat equivalent to SOAP notes, H&P, etc.

    Eventually, should support 3 models:
        - evaluations (most important)
        - roundings
        - ambulatory care
    """

    def __init__(self, note, **kwargs):
        kwargs['jsondict'] = self._get_jsondict(note)
        super(ClinicalImpression, self).__init__(**kwargs)

    def _get_jsondict(self, note):
        jsondict = {}

        #Identifier
        if note.code:
            jsondict['identifier'] = [{'value': note.code}]

        #Status
        #GNU Health states - in_progress, done, signed, None
        if note.state in ['done', 'signed'] or (note.evaluation_start and note.evaluation_endtime):
            jsondict['status'] = 'completed'
        elif note.state == 'in_progress' or note.appointment:
            jsondict['status'] = 'draft'
        else:
            jsondict['status'] = 'unknown'

        #Code
        #Type of assessment - TODO More information
        jsondict['code'] = {'text': 'Patient evaluation'}

        #Context
        #Point to encounter
        jsondict['context'] = {'display': note.code or 'code_unknown',
                                'reference': ''.join(['Encounter/', str(note.id)])}
        #Subject
        if note.patient:
            jsondict['subject'] = {'display': note.patient.rec_name,
                                    'reference': ''.join(['Patient/', str(note.patient.id)])}
        #effectiveDateTime - time of assessment
        if note.evaluation_start:
            start = note.evaluation_start.strftime(TIME_FORMAT)
            if note.evaluation_endtime:
                end = note.evaluation_endtime.strftime(TIME_FORMAT)
                jsondict['effectivePeriod'] = {'start': start, 'end': end}
            else:
                jsondict['effectiveDateTime'] = start

        #date - time recorded
        last = note.write_date or note.evaluation_start
        jsondict['date'] = last.strftime(TIME_FORMAT)

        #Shove Objective in here - evaluation_summary
        #Shove HPI in here - present_illness + chief_complaint
        #Shove Plan in here - directions
        jsondict['summary']= 'CC: %s\nHPI: %s\nObjective: %s\nPlan: %s' % tuple(safe_attrgetter(note, 'chief_complaint', 'present_illness', 'evaluation_summary', 'directions', default=''))

        #Other misc garbage
        # extras = [{'text': x} for x in safe_attrgetter(note, 'notes', 'notes_complaint', 'info_diagnosis', default='') if x.strip()]
        # if extras: jsondict['note'] = extras

        return jsondict
