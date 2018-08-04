from .utils import safe_attrgetter
from pendulum import instance
from fhirclient.models import patient

__all__ = ['Patient']

class Patient(patient.Patient):

    def __init__(self, patient, **kwargs):
        kwargs['jsondict'] = self._get_jsondict(patient)
        super(Patient, self).__init__(**kwargs)

    def _get_jsondict(self, patient):
        jsondict = {}

        #TODO Add general_info field - where appropriate?

        #Identifier
        idents = []
        if patient.puid:
            i = {}
            i['use'] = 'usual'
            i['value'] = patient.puid or '<UNKNOWN>'
            i['type'] = {'text': "PUID/MRN"}
            idents.append(i)

        for alt in patient.name.alternative_ids:
            i = {}
            i['use'] = 'official'
            i['value'] = alt.code or '<UNKNOWN>'
            i['type'] = {'text': alt.alternative_id_type}
            idents.append(i)

        if idents:
            jsondict['identifier'] = idents

        #Name
        names=[]
        for name in patient.name.person_names:
            n = {}
            n['given'] = [x for x in name.given.split()]
            n['family'] = name.family if name.family else '<unknown>'
            n['prefix'] = [name.prefix] if name.prefix else []
            n['suffix'] = [name.suffix] if name.suffix else []
            n['use'] = name.use if name.use else '<unknown>'
            if name.date_from:
                n['period'] = {'start': instance(name.date_from).to_iso8601_string()}
                if name.date_to:
                    n['period']['end'] = instance(name.date_to).to_iso8601_string()
            names.append(n)

        if names:
            jsondict['name'] = names

        #Telecom
        telecom = []
        for contact in patient.name.contact_mechanisms:
            c = {}
            c['value'] = contact.value
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

        #Gender
        #NOTE This is a difficult decision - what is gender for record-keeping
        # Currently, simply take biological sex and make further decisions later
        bs = patient.biological_sex
        g = None
        if bs:
            if bs == 'f':
                g = 'female'
            elif bs == 'm':
                g = 'male'
            else:
                g = 'other'

        else:
            g = 'unknown'
        jsondict['gender'] = g

        #birthDate
        dob = patient.name.dob
        if dob:
            jsondict['birthDate'] = instance(dob).to_iso8601_string()

        #deceasedBoolean
        jsondict['deceasedBoolean'] = patient.deceased

        #deceasedDateTime
        dod = patient.dod
        if dod:
            jsondict['deceasedDateTime'] = instance(dod).to_iso8601_string()

        #address
        #Only one currently
        du = patient.name.du
        if du:
            ad = {}
            ad['use'] = 'home'
            ad['type'] = 'physical' #TODO Check for this
            ad['text'] = patient.name.du_address
            line=[]
            number, street, zip_, city, state, country = safe_attrgetter(
                                    du,
                                    'address_street_number',
                                    'address_street',
                                    'address_zip',
                                    'address_city',
                                    'address_subdivision.name',
                                    'address_country.name')

            if number:
                line.append(str(number))

            if street:
                line.append(street)

            if line:
                ad['line'] = [' '.join(line)]

            if city:
                ad['city'] = city

            if state:
                ad['state'] = state

            if zip_:
                ad['postalCode'] = zip_

            if country:
                ad['country'] = country

            jsondict['address'] = [ad]

        #active
        jsondict['active'] = patient.name.active

        #generalPractitioner
        pcp = patient.primary_care_doctor
        if pcp:
            r = {'display': pcp.rec_name,
                    'reference': ''.join(['Practitioner/', str(pcp.id)])}
            jsondict['generalPractitioner'] = [r]

        #managingOrganization
        #TODO

        #communication
        lang = patient.name.lang
        if lang:
            cc = {}
            c = {}
            from re import sub
            c['code'] = sub('_','-', lang.code) #Standard requires dashes
            c['display'] = lang.name
            c['system'] = 'urn:ietf:bcp:47'
            cc['coding'] = [c]
            com = {'preferred': 'true',
                    'language': cc}
            jsondict['communication'] = [com]

        #Photo
        #TODO Figure out contentType of photo

        # import base64
        # if patient.name.photo:
            # b64 = base64.encodestring(patient.name.photo.decode('utf-8')) #Standard requires base64
            # if b64:
                # jsondict['photo'] = {'data': b64}]

        #maritalStatus
        from .value_sets import maritalStatus as ms
        #Health has concubinage and separated, which aren't truly
        # matching FHIR defined statuses
        if patient.name.marital_status:
            us = patient.name.marital_status.upper() #Codes are uppercase
            fhir_status = [x for x in ms.contents\
                                    if x['code'] == us]
            ms = {}
            if fhir_status:
                code = fhir_status[0]['code']
                display = fhir_status[0]['display']
            else:
                code = 'OTH'
                display = 'other'
            ms['coding'] = [{'system': 'http://hl7.org/fhir/v3/MaritalStatus',
                            'code': code,
                            'display': display}]
            jsondict['maritalStatus'] = ms

        #TODO Link - other links to same person

        #Return the dict
        return jsondict
