from operator import attrgetter

# def safe_attrgetter(obj, *attrs, default=None): #py3 declaration
def safe_attrgetter(obj, *attrs, **kwargs): #py2 declaration
    """The fail-safe version of attrgetter"""
    default = kwargs.get('default', None) #py2 compatibility
    v = []
    for attr in attrs:
        try:
           x = attrgetter(attr)(obj)
        except:
           x = default
        v.append(x)
    return v[0] if len(v) == 1 else v

def days_hours_minutes(td):
    '''Return days, hours, minutes given
    timedelta object
    '''
    return td.days, td.seconds // 3600, (td.seconds // 60) % 60

def duration_from_timedelta(td, only='all'):
    '''Return a valid JSON dict of Duration type
    for timedelta object
    '''
    days, hours, minutes = days_hours_minutes(td)
    codes = []
    if days > 0:
        codes.append({'value': days, 'unit': 'day', 'system': 'http://unitsofmeasure.org', 'code': 'd'})
    if hours > 0:
        codes.append({'value': hours, 'unit': 'hour', 'system': 'http://unitsofmeasure.org', 'code': 'h'})
    if minutes > 0:
        codes.append({'value': minutes, 'unit': 'minute', 'system': 'http://unitsofmeasure.org', 'code': 'min'})
    return codes

TIME_FORMAT='%Y-%m-%dT%H:%M:%S%z'

__all__=['safe_attrgetter', 'TIME_FORMAT', 'days_hours_minutes', 'duration_from_timedelta']
