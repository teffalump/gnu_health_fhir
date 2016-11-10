from type_definitions import Reference, Identifier, CodeableConcept, Coding

class diagnosticReportAdapter:
    """
    Class that manages the interface between FHIR Resource DiagnosticReport
    and GNU Health
    """

    def __init__(self, report):
        self.report = report

    @property
    def status(self):
        """Report status (final | etc.)

        Returns: string
        """

        #TODO No clear correlate in Health (?)

        return 'final'

    @property
    def effectiveDateTime(self):
        """Relevant time of lab collection

        Returns: string
        """

        t = self.report.date_analysis
        return t.strftime("%Y-%m-%dT%H:%M:%S") if t is not None else None

    @property
    def identifier(self):
        """Local test ID

        Returns: List of namedtuple (Identifier) - only one supported
        """

        #TODO Return more information

        #patient = self.report.patient
        #date = self.report.date_analysis
        #report = self.report.test

        #if report and patient and date:
            #label = '{0}: {1} on {2}'.format(report.name, patient.rec_name or '<unknown>', date.strftime('%Y-%m-%d'))

        return Identifier(value=str(report.id),
                                use='official')


    @property
    def code(self):
        """Name/code for this report

        Returns: namedtuple (CodeableConcept)
        """

        #TODO Use LOINC coding

        test = self.report.test
        if test:
            cc = CodeableConcept()
            coding = Coding(display=test.name,
                                code=test.code)
            cc.coding = [coding]
            return cc

    @property
    def category(self):
        """Report category (hematology, etc)

        Returns: namedtuple (CodeableConcept)
        """

        #TODO

        return None

    @property
    def issued(self):
        """Time released

        Returns: string
        """

        t = self.report.write_date
        return t.strftime("%Y-%m-%dT%H:%M:%S") if t is not None else None

    @property
    def result(self):
        """The individual observations that comprise the report

        Returns: List of namedtuples (Reference)
        """

        result = self.report.critearea
        references = []
        for test in result:
            r = Reference(display=test.rec_name,
                            reference='/'.join(['Observation', str(test.id)]))
            references.append(r)

        return references

    @property
    def performer(self):
        """The lab technician, company, etc.

        Returns: namedtuple (Reference)
        """

        performer = self.report.pathologist
        if performer:
            r = Reference(display=performer.name.rec_name,
                        reference='/'.join(['Practitioner', str(performer.id)]))
            return r

    @property
    def subject(self):
        """Report's subject

        Returns: namedtuple (Reference)
        """

        subject = self.report.patient
        if subject:
            display = subject.rec_name
            r = Reference(display=subject.rec_name,
                            reference='/'.join(['Patient', str(subject.id)]))
            return r

    @property
    def conclusion(self):
        """Report conclusion

        Returns: string
        """

        return self.report.results or self.report.diagnosis

__all__ = ['diagnosticReportAdapter']
