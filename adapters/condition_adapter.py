from type_definitions import CodeableConcept, Coding, Reference

class conditionAdapter:
    """Adapter for the condition resource"""

    def __init__(self, condition):
        self.condition = condition

    @property
    def patient(self):
        """Patient who has condition

        Returns: namedtuple (Reference)
        """

        patient = self.condition.name
        if patient:
            r = Reference(display=patient.rec_name,
                            reference=''.join(['Patient/', str(patient.id)]))
            return r

    @property
    def asserter(self):
        """Person who asserts condition (diagnoser)

        Returns: namedtuple (Reference)
        """

        asserter = self.condition.healthprof
        if asserter:
            r = Reference(display=asserter.rec_name,
                            reference=''.join(['Practitioner/', str(asserter.id)]))
            return r

    @property
    def dateRecorded(self):
        """When condition first recorded

        Returns: string
        """

        date = self.condition.diagnosed_date
        return date.strftime('%Y-%m-%d') if date is not None else None

    @property
    def notes(self):
        """Additional clinical notes about condition

        Returns: string
        """

        return self.condition.short_comment

    @property
    def abatementDateTime(self):
        """When condition resolved

        Returns: string
        """

        #TODO Time formatting
        date = self.condition.healed_date
        return date.strftime('%Y-%m-%d %H:%M:%S') if date is not None else None

    @property
    def verificationStatus(self):
        """Condition status

        Returns: string (provisional | differential | confirmed, etc)
        """

        # TODO No corresponding Health equivalent (I think?)

        return 'unknown'

    @property
    def severity(self):
        """Condition severity

        Returns: namedtuple (CodeableConcept)
        """

        severity = self.condition.disease_severity
        if severity:
            # These are the snomed codes
            sev={'1_mi': ('Mild', '255604002'),
                '2_mo': ('Moderate', '6736007'),
                '3_sv': ('Severe', '24484000')}
            t=sev.get(severity)
            if t:
                cc = CodeableConcept(text=t[0])
                coding = Coding(display=t[0],
                                code=t[1],
                                system='http://snomed.info/sct')
                cc.coding = [coding]
                return cc

    @property
    def code(self):
        """Retrieve identification code of disease

        Returns: namedtuple (CodeableConcept)
        """

        code = self.condition.pathology
        if code:
            cc = CodeableConcept(text=code.name)
            coding = Coding(system='urn:oid:2.16.840.1.113883.6.90', #ICD-10-CM
                            code=code.code,
                            display=code.name)
            cc.coding=[coding]
            return cc

__all__ = ['conditionAdapter']
