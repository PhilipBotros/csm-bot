from functools import lru_cache
import logging

# This is for chromadb on azure, since it runs with an old version of sqlite
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except:
    pass

from flask import Flask, jsonify, render_template, request
from slack import slack_handler

import config
from src.context import context_manager
from src.langmodel import ChatWithContext, ChatWithoutContext, ChatWithContextTree

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
app.logger.setLevel(config.LOGGING_LEVEL)

MODELS = {"context": ChatWithContext, "nocontext": ChatWithoutContext, "tree": ChatWithContextTree}


@lru_cache
def get_chat_model(model_name):
    return MODELS[model_name]()


# WEB UI
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def web_ui(path):
    return render_template("index.html")


@app.route('/api/context_size')
def get_context_size():
     return jsonify({
        "contextSize": context_manager.count()
    })


@app.route('/api/random_datapoints', methods=['GET'], defaults={'numberofdps': 5})
def get_random_datapoints(numberofdps):
    dps = context_manager.sample_dps(numberofdps)
    logging.debug(dps)
    return jsonify(dps)


@app.route('/api/chat', methods=['POST'], defaults={'numberofanswers': 1, 'modelname': 'context'})
@app.route('/api/chat/<numberofanswers>/<modelname>', methods=['POST'])
def chat(numberofanswers, modelname):
    chat_model = get_chat_model(modelname)
    question = request.json["question"]
    history = request.json.get("history", "")
    answer = chat_model.talk(question, history)
    context = chat_model.get_context(question, top_k=5, return_score=True)
    logging.debug(f"Question: {question}, Answer: {answer}")
    if isinstance(answer, str):
        answer = [answer]
    
    return jsonify({
        "answers": answer,
        "context": context
    })


# SLACK
@app.route("/slack/oauth_redirect", methods=["POST", "GET"])
@app.route("/slack/install", methods=["POST", "GET"])
@app.route("/slack/events", methods=["POST"])
def slack_events():
    logging.debug("Request body: {}".format(request.get_data()))
    return slack_handler.handle(request)


if __name__ == '__main__':
    app.run(port=3000)