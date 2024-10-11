import collections.abc
import collections

collections.Hashable = collections.abc.Hashable


from liveartcorner.chatbot.custom_response import chatbot


# Test the chatbot
response = chatbot.get_response("Hi")
print(response)
