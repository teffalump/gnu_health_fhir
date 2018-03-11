This package aims to provide a functional FHIR interface to GNU Health data models. With the provided classes, one should be able to work with the back-end data from GNU Health in a FHIR-compatible way (through fhirclient).

#### Design
There is a simple adapter class which converts the GNU Health data into a FHIR-like object. These are named things like patientAdapter, conditionAdapter, and so on.

Some further code, sub-classing the fhirclient data models, imports the adapter data into the fhirclient data models - almost just a copy/paste.

There is a final superclass that holds the adapter and fhirclient classes.

If this sounds like a redundant design, I'm quite sure it is. Maybe I don't need the intermediate adapter classes (patientAdapter, etc) and should simply import the data directly into the fhirclient classes and go from there. I'm not opposed to removing the intermediary, but I hade some worries about the standard changing such that simple data classes would be better, rather than bulky standard-compliant models. But, I'm second-guessing that decision. I'll see how it goes.
