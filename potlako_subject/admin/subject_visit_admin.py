from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from edc_visit_schedule.fieldsets import visit_schedule_fieldset_tuple
from edc_visit_tracking.modeladmin_mixins import VisitModelAdminMixin

from ..admin_site import potlako_subject_admin
from ..forms import SubjectVisitForm
from ..models import SubjectVisit
from .modeladmin_mixins import ModelAdminMixin


@admin.register(SubjectVisit, site=potlako_subject_admin)
class SubjectVisitAdmin(
        VisitModelAdminMixin, ModelAdminMixin, admin.ModelAdmin):

    form = SubjectVisitForm

    fieldsets = (
        (None, {
            'fields': [
                'appointment',
                'reason',
                'reason_unscheduled',
                'reason_unscheduled_other',
                'info_source',
                'info_source_other',
                'survival_status',
                'comments'
            ]}),
        visit_schedule_fieldset_tuple,
        audit_fieldset_tuple
    )

    radio_fields = {
        'reason': admin.VERTICAL,
        'reason_unscheduled': admin.VERTICAL,
        'info_source': admin.VERTICAL,
        'survival_status': admin.VERTICAL}
