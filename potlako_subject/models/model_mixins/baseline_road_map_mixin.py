from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from ...constants import UNSURE
from ..clinician_call_enrollment import ClinicianCallEnrollment
from ..subject_visit import SubjectVisit
from potlako_subject.models.subject_screening import SubjectScreening

class BaselineRoadMapMixin:
    """A class to gather all values from Clinician Call Enrollment, 
    Patient Call Initial, Investigations Ordered, Investigations Resulted
    to build the Baseline Roadmap.
    """

    def __init__(self, subject_identifier=None, subject_visit=None):
        
        self.baseline_dict = {}
        try:
            screening_obj = SubjectScreening.objects.get(subject_identifier=subject_identifier)
        except SubjectScreening.DoesNotExist:
            pass
        else:
            self.baseline_dict.update(self.get_clinician_call_attrs(
                screening_identifier=screening_obj.screening_identifier))
        
        
        try:
            subject_visit_obj = SubjectVisit.objects.get(id=subject_visit) 
        except SubjectVisit.DoesNotExist:
            pass
        else:
    
            crfs_list = ['potlako_subject.patientcallinitial',
                         'potlako_subject.investigationsordered',
                         'potlako_subject.investigationsresulted',
                          'potlako_subject.medicalconditions']
    
            attrs_list = [['report_datetime', 'age_in_years', 'hiv_status',
                          'patient_symptoms', 'perfomance_status', 'pain_score'],
                           ['tests_ordered_type', ],
                           ['diagnosis_results', 'cancer_type', 'cancer_stage']]
    
            for crf_cls, attrs in zip(crfs_list, attrs_list):
                crf_model = django_apps.get_model(crf_cls)
                crf_dict = self.get_crf_attrs(crf_model, attrs,
                                   subject_visit=subject_visit_obj,)
                if crf_dict:
                    self.baseline_dict.update(crf_dict)

    def get_clinician_call_attrs(self, screening_identifier=None):
        """Extract values required for Baseline Map from Clinician Call
        Enrollment model.
        """

        enrollment_dict = {}
        attributes = ['suspected_cancer', 'suspected_cancer_other',
                      'gender', 'suspicion_level', 'last_hiv_result']

        try:
            clinician_call_obj = ClinicianCallEnrollment.objects.get(
            screening_identifier=screening_identifier)
        except ObjectDoesNotExist:
            return None
        else:
            for attr in attributes:
                value = getattr(
                        clinician_call_obj, attr)

                if attr == 'suspected_cancer' and value == UNSURE:
                    value = getattr(
                        clinician_call_obj, 'suspected_cancer_unsure')

                enrollment_dict.update({attr:value})

        return enrollment_dict

    def get_crf_attrs(self, model_cls,  *attributes, subject_visit=None):
        """Extract values required for Baseline Map from model.
        """

        crf_dict = {}
        if subject_visit:
            try:
                model_obj = model_cls.objects.get(
                    subject_visit=subject_visit)
            except model_cls.DoesNotExist:
                return None
            else:
                for attr in attributes:
                    value = getattr(model_obj, attr)
                    crf_dict.update({attr:value})

        return crf_dict

