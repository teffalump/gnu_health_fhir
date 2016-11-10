from operator import attrgetter
from StringIO import StringIO
from datetime import datetime
import server.fhir as supermod
from server.common.utils import safe_attrgetter

try:
    from flask import current_app, url_for
    RUN_FLASK=True
except:
    from .datastore import dumb_url_generate
    RUN_FLASK=False

class RelatedPerson_Map:
    model_mapping={
            'gnuhealth.family_member': {
                'identifier': 'party.puid',
                'gender': 'party.sex',
                'photo': 'photo',
                'phone': 'party.phone',
                'email': 'party.email',
                'mobile': 'party.mobile',
                'given': 'party.name',
                'family': 'party.lastname',
                'nickname': 'party.alias',
                'addressNumber': 'party.du.address_street_number',
                'addressStreet': 'party.du.address_street',
                'addressZip': 'party.du.address_zip',
                'addressCity': 'party.du.address_city',
                'addressState': 'party.du.address_subdivision.name',
                'addressCountry': 'party.du.address_country.name'
                }}

    # NOTE We are searching from patient at first, not model,
    #    but then doing a search against the model
    #    -Must handle subject reference separately
    root_search = [('party.is_patient', '=', False)]
    url_prefixes={}
    chain_map={'patient': 'Patient'}

    resource_search_params={
                'patient': 'reference',
                'name': 'string',
                'identifier': 'token',
                'gender': 'token',
                '_id': 'token',
                'address': None,
                '_language': None,
                'phonetic': None,
                'telecom': None}
    search_mapping={
                '_id': ['id'],
                'gender': ['party.sex'],
                'identifier': ['party.puid'],
                'patient': None,
                'name': ['party.lastname', 'party.name']}


