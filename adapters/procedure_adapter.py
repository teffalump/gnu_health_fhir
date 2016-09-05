from type_definitions import Identifier, CodeableConcept, Coding, performer, Reference, Period, Annotation
from operator import attrgetter
from utils import TIME_FORMAT

class procedureAdapter:
    """Adapter for health procedures (e.g., surgeries)"""

    def __init__(self, procedure):
        self.procedure = procedure

    @property
    def identifier(self):
        """Procedure identifiers

        Returns:
            List of namedlists (Identifier) --- only one supported
        """

        i = Identifier(use='official',
                    value='-'.join([self.procedure.procedure.name, str(self.procedure.id)]))
        return [i]

    @property
    def subject(self):
        """Subject of procedure (REQUIRED)

        Returns:
            namedtuple (Reference)
        """

        subject = self.procedure.name.patient
        if subject:
            r = Reference(display=subject.name.rec_name,
                            reference='/'.join(['Patient', str(subject.id)]))
            return r

    @property
    def status(self):
        """Procedure status (REQUIRED)

        Returns:
            string ('in-progress' | 'aborted' | 'completed' | 'entered-in-error')
        """

        state = self.procedure.name.state 

        if state == 'in_progress':
            return 'in-progress'
        elif state == 'cancelled':
            return 'aborted'
        elif state in ['done', 'signed']:
            return 'completed'
        elif state in ['draft', 'confirmed']: #NOT in standard
            return 'scheduled'
        else:
            return 'entered-in-error'

    @property
    def category(self):
        """Procedure classification

        Returns:
            namedlist (CodeableConcept)
        """

        pass

    @property
    def code(self):
        """Procedure identification code (REQUIRED)

        Returns:
            namedlist (CodeableConcept)
        """

        procedure = self.procedure.procedure

        cc = CodeableConcept()
        c = Coding(userSelected='false',
                    system='urn:oid:2.16.840.1.113883.6.4',
                    code=procedure.name) #ICD-10-PCS
        cc.text = c.display = procedure.description.capitalize()

        cc.coding=[c]
        return cc

    @property
    def notPerformed(self):
        """Whether performed or not

        Returns:
            string ('false' | 'true')
        """

        return 'false' #There is no Health equivalent (I think?)

    @property
    def reasonNotePerformed(self):
        """Why procedure was not performed

        Returns:
            list of namedlist (CodeableConcept)
        """

        pass

    @property
    def reasonCodeableConcept(self):
        """Why procedure was performed

        Returns:
            namedlist (CodeableConcept)
        """

        code = self.procedure.name.pathology
        if code:
            cc = CodeableConcept(text=code.name)
            coding = Coding(system='urn:oid:2.16.840.1.113883.6.90', #ICD-10-CM
                            code=code.code,
                            display=code.name)
            cc.coding=[coding]
            return cc

    @property
    def performer(self):
        """The people involved in the procedure

        Returns:
            List of namedlist (performer)
        """
        ### Possibles
        # Surgeon
        # Anesthetist
        # Other team members

        actors = []
        surgeon = self.procedure.name.surgeon
        if surgeon:
            ref = Reference(display=surgeon.name.rec_name,
                            reference='/'.join(['Practitioner', str(surgeon.id)]))
            role = CodeableConcept(
                        text = 'Surgeon',
                        coding = [Coding(code='304292004',
                                        display='Surgeon',
                                        system='urn:oid:2.16.840.1.113883.4.642.2.420')]) #Performer-Role
            actors.append(performer(actor=ref, role=role))

        anesthetist = self.procedure.name.anesthetist
        if anesthetist:
            ref = Reference(display=anesthetist.name.rec_name,
                            reference='/'.join(['Practitioner', str(anesthetist.id)]))
            role = CodeableConcept(
                        text = 'Anesthetist',
                        coding = [Coding(code='158970007',
                                        display='Anesthetist',
                                        system='urn:oid:2.16.840.1.113883.4.642.2.420')]) #Performer-Role
            actors.append(performer(actor=ref, role=role))

        for m in self.procedure.name.surgery_team:
            ref = Reference(display=m.team_member.name.rec_name,
                            reference='/'.join(['Practitioner', str(m.team_member.id)]))
            if m.role:
                code, name = attrgetter('role.specialty.code', 'role.specialty.name')(m)
                role = CodeableConcept(text=name,
                                        coding=[Coding(code=code,
                                                    display=name)])
            actors.append(performer(actor=ref, role=role))
        return actors or None

    @property
    def performedPeriod(self):
        """Duration of the procedure

        Returns:
            namedlist (Period)
        """

        start, end = attrgetter('name.surgery_date', 'name.surgery_end_date')(self.procedure)
        if start is not None:
            p = Period()
            p.start = start.strftime(TIME_FORMAT)
            if end is not None:
                p.end = end.strftime(TIME_FORMAT)
            return p

    @property
    def encounter(self):
        """Associated encounter

        Returns:
            namedlist (Reference)
        """

        pass

    @property
    def location(self):
        """Where the procedure was done

        Returns:
            namedlist (Reference)
        """

        room = self.procedure.name.operating_room
        return Reference(display=room.rec_name,
                            reference='/'.join(['Location', str(room.id)]))

    @property
    def outcome(self):
        """Procedure result

        Returns:
            namedlist (CodeableConcept)
        """

        pass

    @property
    def report(self):
        """Associated diagnostic reports

        Returns:
            List of namedlist (Reference)
        """

        pass

    @property
    def complication(self):
        """Complications

        Returns:
            List of namedlist (CodeableConcept)
        """

        pass #Post-op dx?

    @property
    def followUp(self):
        """Any instructions for follow up

        Returns:
            List of namedlist (CodeableConcept)
        """

        pass

    @property
    def request(self):
        """Initiating request for this procedure

        Returns:
            namedlist (Reference)
        """

        pass #Health equivalent?

    @property
    def notes(self):
        """Additional info

        Returns:
            namedlist (Annotation)
        """

        #TODO Add author reference?

        return Annotation(text=self.procedure.name.extra_info)

    @property
    def used(self):
        """Items used in procedure

        Returns:
            List of namedlist (Reference)
        """

        #TODO Use self.procedure.name.supplies
        # But need to write those endpoints
        pass 

    @property
    def focalDevice(self):
        """Devices that are the focus of the procedure

        Returns:
            List of namedlist (focalDevice)
        """

        pass

__all__ = ['procedureAdapter']
