from fhirclient.models import immunization
from .utils import safe_attrgetter

class Immunization(immunization.Immunization):

    def __init__(self, vaccine):
        jsondict = self._get_jsondict(vaccine)
        super(Immunization, self).__init__(jsondict=jsondict)

    def _get_jsondict(self, vaccination):
        jsondict = {}

        #identifier
        jsondict['identifier'] = [{'use': 'official',
                                    'value': '-'.join([vaccination.vaccine.rec_name,
                                                    str(vaccination.id)])}]
        #date
        date = vaccination.date
        if date: jsondict['date'] = date.strftime("%Y-%m-%d")

        #notGiven
        #TODO Is there a field for this in Health (?)
        jsondict['notGiven'] = False

        #status
        status = vaccination.state
        if status == 'in_progress':
            g = 'in-progress'
        elif status == 'done':
            g = 'completed'
        else:
            g = None
        if g: jsondict['status'] = g

        #patient
        patient = vaccination.name
        if patient:
            jsondict['patient'] = {'display': patient.rec_name,
                                    'reference': ''.join(['Patient/', str(patient.id)])}

        #practitioner
        practitioner = vaccination.healthprof
        if practitioner:
            jsondict['practitioner'] = [{'actor':{'display': practitioner.rec_name,
                                                    'reference': ''.join(['Practitioner/', str(practitioner.id)])}}]

        #lotNumber
        number = safe_attrgetter(vaccination, 'lot.number')
        if number: jsondict['lotNumber'] = str(number)

        #expirationDate
        date = safe_attrgetter(vaccination, 'lot.expiration_date')
        if date: jsondict['expirationDate'] = date.strftime("%Y-%m-%d")

        #doseQuantity
        quantity = vaccination.amount
        if quantity is not None:
            jsondict['doseQuantity'] = {'value': quantity,
                                        'unit': 'mL',
                                        'system': 'http://snomed.info/sct',
                                        'code': '258773002'}

        #note
        notes = vaccination.observations
        if notes:
            jsondict['note'] = {'text': notes}

        #reportOrigin and primarySource
        #DEBUG If there is no attached administered healthprof,
        #   AND no reasonable documents then self-reported (?)
        administer = vaccination.healthprof
        asserter = vaccination.signed_by
        if administer is None and asserter is None:
            jsondict['reportOrigin']= {'text': 'Self-reported'}
            jsondict['primarySource'] = False
        else:
            # don't need to populate if primary source per standard
            # cc = {'text': 'Health professional asserter'}
            jsondict['primarySource'] = True

        #route
        route = vaccination.admin_route
        from .value_sets import immunizationRoute
        if route:
            ir = [i for i in immunizationRoute.contents if i['code'] == route.upper()]
            if ir:
                cc = {}
                c = {}
                c['display'] = cc['text'] = ir[0]['display']
                c['code'] = ir[0]['code']
                cc['coding']=[c]
                jsondict['route'] = cc

        #site
        site = vaccination.admin_site
        from .value_sets import immunizationSite
        if site:
            m=[i for i in immunizationSite.contents if i['code'] == site.upper()]
            if m:
                cc = {}
                c = {}
                c['display'] = cc['text'] = m[0]['display']
                c['code'] = m[0]['code']
                cc['coding'] = [c]
                jsondict['site'] = cc

        #vaccineCode
        #TODO Need better coding, much better!
        type_ = vaccination.vaccine
        if type_:
            cc = {}
            c = {}
            c['display'] = cc['text'] = type_.rec_name
            if type_.name.code:
                c['code'] = type_.name.code
                cc['coding']=[c]
            jsondict['vaccineCode'] = cc

        #reaction
        #TODO Must be reference in standard, but stored as text

        #vaccinationProtocol
        #TODO Better vaccine coding/info
        seq = vaccination.dose
        authority = vaccination.institution
        disease = safe_attrgetter(vaccination, 'vaccine.indications') #DEBUG
        description = vaccination.observations
        if seq:
            vp = {'doseSequence': seq,
                    'description': description}

            ref = {'display': safe_attrgetter(authority, 'name.rec_name'),
                    'reference': ''.join(['Institution/', str(authority.id)])}

            target = {'text': disease}

            # Unclear if equivalent concept in Health
            status = {'text': 'Counts'}
            # coding = Coding(code='count',
                            # display='Counts')
            # status.coding = [coding]
            vp['doseStatus'] = status

            vp['authority'] = ref
            vp['targetDisease'] = [target]

            jsondict['vaccinationProtocol'] = [vp]

        return jsondict

__all__ = ['Immunization']
