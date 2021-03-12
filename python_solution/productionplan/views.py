from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import math

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
            load_val = request.data["load"]
            fuels_dict = request.data["fuels"]        
            powerplants = request.data["powerplants"]
        except KeyError as key_e:
            return Response(f"Data do not have any {key_e} key inside the JSON Object.", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"Unknown error : {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        load_left = load_val

        for elem in powerplants:
            if "gas" in elem["type"]:
                energy_type = "gas"
            elif "wind" in elem["type"]:
                energy_type = "wind"
            else:
                energy_type = "kerosine"

            co2_pricing = 0.3 * self._look_for_key_startswith(fuels_dict, "co2")
            
            if energy_type == "wind":
                price = 0
            elif energy_type == "gas":
                price = round(self._look_for_key_startswith(fuels_dict, energy_type) / elem["efficiency"], 2) + co2_pricing
            else:
                price = round(self._look_for_key_startswith(fuels_dict, energy_type) / elem["efficiency"], 2)
            
            elem["mwh_price"] = price
        
        mwh_price_ordered_pp = sorted(powerplants, key=lambda x: x["mwh_price"])

        output_data = []

        for elem in mwh_price_ordered_pp:
            if "wind" in elem["type"]:
                other_calculation_elem = self._look_for_key_startswith(fuels_dict, "wind") / 100
            else:
                other_calculation_elem = 1

            efficiency_multiplier = elem["efficiency"] * other_calculation_elem
            max_load_difference = round(elem["pmax"] * efficiency_multiplier, 1)
            min_load_difference = round(elem["pmin"] * efficiency_multiplier, 1)

            # Uncomment for debug purpose
            # print(f"{elem['name']}'s max MWh calculated : {max_load_difference} <==> load left : {load_left}")
            # print(f"{elem['name']}'s min MWh calculated : {min_load_difference} <==> load left : {load_left}")
            # print(f"How many p for 0.1MWH ? {(1 / efficiency_multiplier) / 10}")
            # print("-------------------------------")

            if efficiency_multiplier == 0:
                output_data.append({'name': elem["name"], 'p': 0})
            elif load_left >= max_load_difference:
                # output_data.append({'name': elem["name"], 'p': elem["pmax"]})
                output_data.append({'name': elem["name"], 'p': max_load_difference})
                load_left = round(load_left - max_load_difference, 1)
            elif load_left > 0 and load_left >= min_load_difference and load_left <= max_load_difference:
                # output_data.append({'name': elem["name"], 'p': load_left / efficiency_multiplier})
                output_data.append({'name': elem["name"], 'p': load_left})

                load_left = round(load_left - load_left, 1)
            else:
                output_data.append({'name': elem["name"], 'p': 0})
        
        if load_left > 0:
            return Response("Not enough power for the required load. Everything should be at full power.", status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(output_data, status=status.HTTP_200_OK)