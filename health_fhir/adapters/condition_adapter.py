from .utils import TIME_FORMAT
from fhirclient.models import condition

class Condition(condition.Condition):

    def __init__(self, condition):
        jsondict = self._get_jsondict(condition)
        super(Condition, self).__init__(jsondict=jsondict)

    def _get_jsondict(self, condition):
        jsondict = {}

        #subject
        patient = condition.name
        if patient:
            jsondict['subject'] = { 'display': patient.rec_name,
                                'reference': ''.join(['Patient/', str(patient.id)])}

        #asserter
        asserter = condition.healthprof
        if asserter:
            jsondict['asserter'] = {'display': asserter.rec_name,
                                'reference': ''.join(['Practitioner/', str(asserter.id)])}

        #assertedDate
        date = condition.diagnosed_date
        jsondict['assertedDate'] = date.strftime('%Y-%m-%d') if date is not None else None

        #note
        jsondict['note'] = [{'text': condition.short_comment}]

        #abatementDateTime
        date = condition.healed_date
        jsondict['abatementDateTime'] = date.strftime(TIME_FORMAT) if date is not None else None

        #verificationStatus
        # TODO No corresponding Health equivalent (I think?)
        jsondict['verificationStatus'] = 'unknown'

        #severity
        severity = condition.disease_severity
        if severity:
            # These are the snomed codes
            sev={'1_mi': ('Mild', '255604002'),
                '2_mo': ('Moderate', '6736007'),
                '3_sv': ('Severe', '24484000')}
            t=sev.get(severity)
            if t:
                cc = {'text': t[0]}
                coding = {'display': t[0],
                            'code': t[1],
                            'system': 'http://snomed.info/sct'}
                cc['coding'] = [coding]
                jsondict['severity'] = cc

        #code
        code = condition.pathology
        if code:
            cc = {'text': code.name}
            coding = {'system': 'urn:oid:2.16.840.1.113883.6.90', #ICD-10-CM
                        'code': code.code,
                        'display': code.name}
            cc['coding']=[coding]
            jsondict['code'] = cc

        return jsondict

__all__ = ['Condition']
