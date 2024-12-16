from django.contrib import admin
from .models import Survey

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'name', 'job', 'income',
        'foodExpense', 'educationExpense', 'healthExpense',
        'transportationTaxExpense', 'pbbTaxExpense', 'electricityExpense',
        'financialServiceAccess', 'healthServiceAccess', 'governmentAssistance'
    )
    list_filter = (
        'job',
        'financialServiceAccess',
        'healthServiceAccess',
        'governmentAssistance',
    )
    search_fields = ('user__username', 'job')
    ordering = ('user',)
