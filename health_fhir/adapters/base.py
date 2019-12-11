__all__ = ["BaseAdapter"]


class BaseAdapter:
    """The base adapter class:
            - defines multiple functions to be implemented by child classes (CRUD)
            - provides helper functions to covert between object types
    """

    ##### CONVERSION ######
    @classmethod
    def to_fhir_object(cls, gh_object):
        raise NotImplemented()

    @classmethod
    def to_health_object(cls, fhir_object):
        raise NotImplemented()

    ###### CRUD #######
    @classmethod
    def read(cls, gh_object):
        raise NotImplemented()

    @classmethod
    def create(cls, fhir_objects):
        raise NotImplemented()

    @classmethod
    def update(cls, fhir_obj, gh_object):
        raise NotImplemented()

    @classmethod
    def delete(cls, gh_object):
        raise NotImplemented()

    ##### HELPER CLASSES #####
