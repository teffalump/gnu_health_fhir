from .utils import TIME_FORMAT, safe_attrgetter
from fhirclient.models import medicationstatement

__all__ = ['MedicationStatement']

class MedicationStatement(medicationstatement.MedicationStatement):

    def __init__(self, med, **kwargs):
        kwargs['jsondict'] = self._get_jsondict(med)
        super(MedicationStatement, self).__init__(**kwargs)

    def _get_jsondict(self, med):
        jsondict = {}

        #identifier
        jsondict['identifier']= [{'use': 'official',
                                    'value': '-'.join([med.medicament.rec_name,
                                        str(med.id)])}]

        #subject
        subject = med.name
        jsondict['subject'] = {'display': subject.name.rec_name,
                            'reference': '/'.join(['Patient', str(subject.id)])}

        #TODO
        #informationSource #See if we can determine this in Health?

        #dateAsserted - Use create/write date?
        date = med.create_date
        jsondict['dateAsserted'] = date.strftime('%Y-%m-%d')


        #status
        if med.is_active:
            s = 'active'
        elif med.course_completed:
            s = 'completed'
        elif med.discontinued:
            s = 'stopped'
        else:
            s = 'intended'
        jsondict['status'] = s

        #dosage
        # TODO Can always add more information!
        code_conv = {
                'seconds': 's',
                'minutes': 'min',
                'hours': 'h',
                'days': 'd',
                'months': 'mo',
                'years': 'a'}

        dose = {}
        # Amount (this should be listed, but could be patient reported)
        if med.dose:
            dose['doseQuantity'] = {'value': med.dose,
                                    'unit': med.dose_unit.name}

        # Route
        #     TODO Standard route values
        route = med.route
        if route:
            cc = {}
            c = {}
            cc['text'] = c['display'] = route.name
            c['code'] = route.code
            cc['coding'] = [c]
            dose['route'] = cc

        # PRN
        if med.frequency_prn or (safe_attrgetter(med, 'common_dosage.abbreviation') == 'prn'):
            dose['asNeededBoolean'] = True
        else:
            dose['asNeededBoolean'] = False
        
        #TODO
        # Site and Method 

        #timing
        #BID | TID | QID | AM | PM | QD | QOD | Q4H | Q6H +.
        timing = {}
        if med.frequency: #prefer specific information
            rep = {}
            if med.duration_period is not 'indefinite':
                rep['duration'] = med.duration
                rep['durationUnits'] = code_conv.get(med.duration_period)

            # Health stores timing as 1 per X s/min/hr
            rep['frequency'] = '1'
            rep['period'] = med.frequency
            rep['periodUnits'] = code_conv.get(med.frequency_unit)

            timing['repeat'] = rep

        elif med.common_dosage:

            c = {'display': med.common_dosage.abbreviation,
                    'system': 'http://snomed.info/sct',
                    'code': med.common_dosage.code}

            timing['code'] = {'text': med.common_dosage.name,
                            'coding': [c]}

        else: #No dosage information (either unknown or incomplete)
            timing = None
        if timing:
            dose['timing'] = timing

        #Rate - rateRatio
        #    Only if an infusion -- always mL/hr (I think?)
        if med.infusion:
            num = {'value': med.infusion_rate,
                    'unit': 'mL'}
            den = {'value': 1,
                    'unit': 'hr'}
            dose['rateRatio'] = {'numerator': num,
                                'denominator': den}
        jsondict['dosage'] = [dose]

        #taken
        #TODO Health equivalent?
        #y | n | unk | na
        if not med.discontinued:
            jsondict['taken'] = 'y'
        else:
            jsondict['taken'] = 'n'


        #reasonNotTaken
        if med.discontinued:
            jsondict['reasonNotTaken'] = {'text': med.discontinued_reason or '<unknown>'}

        #reasonCode
        # Ideally should make indication connect to patient condition
        reason = med.indication
        if reason:
            cc = {'text': reason.name}
            coding = {'system': 'urn:oid:2.16.840.1.113883.6.90', #ICD-10-CM
                        'code': reason.code,
                        'display': reason.name}
            cc['coding']=[coding]
            jsondict['reasonCode'] = [cc]

        #effectivePeriod
        start, end = med.start_treatment, med.end_treatment
        if start:
            p = {'start': start.strftime(TIME_FORMAT)}
            if end:
                p['end'] = end.strftime(TIME_FORMAT)
            jsondict['effectivePeriod'] = p

        #note
        if med.notes: jsondict['note'] = {'text': med.notes}

        #medicationCodeableConcept
        #TODO Fill this out more
        jsondict['medicationCodeableConcept'] = {'text': med.medicament.rec_name}

        return jsondict
