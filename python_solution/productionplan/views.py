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
            return Response(f"Data do not have any {key_e} key inside the JSON Object.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
                price = self._look_for_key_startswith(fuels_dict, energy_type) + co2_pricing
            else:
                price = self._look_for_key_startswith(fuels_dict, energy_type)
            
            elem["mwh_price"] = price
        
        mwh_price_ordered_pp = sorted(powerplants, key=lambda x: x["mwh_price"])

        output_data = []

        for elem in mwh_price_ordered_pp:
            if "wind" in elem["type"]:
                other_calculation_elem = self._look_for_key_startswith(fuels_dict, "wind") / 100
            else:
                other_calculation_elem = 1

            efficiency_multiplier = elem["efficiency"] * other_calculation_elem
            max_load_difference = elem["pmax"] * efficiency_multiplier
            min_load_difference = elem["pmin"] * efficiency_multiplier

            # Uncomment for debug purpose
            # print(f"{elem['name']}'s max MWh calculated : {max_load_difference} <==> load left : {load_left}")
            # print(f"{elem['name']}'s min MWh calculated : {min_load_difference} <==> load left : {load_left}")
            # print(f"How many p for 0.1MWH ? {(1 / efficiency_multiplier) / 10}")
            # print("-------------------------------")

            if efficiency_multiplier == 0:
                output_data.append({'name': elem["name"], 'p': 0})
            elif load_left >= max_load_difference:
                output_data.append({'name': elem["name"], 'p': elem["pmax"]})
                load_left -= max_load_difference
            elif load_left > 0 and load_left >= min_load_difference and load_left <= max_load_difference:
                # Uncomment the next line if you want the power rounded up (which will then stop to correspond to a multiple of 0.1 MWh)
                # output_data.append({'name': elem["name"], 'p': math.ceil(load_left / efficiency_multiplier)})

                #Use the next line if you want the power to be the closest to a multiple of 0.1 MWh (this will be a big float)
                output_data.append({'name': elem["name"], 'p': load_left / efficiency_multiplier})

                load_left -= load_left
            else:
                output_data.append({'name': elem["name"], 'p': 0})
        
        if load_left > 0:
            return Response("Not enough power for the required load. Everything should be at full power.", status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(output_data, status=status.HTTP_200_OK)