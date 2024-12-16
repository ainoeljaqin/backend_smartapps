from django.db import models
from django.conf import settings

class Survey(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Menghubungkan dengan CustomUser
    name = models.CharField(max_length=200, default='Unknown')  # Menambahkan kolom nama lengkap
    job = models.CharField(max_length=100)
    income = models.CharField(max_length=100)
    foodExpense = models.CharField(max_length=100)
    educationExpense = models.CharField(max_length=100)
    healthExpense = models.CharField(max_length=100)
    transportationTaxExpense = models.CharField(max_length=100)
    pbbTaxExpense = models.CharField(max_length=100)
    electricityExpense = models.CharField(max_length=100)
    financialServiceAccess = models.BooleanField(default=False)
    healthServiceAccess = models.BooleanField(default=False)
    governmentAssistance = models.BooleanField(default=False)
    economicLevel = models.CharField(max_length=30, null=True, blank=True)