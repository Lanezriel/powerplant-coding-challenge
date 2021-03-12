from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json
import os

class ProductionplanTest(APITestCase):
    def test_endpoint_correct_data_response(self):
        url = reverse('productionplan')
        
        with open('../example_payloads/payload1.json') as file:
            data = json.load(file)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_enpoint_key_error_response(self):
        url = reverse('productionplan')
        
        data = {}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_endpoint_response_p_vs_data_load(self):
        url = reverse('productionplan')

        file_path = '../example_payloads/'

        for file in os.listdir(file_path):
            with open(file_path + file) as f:
                data = json.load(f)
            
            load = data['load']
            
            response = self.client.post(url, data, format='json')

            response_total = 0

            for elem in response.data:
                response_total += elem['p']
            
            self.assertEqual(response_total, load)
        
            if response.data[-1]['name'] == 'remaining_load':
                self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
