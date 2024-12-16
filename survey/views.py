from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Survey
from .serializers import SurveySerializer

import joblib
import pandas as pd

try:
    knn_model = joblib.load('AI/knn_model.pkl')
    scaler = joblib.load('AI/scaler.pkl')
except Exception as e:
    knn_model = None
    scaler = None
    print(f"Error loading model or scaler: {e}")

class SurveyDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        try:
            if user_id:
                survey = Survey.objects.get(user_id=user_id)
            else:
                survey = Survey.objects.get(user=request.user)

            serializer = SurveySerializer(survey)
            return Response(serializer.data)

        except Survey.DoesNotExist:
            return Response({"detail": "Survey not found."}, status=status.HTTP_404_NOT_FOUND)
    

class SurveyCreateView(APIView):
    def post(self, request):
        serializer = SurveySerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Extract data for prediction
                data_for_prediction = pd.DataFrame([{
                    "Pendapatan": request.data["income"],
                    "Pengeluaran Makanan": request.data["foodExpense"],
                    "Pengeluaran Pendidikan": request.data["educationExpense"],
                    "Pengeluaran Kesehatan": request.data["healthExpense"],
                    "Pajak": request.data["transportationTaxExpense"],
                    "Transport": request.data["transportationTaxExpense"],
                    "Pajak PBB": request.data["pbbTaxExpense"],
                    "Biaya Listrik": request.data["electricityExpense"],
                }])

                # normalization
                if scaler is None:
                    return Response(
                        {"error": "Scaler is not available."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

                data_scaled = scaler.transform(data_for_prediction)

                # label prediction
                if knn_model is None:
                    return Response(
                        {"error": "Classification model is not available."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

                label_pred = knn_model.predict(data_scaled)[0]

            except KeyError as e:
                return Response(
                    {"error": f"Missing field in input data: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except ValueError as e:
                return Response(
                    {"error": f"Data format error: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                return Response(
                    {"error": f"An unexpected error occurred during prediction: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            survey = serializer.save()
            survey.economicLevel = label_pred
            survey.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)