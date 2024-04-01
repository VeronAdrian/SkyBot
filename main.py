from flask import Flask, jsonify, request
from gui import get_text
#python -m uvicorn main:app --reload

app = Flask(__name__)

def chatbotAnswer(entry):
    text = get_text(entry)
    return text

#Realzar la respuesta
@app.route('/answer/<string:question>', methods=['GET'])
def getAnswer(question):
    #Aca iria el texto pasado por el usuario
    answer = chatbotAnswer(question)
    return jsonify({'answer': answer})

#Testeo de ruta
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong!'})

if __name__ == '__main__':
    app.run(debug=True, port=4000)