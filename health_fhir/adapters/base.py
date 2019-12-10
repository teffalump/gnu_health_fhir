__all__=["BaseAdapter"]

class BaseAdapter:
    """The base adapter class:
            - defines multiple functions to be implemented by child classes (CRUD)
            - provides helper functions to covert between object types
    """

    ##### CONVERSION ######
    @classmethod
    def toFhirObject(gh_obj):
        raise NotImplemented()

    @classmethod
    def toHealthObject(fhir_obj):
        raise NotImplemented()


    ###### CRUD #######
    @classmethod
    def read():
        raise NotImplemented()

    @classmethod
    def create():
        raise NotImplemented()

    @classmethod
    def update():
        raise NotImplemented()

    @classmethod
    def delete():
        raise NotImplemented()


    ##### HELPER CLASSES #####
