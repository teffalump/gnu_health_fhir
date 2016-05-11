# A few data types that are easier as namedtuples

from collections import namedtuple

Identifier = namedtuple("Identifier", 'use type system value period')
Coding = namedtuple("Coding", 'system version code display userSelected')
CodeableConcept = namedtuple("CodeableConcept", 'coding text')
HumanName = namedtuple("HumanName", 'use text family given prefix suffix period')
Period = namedtuple("Period", 'start end')
ContactPoint = namedtuple("ContactPoint", 'system value use rank period')
Attachment = namedtuple("Attachment", 'contentType language data uri size hash title creation')
Language = namedtuple("Language", 'language preferred')
Address = namedtuple("Address", 'use type text line city district state postalCode country period')
Reference = namedtuple("Reference", 'reference display')
ReferenceRange = namedtuple("ReferenceRange", 'low high meaning age text')
Quantity = namedtuple("Quantity", 'value comparator unit uri code')
Condition = namedtuple("Condition", 'code outcome note')
Annotation = namedtuple("Annotation", 'author time text')
vaccinationProtocol = namedtuple("vaccinationProtocol" 'doseSequence description authority series seriesDoses targetDisease doseStatus doseStatusReason')

__all__ = ['Identifier', 'Coding', 'CodeableConcept', 'HumanName', 'Period', 'ContactPoint', 'Attachment', 'Language', 'Address', 'Reference', 'ReferenceRange', 'Quantity', 'Condition', 'Annotation', 'vaccinationProtocol']
