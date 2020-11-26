import nltk
try:
    nltk.data.find('tokenizers/punkt')
except:
    nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np
import tflearn
import tensorflow
import random
import json
import pickle

# Open our base data
with open("./data/intents.json") as file:
    data = json.load(file)

# Try to open our pre-processed data into a pickle file
try:
    with open("./data/data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)

# If there is no model, create it.
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    #
    # Getting all the shit out of our data
    #
    for intent in data['intents']:
        for pattern in intent['patterns']:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent['tag'])

        if intent['tag'] not in labels:
            labels.append(intent['tag'])

    #
    # Removing dupplicate element and stuff related
    #
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]

    #
    # ENCODER
    #
    for x, doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    # Turned our list into np array to be able to work with TF
    training = np.array(training)
    output = np.array(output)

    # Write our pre-processed data into a pickle file
    with open("./data/data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

# Reset then set NN configuration
tensorflow.reset_default_graph()

# Neurol Network configuration
# Input = 45
# Hidden #1 = 8
# Hidden #2 = 8
# Output = 6 -> softmax activation function (prediction on the most highly predicted output)
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
try:
    model.load("./data/model.tflearn")
except:
    model = tflearn.DNN(net)
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("./data/model.tflearn")


# Tokenise and pre-process input from the user to enter into NN
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)

# Handle the interaction with ML model
def chat(message):
    response_object = { 
        'messageResponse': '', 
        'inError': False, 
        'userId': 1,
        'chatbotRevision': 0.5
    }

    # Ask model about his toughts
    results = model.predict([bag_of_words(message, words)])

    # Comparaison then api response
    for result in results:
        results_index = np.argmax(result)
        tag = labels[results_index]

        if result[results_index] > 0.7:
            for tg in data['intents']:
                if tg['tag'] == tag:
                    responses = tg['responses']
            response_object['messageResponse'] = random.choice(responses)
            return response_object

        else:
            response_object['messageResponse'] = "I didn't get that, try again."
            response_object['inError'] = True
            return response_object
