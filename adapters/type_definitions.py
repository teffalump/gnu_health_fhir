# A few data types that are easier as namedlists

from namedlist import namedlist

Identifier = namedlist("Identifier", 'use type system value period', default=None)
Coding = namedlist("Coding", 'system version code display userSelected', default=None)
CodeableConcept = namedlist("CodeableConcept", 'coding text', default=None)
HumanName = namedlist("HumanName", 'use text family given prefix suffix period', default=None)
Period = namedlist("Period", 'start end', default=None)
ContactPoint = namedlist("ContactPoint", 'system value use rank period', default=None)
Attachment = namedlist("Attachment", 'contentType language data uri size hash title creation', default=None)
Address = namedlist("Address", 'use type text line city district state postalCode country period', default=None)
Reference = namedlist("Reference", 'reference display', default=None)
ReferenceRange = namedlist("ReferenceRange", 'low high meaning age text', default=None)
Quantity = namedlist("Quantity", 'value comparator unit uri code', default=None)
Condition = namedlist("Condition", 'code outcome note', default=None)
Annotation = namedlist("Annotation", 'author time text', default=None)

communication = namedlist("communication", 'language preferred', default=None)
vaccinationProtocol = namedlist("vaccinationProtocol", 'doseSequence description authority series seriesDoses targetDisease doseStatus doseStatusReason', default=None)
practitionerRole = namedlist("practitionerRole", 'managingOrganization role specialty period location healthcareService', default=None)
qualification = namedlist("qualification", 'identifer code period issuer', default=None)
performer = namedlist("performer", 'actor role', default=None)

__all__ = ['Identifier', 'Coding', 'CodeableConcept', 'HumanName', 'Period', 'ContactPoint', 'Attachment', 'Address', 'Reference', 'ReferenceRange', 'Quantity', 'Condition', 'Annotation', 'vaccinationProtocol', 'qualification', 'practitionerRole', 'communication', 'performer']
