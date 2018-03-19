# HEALTH_FHIR

This package aims to provide a functional FHIR interface to GNU Health data models. With the provided classes, one should be able to work with the back-end data from GNU Health in a FHIR-compatible way (through fhirclient).

#### Design

The ultimate goal is that for every appropriate FHIR Resource there will be an adapter which subclasses the fhirclient data model. This subclass takes the provided tryton model and imports the data. Basically, this is glue for fhirclient and GNU Health.

#### Resources

Currently, the package supports these FHIR resources:

- Patient
- Practitioner
- Immunization
- Condition
- Observation
- DiagnosticReport
- MedicationStatement
- FamilyMemberHistory
- Procedure

Not every element is supported for each resource, nor will this be the goal. For example, some of the elements have no equivalent in GNU Health.

#### Usage

The easiest example is to use Proteus with this package:

    from proteus import config, Model
    from health_fhir import Patient

    #Connect to the GNU Health demo server
    config = config.set_xmlrpc('http://admin:gnusolidario@health.gnusolidario.org:8000/health32/')

    #Get the patient model
    model = Model.get('gnuhealth.patient')

    #Find the first patient
    first_patient = model.find()[0]

    #Import the data
    patient = Patient(first_patient)

    #Now you can use the data just like in fhirclient
    print(patient.as_json()) #print FHIR JSON data
    <other fhirclient stuff>
