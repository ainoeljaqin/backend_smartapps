from rest_framework import serializers
from .models import Survey

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['user', 'name', 'job', 'income', 
                  'foodExpense', 'educationExpense', 'healthExpense', 'transportationTaxExpense', 
                  'pbbTaxExpense', 'electricityExpense', 'financialServiceAccess', 
                  'healthServiceAccess', 'governmentAssistance', 'economicLevel']
