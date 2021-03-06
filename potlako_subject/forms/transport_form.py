from django import forms

from potlako_validations.form_validators import TransportFormValidator

from ..models import Transport
from .form_mixins import SubjectModelFormMixin


class TransportForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = TransportFormValidator

    class Meta:
        model = Transport
        fields = '__all__'
