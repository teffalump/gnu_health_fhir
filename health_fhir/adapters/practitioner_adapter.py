from operator import attrgetter
from fhirclient.models import practitioner

class Practitioner(practitioner.Practitioner):

    def __init__(self, practitioner, **kwargs):
        kwargs['jsondict'] = self._get_jsondict(practitioner)
        super(Practitioner, self).__init__(**kwargs)

    def _get_jsondict(self, hp):
        jsondict = {}

        #active
        jsondict['active']= hp.name.active

        #telecom
        telecom = []
        for contact in hp.name.contact_mechanisms:
            c = {'value': contact.value}
            if contact.type == 'phone':
                c['system'] = 'phone'
                c['use'] = 'home'
            elif contact.type == 'mobile':
                c['system'] = 'phone'
                c['use'] = 'mobile'
            else:
                c['use'] = c['system'] = contact.type
            telecom.append(c)
        if telecom:
            jsondict['telecom'] = telecom

        #name
        names = []
        for name in hp.name.person_names:
            n = {}
            n['given'] = [x for x in name.given.split()]
            n['family'] = name.family
            n['prefix'] = [name.prefix] if name.prefix else []
            n['suffix'] = [name.suffix] if name.suffix else []
            n['use'] = name.use
            n['period'] = {'start': name.date_from, 'end': name.date_to} #DEBUG Date to string conversion
            names.append(n)
        if names:
            jsondict['name'] = names
        else:
            #try in default fields
            n = {}
            n['given'] = [x for x in hp.name.name.split()]
            n['family'] = hp.name.lastname
            n['use'] = 'official'
            jsondict['name'] = [n]

        #identifier
        idents = []
        if hp.puid:
            i = {'use': 'usual',
                    'value': hp.puid or '<UNKNOWN>',
                    'type': {'text': 'PUID/MRN'}}
            idents.append(i)

        for alt in hp.name.alternative_ids:
            i = {'use': 'official',
                    'value': alt.code or '<UNKNOWN>',
                    'type': {'text': alt.alternative_id_type}}
            idents.append(i)
        if idents: jsondict['identifier'] = idents


        #gender
        g = hp.name.gender
        if g:
            if g == 'f':
                l = 'female'
            elif g == 'm':
                l = 'male'
            else:
                l = 'other'
        else:
            l = 'unknown'
        jsondict['gender'] = l

        #communication
        lang = hp.name.lang
        if lang:
            cc = {'text': lang.name}
            from re import sub
            c = {'code': sub('_','-', lang.code),
                    'display': lang.name,
                    'system': 'urn:ietf:bcp:47'}
            cc['coding'] = [c]
            jsondict['communication'] = [cc]

        #TODO Handle the specialties and roles better
        #     Specifically, output better job titles -- e.g., radiology tech, etc.
        # inst = self.hp.institution
        # occ = self.hp.name.occupation.name #Is this the right place for employee job title?

        # role = CodeableConcept(text=occ, coding=[Coding(display=occ)])

        # organization = Reference(display=inst.rec_name,
                        # reference='/'.join(['Organization', str(inst.id)]))

        # specialties = []
        # for spec in self.hp.specialties:
            # code, name = attrgetter('specialty.code', 'specialty.name')(spec)
            # cc = CodeableConcept(text=name)
            # cc.coding = [Coding(code=code,
                            # display=name)]
            # specialties.append(cc)

        # pr = practitionerRole(role=role, specialty=specialties,
                                # managingOrganization=organization)

        return jsondict

__all__=['Practitioner']
