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

TIME_FORMAT='%Y-%m-%dT%H:%M:%S%z'

__all__=['safe_attrgetter', 'TIME_FORMAT']
