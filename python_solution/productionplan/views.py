from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import json

class ProductionPlan(APIView):
    def _look_for_key_startswith(self, dictionary, searched_key):
        for key, value in dictionary.items():
            if key.startswith(searched_key):
                return value
        
        return None

    def get(self, request, format=None):
        return Response(
            "Nothing to get here! You should use the POST method to ask for the production plan.",
            status=status.HTTP_400_BAD_REQUEST
        )

    def post(self, request, format=None):
        try:
            load = request.data["load"]
            fuels = request.data["fuels"]        
            powerplants = request.data["powerplants"]
        except KeyError as key_e:
            return Response(f"Data do not have any {key_e} key inside the JSON Object.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(f"Unknown error : {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        merit_ordered_pp = []

        for elem in powerplants:
            print(elem)

        return Response("Good start!", status=status.HTTP_200_OK)