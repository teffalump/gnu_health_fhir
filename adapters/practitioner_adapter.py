from operator import attrgetter

class practitioner_adapter:
    def __init__(self, hp):
        self.hp = hp

    @property
    def active(self):
        """Active or not

        Returns: string (true | false)
        """

        return 'true' if self.hp.name.active else 'false'

    @property
    def telecom(self):
        """Retrieve contact information for doctor

        Returns: List of namedtuple (ContactPoint)
        """

        telecom = []
        for contact in self.hp.name.contact_mechanisms:
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
    def name(self):
        """Practitioner's name

        Returns: namedtuple (HumanName)
        """

        for name in self.hp.name.person_names:
            if name.use in ('official', 'usual'):
                n = HumanName()
                n.given = [x for x in name.given.split()]
                n.family = [x for x in name.family.split()]
                n.prefix = name.prefix
                n.suffix = name.suffix
                n.use = name.use
                n.period = Period(start=name.date_from, end=name.date_to) #DEBUG Date to string conversion
                return n

    @property
    def identifier(self):
        """Retrieve a list of ids

        Returns: List of namedtuple (Identifier)
        """

        idents = []
        if self.hp.puid:
            i = Identifier()
            i.use = 'usual'
            i.value = self.patient.puid or '<UNKNOWN>'
            i.type = CodeableConcept()
            i.type.text = "PUID/MRN"

            idents.append(i)

        for alt in self.hp.name.alternative_ids:
            i = Identifier()
            i.use = 'official'
            i.value = alt.code or '<UNKNOWN>'
            i.type = CodeableConcept()
            i.type.text = alt.alternative_id_type
            idents.append(i)

        return idents

    @property
    def gender(self, gender):
        """Gender

        Returns: string (male | female | etc)
        """

        g = self.hp.name.gender
        if g:
            if g == 'f':
                return 'female'
            elif g == 'm':
                return 'male'
            else:
                return 'other'

        return 'unknown'

    @property
    def communication(self, communication):
        """Languages practitioner speaks

        Returns: List of namedtuple (CodeableConcept) -- only one supported
        """

        lang = self.hp.name.lang
        if lang:
            cc = CodeableConcept(text=lang.name)
            c = Coding()
            from re import sub
            c.code = sub('_','-', lang.code) #Standard requires dashes
            c.display = lang.name
            c.system = 'urn:ietf:bcp:47'
            cc.coding = [c]
            return [cc]

    @property
    def practitionerRole(self):
        """Roles and specialties

        Returns: List of namedtuple (practitionerRole) --- only one supported
        """

        #TODO Handle the specialties and roles better
        #     Specifically, output better job titles -- e.g., radiology tech, etc.

        inst = self.hp.institution
        occ = self.hp.name.occupation.name #Is this the right place for employee job title?

        role = CodeableConcept(text=occ, coding=[Coding(display=occ)])

        organization = Reference(display=inst.rec_name,
                        reference='/'.join(['Organization', str(inst.id)]))

        specialties = []
        for spec in self.hp.specialties:
            code, name = attrgetter('specialty.code', 'specialty.name')(spec)
            cc = CodeableConcept(text=name)
            cc.coding = [Coding(code=code,
                            display=name)]
            specialties.append(cc)

        pr = practitionerRole(role=role, specialty=specialties,
                                managingOrganization=organization)
        return [pr]

    @property
    def qualification(self):
        """Training and certification information

        Returns: List of namedtuple (qualification)
        """

        #TODO

        pass
