from .utils import TIME_FORMAT, safe_attrgetter
from fhirclient.models import observation

class Observation(observation.Observation):

    def __init__(self, observation):
        jsondict = self._get_jsondict(observation)
        super(Observation, self).__init__(jsondict=jsondict)

    def _get_jsondict(self, observation):
        jsondict = {}

        #comment
        jsondict['comment'] = observation.remarks

        #identifier
        jsondict['identifier'] = [{'use': 'official',
                                    'value': '-'.join([observation.name, str(observation.id)])}]

        #interpretation
        # TODO: Interpretation is complicated
        value = observation.result
        lower_limit = observation.lower_limit
        upper_limit = observation.upper_limit

        if value is not None \
            and lower_limit is not None \
            and upper_limit is not None:
            cc = {}
            coding = {}
            if value < lower_limit:
                v = 'L'
                d = 'Low'
            elif value > upper_limit:
                v = 'H'
                d = 'High'
            else:
                v = 'N'
                d = 'Normal'
            coding['system'] = 'http://hl7.org/fhir/v2/0078'
            coding['code'] = v
            coding['display'] = cc['text'] = d
            cc['coding'] = [coding]
            jsondict['interpretation'] = cc

        #issued
        issued = observation.write_date or observation.create_date
        if issued: jsondict['issued']= issued.strftime(TIME_FORMAT)

        #code
        #TODO Better coding!!
        code = observation.name
        if code:
            cc = {'text': code}
            cc['coding'] = [{'code': code, 'display': code}]
            jsondict['code'] = cc

        #performer
        persons = []
        performers = [x for x in\
                        safe_attrgetter(observation, 'gnuhealth_lab_id.pathologist', 'gnuhealth_lab_id.done_by')\
                        if x]
        for performer in performers:
            r = {'display': performer.name.rec_name,
                    'reference': ''.join(['Practitioner/', str(performer.id)])}
            persons.append(r)
        if persons: jsondict['performer'] = persons

        #referenceRange
        units = safe_attrgetter(observation, 'units.name', default='unknown')
        lower_limit = observation.lower_limit
        upper_limit = observation.upper_limit

        if units is not None \
            and lower_limit is not None \
            and upper_limit is not None:
                ref = {'low': {'value': lower_limit, 'unit': units},
                        'high': {'value': upper_limit, 'unit': units}}
                    # 'meaning': {
                        # 'text': 'Normal range',
                        # 'coding': [{
                            # 'system':'http://hl7.org/fhir/referencerange-meaning',
                            # 'code': 'normal'}]}}
                jsondict['referenceRange'] = [ref]

        #status
        value = observation.result
        if observation.excluded:
            if value is not None:
                status = 'cancelled'
            else:
                status = 'entered in error'
        else:
            if value is not None:
                status = 'final'
            else:
                status = 'registered'
        jsondict['status'] = status

        #valueQuantity
        #TODO More information
        value = observation.result
        units = safe_attrgetter(observation, 'units.name', default='unknown')
        # code = None
        if value is not None:
            jsondict['valueQuantity'] = {'value': value,
                                        'unit': units}

        #subject
        subject = safe_attrgetter(observation, 'gnuhealth_lab_id.patient')
        if subject:
            jsondict['subject'] = {'display': subject.name.rec_name,
                                    'reference': ''.join(['Patient/', str(subject.id)])}

        #effectiveDateTime
        t = safe_attrgetter(observation, 'gnuhealth_lab_id.date_analysis')
        if t: jsondict['effectiveDateTime'] = t.strftime(TIME_FORMAT)

        return jsondict

__all__=['Observation']
