from .utils import safe_attrgetter, TIME_FORMAT
from fhirclient.models import encounter

class Encounter(encounter.Encounter):
    """In GNU Health, `encounters` are patient evaluations
    """

    def __init__(self, enc, **kwargs):
        kwargs['jsondict'] = self._get_jsondict(enc)
        super(Encounter, self).__init__(**kwargs)

    def _get_jsondict(self, enc):
        jsondict = {}

        #Identifier
        if enc.code:
            jsondict['identifier'] = [{'value': enc.code}]

        #Status
        #GNU Health states - in_progress, done, signed, None
        if enc.state in ['done', 'signed'] or (enc.evaluation_start and enc.evaluation_endtime):
            jsondict['status'] = 'finished'
        elif enc.state == 'in_progress':
            jsondict['status'] = 'in-progress'
        elif enc.appointment:
            if enc.appointment.checked_in_date:
                jsondict['status'] = 'arrived'
            else:
                jsondict['status'] = 'planned'
        else:
            jsondict['status'] = 'unknown'

        #Class
        #GNU Health types - outpatient, inpatient
        if enc.evaluation_type == 'outpatient':
            jsondict['class'] = {'code': 'AMB',
                                    'display': 'ambulatory'}
        elif enc.evaluation_type == 'inpatient':
            jsondict['class'] = {'code': 'IMP',
                                    'display': 'inpatient encounter'}
        else:
            pass #TODO

        #Type
        # GNU Health - well_woman/man/child, followup, new
        if enc.visit_type == 'new':
            g = {'text': 'New health condition', 'coding': [{'code': 'new'}]}
        elif enc.visit_type == 'well_woman':
            g = {'text': 'Well woman visit', 'coding': [{'code': 'well_woman'}]}
        elif enc.visit_type == 'well_child':
            g = {'text': 'Well child visit', 'coding': [{'code': 'well_child'}]}
        elif enc.visit_type == 'well_man':
            g = {'text': 'Well man visit', 'coding': [{'code': 'well_man'}]}
        elif enc.visit_type == 'followup':
            g = {'text': 'Followup visit', 'coding': [{'code': 'followup'}]}
        else:
            g = {}
        if g: jsondict['type'] = [g]

        #Priority
        #GNU Health - a = Normal, b = Urgent, c = Medical Emergency
        if enc.urgency == 'a':
            g = {'text': 'Normal', 'coding': [{'code': 'a'}]}
        elif enc.urgency == 'b':
            g = {'text': 'Urgent', 'coding': [{'code': 'b'}]}
        elif enc.urgency == 'c':
            g = {'text': 'Medical Emergency', 'coding': [{'code': 'c'}]}
        else:
            g = {}
        if g: jsondict['priority'] = g

        #Subject
        if enc.patient:
            jsondict['subject'] = {'display': enc.patient.rec_name,
                                    'reference': ''.join(['Patient/', str(enc.patient.id)])}

        #Participant
        # signed_by (sign), healthprof (initiate)
        parts = []
        if enc.signed_by:
            parts.append({'individual': {'display': enc.signed_by.rec_name,
                            'reference': ''.join(['Practitioner/', str(enc.signed_by.id)])}})
        if enc.healthprof:
            parts.append({'individual': {'display': enc.healthprof.rec_name,
                            'reference': ''.join(['Practitioner/', str(enc.healthprof.id)])}})
        if parts:
            if len(parts) > 1:
                jsondict['participant'] = parts[:1] if parts[0] == parts[1] else parts
            else:
                jsondict['participant'] = parts


        #Period
        if enc.evaluation_start:
            jsondict['period'] = {'start': enc.evaluation_start.strftime(TIME_FORMAT)}
            if enc.evaluation_endtime:
                jsondict['period']['end'] = enc.evaluation_endtime.strftime(TIME_FORMAT)

        #Length
        #TODO
        if enc.evaluation_length:
            pass

        return jsondict

__all__=['Encounter']
