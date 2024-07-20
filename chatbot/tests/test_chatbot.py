from django.test import TestCase, Client
from django.urls import reverse


class ChatbotResponseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('chatbot-response')
    
    def test_chatbot_response(self):
        # Test the response for a specific message
        response = self.client.get(self.url, {'userMessage': 'Hi'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('How are you doing?', response.content.decode())

        response = self.client.get(self.url, {'userMessage': 'I am a registered user'})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Great! You'll have full access to all features, including wishlists and custom art services.", response.content.decode())

        response = self.client.get(self.url, {'userMessage': 'I am browsing anonymously'})
        self.assertEqual(response.status_code, 200)
        self.assertIn("No worries, you can still browse artwork and make purchases. To access wishlists and custom art services, you'll need to register - it's free and easy!", response.content.decode())

        response = self.client.get(self.url, {'userMessage': 'Who are you?'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('I am just an artificial intelligence.', response.content.decode())
    
    
    def test_chatbot_default_response(self):
        # Test the default response for an unrecognized message
        response = self.client.get(self.url, {'userMessage': 'Unrecognized message'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('I am sorry, but I do not understand.', response.content.decode())
