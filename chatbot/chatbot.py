import nltk
from nltk.chat.util import Chat, reflections

# Define a set of pairs (patterns and responses)
pairs = [
    [
        r"(hi|hello|hey|hola|howdy)(.*)",
        ["Hello! How can I assist you today?", "Hi there! What can I do for you?"]
    ],
    [
        r"what is your name ?",
        ["I am a chatbot created to assist you with your queries.", ]
    ],
    [
        r"how are you ?",
        ["I'm just a program, so I don't have feelings, but I'm here to help you!"]
    ],
    [
        r"sorry (.*)",
        ["It's alright.", "No problem at all."]
    ],
    [
        r"(.*)(help|support)(.*)",
        ["Sure, I'd be happy to help! What do you need assistance with?"]
    ],
    [
        r"(.*)(your (.*) creator|made you|created you)(.*)",
        ['I was created by an yageswaran loves to build AI applications.']
    ],
    [
        r"quit",
        ["Goodbye! Have a great day ahead."]
    ],
    [
        r"(.*)",
        ["I'm sorry, I don't understand that. Could you please rephrase?"]
    ]
]

# Create Chatbot instance
chatbot = Chat(pairs, reflections)


# Start conversation
def chat():
    print("Hi! I am your chatbot. Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Chatbot: Goodbye! Have a great day ahead.")
            break
        response = chatbot.respond(user_input)
        print(f"Chatbot: {response}")


if __name__ == "__main__":
    nltk.download('punkt')
    chat()
