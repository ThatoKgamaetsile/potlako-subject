from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import potlako_subject_admin
from ..forms import BaselineClinicalSummaryForm
from ..models import BaselineClinicalSummary
from .modeladmin_mixins import ModelAdminMixin


@admin.register(BaselineClinicalSummary, site=potlako_subject_admin)
class BaselineClincalSummaryAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = BaselineClinicalSummaryForm

    fieldsets = (
        (None, {
            'fields': ('subject_identifier',
                       'symptoms_summary',
                       'cancer_concern',
                       'cancer_concern_other',
                       'cancer_probability'),
        }), audit_fieldset_tuple)

    radio_fields = {
        'cancer_concern': admin.VERTICAL,
        'cancer_probability': admin.VERTICAL,
    }

    list_display = ('subject_identifier', 'cancer_concern', 'cancer_concern_other', 'cancer_probability')
