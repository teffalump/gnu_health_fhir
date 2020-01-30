__all__ = ["COMMON_SYSTEMS"]


class COMMON_SYSTEMS:
    @classmethod
    def get_icd_10_cm_system(cls):
        return "urn:oid:2.16.840.1.113883.6.90"

    @classmethod
    def get_icd_10_pcs_system(cls):
        return "urn:oid:2.16.840.1.113883.6.4"

    @classmethod
    def get_bcp_47_language_system(cls):
        return "urn:ietf:bcp:47"
