This package aims to provide a functional FHIR interface to GNU Health data models. With the provided classes, one should be able to work with the back-end data from GNU Health in a FHIR-compatible way (through fhirclient).

#### Design

For every FHIR Resource, there will be an adapter which subclasses the fhirclient data model. This subclass takes the provided tryton model and imports the data. Basically, this is glue for fhirclient and GNU Health.