#TODO: Use and add to parent methods
#TODO: Have standard None/True/False checks and conventions
class health_RelatedPerson(supermod.RelatedPerson, RelatedPerson_Map):
    '''Mediate between XML/JSON schema bindings and
        the GNU Health models for RelatedPerson resource
    '''

    def __init__(self, *args, **kwargs):
        related_person=kwargs.pop('gnu_record', None)
        related_patient=kwargs.pop('related_patient', None)
        super(health_RelatedPerson, self).__init__(*args, **kwargs)
        if not related_patient:
            raise ValueError('Need patient!')
        self.related_patient=related_patient
        if related_person:
            self.set_gnu_related_person(related_person)

    def set_gnu_related_person(self, related_person):
        '''Set gnu related_person record'''
        if related_person:
            self.related_person = related_person

            if self.related_person.__name__ not in self.model_mapping:
                raise ValueError('Not a valid model')

            self.map = self.model_mapping[self.related_person.__name__]
            self.__import_from_gnu_related_person()

    def __import_from_gnu_related_person(self):
        '''Set the model info'''
        if self.related_person:
            self.__set_gnu_identifier()
            self.__set_gnu_name()
            self.__set_gnu_telecom()
            self.__set_gnu_gender()
            self.__set_gnu_address()
            self.__set_gnu_photo()
            self.__set_gnu_patient()

            self.__set_feed_info()

    def __set_feed_info(self):
        ''' Sets the feed-relevant info
        '''
        if self.related_person:
            self.feed={'id': self.related_person.id,
                    'published': self.related_person.create_date,
                    'updated': self.related_person.write_date or self.related_person.create_date,
                    'title': self.related_person.party.rec_name
                        }

    def __set_gnu_patient(self):
        if self.related_patient:
            if RUN_FLASK:
                uri = url_for('pat_record', log_id=self.related_patient.id)
            else:
                uri = dumb_url_generate(['Patient', self.related_patient.id])
            display = self.related_patient.rec_name
            ref=supermod.ResourceReference()
            ref.display = supermod.string(value=display)
            ref.reference = supermod.string(value=uri)
            self.set_subject(ref)


    def __set_gnu_identifier(self):
        if self.related_person:
            puid=safe_attrgetter(self.related_person, self.map['identifier'])
            if puid:
                ident = supermod.Identifier(
                            use=supermod.IdentifierUse(value='usual'),
                            label=supermod.string(value='PUID'),
                            value=supermod.string(value=puid))

                self.add_identifier(value=ident)

    def __set_gnu_name(self):
        family=[]
        given=[supermod.string(value=x) for x in safe_attrgetter(
                        self.related_person, self.map['given'], '').split()]
        after_names=[supermod.string(value=x) for x in safe_attrgetter(
                        self.related_person, self.map['family'], '').split()]
        if len(after_names) > 1:
            family=after_names[-1:]
            given.extend(after_names[:-1])
        else:
            family=after_names
        name=supermod.HumanName(
                    use=supermod.NameUse(value='usual'),
                    family=family,
                    given=given)


        self.set_name(name)

    def __set_gnu_telecom(self):
        telecom = []
        phone=safe_attrgetter(self.related_person, self.map['phone'])
        if phone:
            telecom.append(supermod.Contact(
                    system=supermod.ContactSystem(value='phone'),
                    value=supermod.string(value=phone),
                    use=supermod.ContactUse(value='home')))
        mobile=safe_attrgetter(self.related_person, self.map['mobile'])
        if mobile:
            telecom.append(supermod.Contact(
                    system=supermod.ContactSystem(value='phone'),
                    value=supermod.string(value=mobile),
                    use=supermod.ContactUse(value='mobile')))
        email=safe_attrgetter(self.related_person, self.map['email'])
        if email:
            telecom.append(supermod.Contact(
                    system=supermod.ContactSystem(value='email'),
                    value=supermod.string(value=email),
                    use=supermod.ContactUse(value='email')))
        for x in telecom:
            self.add_telecom(x)

    def __set_gnu_gender(self):
        try:
            gender = attrgetter(self.map['gender'])(self.related_person)
            coding = supermod.Coding(
                        system=supermod.uri(value='http://hl7.org/fhir/v3/AdministrativeGender'),
                        code=supermod.code(value=gender.upper()),
                        display=supermod.string(value='Male' if gender == 'm' else 'Female')
                        )
            gender=supermod.CodeableConcept(coding=[coding])
            self.set_gender(gender)
        except:
            raise ValueError('No gender')

    def __set_gnu_address(self):
        #FIX Ugly, but clear
        if self.related_person:
            try:
                address=supermod.Address()
                address.set_use(supermod.string(value='home'))
                line=[]
                try:
                    line.append(str(attrgetter(self.map['addressNumber'](self.related_person))))
                except:
                    pass

                try:
                    line.append(attrgetter(self.map['addressStreet'])(self.related_person))
                except:
                    pass

                try:
                    city = attrgetter(self.map['addressCity'])(self.related_person)
                    if city:
                        address.set_city(supermod.string(value=city))
                except:
                    pass

                try:
                    state = attrgetter(self.map['addressState'])(self.related_person)
                    if state:
                        address.set_state(supermod.string(value=state))
                except:
                    pass

                try:
                    z = attrgetter(self.map['addressZip'])(self.related_person)
                    if z:
                        address.set_zip(supermod.string(value=z))
                except:
                    pass

                try:
                    country = attrgetter(self.map['addressCountry'])(self.related_person)
                    if country:
                        address.set_country(supermod.string(value=value))
                except:
                    pass

                if line:
                    address.add_line(supermod.string(value=' '.join(line)))
                self.add_address(address)
            except:
                pass

    def __set_gnu_photo(self):
        import base64
        if self.related_person:
            try:
                b64 = base64.encodestring(attrgetter(self.map['photo'])(self.related_person))
                if b64:
                    data = supermod.base64Binary(value=b64)
                    im = supermod.Attachment(data=data)
                    self.add_photo(im)
            except:
                pass

    def export_to_xml_string(self):
        output = StringIO()
        self.export(outfile=output, namespacedef_='xmlns="http://hl7.org/fhir"', pretty_print=False, level=4)
        content = output.getvalue()
        output.close()
        return content

supermod.RelatedPerson.subclass=health_RelatedPerson
