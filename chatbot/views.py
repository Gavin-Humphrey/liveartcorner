from django.http import HttpResponse
from chatbot.custom_response import get_bot, preprocess_input
import collections.abc
import collections
import time

collections.Hashable = collections.abc.Hashable


def chatbot_response(request):
    if request.method == "GET":
        user_message = request.GET.get("userMessage", "")

        # Preprocess the user message with spaCy before passing it to the bot
        preprocessed_message = preprocess_input(user_message)

        # Retrieve the bot instance
        bot = get_bot()

        # Start timing the response generation
        start_time = time.time()

        # Get the chatbot's response to the preprocessed message
        chat_response = str(bot.get_response(preprocessed_message))
        response_time = time.time() - start_time  # Calculate the time taken

        # Print the response time for debugging purposes
        print(f"Response time: {response_time:.4f} seconds")

        if chat_response == "I am sorry, but I do not understand.":
            chat_response = (
                "Could you please rephrase that? I'm here to help with art inquiries!"
            )

        return HttpResponse(chat_response)
