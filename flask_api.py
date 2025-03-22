from flask import Flask, jsonify
from llm_trivia import get_trivia_question

app = Flask(__name__)

@app.route('/api/trivia', methods=['GET'])
def trivia():
    question = get_trivia_question()
    return jsonify(question)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)