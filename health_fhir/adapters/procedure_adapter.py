from operator import attrgetter
from .utils import TIME_FORMAT
from fhirclient.models import procedure

class Procedure(procedure.Procedure):

    def __init__(self, procedure):
        jsondict = self._get_jsondict(procedure)
        super(Procedure, self).__init__(jsondict=jsondict)

    def _get_jsondict(self, procedure):
        jsondict = {}

        #identifier
        i = {'use': 'official',
                'value': '-'.join([procedure.procedure.name, str(procedure.id)])}
        jsondict['identifier'] = [i]

        #subject
        subject = procedure.name.patient
        if subject:
            jsondict['subject'] = {'display': subject.name.rec_name,
                                'reference': ''.join(['Patient/', str(subject.id)])}

        #status
        state = procedure.name.state
        s = None
        if state == 'in_progress':
            s = 'in-progress'
        elif state == 'cancelled':
            s = 'aborted'
        elif state in ['done', 'signed']:
            s = 'completed'
        elif state in ['draft', 'confirmed']: #NOT in standard
            s = 'scheduled'
        else:
            s = 'entered-in-error'
        jsondict['status'] = s

        #category
        #TODO

        #code
        cc = {}
        c = {'userSelected': False,
                'system': 'urn:oid:2.16.840.1.113883.6.4',
                'code': procedure.procedure.name} #ICD-10-PCS
        cc['text'] = c['display'] = procedure.procedure.description.capitalize()

        cc['coding']=[c]
        jsondict['code'] = cc

        #notDone
        jsondict['notDone'] = False #There is no Health equivalent (I think?)

        #reasonCode
        code = procedure.name.pathology
        if code:
            cc = {'text': code.name}
            coding = {'system': 'urn:oid:2.16.840.1.113883.6.90', #ICD-10-CM
                    'code': code.code,
                    'display': code.name}
            cc['coding']=[coding]
            jsondict['reasonCode'] = [cc]

        #performer
        actors = []
        surgeon = procedure.name.surgeon
        if surgeon:
            ref = {'display': surgeon.name.rec_name,
                    'reference': '/'.join(['Practitioner', str(surgeon.id)])}
            role = {'text': 'Surgeon',
                    'coding': [{'code': '304292004',
                                'display': 'Surgeon',
                                'system': 'urn:oid:2.16.840.1.113883.4.642.2.420'}]} #Performer-Role
            actors.append({'actor': ref, 'role': role})

        anesthetist = procedure.name.anesthetist
        if anesthetist:
            ref = {'display': anesthetist.name.rec_name,
                    'reference': ''.join(['Practitioner/', str(anesthetist.id)])}
            role = {'text': 'Anesthetist',
                    'coding': [{'code': '158970007',
                                'display': 'Anesthetist',
                                'system': 'urn:oid:2.16.840.1.113883.4.642.2.420'}]} #Performer-Role
            actors.append({'actor': ref, 'role': role})

        for m in procedure.name.surgery_team:
            ref = {'display': m.team_member.name.rec_name,
                    'reference': ''.join(['Practitioner/', str(m.team_member.id)])}
            role =  {}
            if m.role:
                code, name = attrgetter('role.specialty.code', 'role.specialty.name')(m)
                role = {'text': name,
                        'coding': [{'code': code,
                                    'display': name}]}
            actors.append({'actor': ref, 'role': role or None})
        if actors: jsondict['performer'] = actors

        #performedPeriod
        start, end = attrgetter('name.surgery_date', 'name.surgery_end_date')(procedure)
        if start is not None:
            p = {'start': start.strftime(TIME_FORMAT)}
            if end is not None:
                p['end'] = end.strftime(TIME_FORMAT)
            jsondict['performedPeriod'] = p

        #location
        # room = procedure.name.operating_room
        # (display=room.rec_name,
                            # reference='/'.join(['Location', str(room.id)]))

        #note
        if procedure.name.extra_info:
            jsondict['note'] = [ {'text': procedure.name.extra_info}]

        #usedCode
        #TODO Use procedure.name.supplies

        return jsondict

__all__ = ['Procedure']
