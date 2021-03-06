from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_constants.constants import NO, YES
from edc_form_validators import FormValidatorMixin

from potlako_validations.form_validators import ClinicianCallEnrollmentFormValidator
from potlako_validations.form_validators import NextOfKinFormValidator

from ..models import ClinicianCallEnrollment
from ..models import NextOfKin


class ClinicianCallEnrollmentForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = ClinicianCallEnrollmentFormValidator

    screening_identifier = forms.CharField(
        label='Screening Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        cleaned_data = super().clean()

        next_of_kin = self.data.get(
            'nextofkin_set-0-kin_lastname')

        if (cleaned_data.get('kin_details_provided') == YES
                and not next_of_kin):
            raise forms.ValidationError(
                {'kin_details_provided': 'Please complete the next of kin '
                 'table below.'})
        elif (cleaned_data.get('kin_details_provided') == NO
                and next_of_kin):
            raise forms.ValidationError(
                {'kin_details_provided': 'The next of kin table below is not'
                 'required.'})

    class Meta:
        model = ClinicianCallEnrollment
        fields = '__all__'


class NextOfKinForm(FormValidatorMixin, forms.ModelForm):

    form_validator_cls = NextOfKinFormValidator

    class Meta:
        model = NextOfKin
        fields = '__all__'
