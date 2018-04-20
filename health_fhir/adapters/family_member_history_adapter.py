from fhirclient.models import  familymemberhistory

__all__ = ['FamilyMemberHistory']

class FamilyMemberHistory(familymemberhistory.FamilyMemberHistory):

    def __init__(self, member, **kwargs):
        kwargs['jsondict'] = self._get_jsondict(member)
        super(FamilyMemberHistory, self).__init__(**kwargs)

    def _get_jsondict(self, member):
        #TODO Add more info to family history data model on Health side
        jsondict = {}

        #gender
        ### NOTE KEEP THIS UPDATED ###
        # Possible selections (currently)
        #
        # Female
        # 'mother'
        # 'sister'
        # 'aunt'
        # 'niece'
        # 'grandmother'
        #
        # Male
        # 'father'
        # 'brother'
        # 'uncle'
        # 'nephew'
        # 'grandfather'
        #
        # Unknown
        # 'cousin'

        females = ['mother', 'sister', 'aunt', 'niece', 'grandmother']
        males = ['father', 'brother', 'uncle', 'nephew', 'grandfather']
        rel = member.relative
        if rel in females:
            g = 'female'
        elif rel in males:
            g = 'male'
        else:
            g = 'unknown'
        jsondict['gender'] = g

        #date
        date = member.write_date or member.create_date
        if date: date.strftime("%Y-%m-%d")

        #patient
        patient = member.patient
        if patient:
            jsondict['patient'] = {'display': patient.rec_name,
                                    'reference': ''.join(['Patient/', str(patient.id)])}

        #relationship
        from .value_sets import familyMember
        if member:
            cc = {}
            c = {}

            t = {'m': 'maternal', 'f': 'paternal'} #ignore sibling code
            k = ' '.join((t.get(member.xory, ''), member.relative)).strip()
            info = [d for d in familyMember.contents if d['display'] == k]

            if info:
                c['code'] = info[0]['code']
                c['system'] = info[0]['system']
            cc['text'] = c['display'] = k
            cc['coding']=[c]
            jsondict['relationship'] = cc

        #status
        #TODO Unknown equivalent in Health
        jsondict['status'] = 'completed'

        #condition
        path = member.name
        if path:
            code = {}
            coding = {'code': path.code,
                    'system': 'urn:oid:2.16.840.1.113883.6.90'} #ICD-10-CM
            code['text'] = coding['display'] = path.name
            code['coding'] = [coding]
            jsondict['condition'] = [{'code': code}]

        return jsondict
