from django.test import TestCase, Client
from django.urls import reverse


class ChatbotResponseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("chatbot-response")

    def test_chatbot_default_response(self):
        # Test the default response for an unrecognized message
        response = self.client.get(self.url, {"userMessage": "Unrecognized message"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Could you please rephrase that? I'm here to help with art inquiries!",
            response.content.decode(),
        )

    def test_chatbot_response(self):
        response = self.client.get(self.url, {"userMessage": "Hi"})
        print("Test Response Content: ", response.content.decode())  
        self.assertEqual(response.status_code, 200)
        self.assertIn("How are you doing?", response.content.decode())
