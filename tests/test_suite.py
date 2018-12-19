from health_fhir.adapters import Patient, Condition, Procedure, Practitioner, Observation, DiagnosticReport, Immunization, FamilyMemberHistory, MedicationStatement, Encounter, ClinicalImpression
from proteus import config, Model
import pytest

config = config.set_xmlrpc('http://admin:gnusolidario@health.gnusolidario.org:8000/health32/')

# @pytest.mark.skip
def test_ci_info():
    CI = Model.get('gnuhealth.patient.evaluation')
    for ci in CI.find():
        info = ClinicalImpression(ci)
        print(info.as_json())
    assert 0

# @pytest.mark.skip
def test_enc_info():
    ENC = Model.get('gnuhealth.patient.evaluation')
    for enc in ENC.find():
        info = Encounter(enc)
        print(info.as_json())
    assert 0

# @pytest.mark.skip
def test_ms_info():
    MS = Model.get('gnuhealth.patient.medication')
    for ms in MS.find():
        info = MedicationStatement(ms)
        print(info.as_json())
    assert 0

# @pytest.mark.skip
def test_fh_info():
    FH = Model.get('gnuhealth.patient.family.diseases')
    for fh in FH.find():
        info = FamilyMemberHistory(fh)
        print(info.as_json())
    assert 0

# @pytest.mark.skip
def test_dr_info():
    DR = Model.get('gnuhealth.lab')
    for dr in DR.find([('date_analysis', '!=', None)]):
        report = DiagnosticReport(dr)
        print(report.as_json())
    assert 0

# @pytest.mark.skip
def test_vac_info():
    VAC = Model.get('gnuhealth.vaccination')
    for vac in VAC.find():
        v = Immunization(vac)
        print(v.as_json())
    assert 0

# @pytest.mark.skip
def test_patient_info():
    Pat = Model.get('gnuhealth.patient')
    for p in Pat.find():
        patient = Patient(p)
        print(patient.as_json())
        # assert set(keys).issubset(p.keys())
        # for key in keys:
            # print(getattr(patient.resource, key))
    assert 0

# @pytest.mark.skip
def test_condition_info():
    Cond = Model.get('gnuhealth.patient.disease')
    for c in Cond.find():
        condition = Condition(c)
        print(condition.as_json())
    assert 0

# @pytest.mark.skip
def test_procedure_info():
    Proc = Model.get('gnuhealth.operation')
    for p in Proc.find():
        procedure = Procedure(p)
        print(procedure.as_json())
    assert 0

# @pytest.mark.skip
def test_practitioner_info():
    HP = Model.get('gnuhealth.healthprofessional')
    for hp in HP.find():
        hprof = Practitioner(hp)
        print(hprof.as_json())
    assert 0

# @pytest.mark.skip
def test_obs_info():
    Obs = Model.get('gnuhealth.lab.test.critearea')
    for obs in Obs.find([[('gnuhealth_lab_id', '!=', None)]]):
        observ = Observation(obs)
        print(observ.as_json())
    assert 0
