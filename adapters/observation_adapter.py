class observation_adapter:
    """Interface between FHIR Observation resource and data models"""

    def __init__(self, observation):
        self.observation = observation

    @property
    def comments(self):
        """Comments about the result

        Returns: string
        """

        return self.observation.remarks

    @property
    def identifier(self):
        """The identifiers for this observation

        Returns: List of namedtuple (Identifier) -- only one supported
        """

        i = Identifier(use='official',
                    value='-'.join([self.observation.name, str(self.observation.id)]))
        return [i]

    @property
    def interpretation(self):
        """Result interpretation (high, low, etc.)

        Returns: namedtuple (CodeableConcept)
        """
        # TODO: Interpretation is complicated

        value = self.observation.result
        lower_limit = self.observation.lower_limit
        upper_limit = self.observation.upper_limit

        if value is not None \
            and lower_limit is not None \
            and upper_limit is not None:
            cc = CodeableConcept()
            coding = Coding()
            if value < lower_limit:
                v = 'L'
                d = 'Low'
            elif value > upper_limit:
                v = 'H'
                d = 'High'
            else:
                v = 'N'
                d = 'Normal'
            coding.system = 'http://hl7.org/fhir/v2/0078'
            coding.code = v
            coding.display = d
            cc.coding = coding
            return cc

    @property
    def issued(self):
        """The time the observation was made available

        Returns: string
        """

        issued = self.observation.write_date or self.observation.create_date
        return issued.strftime("%Y-%m-%dT%H:%M:%S") if issued is not None else None

    @property
    def code(self):
        """What was observed

        Returns: namedtuple (CodeableConcept)
        """
        #TODO Better coding!!

        code = self.observation.name
        if code:
            cc = CodeableConcept(text=code)
            cc.coding = [Coding(code=code, display=code)]
            return cc

    @property
    def performer(self):
        """Who performed the observation

        Returns: List of namedtuple (Reference) -- only one supported
        """

        persons = []
        performer = self.observation.pathologist
        if performer:
            r = Reference(display=performer.name.rec_name,
                            reference='/'.join(['Practitioner', str(performer.id)]))
            persons.append(r)
        return persons

    @property
    def referenceRange(self):
        """The observation's reference range 

        Returns: namedtuple (ReferenceRange)
        """

        units = self.observation.units.name or 'unknown'
        lower_limit = self.observation.lower_limit
        upper_limit = self.observation.upper_limit

        if units is not None \
                and lower_limit is not None \
                and upper_limit is not None:
            ref = ReferenceRange()
            ref.low = lower_limit
            ref.high = upper_limit
            ref.meaning = CodeableConcept()
            coding = Coding()
            ref.meaning.text = coding.display = 'Normal range'
            coding.system = 'http://hl7.org/fhir/referencerange-meaning'
            coding.code = 'normal'
            ref.meaning.coding = [coding]
            return ref

    @property
    def status(self):
        """The observation status (final | etc.)

        Returns: string
        """
        value = self.observation.result
        if self.observation.excluded:
            if value is not None:
                status = 'cancelled'
            else:
                status = 'entered in error'
        else:
            if value is not None:
                status = 'final'
            else:
                status = 'registered'
        return status

    @property
    def valueQuantity(self):
        """The actual result

        Returns: namedtuple (Quantity)
        """

        #TODO More information

        value = self.observation.result
        units = self.observation.units.name
        system = None
        code = None
        if value is not None:
            q = Quantity(value=value,
                            unit=str(units),
                            code=code,
                            uri=system)
            return q

    @property
    def subject(self, subject):
        """Subject of observation (usually patient)

        Returns: namedtuple (Reference)
        """

        subject = self.observation.gnuhealth_lab_id.patient
        if subject:
            r = Reference(display=subject.name.rec_name,
                            reference='/'.join(['Patient', str(subject.id)]))
            return r

    @property
    def effectiveDateTime(self):
        """Clinically relevant time for observation

        Returns: string
        """

        t = self.observation.gnuhealth_lab_id.date_analysis
        return t.strftime("%Y-%m-%dT%H:%M:%S") if t is not None else None

    @property
    def specimen(self):
        pass

    @property
    def related(self):
        pass

    @property
    def method(self):
        pass
