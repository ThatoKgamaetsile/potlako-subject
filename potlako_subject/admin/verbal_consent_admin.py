from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fields, audit_fieldset_tuple)

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import potlako_subject_admin
from ..forms import VerbalConsentForm
from ..models import VerbalConsent


@admin.register(VerbalConsent, site=potlako_subject_admin)
class VerbalConsentAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = VerbalConsentForm

    fieldsets = (
        (None, {
            'fields': (
                'verbal_consent_image',
                'user_uploaded',
                'datetime_captured',
                'screening_identifier',
                'version',
                'subject_identifier',
                'language'
            )}),
        audit_fieldset_tuple)

    search_fields = ('subject_identifier',)


    def get_readonly_fields(self, request, obj=None):
        return (super().get_readonly_fields(request, obj=obj) + audit_fields +
                ('language', 'screening_identifier', 
                 'subject_identifier', 'report_datetime',
                 'verbal_consent_image', 'datetime_captured',
                 'user_uploaded'))
