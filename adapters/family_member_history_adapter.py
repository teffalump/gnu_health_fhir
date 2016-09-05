from type_definitions import Condition, CodeableConcept, Coding, Reference

class familyMemberHistoryAdapter:
    #TODO Add more info to family history data model on Health side

    def __init__(self, member):
        self.member = member

    @property
    def gender(self):
        """Family member gender

        Returns: string (male | female | etc.)
        """

        ### NOTE KEEP THIS UPDATED ###
        # Possible selections (currently)
        #
        # Female
        # 'mother'
        # 'sister'
        # 'aunt'
        # 'niece'
        # 'grandmother'
        #
        # Male
        # 'father'
        # 'brother'
        # 'uncle'
        # 'nephew'
        # 'grandfather'
        #
        # Unknown
        # 'cousin'

        member = self.member
        females = ['mother', 'sister', 'aunt', 'niece', 'grandmother']
        males = ['father', 'brother', 'uncle', 'nephew', 'grandfather']

        if member in females:
            return 'female'
        elif member in males:
            return 'male'
        else:
            return 'unknown'

    @property
    def date(self):
        """When captured or updated

        Returns: string
        """

        date = self.member.write_date or self.member.create_date
        return date.strftime("%Y-%m-%d") if date is not None else None

    @property
    def subject(self):
        """Relevant patient

        Returns: namedtuple (Reference)
        """

        subject = self.member.patient
        if subject:
            r = Reference(display=subject.rec_name,
                            reference='/'.join(['Patient', str(subject.id)]))
            return r

    @property
    def relationship(self):
        """Relationship to patient

        Returns: namedtuple (CodeableConcept)
        """

        from value_sets import familyMember
        member = self.member
        if member:
            cc = CodeableConcept()
            coding = Coding()

            t = {'m': 'maternal', 'f': 'paternal'} #ignore sibling code
            k = ' '.join((t.get(member.xory, ''), member.relative)).strip()
            info = [d for d in familyMember.contents if d['display'] == k]

            if info:
                coding.code = info[0]['code']
                coding.system = value=info[0]['system']
            cc.text = coding.display = k
            cc.coding=[coding]
            return cc

    @property
    def condition(self):
        """Family member's conditions

        Returns: namedtuple (Condition)
        """

        path = self.member.name
        if path:
            code = CodeableConcept()
            coding = Coding(code=path.code,
                            system='urn:oid:2.16.840.1.113883.6.90') #ICD-10-CM
            code.text = coding.display = path.name
            code.coding = coding
            condition = Condition(code=code)
            return condition

__all__ = ['familyMemberHistoryAdapter']
