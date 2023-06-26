# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.test import TestCase
from django.urls import reverse
from staticfiles.XMLGenerator import xml_config_to_dict, dict_to_xml_file
class LaserPageViewTestCase(TestCase):
    def test_update_laser_info(self):
        # Create a test XML file for the laser configuration
        xml_file_path = "staticfiles/toptica.xml"
        # You can create a copy of your original XML file or create a separate test XML file for testing purposes.

        # Define the updated laser information
        updated_host = "129.129.131.136"
        updated_port = 1234

        # Simulate a POST request to update the laser information
        response = self.client.post(reverse('laser_page'), {
            'laser_host': updated_host,
            'laser_port': updated_port,
        })

        # Check if the response is a redirect to the laser page
        self.assertRedirects(response, reverse('laser_page'))

        # Verify that the XML file was updated correctly
        toptica_host = xml_config_to_dict(xml_file_path)
        self.assertEqual(toptica_host["host"], updated_host)
        self.assertEqual(toptica_host["port"], updated_port)

        # You can also add additional assertions to verify the behavior and messages displayed on the page.
