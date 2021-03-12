from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class ProductionPlan(APIView):
    def _look_for_key_startswith(self, dictionary, searched_key):
        for key, value in dictionary.items():
            if key.startswith(searched_key):
                return value
        
        return None
    
    def _calculate_price_ordered_pp(self, pp_list, fuels_dict):
        co2_pricing = 0.3 * self._look_for_key_startswith(fuels_dict, "co2")

        for elem in pp_list:
            if "gas" in elem["type"]:
                price = round(self._look_for_key_startswith(fuels_dict, "gas") / elem["efficiency"], 2) + co2_pricing
            elif "wind" in elem["type"]:
                price = 0
            else:
                price = round(self._look_for_key_startswith(fuels_dict, "kerosine") / elem["efficiency"], 2)
            
            elem["mwh_price"] = price
        
        return sorted(pp_list, key=lambda x: x["mwh_price"])
    
    def _calculate_output_data(self, pp_list, fuels_dict, load_left):
        data = []

        for elem in pp_list:
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
                data.append({'name': elem["name"], 'p': 0})

            elif load_left >= max_load_difference:
                data.append({'name': elem["name"], 'p': max_load_difference})
                load_left = round(load_left - max_load_difference, 1)

            elif load_left > 0 and load_left >= min_load_difference and load_left <= max_load_difference:
                data.append({'name': elem["name"], 'p': load_left})
                load_left = round(load_left - load_left, 1)

            else:
                data.append({'name': elem["name"], 'p': 0})
        
        return data, load_left

    def post(self, request, format=None):
        try:
            load_val = request.data["load"]
            fuels_dict = request.data["fuels"]        
            powerplants = request.data["powerplants"]
        except KeyError as key_e:
            return Response(f"Data do not have any {key_e} key inside the JSON Object.", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"Unknown error : {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        mwh_price_ordered_pp = self._calculate_price_ordered_pp(powerplants, fuels_dict)

        output_data, load_left = self._calculate_output_data(mwh_price_ordered_pp, fuels_dict, load_val)
        
        if load_left > 0:
            # output_data.insert(0, {'warning': "Not enough power for the required load. Everything should be at full power."})
            output_data.append({'name': 'remaining_load', 'p' : load_left})

            return Response(output_data, status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(output_data, status=status.HTTP_200_OK)