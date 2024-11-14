from django.shortcuts import render

from rest_framework.decorators import api_view
from django.http import JsonResponse

@api_view(['GET'])
def getData(request):
    person = {
        "Kelas": "4B",
        "Kelompok": 1,
        "Anggota": [
            "Ainul", "Bahrul", "Nasrul"
        ],
    }

    return JsonResponse(person)

