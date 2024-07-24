import collections.abc
import collections
collections.Hashable = collections.abc.Hashable

from django.http import HttpResponse
#from django.views.decorators.csrf import csrf_exempt
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot.logic import BestMatch
import json
import os
import ssl
import certifi
from decouple import config


ssl._create_default_https_context = ssl._create_unverified_context
ssl.get_default_verify_paths = certifi.where()

# # Initialize the ChatBot
bot = ChatBot(
    "chatbot",
    read_only=False,
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.70
        }
     ],
    storage_adapter='chatterbot.storage.SQLStorageAdapter', 
    #database_uri='postgres://postgres:Prod123@db:5432/LiveArtCorner'
    database_uri=config('DATABASE_URL')

)

# Load custom responses from JSON file
file_path = os.path.join(os.path.dirname(__file__), 'custom_responses.json')
with open(file_path, 'r') as f:
    custom_responses = json.load(f)
list_to_train = custom_responses['responses']

# Train the ChatBot with the ChatterBot corpus
chatterbot_corpus_trainer = ChatterBotCorpusTrainer(bot)
chatterbot_corpus_trainer.train("chatterbot.corpus.english")

# Train the ChatBot with the custom responses
list_trainer = ListTrainer(bot)
for i in range(0, len(list_to_train), 2):
    list_trainer.train([list_to_train[i], list_to_train[i + 1]])

#@csrf_exempt
def chatbot_response(request):
    if request.method == 'GET':
        user_message = request.GET.get('userMessage', '')
        chat_response = str(bot.get_response(user_message))
        return HttpResponse(chat_response)

