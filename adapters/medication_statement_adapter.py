from type_definitions import Reference, Identifier, CodeableConcept, Coding, Period, dosage, Quantity, Timing, repeat
from utils import TIME_FORMAT, safe_attrgetter

class medicationStatementAdapter:
    """Adapter for patient medications"""

    def __init__(self, med):
        self.med = med

    @property
    def identifier(self):
        """Identifiers for medication

        Returns:
            List of namedlist (Identifier) --- only one supported
        """

        i = Identifier(use='official',
                    value='-'.join([self.med.medicament.rec_name,
                                    str(self.med.id)]))
        return [i]

    @property
    def patient(self):
        """Who is taking the medication

        Returns:
            namedlist (Reference)
        """
        patient = self.med.name
        return Reference(display=patient.name.rec_name,
                            reference='/'.join(['Patient', str(patient.id)]))

    @property
    def informationSource(self):
        """Who asserted the information

        Returns:
            namedlist (Reference)
        """

        return None #See if we can determine this in Health?

    @property
    def dateAsserted(self):
        """When asserted

        Returns:
            string
        """

        pass #Use create/write date?

    @property
    def status(self):
        """Status of medication statement (REQUIRED)

        Returns:
            string (active | completed | entered-in-error | intended)
        """

        if self.med.is_active:
            return 'active'
        elif self.med.course_completed or self.med.discontinued:
            return 'completed'
        else:
            return 'intended'

    @property
    def dosage(self):
        """The dosage information

        Returns:
            List of namedlist (dosage)
        """
        # TODO Can always add more information!

        code_conv = {
                'seconds': 's',
                'minutes': 'min',
                'hours': 'h',
                'days': 'd',
                'months': 'mo',
                'years': 'a'}

        dose = dosage()

        # Amount (this should be listed, but could be patient reported)
        if self.med.dose:
            dose.quantityQuantity = Quantity(value=str(self.med.dose),
                                        unit=self.med.dose_unit.name)

        # Route
        #     TODO Standard route values
        route = self.med.route
        if route:
            cc = CodeableConcept()
            c = Coding()
            cc.text = c.display = route.name
            c.code = route.code
            cc.coding = [c]
            dose.route = cc

        # PRN
        if self.med.frequency_prn or safe_attrgetter(self.med, 'common_dosage.abbreviation') == 'prn':
            dose.asNeededBoolean = 'true'
        else:
            dose.asNeededBoolean = 'false'

        # Site and Method -- ignore
        #     Could add 'form' info (from the model)

        timing = Timing()

        if self.med.frequency: #prefer specific information

            rep = repeat()

            if self.med.duration_period is not 'indefinite':
                rep.duration = str(self.med.duration)
                rep.durationUnits = code_conv.get(self.med.duration_period)

            # Health stores timing as 1 per X s/min/hr
            rep.frequency = '1'
            rep.period = str(self.med.frequency)
            rep.periodUnits = code_conv.get(self.med.frequency_unit)

            timing.repeat = rep

        elif self.med.common_dosage:

            c = Coding(display=self.med.common_dosage.abbreviation,
                        system='http://snomed.info/sct',
                        code=self.med.common_dosage.code)

            timing.code = CodeableConcept(text=self.med.common_dosage.name,
                                            coding=[c])

        else: #No dosage information (either unknown or incomplete)
            timing = None

        dose.timing = timing

        #Rate - rateRatio
        #    Only if an infusion -- always mL/hr (I think?)
        if self.med.infusion:
            num = Quantity(value=str(self.med.infusion_rate),
                            unit='mL')
            den = Quantity(value='1',
                            unit='hr')
            dose.rateRatio = Ratio(numerator=num,
                                denominator=den)

        return [dose]

    @property
    def wasNotTaken(self):
        """Was not taken

        Returns:
            string ('true' | 'false')
        """

        return 'false' #Any Health equivalent?

    @property
    def reasonNotTaken(self):
        """Why not taken

        Returns:
            List of namedlist (CodeableConcept)
        """

        pass #Any Health equivalent?

    @property
    def reasonForUseCodeableConcept(self):
        """Why medication was taken

        Returns:
            namedlist (CodeableConcept)
        """

        # Ideally should make indication connect to patient condition
        reason = self.med.indication
        if reason:
            cc = CodeableConcept(text=reason.name)
            coding = Coding(system='urn:oid:2.16.840.1.113883.6.90', #ICD-10-CM
                            code=reason.code,
                            display=reason.name)
            cc.coding=[coding]
            return cc

    @property
    def effectivePeriod(self):
        """Over what period

        Returns:
            namedlist (Period)
        """

        start, end = self.med.start_treatment, self.med.end_treatment
        if start:
            p = Period(start=start.strftime(TIME_FORMAT))
            if end:
                p.end = end.strftime(TIME_FORMAT)
            return p

    @property
    def note(self):
        """Additional information

        Returns:
            string
        """

        return self.med.notes

    @property
    def medicationReference(self):
        """The medication taken

        Returns:
            namedlist (Reference)
        """

        med = self.med.medicament
        return Reference(display=med.active_component,
                            reference='/'.join(['Medication', str(med.id)]))

__all__ = ['medicationStatementAdapter']
