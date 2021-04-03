from flask import Flask, render_template, request
import pandas as pd
import random
import pandas as pd
import string
import nltk
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    def categorize_words():
        '''
        Catagorizes each spam/non-spam word into a corresponding list
        Repeating words in each list will help with categorizing
        '''
        spam_words = []
        ham_words = []
        for sms in data['processed'][data['label'] == 'spam']:
            for word in sms:
                spam_words.append(word)
        for sms in data['processed'][data['label'] == 'ham']:
            for word in sms:
                ham_words.append(word)
        return spam_words, ham_words

    def pre_process(sms):
        '''
        Remove punctuation and stop words from the custom sms
        '''
        remove_punct = "".join([word.lower() for word in sms if word not in string.punctuation])
        tokenize = nltk.tokenize.word_tokenize(remove_punct)
        remove_stop_words = [word for word in tokenize if word not in nltk.corpus.stopwords.words('english')]
        return remove_stop_words

    def pred(input_string):
        spam_counter = 0
        ham_counter = 0

        for word in input_string:
            spam_counter += spam_words.count(word)
            ham_counter += ham_words.count(word)

        if ham_counter > spam_counter:
            #adding accuracy
            certainty = round((ham_counter / (ham_counter + spam_counter)) * 100, 2)
            result=1
            return result,certainty
        elif spam_counter > ham_counter:
            certainty = round((spam_counter / (ham_counter + spam_counter)) * 100, 2)
            result=0
            return result,certainty
        else:
            return 0.5,50

    data = pd.read_csv('Database.txt', sep = '\t', header=None, names=["label", "sms"])
    data['processed'] = data['sms'].apply(lambda x: pre_process(x))
    #creating lists to store spam/non-spam associated words and their instances
    spam_words, ham_words = categorize_words()

    if request.method == 'POST':
        message = request.form['message']
        #print(message)
        input_string = [message]
        #print(input_string)
        input_string=pre_process(input_string)
        #print(input_string)
        my_prediction=pred(input_string)
        #print(my_prediction)

    return render_template('index.html', prediction=my_prediction[0],certainity=my_prediction[1])

if __name__ =='__main__':
    app.run()