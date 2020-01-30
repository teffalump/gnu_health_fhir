__all__ = ["helper_mixin"]


class helper_mixin(object):
    @classmethod
    def build_codeable_concept(cls, code, system=None, text=None):
        codeable_concept = {}
        if code:
            coding = {}
            if system:
                coding["system"] = system
            if text:
                coding["display"] = text
            coding["code"] = str(code)
            codeable_concept = {"coding": [coding]}
        if text:
            codeable_concept["text"] = text
        return codeable_concept
