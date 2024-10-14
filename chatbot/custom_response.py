import collections.abc
import collections
import json
import os
import ssl
import certifi
import spacy
from decouple import config
from django.http import HttpResponse
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

# Handle SSL context
collections.Hashable = collections.abc.Hashable
ssl._create_default_https_context = ssl._create_unverified_context
ssl.get_default_verify_paths = certifi.where()

# Initialize spaCy
nlp = spacy.load("en_core_web_sm")  # Load spaCy model

# Initialize the ChatBot
bot = ChatBot(
    "chatbot",
    read_only=False,
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "default_response": "I am sorry, but I do not understand.",
            "maximum_similarity_threshold": 0.70,
        }
    ],
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    #database_uri=config("DATABASE_URL"), # For Production
    database_uri="sqlite:///database.sqlite3",  # For Dev.
)

# Load custom responses from JSON file
file_path = os.path.join(os.path.dirname(__file__), "custom_responses.json")

try:
    with open(file_path, "r") as f:
        custom_responses = json.load(f)
except FileNotFoundError:
    raise RuntimeError(f"Custom responses file not found: {file_path}")
except json.JSONDecodeError:
    raise RuntimeError("Error decoding JSON from custom responses file")

list_to_train = custom_responses.get("responses", [])

# Train the ChatBot with the ChatterBot corpus
chatterbot_corpus_trainer = ChatterBotCorpusTrainer(bot)
chatterbot_corpus_trainer.train("chatterbot.corpus.english")

# Train the ChatBot with the custom responses
list_trainer = ListTrainer(bot)
for i in range(0, len(list_to_train) - 1, 2):
    list_trainer.train([list_to_train[i], list_to_train[i + 1]])


# Preprocess user input with spaCy before passing to the bot
def preprocess_input(user_input):
    doc = nlp(user_input)
    # Example: You can extract entities, keywords, etc.
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print(f"Entities: {entities}")  # Print for debugging
    return doc.text  # For now, just returning text, but can expand this


# Handle chat responses with spaCy preprocessing
def get_response(user_input):
    preprocessed_input = preprocess_input(user_input)
    response = bot.get_response(preprocessed_input)
    return response


# Function to return the chatbot instance (in case I need it elsewhere)
def get_bot():
    return bot
