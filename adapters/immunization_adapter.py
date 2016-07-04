from type_definitions import Identifier, Reference, Quantity, vaccinationProtocol, CodeableConcept, Coding, Annotation

class immunizationAdapter:
    """Adapter for immunization resource"""

    def __init__(self, vaccination):
        self.vaccination = vaccination

    @property
    def identifier(self):
        """Unique identifiers

        Returns: List of namedtuple (Identifier) -- only one supported
        """

        i = Identifier(use='official',
                    value='-'.join([self.vaccination.vaccine.rec_name,
                                    str(self.vaccination.id)]))
        return [i]

    @property
    def date(self):
        """Administration date

        Returns: string
        """

        date = self.vaccination.date
        return date.strftime("%Y-%m-%d") if date is not None else None

    @property
    def wasNotGiven(self):
        """Whether immunization was not given or refused

        Returns: string ('true' | 'false')
        """
        #TODO Is there a field for this in Health (?)

        return 'false'

    @property
    def status(self):
        """Vaccination status (in-progress | etc.)

        Returns: string
        """

        status = self.vaccination.state
        if status == 'in_progress':
            return 'in-progress'
        elif status == 'done':
            return 'completed'
        else:
            return None

    @property
    def subject(self):
        """Who was immunized

        Returns: namedtuple (Reference)
        """

        subject = self.vaccination.name
        if subject:
            r = Reference(display=subject.rec_name,
                            reference='/'.join(['Patient', str(subject.id)]))
            return r

    @property
    def performer(self):
        """Who gave it

        Returns: namedtuple (Reference)
        """

        performer = self.vaccination.healthprof
        if performer:
            r = Reference(display=performer.rec_name,
                            reference='/'.join(['Practitioner', str(performer.id)]))
            return r

    @property
    def lotNumber(self):
        """Vaccine lot number

        Returns: string
        """

        number = self.vaccination.lot.number
        return str(number) if number is not None else None

    @property
    def expirationDate(self):
        """Vaccine expiration date

        Returns: string
        """

        date = self.vaccination.lot.expiration_date
        return date.strftime("%Y-%m-%d") if date is not None else None

    @property
    def doseQuantity(self):
        """Amount administered

        Returns: namedtuple (Quantity)
        """

        quantity = self.vaccination.amount
        if quantity is not None:
            amt = Quantity(value=str(quantity),
                            unit='mL',
                            uri='http://snomed.info/sct',
                            code='258773002')
            return amt

    @property
    def notes(self):
        """Misc. notes

        Returns: namedtuple (Annotation)
        """

        notes = self.vaccination.observations
        if notes:
            a = Annotation(text=notes)
            return a

    @property
    def reported(self):
        """Self-reported or not

        Returns: string ('true' or 'false')
        """

        # If there is no attached administered healthprof,
        #   AND no reasonable documents then self-reported (?)

        administer = self.vaccination.healthprof
        asserter = self.vaccination.signed_by

        if administer is None and asserter is None:
            return 'true'
        else:
            return 'false'

    @property
    def route(self):
        """How vaccine entered body

        Returns: namedtuple (CodeableConcept)
        """

        route = self.vaccination.admin_route
        from value_sets import immunizationRoute
        if route:
            ir=[i for i in immunizationRoute.contents if i['code'] == route.upper()]
            if ir:
                cc = CodeableConcept()
                c = Coding()
                c.display = cc.text = ir[0]['display']
                c.code = ir[0]['code']
                cc.coding=[c]
                return cc

    @property
    def site(self):
        """The body site vaccine was administered

        Returns: namedtuple (CodeableConcept)
        """

        site = self.vaccination.admin_site
        from value_sets import immunizationSite
        if site:
            m=[i for i in immunizationSite.contents if i['code'] == site.upper()]
            if m:
                cc = CodeableConcept()
                coding = Coding()
                coding.display = cc.text = m[0]['display']
                coding.code = m[0]['code']
                cc.coding=[coding]
                return cc

    @property
    def vaccineCode(self):
        """Vaccine code administered

        Returns: namedtuple (CodeableConcept)
        """
        #TODO Need better coding, much better!

        type_ = self.vaccination.vaccine
        if type_:
            cc = CodeableConcept()
            coding = Coding()
            coding.display = cc.text = type_.rec_name
            if type_.name.code:
                coding.code = type_.name.code
                cc.coding=[coding]
            return cc

    @property
    def reaction(self):
        """Note any reactions from vaccine

        Returns: namedtuple (reaction)
        """

        #TODO Must be reference in standard, but stored as text on vaccination model (?!)

        pass

    @property
    def vaccinationProtocol(self):
        """The protocol followed

        Returns: List of namedtuple (vaccinationProtocol)
        """

        #TODO Better vaccine coding/info

        seq = self.vaccination.dose
        authority = self.vaccination.institution
        disease = self.vaccination.vaccine.active_component[:1] #Get name of vaccine
        description = self.vaccination.observations

        if seq:
            vp = vaccinationProtocol(doseSequence=seq,
                                        description=description)

            ref = Reference(display=authority.name.rec_name,
                            reference='/'.join(['Institution', str(authority.id)]))

            target = CodeableConcept(text=disease)
            coding = Coding(display=disease)
            target.coding = [coding]

            # Unclear if equivalent concept in Health
            status = CodeableConcept(text='Counts')
            coding = Coding(code='count',
                            display='Counts')
            status.coding = [coding]

            vp.authority = ref
            vp.targetDisease = target
            vp.doseStatus = status

            return [vp]
