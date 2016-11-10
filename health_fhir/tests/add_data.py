# Create a person
import sys

from proteus import Model, config, Wizard
from random import choice, random
import datetime

# Test database with required modules already installed
#config = config.set_trytond(config_file='trytond.conf',
                            #database='gnuhealth_test')

config = config.set_xmlrpc('http://admin:admin@teffalump.com:8001/demo')

# Models
User = Model.get('res.user')
Patient = Model.get('gnuhealth.patient')
Du = Model.get('gnuhealth.du')
Alt = Model.get('gnuhealth.person_alternative_identification')
Name = Model.get('gnuhealth.person_name')
Party = Model.get('party.party')
Lang = Model.get('ir.lang')
Hp = Model.get('gnuhealth.healthprofessional')
Spec = Model.get('gnuhealth.specialty')
MSpec = Model.get('gnuhealth.hp_specialty')
Inst = Model.get('gnuhealth.institution')
Path = Model.get('gnuhealth.pathology')
TestType = Model.get('gnuhealth.lab.test_type')
Lab = Model.get('gnuhealth.lab')
Request = Model.get('gnuhealth.patient.lab.test')
Fh = Model.get('gnuhealth.patient.family.diseases')
Medicament = Model.get('gnuhealth.medicament')
Surgery = Model.get('gnuhealth.surgery')
Procedure = Model.get('gnuhealth.procedure')
OR = Model.get('gnuhealth.hospital.or')

#### Institution

party = Party()
party.is_institution = True
party.name = 'St. Example Hospital'
party.save()

inst = Inst()
inst.name = party
inst.code = 'HOSPITAL1'
inst.institution_type = 'hospital'
inst.public_level = 'public'
inst.save()

op_room = OR()
op_room.name = 'West Operating Room'
op_room.institution = inst
op_room.save()

print('Institution added')

#### PATIENT

# An address
du = Du()
du.name = 'Weird'
du.address_street = 'Test Drive Road'
du.address_street_number = 100
du.address_zip = '94949'
du.address_city = 'Test City'
du.municipality = 'Test Haven'
du.save()

# A person
party = Party()
party.name = 'First Test'
party.lastname = 'Weird'
party.is_person = party.is_patient = True
party.gender = 'f'
party.dob = datetime.date(1980,1,1)
party.marital_status = 'm'
party.active = True
party.save()

# Set language
(en, ) = Lang.find([('code', '=', 'en_US')])
party.lang = en
party.save()

# A nickname
party.person_names.new(use='nickname',
        family='Weird',
        given='Nickname Test',
        prefix='Dr',
        suffix='III')
party.save()

# Contacts
party.contact_mechanisms.new(type='phone', value='245-234-2344')
party.contact_mechanisms.new(type='mobile', value='245-234-2344')
party.contact_mechanisms.new(type='email', value='test@example.com')
party.save()

# Add the domiciliary unit
party.du = du
party.save()

# Alt ids
party.alternative_identification = True
party.alternative_ids.new(code='PASSPORTID_2222',
                            alternative_id_type='country_id',
                            comments='Passport ID')
party.save()

print('Party saved')

# A patient
pat = Patient()
pat.biological_sex = 'f'
pat.deceased = False
pat.name = party
pat.save()

print('Patient saved')

#### DOCTOR

# A person
party = Party()
party.name = 'Doctor Test'
party.lastname = 'Smart'
party.is_person = party.is_healthprof = True
party.gender = 'f'
party.dob = datetime.date(1970,1,1)
party.active = True
party.internal_user = User.find(['id', '=', 1])[0] #admin
party.save()

# Contacts
party.contact_mechanisms.new(type='phone', value='245-444-2344')
party.contact_mechanisms.new(type='email', value='doctor@example.com')
party.save()

# Set language
(en, ) = Lang.find([('code', '=', 'en_US')])
party.lang = en
party.save()

# Health Prof info 
hp = Hp()
hp.name = party
hp.code = 'BOARDCERTIFIED'
hp.save()

# Add specialties
(im, ) = Spec.find(['code', '=', 'INTERNAL'])
(g, ) = Spec.find(['code', '=', 'GERIATRICS'])
(n, ) = Spec.find(['code', '=', 'NEPHRO'])
hp.specialties.new(specialty=n)
hp.specialties.new(specialty=g)
hp.specialties.new(specialty=im)
hp.save()

# Pick main specialty
(ms, ) = MSpec.find([('specialty', '=', im.id),
                    ('name', '=', hp.id)])
hp.main_specialty = ms
hp.save()

# Connect to institution
hp.institution = inst
hp.save()

# Connect to patient
pat.primary_care_doctor = hp
pat.save()

print('Doctor saved')

#### Conditions

conditions = Path.find([('id', 'in', [1, 9, 68, 100])])
for c in conditions:
    pat.diseases.new(pathology=c,
                    healthprof=hp,
                    diagnosed_date=datetime.date(2010, 2, 4),
                    healed_date=choice([datetime.date(2016, 1, 1), None]),
                    short_comment='It will relapse',
                    disease_severity=choice(['1_mi', '2_mo', '3_sv']))
pat.save()

print('Added conditions')

#### Lab

# Make request
cbc = TestType.find([('code', '=', 'CBC')])[0]
wiz = Wizard('gnuhealth.patient.lab.test.request')
wiz.form.patient = pat
wiz.form.doctor = hp
wiz.form.tests.append(cbc)
wiz.execute('request')

# Create lab test
request = Request.find()[0]
wiz = Wizard('gnuhealth.lab.test.create', [request])
wiz.execute('create_lab_test')

# Fill-in results
lab = Lab.find()[0]
for test in lab.critearea:
    test.result = round(random() * 10, 1)
    test.save()

print('Added lab test')

#### Family History

conditions = Path.find([('id', 'in', [17, 33, 35, 45, 88])])
pat.family_history.new(name=conditions[0],
                        relative='mother')
pat.family_history.new(name=conditions[1],
                        xory='s',
                        relative='sister')
pat.family_history.new(name=conditions[2],
                        relative='nephew')
pat.family_history.new(name=conditions[3],
                        xory='f',
                        relative='aunt')
pat.family_history.new(name=conditions[4],
                        xory='s',
                        relative='brother')
pat.save()

print('Added family history')

#### Immunization
cholera = Medicament.find([('rec_name', '=', 'cholera vaccine')])[0]
measles = Medicament.find([('rec_name', '=', 'measles vaccine')])[0]
pat.vaccinations.new(vaccine=cholera,
                        institution=inst)
pat.vaccinations.new(vaccine=measles,
                        institution=inst)
pat.save()
print('Added immunizations')

#### Surgeries/Procedures

procedures = Procedure.find([('id', 'in', [43, 222, 454, 42, 22, 24, 500])])

for i in range(5):
    #Add more team members?
    pat.surgery.new(surgeon=hp,
                    anesthetist=hp,
                    institution=inst,
                    pathology=conditions[i],
                    operating_room=op_room
                    )

pat.save()
for sx in Surgery.find():
    for proc in procedures:
        sx.procedures.new(procedure=proc)
    sx.save()
print('Added surgeries')

#### Medications
