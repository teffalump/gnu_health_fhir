class Resource:
    """Common superclass for the interface classes

    Provides basic methods
    """

    def __init__(self, adapter):
        self.adapter = adapter
        self._import_data()

    def _import_data(self):
        'Implement the data importing here'

        raise NotImplemented

    @property
    def json(self):
        '''Return FHIR-valid JSON'''

        self.as_json()

    @property
    def xml(self):
        '''Return FHIR-valid XML'''

        raise NotImplemented
