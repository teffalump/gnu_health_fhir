from type_definitions import Identifier, CodeableConcept, Coding, HumanName, Period, ContactPoint, Address, communication
from utils import safe_attrgetter, TIME_FORMAT

class patientAdapter:

    def __init__(self, patient):
        self.patient = patient

    @property
    def identifier(self):
        """Retrieve a list of identifiers


        Returns: List of namedtuples (Identifier)
        """

        idents = []
        if self.patient.puid:
            i = Identifier()
            i.use = 'usual'
            i.value = self.patient.puid or '<UNKNOWN>'
            i.type = CodeableConcept()
            i.type.text = "PUID/MRN"

            idents.append(i)

        for alt in self.patient.name.alternative_ids:
            i = Identifier()
            i.use = 'official'
            i.value = alt.code or '<UNKNOWN>'
            i.type = CodeableConcept()
            i.type.text = alt.alternative_id_type
            idents.append(i)

        return idents

    @property
    def name(self):
        """Retrieve names

        Returns: Lists of namedtuple (HumanName)
        """

        names=[]
        for name in self.patient.name.person_names:
            n = HumanName()
            n.given = [x for x in name.given.split()]
            n.family = [x for x in name.family.split()]
            n.prefix = name.prefix
            n.suffix = name.suffix
            n.use = name.use
            n.period = Period(start=name.date_from, end=name.date_to) #DEBUG Date to string conversion
            names.append(n)

        return names

    @property
    def telecom(self):
        """Retrieve telecom information

        Returns: List of namedtuple (ContactPoint)
        """

        telecom = []
        for contact in self.patient.name.contact_mechanisms:
            c = ContactPoint()
            c.value = contact.value
            if contact.type == 'phone':
                c.system='phone'
                c.use='home'
            elif contact.type == 'mobile':
                c.system='phone'
                c.use='mobile'
            else:
                c.use = c.system = contact.type
            telecom.append(c)

        return telecom

    @property
    def gender(self):
        """Retrieve patient's administrative gender

        Returns: string (male | female | other | unknown)
        """

        #NOTE This is a difficult decision - what is gender for record-keeping
        # Currently, simply take biological sex and make further decisions later

        g = self.patient.biological_sex
        if g:
            if g == 'f':
                return 'female'
            elif g == 'm':
                return 'male'
            else:
                return 'other'

        return 'unknown'

    @property
    def birthDate(self):
        """Retrieve the patient's birthdate

        Returns: string
        """

        dob = self.patient.name.dob
        return dob.strftime("%Y-%m-%d") if dob is not None else None

    @property
    def deceasedBoolean(self):
        """Is patient deceased

        Returns: True or False
        """

        return self.patient.deceased

    @property
    def deceasedDateTime(self):
        """Date and time of death

        Returns: string
        """

        #TODO Figure out timezone/proper formatting

        dod = self.patient.dod
        return dod.strftime(TIME_FORMAT) if dod is not None else None

    @property
    def address(self):
        """Retrieve patient's address information

        Returns: List of namedtuples (Address) only one supported
        """

        du = self.patient.name.du
        if du:
            ad=Address()
            ad.use = 'home'
            ad.type = 'physical' #TODO Check for this
            ad.text = self.patient.name.du_address
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
                ad.line = ' '.join(line)

            if city:
                ad.city = city

            if state:
                ad.state = state

            if zip_:
                ad.postalCode = zip_

            if country:
                ad.country = country

            return [ad]

    @property
    def active(self):
        """Active patient or not

        Returns: True or False
        """

        return self.patient.name.active

    @property
    def careProvider(self):
        """Return patient's primary care provider

        Returns: List of namedtuple (Reference) only one supported
        """

        pcp = self.patient.primary_care_doctor
        if pcp:
            r = Reference(display=pcp.rec_name)
            r.reference = ''.join(['Practitioner/', pcp.id])
            return [r]

    @property
    def managingOrganization(self):
        """Retrieve patient record custodian

        Returns: namedtuple (Reference)
        """

        return None

    @property
    def communication(self):
        """Retrieve patient language preferences

        Returns: List of namedtuples (communication) although only one supported
        """

        lang = self.patient.name.lang
        if lang:
            cc = CodeableConcept()
            c = Coding()
            from re import sub
            c.code = sub('_','-', lang.code) #Standard requires dashes
            c.display = lang.name
            c.system = 'urn:ietf:bcp:47'
            cc.coding = [c]
            com = communication(preferred='true',
                                language=cc)
            return [com]

    @property
    def photo(self):
        """Retrieve patient's photos

        Returns: List of namedtuples (Attachments) but only one returned
        """

        #TODO Figure out contentType of photo

        import base64
        if self.patient.name.photo:
            b64 = base64.encodestring(self.patient.name.photo) #Standard requires base64
            if b64:
                a = Attachment()
                a.data = b64
                return [a]

    @property
    def maritalStatus(self):
        """Retrieve the patient's marital status

        Returns: namedtuple (CodeableConcept)
        """

        from value_sets import maritalStatus as ms
        #Health has concubinage and separated, which aren't truly
        # matching FHIR defined statuses
        us = self.patient.name.marital_status.upper() #Codes are uppercase
        if us:
            fhir_status = [x for x in ms.contents\
                                    if x['code'] == us]
            ms = CodeableConcept()
            if fhir_status:
                code = fhir_status[0]['code']
                display = fhir_status[0]['display']
            else:
                code = supermod.code(value='OTH')
                display = supermod.string(value='other')
            ms.coding = [ Coding(system='http://hl7.org/fhir/v3/MaritalStatus',
                                code=code,
                                display=display)]
            return ms

    @property
    def link(self):
        """Various other links to same person"""
        return None

__all__ = ['patientAdapter']
