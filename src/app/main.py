from flask import Flask, request
from textblob import TextBlob
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from flask_basicauth import BasicAuth
import pandas as pd
import pickle
import os

# df = pd.read_csv('casa.csv')
# X = df.drop(['preco'],axis=1)
columns = ['tamanho', 'ano', 'garagem']
# X = df[columns]
# y = df['preco']
# X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)
# model = LinearRegression()
# model.fit(X_train,y_train)
# path = '../../models'
path = 'models'

with open(os.path.join(path,'model.pkl'),'rb') as file:
    model = pickle.load(file)



app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)

@app.route('/')
def home():
    return 'testando API 2'


@app.route('/sentence/<frase>')
@basic_auth.required
def sentiment(frase):
    tb = TextBlob(frase).translate(from_lang='pt', to='en')
    return 'The polarity of the sentece is {:.2f}%'.format(tb.sentiment.polarity * 100)

@app.route('/casa', methods = ['POST'])
@basic_auth.required
def preco():
    data_json = request.get_json()
    data = [data_json[col] for col in columns]
    previsao = model.predict([data])
    return str(previsao[0])

if (__name__ == '__main__'):
    app.run(port=5000, debug=True, host='0.0.0.0')